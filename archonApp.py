import main
import ExampleStrategies
import random
import inspect
from PIL import Image, ImageDraw
from itertools import repeat

def visualizePrison(prison):
	'''Given a prison, output a PIL image of the current state'''
	size = prison.size
	im = Image.new('RGB', map(lambda x: x*10, size))
	draw = ImageDraw.Draw(im)
	for key in prison.cells.keys():
		color=colorFunction(prison.cells[key])
		draw.rectangle([tuple(map(lambda x: x*10, key)), tuple(map(lambda x: (x+1)*10, key))], fill=color)
	return im

def colorFunction(cell):
	'''Given a cell, outputs an appropriate colour based on the contents'''
	if cell.content==None:
		return '#888888'
	else:
		return cell.content.attributes['colour']


def randomColour():
	'''Generate a random PIL colour string ("#xxxxxx")'''
	return '#' + str(hex(random.randint(0, 16777215)))[2:].rjust(6, '0')

def createRandomPrisoner():
	'''Create and return a randomised prisoner, with a "colour" attribute and a 
	strategy chosen from ExampleStrategies.randomStrategy'''
	return main.Prisoner({'colour':randomColour()}, ExampleStrategies.randomStrategy())

def generate(size=(30, 30), prisonerDensity=0.3, frames = 100):
	'''Creates a prison with given parameters, runs a sequence of stages, and returns appropriate images'''
	images = []
	p = main.Prison(size)
	for cell in p.cells:
		if random.random() > prisonerDensity:
			p.cells[cell].content = createRandomPrisoner()

	w = main.Warden(p)

	images.append(visualizePrison(p))

	for i in repeat(None, frames-1):
		w.executeStage()
		images.append(visualizePrison(p))

	return images

def makeGif(filename, images):
	'''Given a filename and a sequence of images, output a gif'''
	import sys
	sys.path.append('src')
	import images2gif
	images2gif.writeGif(filename, images)
