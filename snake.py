import pygame
import time
import random
from enum import Enum
import numpy as np
import sys
from gym import error, spaces, utils, core
import gym
import game

window_size = width, height = 1000, 1000
grid_size = 20

colors = {
    "black": (0,0,0),
    "white": (255,255,255),
    "blue":  (0, 0, 255),
    "red":   (255,0,0)
}

directions = {
    "up":       [0, -1],
    "right":    [1, 0],
    "down":     [0, 1],
    "left":     [-1, 0]
}

default_snake = [
            (25, 25),
            (24, 25),
            (23, 25),
            (22, 25)
        ]


def game_to_screen(x: int, y: int):
    return x * grid_size, y * grid_size

class snake_game(gym.Env):
    metadata = {'render.modes': ['human']}

    snake = []

    def __init__(self, board_dim = (50, 50), simspeed = 100, initial_length = 4, initial_dir=[1,0]) -> None:
        self.dt = simspeed

        self.width, self.height = int(board_dim[0]), int(board_dim[1])
        self.board_dim = width, height 

        self.highscore = 0

        self.action_space = spaces.Discrete(4)
        low = np.zeros(3)
        high = np.zeros(3)
        high.fill(255)

        self.observaion_space = spaces.Box(low=0, high=255, shape=(width, height, 3), dtype=np.uint8)
        self.reset()

        #init game window
        pygame.init()
        pygame.display.set_caption("snake:ai")
        self.window = pygame.display.set_mode(window_size)
        self.window.fill(colors["black"])
        pygame.display.flip()

            
        
    
    def reset(self):
        if (len(self.snake) > self.highscore):
            self.highscore = len(self.snake)

        print("score: " + str(len(self.snake)))
        self.score = 0
        self.head_dir = directions["right"]
        self.snake = default_snake
        self.game_over = False
        self.spawn_apple()


    def spawn_apple(self):
        spaces = list(np.ndindex(*self.board_dim))
        for block in self.snake:
            spaces.remove(block)
        
        random_index = random.randint(0, len(spaces) - 1)  
        #print("apple: " + str(spaces[random_index]))
        self.apple = spaces[random_index]

    def is_valid(self):
        snake_copy = []
        for block in self.snake:
            snake_copy.append(block)

        head = self.snake[0]
        snake_copy.pop(0)

        #check if head collides with rest
        for x, y in snake_copy:
            x_head, y_head = head
            if (x_head, y_head) == (x, y):
                return False

        #check map boundaries        
        x_max, y_max = self.board_dim
        x, y = head

        if x < 0 or x > x_max:
            return False
        if y < 0 or y > y_max:
            return False
        
        return True

    def valid_direction(self, action):
        if self.head_dir == directions["up"] and action == directions["down"]:
            return False
        if self.head_dir == directions["right"] and action == directions["left"]:
            return False
        if self.head_dir == directions["down"] and action == directions["up"]:
            return False
        if self.head_dir == directions["left"] and action == directions["right"]:
            return False
        
        return True

    def step(self, action):
        reward = 0
         
        if self.valid_direction(action):
           self.dir = action 

        #update snake head
        head = tuple(np.add(self.snake[0], self.head_dir))
        self.snake = [head] + self.snake

        if not (np.array_equal(head, self.apple)):
            self.snake.pop(-1)
            reward = -1
        else:
            self.spawn_apple()
            reward = 25

        if not self.is_valid():
            self.game_over = True
            reward = -100
            self.reset()

        return {
            "snake": self.snake,
            "game_over": self.game_over,
            "apple": self.apple,
            "reward": reward
        }
    
    def render(self):
        self.window.fill(colors["black"])

        #render snake
        for block in self.snake:
            x, y = game_to_screen(*block)
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(self.window, colors["blue"], rect)

        #render apple
        ax, ay = game_to_screen(*self.apple)
        pygame.draw.rect(self.window, colors["red"], pygame.Rect(ax, ay, grid_size, grid_size))
        
        pygame.display.flip()
