import tkinter as tk
from tkinter import messagebox
from game import InfiniteTicTacToe
import pickle

class InfiniteTicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinite Tic Tac Toe")

        self.game = None
        self.buttons = []
        self.board_size = 3  # Default board size

        # Initialize info_label as None
        self.info_label = None

        self.ai_player = None
        self.ai_model = None  # Variable to hold the AI model

        self.create_board_buttons()
        self.create_menu()
        self.create_info_label()  # Add method to create info label

    def create_info_label(self):
        # Create label to display current player
        self.info_label = tk.Label(self.root, text=f"Current Player: {self.game.current_player}", font=('Arial', 14))
        self.info_label.grid(row=self.board_size, columnspan=self.board_size, pady=10)

    def update_info_label(self):
        # Update info label with current player
        if self.info_label:  # Check if info_label is initialized
            self.info_label.config(text=f"Current Player: {self.game.current_player}")

    def create_board_buttons(self):
        # Create buttons for the board
        for row in range(self.board_size):
            button_row = []
            for col in range(self.board_size):
                button = tk.Button(self.root, text="", font=('Arial', 20), width=6, height=3,
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

    def create_menu(self):
        # Create a menu to select board size
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        size_menu = tk.Menu(menu, tearoff=0)
        size_menu.add_command(label="3x3", command=lambda: self.start_new_game(3))
        size_menu.add_command(label="5x5", command=lambda: self.start_new_game(5))

        menu.add_cascade(label="Board Size", menu=size_menu)

        # Option to start game with AI
        menu.add_command(label="Play with AI (O)", command=self.load_ai_model_O)

        # Start a new game initially with default board size
        self.start_new_game(self.board_size)

    def start_new_game(self, size):
        # Initialize a new game
        self.game = InfiniteTicTacToe(size=size, win_length=3, disappear_after=3)
        self.update_board()
        self.update_info_label()  # Update info label after starting new game


    def load_ai_model_O(self):
        # Load AI model for player O from file
        try:
            with open('tictactoe_q_model_O.pkl', 'rb') as f:
                self.ai_model = pickle.load(f)
            self.ai_player = 'O'
            self.start_new_game(self.board_size)  # Start a new game with AI
        except FileNotFoundError:
            messagebox.showerror("Error", "AI model file not found.")

    def make_move(self, row, col):
        # Function to handle button click and make a move
        if not self.game.game_over:
            # Human player move
            game_state = self.game.make_move(row, col)
            if game_state['valid_move']:
                self.update_board()
                self.update_info_label()  # Update info label after making move
                if self.game.game_over:
                    self.show_game_result()
                    return

                # AI player move (if AI is playing as O and it's AI's turn)
                if self.game.current_player == self.ai_player:
                    ai_move = self.get_ai_move()
                    if ai_move:
                        game_state = self.game.make_move(ai_move[0], ai_move[1])
                        self.update_board()
                        self.update_info_label()  # Update info label after AI's move
                        if self.game.game_over:
                            self.show_game_result()

    def get_ai_move(self):
        # Get AI move based on the current game state
        if self.ai_model and self.game.current_player == self.ai_player:
            state = self.get_state()    

            q_values = self.ai_model[str(self.game.history)+'_'+self.game.current_player]
            max_q = -float('inf')
            best_move = None
            for r in range(self.board_size):
                for c in range(self.board_size):
                    if q_values[r][c] > max_q and self.game.board[r][c] == ' ':
                        max_q = q_values[r][c]
                        best_move = (r, c)
            print(q_values)
            print(best_move)
            return best_move
        return None

    def get_state(self):
        # Get state representation of the current game board for AI
        state = []
        for row in self.game.board:
            state.extend(row)
        return tuple(state)

    def update_board(self):
        # Update GUI based on current game state
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                button['text'] = self.game.board[row][col]

                # Check if the cell is a disappear_cell
                disappear_cell = self.game.next_disappear_cell()
                if disappear_cell and (row, col) == disappear_cell:
                    button['fg'] = 'red'  # Change font color to red for disappear_cell
                else:
                    button['fg'] = 'black'  # Default font color

    def show_game_result(self):
        # Display message box with game result
        if self.game.winner:
            messagebox.showinfo("Game Over", f"Player {self.game.winner} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = InfiniteTicTacToeGUI(root)
    root.mainloop()
