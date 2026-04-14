import random
import json
import os

class QLearningAgent:

    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q = {}


    def get_state(self, board):
        return " ".join(map(str, board.flatten()))

    def choose_action(self, state, valid_moves):

        if state not in self.q:
            self.q[state] = [0]*7

        # exploracion
        if random.random() < self.epsilon:
            return random.choice(valid_moves)

        values = self.q[state]
        max_value = max([values[m] for m in valid_moves])
        best = [m for m in valid_moves if values[m] == max_value]

        return random.choice(best)

    def update(self, state, action, reward, next_state):

        if state not in self.q:
            self.q[state] = [0]*7

        if next_state not in self.q:
            self.q[next_state] = [0]*7

        old = self.q[state][action]
        future = max(self.q[next_state])

        # Fórmula Q-Learning
        self.q[state][action] = old + self.alpha * (reward + self.gamma * future - old)


    def save(self):
        q_str = {str(k): v for k, v in self.q.items()}

        with open("q_table.json", "w") as f:
            json.dump(q_str, f, indent=4)


    def load(self):
        if os.path.exists("q_table.json"):
            with open("q_table.json", "r") as f:
                q_str = json.load(f)

            self.q = {k: v for k, v in q_str.items()}