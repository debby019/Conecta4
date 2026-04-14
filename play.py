import pygame
import sys
import numpy as np
from game import *
from agent import QLearningAgent

# Colores
BLUE = (21, 0, 99)
BLACK = (255, 255, 255)
RED = (150, 30, 0)      
YELLOW = (255, 255, 0)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

pygame.init()

width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Conecta 4 vs IA")

font = pygame.font.SysFont("monospace", 50)

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AGENT:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def main():
    board = create_board()

    agent = QLearningAgent(epsilon=0)
    agent.load()

    game_over = False
    turn = PLAYER

    draw_board(board)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if col in get_valid_moves(board):
                    drop_piece(board, col, PLAYER)

                    if check_winner(board, PLAYER):
                        label = font.render("GANASTE!", True, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn = AGENT
                    draw_board(board)

        # Turno del agente
        if turn == AGENT and not game_over:
            state = agent.get_state(board)
            moves = get_valid_moves(board)
            col = agent.choose_action(state, moves)

            pygame.time.wait(500)

            drop_piece(board, col, AGENT)

            if check_winner(board, AGENT):
                label = font.render("IA GANA!", True, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            draw_board(board)
            turn = PLAYER

        if game_over:
            pygame.time.wait(3000)

if __name__ == "__main__":
    main()