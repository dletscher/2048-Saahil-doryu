from Game2048 import *
import math
import random
import time

class Player(BasePlayer):
    def __init__(self, timeLimit):
        super().__init__(timeLimit)
        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0
        self.num_simulations = 50
        self.max_depth = 5

    def findMove(self, state):
        self._count += 1
        actions = self.moveOrder(state)
        depth = 1
        while self.timeRemaining():
            self._depthCount += 1
            self._parentCount += 1
            self._nodeCount += 1
            print('Search depth', depth)
            bestMove = None
            best = -float('inf')
            for a in actions:
                if not self.timeRemaining():
                    return
                result, _ = state.result(a)
                v = self.monte_carlo_simulation(result)
                if v is None:
                    return
                if v > best:
                    best = v
                    bestMove = a
            self.setMove(bestMove if bestMove else actions[0])
            print('\tBest value', best, bestMove)
            depth += 1

    def monte_carlo_simulation(self, state):
        total_score = 0
        
        for _ in range(self.num_simulations):
            if not self.timeRemaining():
                break
            sim_score = self.simulate_random_play(state)
            total_score += sim_score
            
        return total_score / self.num_simulations if self.num_simulations > 0 else 0

    def simulate_random_play(self, state):
        current_state = state
        depth = 0
        
        while not current_state.gameOver() and depth < self.max_depth:
            if not self.timeRemaining():
                break
                
            actions = current_state.actions()
            if not actions:
                break
                
            random_action = random.choice(actions)
            current_state, _ = current_state.result(random_action)
            depth += 1
            
        return current_state.getScore()

    def heuristic(self, state):
        return state.getScore()

    def moveOrder(self, state):
        return state.actions()

    def stats(self):
        print(f"Average depth: {self._depthCount/self._count:.2f}")
        print(f"Branching factor: {self._childCount / self._parentCount:.2f}")
        print(f"Monte Carlo simulations per move: {self.num_simulations}")
        print(f"Max simulation depth: {self.max_depth}")