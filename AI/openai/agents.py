import gym


class Memory:
    def __init__(self, mem_size):
        self.mem_size = mem_size
        self.items = []
    def add(self, item):
        if len(self.items) >= self.mem_size:
            self.items.pop(0)
        self.items.append(item)
    @property
    def entries(self):
        return self.items
    @property
    def count(self):
        return len(self.items)

class Agent:
    def __init__(self, environment, episode_memory):
        self.env = environment
        self.episode_mem = episode_memory
        self.curr_episode = Episode()
    def play(self):
        while self.act() != True:
            pass
        return

    def act(self):
        if self.curr_episode.done == True:
            self.start_new_episode()
        action = self._select_action()
        obs, r, done, info = self.env.step(action)
        self.curr_episode.push(obs, r, info)
        if done:
            self.finalize_episode()
            return True
        return False

    def start_new_episode(self):
        if self.curr_episode.done != True:
            raise RuntimeError("Starting new episode when current episode is not done!")
        self.curr_episode = Episode()
        self.env.reset()
    
    def finalize_episode(self):
        self.curr_episode.mark_finished()
        self.episode_mem.add(self.curr_episode)


    @property
    def episode_memory(self):
        return self.episode_mem
    def _select_action(self):
        raise NotImplementedError("")


class Environment:
    def __init__(self, name):
        self.name = name
        self.env = gym.make(name)
        self.reset()
    def step(self, action):
        self.obs, self.reward, self.done, self.info = self.env.step(action)
        return self.state 
    def reset(self):
        self.obs, self.reward, self.done, self.info = self.env.reset()
    @property
    def state(self):
        return self.obs, self.reward, self.done, self.info
    @property
    def action_space(self):
        return self.env.action_space



class Episode:
    def __init__(self):
        self.memory = dict(observations=[], rewards=[], info=[])
        self.done = False
    def push(self, observation, reward, info=None):
       self.memory['observations'].append(observation)
       self.memory['rewards'].append(reward)
       if info == "":
           info = None
       self.memory['info'].append(info)
    def mark_finished(self):
        self.done = True
    @property
    def steps(self):
        return len(self.observations)
    @property
    def observations(self):
        return self.memory['observations']
    @property
    def rewards(self):
        return self.memory['rewards']
    @property
    def infos(self):
        return self.memory['info']


class RandomActionAgent(Agent):
    def __init__(self, environment, memory):
        super().__init__(environment, memory) 
    def _select_action(self):
        return self.env.action_space.sample()


def run_simulation(environ_name, agent_type, episode_count, produce_statistics):
    environ = Environment(environ_name)
    memory = Memory(episode_count)
    agent = agent_type(environ, memory)
    for episode_index in range(episode_count):
        agent.play()
    memory = agent.episode_memory
    return produce_statistics(memory)

def steps_rewards(episode_memory):
    from statistics import mean
    episodes = episode_memory.entries
    steps = []
    rewards = []
    for episode in episodes:
        steps.append(episode.steps)
        rewards.append(sum(episode.rewards))

    avg_steps = mean(steps)
    avg_rewards = mean(rewards)
    return {"avg_step" : avg_steps, "avg_reward" : avg_rewards}


if __name__ == "__main__":
    stats = run_simulation('CartPole-v0', RandomActionAgent, 1000, steps_rewards)
    print(stats) 










