import json

class InfiniteTicTacToe:
    def __init__(self, size=3, win_length=3, disappear_after=3):
        self.size = size
        self.win_length = win_length
        self.disappear_after = disappear_after
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.history = {'X':[], 'O':[]}
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def start_game(self):
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.history = {'X':[], 'O':[]}
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.game_over:
            return self.get_game_state()

        if not (0 <= row < self.size and 0 <= col < self.size):
            return self.get_game_state("Invalid move. Out of bounds.")

        if self.board[row][col] != ' ':
            return self.get_game_state("Invalid move. Cell already taken.")

        if self.history[self.current_player] and len(self.history[self.current_player]) >= self.disappear_after:
            oldest_cell = self.history[self.current_player][0]
            if oldest_cell == (row, col):
                return self.get_game_state("Invalid move. Cell will disappear.")

        # Handle disappearing moves
        disappear_cell = None
        if len(self.history[self.current_player]) == self.disappear_after:
            disappear_cell = self.history[self.current_player].pop(0)
            self.board[disappear_cell[0]][disappear_cell[1]] = ' '

        # Place the move
        self.board[row][col] = self.current_player
        self.history[self.current_player].append((row, col))

        # Check for win
        if self.check_winner(row, col):
            self.game_over = True
            self.winner = self.current_player
            return self.get_game_state(f"Player {self.current_player} wins!")

        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

        return self.get_game_state()

    def check_winner(self, row, col):
        def check_direction(dx, dy):
            count = 0
            for i in range(-self.win_length + 1, self.win_length):
                new_row, new_col = row + i * dx, col + i * dy
                if 0 <= new_row < self.size and 0 <= new_col < self.size and self.board[new_row][new_col] == self.current_player:
                    count += 1
                    if count >= self.win_length:
                        return True
                else:
                    count = 0
            return False

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(check_direction(dx, dy) for dx, dy in directions)

    def get_game_state(self, message=None):
        return {
            "board": self.board,
            "current_player": self.current_player,
            "disappear_cell": self.history[self.current_player][0] if len(self.history[self.current_player]) == self.disappear_after else None,
            "winner": self.winner,
            "message": message,
            "valid_move": message is None,  # True if no message (valid move), False otherwise
        }

# Example usage
# game = InfiniteTicTacToe(size=3, win_length=3, disappear_after=4)
# game.start_game()
# print(game.make_move(0, 0))
# print(game.make_move(1, 1))
# print(game.make_move(0, 1))
# print(game.make_move(1, 0))
# print(game.make_move(2, 1))  # This move should set (1, 1) to disappear
# print(game.make_move(2, 2))  # This move should return an error about disappearing cell