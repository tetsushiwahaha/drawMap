#!/usr/bin/env python
import sys, json
import numpy as np
import matplotlib.pyplot as plt

import pptools

def main():

	data = pptools.init()
	x0 = data.dic['x0']

	running = True
	
	cnt = 0
	xlist = []
	ylist = []
	while True:
		if pptools.window_closed(data.ax) == True:
			sys.exit()
		x = pptools.func(x0, data)
		if np.linalg.norm(x, ord=2) > data.dic['explode']:
			x = x0
			explodeflag = True
		else:
			explodeflag = False
		xlist.append(x[0])
		ylist.append(x[1])
		x0 = x
		cnt += 1
		if (cnt > data.dic['break']): 
			if explodeflag == True:
				print("exploded.")
			plt.plot(xlist, ylist, 'o', markersize = 0.3, 
				color="black", alpha = data.dic['alpha'])
			xlist.clear()
			ylist.clear()
			data.dic['x0'] = x0
			cnt = 0
			plt.pause(0.01) 

if __name__ == '__main__':
	main()
