from Game2048 import *
import numpy as np
import random

class Player(BasePlayer):
    def __init__(self, timeLimit):
        super().__init__(timeLimit)
        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0
        self.initial_tries = 5
        self.num_tries = 200
        self.max_depth = 10
        self.debug = True
        
        self.indextomove = {0:'U', 1:'D', 2:'L', 3:'R'}
        self.movetoindex = {'U':0, 'D':1, 'L':2, 'R':3}

    def findMove(self, state):
        self._count += 1
        actions = self.moveOrder(state)
        if not actions:
            self.setMove(None)
            return
            
        bestmove = self.ucb_monte_carlo(state, actions)
        self.setMove(bestmove)

    def ucb_monte_carlo(self, state, actions):
        bestscore = -1
        bestmove = actions[0]
        validmoves = []

        action_score = np.array([0.0, 0.0, 0.0, 0.0])
        action_tries = np.array([0, 0, 0, 0])

        exploration_tries, exploration_score = 0, 0

        # Initial exploration phase
        for move in ['U', 'D', 'L', 'R']:
            if move in actions:
                validmoves.append(move)
                
                for tries in range(self.initial_tries):
                    if not self.timeRemaining():
                        break
                    result, _ = state.result(move)
                    montecarlo_score = self.playthrough(result, 1, self.max_depth)

                    maxindex = self.movetoindex[move]
                    action_tries[maxindex] += 1
                    action_score[maxindex] += montecarlo_score

                    exploration_tries += 1
                    exploration_score += montecarlo_score
            else:
                action_tries[self.movetoindex[move]] = self.initial_tries
                action_score[self.movetoindex[move]] = -1000000

        # UCB exploration factor
        c = max(1, state.getScore())
        if self.debug:
            print('Exploration Factor:', c)

        # Main UCB Monte Carlo phase
        for totaltries in range(self.num_tries):
            if not self.timeRemaining():
                break
                
            # Calculate UCB values
            action_heuristic = action_score/action_tries + c*np.sqrt(np.log(totaltries+1)/action_tries)

            maxindex = np.argmax(action_heuristic)
            move = self.indextomove[maxindex]

            if move in actions:
                result, _ = state.result(move)
                montecarlo_score = self.playthrough(result, 1, self.max_depth)

                action_tries[maxindex] += 1
                action_score[maxindex] += montecarlo_score

        if self.debug:
            print('No. of tries:', action_tries)
            print('avg score:', action_score/action_tries)

        bestmoveindex = np.argmax(action_score/action_tries)
        bestmove = self.indextomove[bestmoveindex]

        if self.debug:
            print('Best move:', bestmove)
            
        return bestmove

    def playthrough(self, state, num_tries, max_depth):
        total_score = 0
        for i in range(num_tries):
            if not self.timeRemaining():
                break
            newstate = state
            depth = 0
            
            while not newstate.gameOver() and depth < max_depth:
                if not self.timeRemaining():
                    break
                    
                actions = newstate.actions()
                if not actions:
                    break
                    
                random_action = random.choice(actions)
                newstate, _ = newstate.result(random_action)
                depth += 1
                
            total_score += newstate.getScore()
            
        return total_score / num_tries if num_tries > 0 else 0

    def heuristic(self, state):
        return state.getScore()

    def moveOrder(self, state):
        return state.actions()

    def stats(self):
       print(f'Average depth: {self._depthCount/self._count:.2f}')
       print(f'Branching factor: {self._childCount / self._parentCount:.2f}')