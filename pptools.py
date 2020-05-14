import json, sys
import numpy as np
import matplotlib.pyplot as plt

class DataStruct():
	def __init__(self):
		if len(sys.argv) != 2:
			print(f"Usage: python {sys.argv[0]} filename")
			sys.exit(0)
		fd = open(sys.argv[1], 'r')
		self.dict = json.load(fd)
		fd.close()
		self.param_ptr = 0
		self.ax =None
		self.fig =None
		if self.dict.get('alpha', None) == None:
			self.dict['alpha'] = 1.0

def window_closed(ax):
    fig = ax.figure.canvas.manager
    mgr = plt._pylab_helpers.Gcf.figs.values()
    return fig not in mgr

def keyin(event, s, data):
	ptr = data.param_ptr
	if event.key == 'q':
		print("quit")	
		plt.close('all') 
		sys.exit()
	elif event.key == 'w':
		jd = json.dumps(data.dict)
		print(jd)
		with open("__ppout__.json", 'w') as fd:
			json.dump(data.dict, fd, indent=4)
		print("wrote a file")
	elif event.key == ' ' or event.key == 'e':
		plt.cla()
		initial_setup(data)
	elif event.key == 'f':
		plt.cla()
		initial_setup(data)
	elif event.key == 's':
		for i in data.dict['params']:
			print(i, end=' ')
		print(s[0], s[1])
	elif event.key == 'p':
		data.param_ptr += 1
		if data.param_ptr >= len(data.dict['params']):
			data.param_ptr = 0
		print(f"changable parameter: {data.param_ptr}")
	elif event.key == 'up':
		ptr = data.param_ptr
		data.dict['params'][ptr] += data.dict['dparams'][ptr] 
	elif event.key == 'down':
		ptr = data.param_ptr
		data.dict['params'][ptr] -= data.dict['dparams'][ptr] 
	show_param(data)

def show_param(data):
	s = ""
	cnt = 0
	for key in data.dict['params']:
		s += " param{:d}: {:.5f}  ".format(cnt, key) 
		cnt += 1
	plt.title(s, color=(0.8, 0.8, 0.8))

def on_click(event, s0, data):
	s0[0] = event.xdata
	s0[1] = event.ydata
	plt.plot(s0[0], s0[1], 'o', markersize = 2, color="red")
	print(s0[0], s0[1])
	initial_setup(data)
	show_param(data)

def on_close():
	running = False

def initial_setup(data):
	xr = data.dict['xrange']
	yr = data.dict['yrange']
	data.ax.set_xlim(xr[0], xr[1])
	data.ax.set_ylim(yr[0], yr[1])
	data.ax.set_xlabel('x')
	data.ax.set_ylabel('y')
	data.ax.grid(c = 'gainsboro', zorder = 9)

