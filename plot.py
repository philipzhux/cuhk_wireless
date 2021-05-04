"""
===============
Curve fitting
===============

Demos a simple curve fitting
"""

############################################################
# First generate some data
import numpy as np
import csv
# Seed the random number generator for reproducibility
np.random.seed(0)
with open('/Users/philip/Downloads/Untitled 6.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
x_data = []
y_data = []
for d in data:
    print(d[2])
    x_data.append(d[1])
    y_data.append(d[2])
x_data = np.asarray(x_data,dtype='float64')
y_data = np.asarray(y_data,dtype='float64')

# And plot it
import matplotlib.pyplot as plt

# plt.figure()
# plt.scatter(x_data, y_data)

############################################################
# Now fit a simple sine function to the data
from scipy import optimize
def linear(x, a, b):
    return a*x+b

def two_degree(x, a, b,c):
    return a*x**2+b*x+c

linear_params, linear_params_covariance = optimize.curve_fit(linear, x_data, y_data)
two_params, two_params_covariance = optimize.curve_fit(two_degree, x_data, y_data)
print("LINEAR:")
print("PARAMS:",linear_params)
print("COVARIANCE:",linear_params_covariance)

print("SECOND DEGREE:")
print("PARAMS:",two_params)
print("COVARIANCE:",two_params_covariance)
############################################################
# And plot the resulting curve on the data

plt.figure()
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, linear(x_data, linear_params[0], linear_params[1]),
         label='Linear Fitted function')
plt.plot(x_data, two_degree(x_data, two_params[0], two_params[1],two_params[2]),
         label='Second Degree Fitted function')


plt.show()
