# drawMap

* map.py --- main routine
* def_func.py --- a function definiton. Change this appropriately.
* in.json --- sample input file.

# to exec

    % python map.py in.json
 
 # to examine another map
 
 Edit `def_func.py` and change expressions in this file.
 
 * `x[0]`, `x[1]`: state variables
 * `data.dict['params'][0]`, `data.dict['params'][1]`: parameters
 
 ## to examine Henon map
  
    return [ 1.0 - data.dict['params'][0] * x[0] * x[0] + x[1], 
        data.dict['params'][1] * x[0] 
    ]
 
 
    
