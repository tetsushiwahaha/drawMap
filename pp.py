import sys, json
# import numpy as np
import matplotlib.pyplot as plt

import pptools
import ppfunc

def main():

	data = pptools.init()
	x0 = data.dict['x0']

	running = True
	
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
			plt.plot(xlist, ylist, 'o', markersize = 0.3, 
				color="black", alpha = data.dict['alpha'])
			xlist.clear()
			ylist.clear()
			data.dict['x0'] = x0
			plt.pause(0.01) 
			cnt = 0
		cnt += 1

if __name__ == '__main__':
	main()
