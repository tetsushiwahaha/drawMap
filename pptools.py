import os
import sys, json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.backends.backend_pdf import PdfPages

class DataStruct():
	def __init__(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-tex', action='store_true')
		parser.add_argument('arg1')
		args = parser.parse_args()
		fd = open(args.arg1, 'r')
		self.dic = json.load(fd)
		fd.close()
		self.tex = args.tex
		self.param_ptr = 0
		self.ax =None
		self.fig =None
		self.dispx = 0
		self.dispy = 1
		self.dim = len(self.dic['func'])
		self.now = [0.0] * self.dim
		if self.dic.get('alpha', None) == None:
			self.dic['alpha'] = 1.0
		if self.dic.get('dump_data', None) == 1:
			bn = os.path.splitext(os.path.basename(sys.argv[1]))[0]
			bn += '.dat'
			self.fd_file = open(bn, mode='w')

def init():
	data = DataStruct()
	plt.rcParams['keymap.save'].remove('s')
	plt.rcParams['keymap.quit'].remove('q')
	plt.rcParams['keymap.fullscreen'].remove('f')

	if data.tex:
		params = {'text.usetex': True,
			'legend.fontsize': 12, 'axes.labelsize': 12,
			'axes.titlesize': 12, 'xtick.labelsize' :10,
			'ytick.labelsize': 10, 'font.family': 'serif',
			'grid.color': 'k', 'grid.linestyle': ':',
			'grid.linewidth': 0.2,
			'axes.xmargin': 0,'axes.ymargin': 0,
		}
		plt.rcParams.update(params)

	data.fig = plt.figure(figsize=(10, 10))
	data.ax = data.fig.add_subplot(111)

	redraw_frame(data)
	data.visual_orbit = 1

	plt.connect('button_press_event', 
		lambda event: on_click(event, data))
	plt.connect('key_press_event', 
		lambda event: keyin(event, data))
#	plt.connect('close_event', 
#		lambda event: closeall(event, data))
#	plt.connect('figure_enter_event', 
#		lambda event: figureenter(event, data))
#	data.fig.canvas.get_tk_widget().focus_force()

	show_param(data)
	return data


def redraw_frame(data):
	xr = data.dic['xrange']
	yr = data.dic['yrange']
	data.ax.set_xlim(xr)
	data.ax.set_ylim(yr)
	data.ax.set_xlabel('$x$', fontsize=12)
	data.ax.set_ylabel('$y$', fontsize=12)
	data.ax.grid(c='gainsboro', ls='--', zorder=9)


class jsonconvert(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj)
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		else:
			return super(jsonconvert, self).default(obj)

def window_closed(ax):
	fig = ax.figure.canvas.manager
	mgr = plt._pylab_helpers.Gcf.figs.values()
	return fig not in mgr

def keyin(event, data):
	ptr = data.param_ptr
	#dim = len(data.dic['x0'])
	dim = len(data.dic['func'])
	if event.key == '+':
		data.dispx += 1
		if data.dispx >= dim:
			data.dispx = 0
		data.dispy = data.dispx + 1
		if data.dispy >= dim:
			data.dispy = 0
		print(data.dispx, data.dispy)
	elif event.key == '-':
		data.dispx -= 1
		if data.dispx < 0 :
			data.dispx = dim - 1
		data.dispy -= 1
		if data.dispy < 0 :
			data.dispy = dim - 1
		print(data.dispx, data.dispy)
	elif event.key == 'q':
		plt.close('all') 
		print("quit")	
		sys.exit()
	elif event.key == 'w':
		jd = json.dumps(data.dic, cls = jsonconvert)
		print(jd)
		with open("__ppout__.json", 'w') as fd:
			json.dump(data.dic, fd, indent=4, cls = jsonconvert)
		print("now writing...", end="")
		pdf = PdfPages('snapshot.pdf')
		pdf.savefig()
		pdf.close()
		print("done.")
	elif event.key == ' ' or event.key == 'e':
		plt.cla()
		redraw_frame(data)
	elif event.key == 'f':
		#plt.cla()
		redraw_frame(data)
		data.visual_orbit = 1 - data.visual_orbit
	elif event.key == 's':
		for i in data.dic['params']:
			print(i, end=' ')
		print(data.dic['x0'])
		#print(data.dic['period'])
	elif event.key == 'p':
		data.param_ptr += 1
		if data.param_ptr >= len(data.dic['params']):
			data.param_ptr = 0
		print(f"changable parameter: {data.param_ptr}")
	elif event.key == 'P':
		data.param_ptr -= 1
		if data.param_ptr < 0:
			data.param_ptr = len(data.dic['params'])-1
		print(f"changable parameter: {data.param_ptr}")
	elif event.key == 'up':
		ptr = data.param_ptr
		data.dic['params'][ptr] += data.dic['dparams'][ptr] 
	elif event.key == 'down':
		ptr = data.param_ptr
		data.dic['params'][ptr] -= data.dic['dparams'][ptr] 
	show_param(data)
	return

def show_param(data):
	s = ""
	cnt = 0
	for key in data.dic['params']:
		s += " $p_{:d}: {:.5g}$,  ".format(cnt, key) 
		cnt += 1
	print(s)
	plt.title(s, color='b')

def on_click(event, data):
	if event.xdata == None or event.ydata == None:
		return
	s0 = data.now # only alloc s0
	s0[data.dispx] = event.xdata
	s0[data.dispy] = event.ydata
	#print(s0, data.dic['period'])
	print(s0)
	plt.plot(s0[data.dispx], s0[data.dispy], 'o', markersize = 2, color="blue")
	# copies an average value to the rest state variables
	avg = (s0[data.dispx] + s0[data.dispy])/2.0
	for i in np.arange(len(s0)):
		if (i != data.dispx and i != data.dispy):
			s0[i] = avg
	redraw_frame(data)
	show_param(data)
	data.now = s0
	return

def func(x, data):
	v =  []
	for k in np.arange(len(data.dic['func'])):
		v.append(eval(data.dic['func'][k]))
	return v

def figureenter(event, data):
	print("xxxxxxxxxxxxx")
	return

def on_close():
	running = False

def dump_data(time, state, data):
	for i in np.arange(len(state.t)):
		data.fd_file.write("{0:.6f} ".format(time + state.t[i]))
		for j in np.arange(len(data.dic['x0'])):
			data.fd_file.write("{0:.6f} ".format(state.y[j,i]))
		data.fd_file.write("\n")
