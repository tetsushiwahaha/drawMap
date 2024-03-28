#!/usr/bin/env python
import sys, json
import numpy as np
import matplotlib.pyplot as plt

import pptools

def main():
	data = pptools.init()
	x0 = data.dic['x0']
	cnt = 0
	xlist = [[0] ,[0], [0]] 
	while True:
		x = pptools.func(x0, data) 	# x(k+1) = f(x(k))
		if np.linalg.norm(x, ord=2) > data.dic['explode']:
			x = x0
			explodeflag = True
		else:
			explodeflag = False
		for m in range(data.dim):
			xlist[m].append(x[m])
		x0 = x
		cnt += 1
		if (cnt > data.dic['break']): 
			if pptools.window_closed(data.ax) == True:
				sys.exit()
			if explodeflag == True:
				print("exploded.")
			plt.plot(xlist[data.dispx], xlist[data.dispy], '.', 
				markersize = 1, color = "black", alpha = data.dic['alpha'])
			#xlist.clear()
			xlist = [[0] ,[0], [0]] 
			data.dic['x0'] = x0
			cnt = 0
			plt.pause(0.01) 	# plot data and check events

if __name__ == '__main__':
	main()
