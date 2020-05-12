import sys, json
import numpy as np
import matplotlib.pyplot as plt

import pptools
import ppfunc

#########################################################################
# ESSENTIAL CODES BELOW
#########################################################################


def main():
	plt.rcParams['keymap.save'].remove('s')
	plt.rcParams['keymap.quit'].remove('q')

	data = pptools.DataStruct()

	data.fig = plt.figure(figsize=(10, 10))
	data.ax = data.fig.add_subplot(111)

	x0 = data.dict['x0']

	pptools.initial_setup(data)

	plt.connect('button_press_event', 
		lambda event: pptools.on_click(event, x0, data))
	plt.connect('key_press_event', 
		lambda event: pptools.keyin(event, x0, data))
	plt.ion() # I/O non blocking

	running = True

	print(data.dict['params'][0])
	print(data.dict['params'][1])
	
	cnt = 0
	xlist = []
	ylist = []
	while running:
		if pptools.window_closed(data.ax) == True:
			sys.exit()
		x = ppfunc.func(x0, data)
		xlist.append(x[0])
		ylist.append(x[1])
		x0 = x
		if (cnt > data.dict['break']): 
			plt.plot(xlist, ylist, 'o', markersize = 0.3, color="black")
			xlist.clear()
			ylist.clear()
			plt.pause(0.01) 
			cnt = 0
		cnt += 1

if __name__ == '__main__':
	main()
