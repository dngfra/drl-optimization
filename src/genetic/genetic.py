# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SjH7SLZuhPFiD00JbG2pf4iOT_EFBiPP
"""

import numpy as np
import gym
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from .genetic_functions import crossover_function, generate_population


class Agent:

    def __init__(self, env=gym.make('CartPole-v1'), weights=None):
        # if you want to see Cartpole learning, then change to True
        self.max_time = 2000
        self.env = env
        # In case of CartPole-v1, maximum length of episode is 500
        self.env._max_episode_steps = 2000
        # score_logger = ScoreLogger('CartPole-v1')
        # get size of state and action from environment
        self.state_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        self.render = False
        self.load_model = False
        # get size of state and action
        self.value_size = 1
        # create model for policy network
        self.model = self.build_model()
        if weights is not None:
          self.model.set_weights(weights)

    def build_model(self):
      model = Sequential()
      model.add(Dense(24, input_dim=self.state_size, activation='relu',
                      kernel_initializer='he_uniform', name="input"))
      model.add(Dense(self.action_size, activation='softmax',
                      kernel_initializer='he_uniform', name="output"))
      #model.summary()
      return model

    def get_action(self, state):
        policy = self.model.predict(state, batch_size=1).flatten()
        #secondo me non ha molto senso fare una multinomial perchè ora non stiamo trainando niente quindi è solo una cosa deterministica che sceglie l'azione in base alla policy, dall'esploration non trarrebbe effettivamente nessun vantaggio se non eventualmente un punteggio più alto dovuto alla casualità del sampling e che quindi non rispecchia proprimanete la policy e lo stesso per un punteggio più basso.
        #per questo prenderei soltanto l'azione con la probabilità maggiore
        #return np.random.choice(self.action_size, 1, p=policy)[0]
        return np.argmax(policy)

    def run_agent(self):
        done = False
        score = 0
        state = self.env.reset()
        state = np.reshape(state, [1, self.state_size])
        # print("intial state: ",state)
        while (not done) and (score < self.max_time):
            if self.render:
                self.env.render()

            action = self.get_action(state)
            next_state, reward, done, info = self.env.step(action)
            next_state = np.reshape(next_state, [1, self.state_size])
            score += reward
            state = next_state

            if done:
                return score


def run_agent_genetic(env=gym.make('CartPole-v1'), N=50, n_generations=100):

    agents = []
    #scores è quello che nella funzione crossover abbiamo chiamo rewards forse bisogna rinominarli
    scores = []
    for i in range(N):
      agent = Agent(env)
      agents.append(agent)

    #ho rimosso la tupla perchè probabilmente ci basta solo una lista di agent e poi resettiamo sempre lo stesso ambiente
    mean_score_gen = []
    variance_score_gen = []
    max_score_gen = []

    for i in range(n_generations):
        print("generation: ", i)
        scores = []
        for agent in agents:
            score = agent.run_agent()
            #print(score)
            scores.append(score)
            #state = env.reset()
            #sys.exit()
        print(np.mean(scores))
        print(np.max(scores))
        mean_score_gen.append(np.mean(scores))
        variance_score_gen.append(np.var(scores))
        max_score_gen.append(np.max(scores))
        #Ore creiamo il genitore della prossima generazione a partire dai risultati di quella precedente e sostituiamo la lista agents
        #parent = crossover_function(agents,scores)
        #agents = generate_population(parent,N, agents,0.1)
        child = crossover_function(agents, scores)
        if i == 0:
            initial_agent = Agent(env, weights=child)
        agents = generate_population(child, N, agents)
        #scores.pop(scores.index(np.max(scores)))
        #print(np.max(scores))

    data = pd.DataFrame({'mean': mean_score_gen,'variance': variance_score_gen,'max': max_score_gen})
    data.to_csv('data.csv')
    final_agent = Agent(env, weights=child)
    return initial_agent, final_agent


def run_agent_genetic_2(env=gym.make('CartPole-v1'), n_agents=50, n_generations=100, return_children=False):

    # results stores all the agents and scores of each generation
    results = np.empty((n_generations, 2, n_agents), dtype=object)

    # initialize agents
    agents = [Agent(env) for _ in range(n_agents)]

    # chidren models
    children = np.empty((n_generations, 4), dtype=np.ndarray)

    for i in range(n_generations):
        results[i][0] = agents
        for j, agent in enumerate(agents):
            score = agent.run_agent()
            results[i][1][j] = score

        child = crossover_function(agents, results[i][1])
        children[i] = np.array(child, dtype=np.ndarray).reshape(4)
        agents = generate_population(child, n_agents, agents)

    if return_children:
        return results, children

    return results
