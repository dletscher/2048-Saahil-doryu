from Game2048 import *
import math

class Player(BasePlayer):
    def __init__(self, timeLimit):
        super().__init__(timeLimit)
        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0

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
                v = self.expectimax(result, depth-1, False)
                if v is None:
                    return
                if v > best:
                    best = v
                    bestMove = a
            self.setMove(bestMove if bestMove else actions[0])
            print('\tBest value', best, bestMove)
            depth += 1

    def expectimax(self, state, depth, is_player_turn):
        if state.gameOver() or depth == 0:
            return self.heuristic(state)
        if is_player_turn:
            actions = self.moveOrder(state)
            best = -float('inf')
            for a in actions:
                result, _ = state.result(a) 
                v = self.expectimax(result, depth-1, False)
                if v is not None and v > best:
                    best = v
            return best
        else:
 
            total = 0 
            count = 0  
            for a in state.actions(): 
                for next_state, prob in state.possibleResults(a):  
                    v = self.expectimax(next_state, depth-1, True)  
                    if v is not None:
                        total += prob * v 
                        count += prob    
            if count == 0:
                return self.heuristic(state)  
            return total / count  

    def heuristic(self, state):
        return state.getScore()

    def moveOrder(self, state):

        return state.actions()

    def stats(self):

        print(f"Average depth: {self._depthCount/self._count:.2f}")
        print(f"Branching factor: {self._childCount / self._parentCount:.2f}")