import pygame
import time
import random
from enum import Enum
import numpy as np
import sys
import snake
from snake import directions, colors, window_size, grid_size, snake_game, width, height

def init_pygame():
    #init game window
    pygame.init()
    pygame.display.set_caption("snake:ai")
    screen = pygame.display.set_mode(window_size)
    screen.fill(colors["black"])
    pygame.display.flip()

    return screen

def game_to_screen(x: int, y: int):
    return x * grid_size, y * grid_size


def update_frame(window, game):
    window.fill(colors["black"])

    #render snake
    for block in game.snake:
        x, y = game_to_screen(*block)
        rect = pygame.Rect(x, y, grid_size, grid_size)
        pygame.draw.rect(window, colors["blue"], rect)

    #render apple
    ax, ay = game_to_screen(*game.apple)
    pygame.draw.rect(window, colors["red"], pygame.Rect(ax, ay, grid_size, grid_size))
    
    pygame.display.flip()
    


if __name__=="__main__":
    action = directions["right"]
    game = snake_game(board_dim=(width / grid_size, height / grid_size), initial_dir=action)
    window = init_pygame()
    running = True

    pygame.draw.rect(window, colors["blue"], pygame.Rect(0, 0, 200, 200))
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = directions["up"]
                if event.key == pygame.K_RIGHT:
                    action = directions["right"]
                if event.key == pygame.K_DOWN:
                    action = directions["down"]
                if event.key == pygame.K_LEFT:
                    action = directions["left"]

        current_state = game.step(action)
        update_frame(window, game)
        pygame.time.wait(game.dt)
    

