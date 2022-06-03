# snake_ai

clip of a pretrained model playing snake (2.5M timesteps, 12 parallel Envs trained)


https://user-images.githubusercontent.com/28564983/171817440-e4979fd7-3374-4ac9-88ff-ffb23bfdd0f4.mp4

This project contains my own implementation of snake in the form of a stable_baselines3 VecEnv, and a training script that trains an agend based on PPO.
To get more information on stable_baselines3's PPO, check out https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html


The observation space is a 12 dimensional vector, containing:
- relative apple direction 
  - e.g. [1, 0, 0, 0] -> apple is above
- snake head direction 
  - e.g. [0, 1, 0, 0] -> snake is headed right
- is there an obstacle next to the head? 
  - e.g. [0, 1, 0, 1] there is an obstacle to the left and right of the snake's head

the loss function:
- eating an apple: +100
- dying: -100
- for every step: ((1 / distance(apple, head)) - 0.5) * 10
