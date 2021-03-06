import pygame
import random
import numpy as np
from gym import spaces
import gym
import math

window_size = width, height = 1000, 1000
grid_size = 20

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "blue": (0, 0, 255),
    "red": (255, 0, 0)
}

dirs = [
    [0, -1], [1, 0], [0, 1], [-1, 0]
]

default_snake = [
    (25, 25),
    (24, 25),
    (23, 25),
    (22, 25)
]


def game_to_screen(x: int, y: int):
    return x * grid_size, y * grid_size


def distance_reward(snake, apple):
    head = snake[0]
    distance = math.dist(head, apple)
    return ((1 / distance) - 0.5) * 10


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    snake = []
    frame = []
    current_dist = []  # to apple

    def __init__(self, board_dim=(50, 50), simspeed=500, initial_length=4, initial_dir=[1, 0]) -> None:
        self.dt = simspeed
        self.episode = 0
        self.cumulative_reward = 0
        self.steps = 0
        self.width, self.height = int(board_dim[0]), int(board_dim[1])
        self.board_dim = board_dim

        self.highscore = 0

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=(12,))

        # init game window
        pygame.init()
        pygame.display.set_caption("snake:ai")
        self.window = pygame.display.set_mode(window_size)
        self.window.fill(colors["black"])
        pygame.display.flip()

        self.reset()

    def reset(self):
        if len(self.snake) > self.highscore:
            self.highscore = len(self.snake)
            print("new highscore: ", self.highscore)

        # print("score: " + str(len(self.snake)))
        self.score = 0
        self.head_dir = 1  # right
        self.snake = default_snake
        self.game_over = False
        self.spawn_apple()
        self.current_dist = math.dist(self.apple, self.snake[0])
        self.update_frame()
        return self.get_state()

    def spawn_apple(self):
        spaces = list(np.ndindex(*self.board_dim))
        for block in self.snake:
            spaces.remove(block)

        random_index = random.randint(0, len(spaces) - 1)
        # print("apple: " + str(spaces[random_index]))
        self.apple = spaces[random_index]

    def is_valid(self):
        snake_copy = []
        for block in self.snake:
            snake_copy.append(block)

        head = self.snake[0]
        snake_copy.pop(0)

        # check if head collides with rest
        for x, y in snake_copy:
            x_head, y_head = head
            if (x_head, y_head) == (x, y):
                return False

        # check map boundaries
        x_max, y_max = self.board_dim
        x, y = head

        if x < 0 or x >= x_max:
            return False
        if y < 0 or y >= y_max:
            return False

        return True

    def valid_direction(self, action):
        if self.head_dir == 0 and action == 2:
            return False
        if self.head_dir == 1 and action == 3:
            return False
        if self.head_dir == 2 and action == 0:
            return False
        if self.head_dir == 3 and action == 1:
            return False

        return True

    def step(self, action):
        reward = 0
        self.steps += 1

        if self.valid_direction(action):
            self.head_dir = action

            # update snake head
        head = tuple(np.add(self.snake[0], dirs[self.head_dir]))
        self.snake = [head] + self.snake

        if not (np.array_equal(head, self.apple)):
            self.snake.pop(-1)
        else:
            self.spawn_apple()
            reward = 100

        if not self.is_valid():
            self.game_over = True
            reward = -100
            self.reset()
        else:
            self.update_frame()

        dr = distance_reward(self.snake, self.apple)
        reward += dr
        # print(reward, dr)
        self.cumulative_reward += dr
        self.current_dist = math.dist(self.apple, self.snake[0])
        # TODO: change reward to punish going further away and reward going closer
        # the current reward essentially does the same, but maybe it's better this way

        return self.get_state(), reward, self.game_over, {
            'episode': {'episode': self.episode, 'r': self.cumulative_reward, 'l': self.steps}}

    def update_frame(self):
        next = np.zeros(shape=(self.width, self.height))
        next[self.apple] = 2

        for block in self.snake:
            next[block] = 1

        pygame.time.delay(self.dt)
        self.frame = next
        # self.render()

    def render(self):
        self.window.fill(colors["black"])

        # render snake
        for block in self.snake:
            x, y = game_to_screen(*block)
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(self.window, colors["blue"], rect)

        # render apple
        ax, ay = game_to_screen(*self.apple)
        pygame.draw.rect(self.window, colors["red"], pygame.Rect(ax, ay, grid_size, grid_size))
        pygame.display.flip()
        pygame.time.delay(self.dt)

    def near_obstacle_state(self):
        vec = [0, 0, 0, 0]
        hx, hy = self.snake[0]
        vec[0] = 1 if hy == 1 or [hx, hy - 1] in self.snake else 0  # 1 if danger above
        vec[1] = 1 if hx == self.width - 2 or [hx + 1, hy] in self.snake else 0  # 1 if danger is to right
        vec[2] = 1 if hy == self.height - 2 or [hx, hy + 1] in self.snake else 0  # 1 if danger is below
        vec[3] = 1 if hx == 1 or [hx - 1, hy] in self.snake else 0  # 1 if danger is to left

        return vec

    def dir_one_hot(self):
        vec = [0, 0, 0, 0]
        for i in range(0, 3):
            vec[0] = 1 if self.head_dir == i else 0
        return vec

    def apple_dir(self):
        vec = [0, 0, 0, 0]
        x, y = np.subtract(self.apple, self.snake[0])
        dominant_direction = "horizontal" if abs(x) >= abs(y) else "vertical"
        vec[0] = 1 if y > 0 and dominant_direction == "vertical" else 0
        vec[1] = 1 if x > 0 and dominant_direction == "horizontal" else 0
        vec[2] = 1 if y <= 0 and dominant_direction == "vertical" else 0
        vec[3] = 1 if x <= 0 and dominant_direction == "horizontal" else 0
        return vec

    def get_state(self):
        state = []
        state.extend(self.apple_dir())
        state.extend(self.near_obstacle_state())
        state.extend(self.dir_one_hot())
        return state
