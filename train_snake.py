
import os.path as osp
import os
import gym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import stable_baselines3
import snake
from stable_baselines3 import PPO
from stable_baselines3.ppo import ppo
from stable_baselines3.common.env_util import make_vec_env

#Goes much faster without gpu for some reason...
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"

snake_env = make_vec_env(snake.snake_game, n_envs=1)

model = PPO("MlpPolicy", snake_env, verbose=1)
model.learn(total_timesteps=1000)
model.save("snek")

obs = snake_env.reset()

while True:
    action, _states = model.predict(obs)
    obs, rewards, done, info = snake_env.step(action)
    snake_env.render