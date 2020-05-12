def func(x, data):
	''' A function definition for map.py
	Parameters:
	x: float array
	data: class
		data.dict: parameters from an input Json file
		data.dict['params']: parameter array
'''


	return [
		x[1] + data.dict['params'][0] * x[0],
		x[0] * x[0] +  data.dict['params'][1]
	]
