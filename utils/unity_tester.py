import numpy as np
import time
from pyvirtualdisplay import Display
from mlagents_envs.environment import UnityEnvironment
from gym_unity.envs import UnityToGymWrapper

display = Display(backend='xvnc', size=(64, 64), visible=0, rfbport=0)
display.start()
env_path = '/common/home/jy651/rl-starter-files/unity_envs/GridWorld/GridWorld-linux'
unity_env = UnityEnvironment(env_path)
env = UnityToGymWrapper(unity_env, True, True, True)
obs = env.reset()

done = False
action_size = 3
step = 0
while not done:

  action = np.random.choice(action_size)
  obs, reward, done, info = env.step(int(action))
  step += 1
  print(step, reward, done)

env.close()
display.stop()
