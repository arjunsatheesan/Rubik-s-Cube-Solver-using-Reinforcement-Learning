'''Q_Learn.py
Final Project
CSE 415 Wi-18 by
Ajay Dhavane(ajayd92), Arjun Satheesan(arjun89)
Guide: S. Tanimoto

This file descibes the Q-learning algorithm using
the approach of SARSA with linear function
approximation for a 2x2x2 Rubik's cube

'''
import random

# State class for Q-learning
class State:
    def __init__(self):
        self.next_state = None # s'
        self.nextAction = None # a
        self.nextActionPrime = None # a'
        self.count = {} # dictionary mapping each state to its visit count

    def import_parameters(self,paramterlist):
        self.start_state = paramterlist[0] # s
        self.current_state = self.start_state

        self.ops = paramterlist[1] # list of all possible operators

        self.R = paramterlist[2] # reward function

        self.features = paramterlist[3]

        self.weights = paramterlist[4]

        self.goal_test = paramterlist[5]

        self.goal_message = paramterlist[6] 

    # Return next action to be taken from initial state
    # based on epsilon greedy algorithm
    def select_action_epsilon_greedy(self, epsilon):
        intended_action_prob = random.uniform(0.0,1.0)
        # If it's not epsilon percent, we must find the optimal action
        if intended_action_prob > epsilon:
            nextAction = self.select_action_policy_based(self.current_state)

        # Choose random action
        else:
            nextAction = random.choice(self.ops)
                
        return nextAction

    # Return best/optimal action using a policy
    # based on Q values
    def select_action_policy_based(self, state):
        maxsuccQ = -float("inf")
        nextAction = None
        for op in self.ops:
            successor = op.apply(state)
            succQ_val = self.computesuccQval(successor)

            if succQ_val > maxsuccQ:
                maxsuccQ = succQ_val
                nextAction = op

        return nextAction

    # Used to make a specified rotation
    def carry_action(self,action_op):
        successor = action_op.apply(self.current_state)
        if successor not in self.count.keys():
            self.count[successor] = 1 # insert new explored state as key
        else:
            self.count[successor] += 1 # increase visit count of state
            
        succQ_val = self.computesuccQval(successor)
        self.Q[(self.current_state,action_op.name)] = succQ_val # update Q dictionary
        
        return successor # return new state

    # Run nEpisodes of Q-learning
    def QLearning(self, discount, nEpisodes, epsilon, step_size):
        self.Q = {}
        for i in range(nEpisodes):
            print("======================")
            print("Episode ", i)
            self.current_state = self.start_state # initialize current state for each episode
            self.nextAction = self.select_action_epsilon_greedy(epsilon) # select action based on epsilon greedy
            counter = 0
            while(counter < 51): # run specified number of steps for each episode
                if self.goal_test(self.current_state):
                    print(self.goal_message(self.current_state))
                    break

                self.next_state = self.carry_action(self.nextAction) # make a move from current state
                print("Action:", self.nextAction.name) 
                print("Next state:")
                print(self.next_state)
             
                reward = self.R(self.next_state) # compute reward on new state

                # Compute best action to be taken from this new state
                self.nextActionPrime = self.select_action_policy_based(self.next_state)

                # update Q dictionary
                self.Q[(self.next_state, self.nextActionPrime.name)] = self.computesuccQval(self.nextActionPrime.apply(self.next_state))

                # compute value of delta according to sarsa approach
                delta = reward + discount * self.Q[(self.next_state, self.nextActionPrime.name)] - self.Q[(self.current_state, self.nextAction.name)]

                feature_list = [1]
                for i in range(5):
                    feature_list.append(self.features[i](self.next_state))

                # update weights
                for i in range(6):
                    self.weights[i] += step_size * delta * feature_list[i]

                self.current_state = self.next_state # s = s'
                self.nextAction = self.nextActionPrime # a = a'
                counter +=1

    # Return Q value of state using weighted sum of features
    def computesuccQval(self, successor):
        succ_faces_completed = self.features[0](successor)
        succ_layers_completed = self.features[1](successor)
        succ_threes_count = self.features[2](successor)
        succ_twos_count = self.features[3](successor)
        succ_uniquecolors_count = self.features[4](successor)
        
        succQ_val = self.weights[0] + self.weights[1] * succ_faces_completed\
                        + self.weights[2] * succ_layers_completed\
                        + self.weights[3] * succ_threes_count\
                        + self.weights[4] * succ_twos_count\
                        + self.weights[5] * succ_uniquecolors_count

        # decrease Q value for frquently visited states 
        if successor in self.count.keys():
            succQ_val -= self.count[successor]*3

        return succQ_val
