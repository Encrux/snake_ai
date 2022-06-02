import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from snake import SnakeEnv


def from_default_parameters():
    return SnakeEnv(board_dim=(50, 50), simspeed=5, initial_length=4, initial_dir=[1, 0])


# Parallel environments
snake_env = make_vec_env(from_default_parameters, n_envs=24)

model = PPO("MlpPolicy", snake_env, verbose=1, device="auto")
model.learn(total_timesteps=2500000)
model.save("smart_snek")

del model  # remove to demonstrate saving and loading

model = PPO.load("smart_snek")

obs = snake_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = snake_env.step(action)
    snake_env.render()
