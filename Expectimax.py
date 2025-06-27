from Game2048 import *
import math

class Player(BasePlayer):
    def __init__(self, timeLimit):
        # Initialize the base player with the given time limit
        super().__init__(timeLimit)
        # Stats for debugging and analysis (optional)
        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0

    def findMove(self, state):
        self._count += 1
        actions = self.moveOrder(state)
        depth = 1  # Start search depth at 1
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
        # If the game is over or we've reached the search depth, return heuristic value
        if state.gameOver() or depth == 0:
            return self.heuristic(state)
        if is_player_turn:
            # Player's turn (max node): try all moves and pick the one with the highest value
            actions = self.moveOrder(state)
            best = -float('inf')
            for a in actions:
                result, _ = state.result(a)  # Simulate move 'a'
                v = self.expectimax(result, depth-1, False)  # Next is a chance node
                if v is not None and v > best:
                    best = v  # Update best value
            return best
        else:
            # Chance node: average over all possible random tile placements
            total = 0  # Sum of weighted values
            count = 0  # Sum of probabilities
            for a in state.actions():  # For each possible move
                for next_state, prob in state.possibleResults(a):  # For each possible result and its probability
                    v = self.expectimax(next_state, depth-1, True)  # Next is player's turn
                    if v is not None:
                        total += prob * v  # Weighted sum
                        count += prob     # Total probability
            if count == 0:
                return self.heuristic(state)  # If no possible results, use heuristic
            return total / count  # Return expected value

    def heuristic(self, state):
        return state.getScore()

    def moveOrder(self, state):
        # Return all legal moves from the current state
        return state.actions()

    def stats(self):
        # Print average search depth and branching factor (for analysis)
        print(f"Average depth: {self._depthCount/self._count:.2f}")
        print(f"Branching factor: {self._childCount / self._parentCount:.2f}")