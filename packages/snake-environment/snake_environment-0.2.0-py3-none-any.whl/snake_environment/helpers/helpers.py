import pygame
from ..game.snake_game import SnakeGame


def play_game():
    game = SnakeGame(render=True)
    action = 0
    done = False
    game.reset()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action = 0
                if event.key == pygame.K_DOWN:
                    action = 1
                if event.key == pygame.K_LEFT:
                    action = 2
                if event.key == pygame.K_UP:
                    action = 3

        done, reward, score, next_state = game.step(action)
