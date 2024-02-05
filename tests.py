from wsgiref import headers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import matplotlib as mpl
import time
'''
# Import data
file = pd.read_csv('test_in.csv',header=None,  names=['Time', 'root.test.d1.s1', 'root.test.d2.s2', 'root.test.d3.s3'])
data = pd.DataFrame(file)
#print(data)
# 数组切片
for i in range(len(data)):
    data['Time'][i] = time.mktime(time.strptime(
        data['Time'][i], "%Y-%m-%d %H:%M:%S"))-time.mktime(time.strptime(
            data['Time'][0], "%Y-%m-%d %H:%M:%S"))
'''
x = [0, 0.3, 0.5, 0.7, 0.9, 1.1, 1.2, 1.3,
     1.4, 1.5]  # Take the first column of data
# Take the second column of data
y = [0, 1.2, 1.7, 2, 2.1, 2, 1.8, 1.2, 1, 1.6]
# Spline interpolation of correlation functions in SciPy Library
tck = interpolate.splrep(x, y)  # （t，c，k）包含节点向量、B样条曲线系数和样条曲线阶数的元组。
xx = np.linspace(min(x), max(x), 151)
yy = interpolate.splev(xx, tck, der=0)
'''
x1, x2 = -0.02, 2.56
y1 = interpolate.splev(x1, tck, der=0)
y2 = interpolate.splev(x2, tck, der=0)
print('When x = -0.02, the value of Y is：', y1)
print('When x = 2.56, the value of Y is：', y2)
'''
print(yy)

plt.plot(x, y, 'ro', xx, yy, 'b')
plt.legend(['true', 'cubic spline'])
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.title('Three moment method of cubic spline interpolation')
# Save picture
plt.savefig('out2.png', dpi=600)
# Set the resolution at which you want to save the picture
plt.show()
