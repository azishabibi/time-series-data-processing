import matplotlib.pyplot as plt
import math
import numpy as np
import time

class Spline:
    u"""
    Cubic Spline class
    usage:
        spline=Spline(x,y)
        rx=np.arange(0,4,0.1)
        ry=[spline.calc(i) for i in rx]
    """

    def __init__(self, x, y):
        self.b, self.c, self.d, self.w = [], [], [], []

        self.x = x
        self.y = y

        self.nx = len(x)  # dimension of x
        h = np.diff(x)

        # calc coefficient c
        self.a = [iy for iy in y]

        # calc coefficient c
        A = self.__calc__A(h)
        B = self.__calc__B(h)
        self.c = np.linalg.solve(A, B)
        #  print(self.c1)

        # calc spline coefficient b and d
        for i in range(self.nx - 1):
            self.d.append((self.c[i + 1] - self.c[i]) / (3.0 * h[i]))
            tb = (self.a[i + 1] - self.a[i]) / h[i] - h[i] * \
                (self.c[i + 1] + 2.0 * self.c[i]) / 3.0
            self.b.append(tb)

    def calc(self, t):
        u"""
        Calc position
        if t is outside of the input x, return None
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.a[i] + self.b[i] * dx + \
            self.c[i] * dx ** 2.0 + self.d[i] * dx ** 3.0

        return result

    def __search_index(self, x):
        u"""
        search data segment index
        """

        for i in range(self.nx):
            if self.x[i] - x > 0:
                return i - 1

    def __calc__A(self, h):
        u"""
        calc matrix A for spline coefficient c
        """
        A = np.zeros((self.nx, self.nx))
        A[0, 0] = 1.0
        for i in range(self.nx - 1):
            if i is not self.nx - 2:
                A[i + 1, i + 1] = 2.0 * (h[i] + h[i + 1])
            A[i + 1, i] = h[i]
            A[i, i + 1] = h[i]

        A[0, 1] = 0.0
        A[self.nx - 1, self.nx - 2] = 0.0
        A[self.nx - 1, self.nx - 1] = 1.0
        return A

    def __calc__B(self, h):
        u"""
        calc matrix B for spline coefficient c
        """
        B = np.zeros(self.nx)
        for i in range(self.nx - 2):
            B[i + 1] = 3.0 * (self.a[i + 2] - self.a[i + 1]) / \
                h[i + 1] - 3.0 * (self.a[i + 1] - self.a[i]) / h[i]

        return B

 # input
x = [0, 0.3, 0.5, 0.7, 0.9, 1.1, 1.2, 1.3, 1.4, 1.5]
y = [0, 1.2, 1.7, 2, 2.1, 2, 1.8, 1.2, 1, 1.6]
points = 10000

# 3d spline interporation
time1=time.time()
spline = Spline(x, y)
rx = (np.linspace(min(x), max(x), points)).tolist()
#ry=[]
ry = [spline.calc(i) for i in rx]
'''
for i in range(len(rx)):
    ry.append(spline.calc(rx[i]))
'''
time2=time.time()
print(time2-time1)
print(ry)
plt.plot(rx,ry)
plt.show()