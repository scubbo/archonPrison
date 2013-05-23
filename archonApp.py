import main
import ExampleStrategies
import random
import inspect
from PIL import Image, ImageDraw
from itertools import repeat

def visualizePrison(prison):
	size = prison.size
	im = Image.new('RGB', map(lambda x: x*10, size))
	draw = ImageDraw.Draw(im)
	for key in prison.cells.keys():
		color=colorFunction(prison.cells[key])
		draw.rectangle([tuple(map(lambda x: x*10, key)), tuple(map(lambda x: (x+1)*10, key))], fill=color)
	return im

def colorFunction(cell):
	if cell.content==None:
		return '#888888'
	else:
		return cell.content.attributes['colour']


#p = main.Prison((5, 5))
#prisoner1 = main.Prisoner({'colour':'#ff0000'}, ExampleStrategies.alwaysCooperate)
#prisoner2 = main.Prisoner({'colour':'#00ff00'}, ExampleStrategies.alwaysCooperate)
#prisoner3 = main.Prisoner({'colour':'#0000ff'}, ExampleStrategies.fiftyFifty)

#p.cells[(0, 0)].content = prisoner1
#p.cells[(2, 3)].content = prisoner2
#p.cells[(4, 1)].content = prisoner3

def randomColour():
	return '#' + str(hex(random.randint(0, 16777215)))[2:].rjust(6, '0')

def createRandomPrisoner():
	return main.Prisoner({'colour':randomColour()}, ExampleStrategies.randomStrategy())

def generate(size=(30, 30), prisonerDensity=0.3, frames = 100):
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

def makeGif(images):
	import sys
	sys.path.append('src')
	import images2gif
	images2gif.writeGif(images)
