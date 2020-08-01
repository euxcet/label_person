import os
import sys


def makedirs(path):
    try:
        os.makedirs(path)
    except:
        pass

def distance(x, y):
    return (x[0] - y[0]) * (x[0] - y[0]) + (x[1] - y[1]) * (x[1] - y[1])

def minPoint(x, y):
    if y[0] > 1 and y[1] > 1:
        p = min(x[0], int(y[0]))
        q = min(x[1], int(y[1]))
        return (p, q)
    return x

def maxPoint(x, y):
    if y[0] > 1 and y[1] > 1:
        p = max(x[0], int(y[0]))
        q = max(x[1], int(y[1]))
        return (p, q)
    return x

def symmetry(p, u, v):
    a = v[1] - u[1]
    b = u[0] - v[0]
    c = v[0] * u[1] - v[1] * u[0]
    x = (b * b * p[0] - a * b * p[1] - a * c) / (a * a + b * b)
    y = (a * a * p[1] - a * b * p[0] - b * c) / (a * a + b * b)
    return (2 * x - p[0], 2 * y - p[1])

def toPoint(x):
    return (int(x[0]), int(x[1]))