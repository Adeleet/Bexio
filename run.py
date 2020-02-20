import ExchangeClient
import time
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv

from envs import BitMEX


# env = BitMEX(API_KEY, API_SECRET)


# model = PPO2(MlpPolicy, env, verbose=1, n_steps=1, nminibatches=1)
# # model.learn(total_timesteps=10000, log_interval=60)

# obs = env.reset()
# for i in range(1000):
#     print(1)
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     time.sleep(60)
#     env.render()
# env.close()
