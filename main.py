class Prison:
	def __init__(self, size):
		self.size = size
		self.cells = {}
		self.scores = {}
		for row in range(size[1]):
			for column in range(size[0]):
				self.cells[(row, column)] = Cell(self, (row, column))
				self.scores[(row, column)] = 0
		for cell in self.cells.values():
			cell.updateNeighbours()

	def resetScores(self):
		for key in self.scores.keys():
			self.scores[key] = 0

	def incrementScore(self, position, increment):
		self.scores[position] += increment

class Cell:
	def __init__(self, parentPrison, position, content=None):
		self.parentPrison = parentPrison
		self.position = position
		self.content = content
		self.neighbours = {}

	def updateNeighbours(self):
		offsets = {'N':(-1, 0), 'E':(0, 1), 'S':(1, 0), 'W':(0, -1)}
		for direction in (offsets):
			neighbourPosition = (self.position[0] + offsets[direction][0], self.position[1] + offsets[direction][1])
			if neighbourPosition[0] > -1 and neighbourPosition[0] < self.parentPrison.size[0] and neighbourPosition[1] > -1 and neighbourPosition[1] < self.parentPrison.size[1]:
				self.neighbours[direction]=self.parentPrison.cells[neighbourPosition]

	def findMaxInNeighbourhood(self):
		scores={}
		for neighbour in self.neighbours.values():
			scores[self.parentPrison.scores[neighbour.position]] = neighbour
		scores[self.parentPrison.scores[self.position]] = self
		return scores[max(scores.keys())]

class Prisoner:
	def __init__(self, attributes, strategy):
		self.attributes = attributes
		self.strategy = strategy
		self.history = {}
		#history is of the form {<Prisoner>: [(n11, n12), (n21, n22), (n31, n32)...]}, where the n values are what this prisoner and <Prisoner> chose at each previous interaction

	def addToHistory(self, opponent, choices):
		try:
			self.history[opponent].append(choices)
		except KeyError:
			self.history[opponent] = [choices]

class ConflictManager:
	def __init__(self, payoutMatrix=None):
		
		#################################################################
		# of the form [[a, b], [c, d]], where:
		# a = both co-operate
		# b = 0 co-operates, 1 defects
		# c = 0 defects, 1 co-operates
		# d = both defect
		#
		# and
		# 
		# each element is a (a1,a2) of int values, with payout for (0, 1)	
		#################################################################

		if payoutMatrix==None:
			self.payoutMatrix = [[(2,2), (0, 3)], [(3,0), (1,1)]]
		else:
			self.payoutMatrix = payoutMatrix

	def manageConflict(self, prisoner0, prisoner1):
		# prisonerNDecision is 0 if they co-operate, 1 if they defect
		prisoner0Decision = prisoner0.strategy(prisoner0, prisoner1)
		prisoner1Decision = prisoner1.strategy(prisoner1, prisoner0)
		prisoner0.addToHistory(prisoner1, (prisoner0Decision, prisoner1Decision))
		prisoner1.addToHistory(prisoner0, (prisoner1Decision, prisoner0Decision))
		return self.payoutMatrix[prisoner0Decision][prisoner1Decision]

class Warden:
	def __init__(self, prison):
		self.prison = prison
		self.cm = ConflictManager()

	def executeRound(self):
		for cell in self.prison.cells.values():
			if cell.content!=None:
				# If the cell has no non-empty neighbours, automatically increment score
				if len(filter(lambda x: x != None, [i.content for i in cell.neighbours.values()])) == 0 and cell.content != None:
					self.prison.incrementScore(cell.position, 0.1)
				else:
					# we only pick the neighbours to the right and below - otherwise, duplication
					neighboursToFight = []
					try:
						neighboursToFight.append(cell.neighbours['E'])
					except KeyError:
						#cell has no east neighbout
						pass
					try:
						neighboursToFight.append(cell.neighbours['S'])
					except KeyError:
						#cell has no south neighbour
						pass
					for neighbour in (neighboursToFight):
						if neighbour.content!=None:
							outcome = self.cm.manageConflict(cell.content, neighbour.content)
							self.prison.incrementScore(cell.position, outcome[0])
							self.prison.incrementScore(neighbour.position, outcome[1])
						else:
							#Have to increment score if players have empty surroundings, otherwise they will not propagate
							self.prison.incrementScore(cell.position, 0.1)

	def executeStage(self):
		self.executeRound()
		self.executeRound()
		self.executeRound()

		new = {}
		for cell in self.prison.cells.values():
			new[cell.position] = cell.findMaxInNeighbourhood().content

		for key in new:
			self.prison.cells[key].content = new[key]

		self.prison.resetScores()
