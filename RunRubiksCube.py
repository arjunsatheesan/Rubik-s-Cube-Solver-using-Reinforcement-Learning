'''RunRubiksCube.py
Final Project
CSE 415 Wi-18 by
Ajay Dhavane(ajayd92), Arjun Satheesan(arjun89)
Guide: S. Tanimoto

This file is used to run n episodes of Q-learning on
2x2x2 rubik's cube

'''

import Cube_formulation as Problem, Q_learn, random

# Parameters used for Q-learning
PARAMETERS = [Problem.START_STATE, Problem.OPERATORS, Problem.Reward,\
              Problem.FEATURES,[random.uniform(0.0,1.0) for i in range(6)], Problem.GOAL_TEST,\
              Problem.GOAL_MESSAGE_FUNCTION]
Discount = 0.9
Episodes = 100
Epsilon = 0.1
StepSize = 0.0001 # for gradient descent

# Create object of Q-learning
rubik_Q_learn = Q_learn.State()
def run_Qlearning():
    # USING RULES FOR 2x2x2 
    rubik_Q_learn.import_parameters(PARAMETERS) # passing parameters as argument
    print("=== Q LEARNING ===")
    rubik_Q_learn.QLearning(Discount, Episodes, Epsilon, StepSize)

run_Qlearning()
