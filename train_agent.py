import numpy as np
import random
from collections import defaultdict
import pickle
from game import InfiniteTicTacToe


class QLearningAgent:
    def __init__(self, player, size=3, win_length=3, disappear_after=3, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.player = player
        self.size = size
        self.win_length = win_length
        self.disappear_after = disappear_after
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = defaultdict(lambda: np.zeros((self.size, self.size)))

    def get_state(self, game):
        return str(game.history)+'_'+game.current_player

    def choose_action(self, game):
        state = self.get_state(game)
        if random.uniform(0, 1) < self.epsilon:
            return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        else:
            q_values = self.q_table[state]
            max_q = np.max(q_values)
            actions = [(r, c) for r in range(self.size) for c in range(self.size) if q_values[r][c] == max_q]
            return random.choice(actions)

    def update_q_value(self, game, row, col, reward, next_game):
        state = self.get_state(game)
        next_state = self.get_state(next_game)
        best_next_q = np.max(self.q_table[next_state])
        self.q_table[state][row][col] += self.alpha * (
                    reward + self.gamma * best_next_q - self.q_table[state][row][col])

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = defaultdict(lambda: np.zeros((self.size, self.size)), pickle.load(f))


def train_agents(episodes=10000):
    agents = {'X': QLearningAgent('X'), 'O': QLearningAgent('O')}

    for episode in range(episodes):
        game = InfiniteTicTacToe(size=3, win_length=3, disappear_after=3)
        game.start_game()

        while not game.game_over:
            current_player = game.current_player
            # print(current_player)
            agent = agents[current_player]

            row, col = agent.choose_action(game)
            game_state = game.make_move(row, col)

            if game_state['winner'] == agent.player:
                reward = 1
            elif game_state['winner'] != agent.player:
                reward = -1
            else:
                reward = 0

            agent.update_q_value(game, row, col, reward, game)

        print(f"Episode {episode + 1}/{episodes} completed.")

    return agents


# Example usage
if __name__ == "__main__":
    # Define the training parameters
    episodes = 10000
    save_model_file_x = 'tictactoe_q_model_X.pkl'
    save_model_file_o = 'tictactoe_q_model_O.pkl'

    # Train agents X and O
    agents = train_agents(episodes=episodes)

    # Save models for agents X and O
    agents['X'].save_model(save_model_file_x)
    agents['O'].save_model(save_model_file_o)

    print(f"Saved trained model for X to {save_model_file_x}")
    print(f"Saved trained model for O to {save_model_file_o}")
