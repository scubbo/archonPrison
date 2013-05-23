import random

def randomStrategy():
	return random.choice([
		alwaysCooperate, 
		alwaysDefect, 
		fiftyFifty, 
		randomChance(random.random()),
		trustUntilBetrayed, 
		trustUntilBetrayedNTimes(random.randint(1, 10)), 
		trustUntilBetrayedNTimesLimitedMemory(random.randint(1, 10), random.randint(10, 30))
	])

def alwaysCooperate(*args):
	'''Always cooperate with opponents'''
	return 0

def alwaysDefect(*args):
	'''Always defect from opponents'''
	return 1

def fiftyFifty(*args):
	'''Fifty fifty chance of cooperating or defecting'''
	return random.randint(0, 1)

def randomChance(chance):
	'''Betray with a probability of `chance`'''
	def f(me, opponent):
		if random.random() > chance:
			return 1
		else:
			return 0
	return f

def trustUntilBetrayed(me, opponent):
	'''Cooperate with opponents until they betray you - then defect from them'''
	try:
		if [i[1] for i in me.history[opponent]].count(1) > 0:
			return 1
		else:
			return 0
	except KeyError:
		#No previous history with this opponent
		return 0

def trustUntilBetrayedNTimes(n):
	'''Cooperate with opponents until they have betrayed you N times - then defect from them'''
	def f(me, opponent):
		try:
			if [i[1] for i in me.history[opponent]].count(1) > n-1:
				return 1
			else:
				return 0
		except KeyError:
			#No previous history with this opponent
			return 0
	return f

def trustUntilBetrayedNTimesLimitedMemory(n, m):
	'''Cooperate with opponents who have betrayed you fewer than n times in the last m encounters'''
	def f(me, opponent):
		try:
			if [i[1] for i in me.history[opponent]][-m:].count(1) > n-1:
				return 1
			else:
				return 0
		except KeyError:
			#No previous history with this opponent
			return 0
	return f
