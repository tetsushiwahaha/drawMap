import sys, json
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

def keyin(event, s, data):
	ptr = data.param_ptr
	if event.key == 'q':
		plt.close('all') 
		print("quit")	
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

#########################################################################
# ESSENTIAL CODES BELOW
#########################################################################

def func(x, data):
    return [
		x[1] + data.dict['params'][0] * x[0],
		x[0] * x[0] +  data.dict['params'][1]
	]

def main():
	plt.rcParams['keymap.save'].remove('s')
	plt.rcParams['keymap.quit'].remove('q')
	data = DataStruct()

	data.fig = plt.figure(figsize=(10, 10))
	data.ax = data.fig.add_subplot(111)

	x0 = data.dict['x0']

	initial_setup(data)

	plt.connect('button_press_event', 
		lambda event: on_click(event, x0, data))
	plt.connect('key_press_event', 
		lambda event: keyin(event, x0, data))
	plt.ion() # I/O non blocking

	running = True
	
	cnt = 0
	x = []
	xlist = []
	ylist = []
	while running:
		x = func(x0, data)
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

