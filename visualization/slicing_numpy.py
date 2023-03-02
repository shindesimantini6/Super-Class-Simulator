'''Without using NumPy, write a python function that takes in a 
list of lists, and returns a list of lists of the same dimensions, where all of 
the elements are increased by 1.'''
#%%
########################### WARMUP ###############################
lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
def my_function(lol):
    result = []
    for i in range(len(lol)):
        temp = []
        for j in range(len(lol[i])):
            temp.append(lol[i][j]+1)
        result.append(temp)
    return result

lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
result = my_function(lol)
print(result)
#%%

#What is NumPy Slicing?

import numpy as np
a = np.arange(1,13).reshape(4, 3)
a
#%%
a + 1
#%%

grid = np.arange(1, 26).reshape(5, 5)
grid

# %%
#Accessing first (i.e. 0th) row, all columns:
grid[0, :]
# %%
#Accessing all rows, first (i.e. 0th) column:
grid[:, 0]
# %%
