from game import *
from agent import QLearningAgent
import random

def train(episodes, epsilon):

    agent = QLearningAgent(epsilon=epsilon)
    agent.load()

    for ep in range(episodes):

        board = create_board()
        state = agent.get_state(board)
        done = False

        turn = AGENT

        while not done:

            moves = get_valid_moves(board)

            if turn == AGENT:

                action = agent.choose_action(state, moves)
                drop_piece(board, action, AGENT)

                next_state = agent.get_state(board)

                if check_winner(board, AGENT):
                    agent.update(state, action, 1, next_state)
                    done = True

                elif is_full(board):
                    agent.update(state, action, 0, next_state)
                    done = True

                else:
                    agent.update(state, action, 0, next_state)
                    state = next_state
                    turn = PLAYER

            else:
                action = random.choice(moves)
                drop_piece(board, action, PLAYER)

                if check_winner(board, PLAYER):
                    agent.update(state, 0, -1, agent.get_state(board))
                    done = True
                elif is_full(board):
                    # El tablero se lleno y es empate
                    done = True
                else:
                    turn = AGENT

        # progreso
        if (ep+1) % 1000 == 0:
            print("Episodio:", ep+1)

    agent.save()

    print("Entrenamiento listo")
    print("Estados aprendidos:", len(agent.q)) 


if __name__ == "__main__":
    train(10000, 0.5)