import json, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class DataStruct():
	def __init__(self):
		if len(sys.argv) != 2:
			print(f"Usage: python {sys.argv[0]} filename")
			sys.exit(0)
		fd = open(sys.argv[1], 'r')
		self.dic = json.load(fd)
		fd.close()
		self.param_ptr = 0
		self.pause = False
		self.ax = None
		self.fig = None
		self.running = True
		if self.dic.get('alpha', None) == None:
			self.dic['alpha'] = 1.0
		if self.dic.get('explode', None) == None:
			self.dic['explode'] = 1000.0

def init():
	plt.rcParams['keymap.save'].remove('s')
	plt.rcParams['keymap.quit'].remove('q')
	plt.rcParams['font.size'] = 16

	data = DataStruct()

	data.fig = plt.figure(figsize=(8, 8))
	data.ax = data.fig.add_subplot(111)

	redraw_frame(data)

	plt.connect('button_press_event', 
		lambda event: on_click(event, data.dic['x0'], data))
	plt.connect('key_press_event', 
		lambda event: keyin(event, data.dic['x0'], data))
	plt.ion() # I/O non blocking
	return data

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
		jd = json.dumps(data.dic)
		print(jd)
		with open("__ppout__.json", 'w') as fd:
			json.dump(data.dic, fd, indent=4)
		print("now writing...", end="")
		pdf = PdfPages('snapshot.pdf')
		pdf.savefig()
		pdf.close()
		print("done.")
	elif event.key == 'x':
		if (data.pause == True):
			data.pause = False
		else:
			data.pause = True
	elif event.key == ' ' or event.key == 'e':
		plt.cla()
		redraw_frame(data)
	elif event.key == 'f':
		plt.cla()
		redraw_frame(data)
	elif event.key == 's':
		for i in data.dic['params']:
			print(i, end=' ')
		print(s[0], s[1])
	elif event.key == 'p':
		data.param_ptr += 1
		if data.param_ptr >= len(data.dic['params']):
			data.param_ptr = 0
		print(f"changable parameter: {data.param_ptr}")
	elif event.key == 'up':
		ptr = data.param_ptr
		data.dic['params'][ptr] += data.dic['dparams'][ptr] 
	elif event.key == 'down':
		ptr = data.param_ptr
		data.dic['params'][ptr] -= data.dic['dparams'][ptr] 
	show_param(data)

def show_param(data):
	s = ""
	cnt = 0
	for key in data.dic['params']:
		s += " param{:d}: {:.5f}  ".format(cnt, key) 
		cnt += 1
	plt.title(s, color=(0.6, 0.6, 0.8))

def on_click(event, s0, data):
	if event.xdata == None and event.ydata == None:
		return
	s0[0] = event.xdata
	s0[1] = event.ydata
	plt.plot(s0[0], s0[1], 'o', markersize = 2, color="red")
	print(s0[0], s0[1])
	data.running = True
	redraw_frame(data)
	show_param(data)

def on_close():
	running = False

def redraw_frame(data):
	xr = data.dic['xrange']
	yr = data.dic['yrange']
	data.ax.set_xlim(xr[0], xr[1])
	data.ax.set_ylim(yr[0], yr[1])
	data.ax.set_xlabel('$x$', fontsize=18)
	data.ax.set_ylabel('$y$', fontsize=18)
	data.ax.grid(c = 'gainsboro', zorder = 9)

def func(x, data):
    v =  []
    for i in np.arange(len(data.dic['func'])):
        v.append(eval(data.dic['func'][i]))
    return v
