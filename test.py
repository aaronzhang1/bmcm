import rand

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def dist(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

xs = []
ys = []
vs = []
ts = []

with open("rand.csv", "r") as f:
  for line in f:
    x, y, v, t = map(int, line.split(","))
    xs.append(x)
    ys.append(y)
    vs.append(v)
    ts.append(t)

dists = [0 for x in range(41)]
n = len(xs)
for i in range(n - 1):
  d = dist(xs[i], ys[i], xs[i + 1], ys[i + 1])
  dists[d] += 1
for i in range(41):
  print i, dists[i]
