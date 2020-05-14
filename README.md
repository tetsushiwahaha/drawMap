<img src="https://user-images.githubusercontent.com/52724526/81895103-6d7dc180-95ec-11ea-8760-c08df1757440.png" width=300px>
 
# drawMap --- draw a chaotic attractor dynamically

Chaotic attractor of a difference equation is visualized. 

## Files

* pp.py --- main routine
* ppfunc.py --- a function definition. Change this appropriately.
* pptools.py --- some functions.
* in.json --- sample input file. A JSON format.

## Requirements

* python 3.6 or later
    * numpy
    * matplotlib

## How to use
### to exec

    % python pp.py in.json

### mouse operation 

- A new initial values is given by clicking on the appropriate location
in the graph.
 
### key operation

- s: print the current status
- w: print the dictionary and dump it to `__ppout__.json`
- p: change the active parameter (default: 0, toggle)
- up and down arrows: increase/decrease the active parameter value
- space: clear transitions
- q: quit 
 
### to examine another map
 
 Edit `ppfunc.py` and change expressions in this file.
 
 * `x[0]`, `x[1]`: state variables
 * `data.dict['params'][0]`, `data.dict['params'][1]`: parameters
 
### Example: Henon map
Replace the return sentence by the following codes:

    return [ 
        1.0 - data.dict['params'][0] * x[0] * x[0] + x[1], 
        data.dict['params'][1] * x[0] 
    ]
 
