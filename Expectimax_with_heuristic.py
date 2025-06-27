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
        bestMove = None 
        depth = 1

        while self.timeRemaining():
            self._depthCount += 1
            self._parentCount += 1
            self._nodeCount += 1

            print(f"Search depth {depth}")

            bestValue = -math.inf
            for move in self.moveOrder(state):
                if not self.timeRemaining(): 
                    break
                child, _ = state.result(move)
                val = self.expectimax(child, depth - 1, isPlayerTurn=False)
                if val is None: 
                    break
                if val > bestValue:
                    bestValue = val
                    bestMove = move

            if bestMove is not None:
                self.setMove(bestMove)
                print(f"\tBest expected value: {bestValue} → {bestMove}")

            depth += 1

    def expectimax(self, state, depth, isPlayerTurn):
        self._nodeCount += 1

        if state.gameOver():
            return state.getScore()

        if depth == 0:
            return self.heuristic(state)

        if isPlayerTurn:
            best = -math.inf
            for move in self.moveOrder(state):
                if not self.timeRemaining():
                    return None
                child, _ = state.result(move)
                val = self.expectimax(child, depth, isPlayerTurn=False)
                if val is None:
                    return None
                best = max(best, val)
                self._childCount += 1
            self._parentCount += 1
            return best

        else:
            exp_value = 0.0
            total_prob = 0.0
            for move in state.actions():
                for next_state, prob in state.possibleResults(move):
                    if not self.timeRemaining():
                        return None
                    val = self.expectimax(next_state, depth - 1, isPlayerTurn=True)
                    if val is None:
                        return None
                    exp_value += prob * val
                    total_prob += prob
                    self._childCount += 1
            self._parentCount += 1
            if total_prob == 0:
                return self.heuristic(state)
            return exp_value / total_prob

    def heuristic(self, state):
         empty = 0
         for i in range(4):
                for j in range(4):
                    if state.getTile(i, j) == 0:
                        empty += 1
         return empty + state.getScore()

    def moveOrder(self, state):
        return state.actions()

    def stats(self):
        print(f"Average depth: {self._depthCount/self._count:.2f}")
        print(f"Branching factor: {self._childCount / self._parentCount:.2f}")