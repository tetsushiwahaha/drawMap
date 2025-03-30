#!/usr/bin/env python
import sys, json
import numpy as np
import matplotlib.pyplot as plt

import pptools

def main():
	data = pptools.init()
	cnt = 0
	xlist = []
	x = data.dic['x0']
	xlist.append(x)

	while True:
		x = pptools.func(x, data) 	# x(k+1) = f(x(k))
		if np.linalg.norm(x, ord=2) > data.dic['explode']:
			explodeflag = True
		else:
			explodeflag = False
		xlist.append(x)
		cnt += 1
		if (cnt > data.dic['break']): 
			if pptools.window_closed(data.ax) == True:
				sys.exit()
			if explodeflag == True:
				print("exploded.")
			plt.plot(
				[row[data.dispx] for row in xlist], 
				[row[data.dispy] for row in xlist], 'o', 
				markersize = 1, 
				color = "black", alpha = data.dic['alpha'])
			x = data.now = xlist[-1]
			xlist.clear()
			cnt = 0
			plt.pause(0.01) 	# plot data and check events

if __name__ == '__main__':
	main()
