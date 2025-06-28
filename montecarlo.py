from Game2048 import *
import random

class Player(BasePlayer):
	def __init__(self, timeLimit):
		BasePlayer.__init__(self, timeLimit)

		self._nodeCount = 0
		self._parentCount = 0
		self._childCount = 0
		self._depthCount = 0
		self._count = 0
		self.num_simulations = 200
		self.max_depth = 10

	def findMove(self, state):
		self._count += 1
		actions = self.moveOrder(state)
		depth = 1
		while self.timeRemaining():
			self._depthCount += 1
			self._parentCount += 1
			self._nodeCount += 1
			print('Search depth', depth)
			
			best = -1000
			for a in actions:
				if not self.timeRemaining(): return
				result, score = state.result(a)
				v = self.monte_carlo_value(result, depth-1)
				if v is None: return
				if v > best:
					best = v
					bestMove = a
					
			self.setMove(bestMove)
			print('\tBest value', best, bestMove)

			depth += 1
			
	def monte_carlo_value(self, state, depth):
		self._nodeCount += 1
		self._childCount += 1

		if state.gameOver():
			return state.getScore()
			
		actions = self.moveOrder(state)

		if depth == 0:
			return self.monte_carlo_simulation(state)

		self._parentCount += 1
		
		best = -10000
		for a in actions:
			if not self.timeRemaining(): return None
			result, score = state.result(a)
			v = self.monte_carlo_value(result, depth-1)
			if v is None: return None
			if v > best:
				best = v

		return best

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
		print(f'Average depth: {self._depthCount/self._count:.2f}')
		print(f'Branching factor: {self._childCount / self._parentCount:.2f}')
		print(f'Monte Carlo simulations per move: {self.num_simulations}')
		print(f'Max simulation depth: {self.max_depth}')
		