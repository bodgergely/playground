import gym
import logging


logger = logging.getLogger()


class Environment:
    def __init__(self, name):
        pass
    def state(self):
        pass

class OpenGymEnvironment(Environment):
    def __init__(self, name, render_on=False):
        self.name = name
        self._env = gym.make(name)
        self.reset()
        self._render_on = render_on
    def step(self, action):
        self.observation = self._env.step(action)
        if self._render_on:
            self.render()
        self._state = self.observation[0]
        return self.observation
    def render(self):
        self._env.render()
    def reset(self):
        self._state = self._env.reset()
    @property
    def state(self):
        return self._state

    def set_rendering(self, on=False):
        self._render_on = on
    @property
    def observation_space_shape(self):
        return self._env.observation_space.shape
        


class Agent:
    def __init__(self, env):
        self.env = env
    def step(self):
        action = self.select_next_action()
        logger.debug(f'Action: {action}')
        feedback = self.do_action(action)
        self.process_feedback(feedback)
        return not self.end()
    def do_action(self, action):
        feedback = self.env.step(action)
        return feedback
    def select_next_action(self):
        raise NotImplementedError("")
    def process_feedback(self, feedback):
        raise NotImplementedError("")
    def end(self):
        raise NotImplementedError("")

    
import numpy as np

def sign(n):
    return 1 if n >=0 else -1

class RandomLinearAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.weights = self.init_weights()
        self.activation = sign
        self.sar = [(self.env.state, 0, 0)]
        self.finished = False
    def select_next_action(self):
        feedback = self.sar[-1]
        X = feedback[0].T
        action = 1 if self.activation(X.dot(self.weights)) == 1 else 0
        self.action = action
        return action
    def process_feedback(self, feedback):
        self.sar.append((feedback[0], self.action, feedback[1]))
        self.finished = feedback[2]
    def end(self):
        return self.finished
    def init_weights(self):
        wshape = self.env.observation_space_shape
        d0 = wshape[0]
        d1 = 1 if len(wshape) == 1 else wshape[1]
        return np.random.randn(d0,d1)


def play_episode(agent, environ):
    environ.reset()
    steps = 0
    while agent.step():
        #print(steps)
        steps += 1
    return steps

from statistics import mean
def random_weight_search(agent, environ, num_trials, num_episodes):
    best_avg_step_count = -1
    best_weights = None
    for trial in range(num_trials):
        ragent = RandomLinearAgent(environ) 
        steps_list = []
        for e in range(num_episodes):
            steps = play_episode(ragent, environ)
            steps_list.append(steps)
        avg_steps = mean(steps_list)
        logger.info(f"Trial: {trial}")
        if avg_steps > best_avg_step_count:
            best_avg_step_count = avg_steps
            best_weights = ragent.weights
    return best_avg_step_count, best_weights


def evaluate(environ, agent, weight):
    steps = [play_episode(agent, environ) for _ in range(1000)]
    return mean(steps)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    env = OpenGymEnvironment('CartPole-v0')
    agent = RandomLinearAgent(env)
    best_avg_step, best_weights = random_weight_search(agent, env, num_trials=300, num_episodes=100)
    logger.info(best_avg_step, best_weights)
    
    logger.setLevel(logging.DEBUG)
    env.set_rendering(on=True)
    steps = evaluate(env, agent, best_weights) 
    print(steps)
