import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import random
import math

T_MAX = 42 * 24 * 60

def rand():
  xs = []
  ys = []
  vs = []
  ts = []
  t = 0
  first = True
  while t <= T_MAX:
    if random.randint(1, 30) == 1:
      x = random.randint(1, 10)
      y = random.randint(1, 10)
      v = int(min(math.ceil(np.random.exponential(4)), 20))
      print v
      if first:
        t = 0
        first = False
      xs.append(x)
      ys.append(y)
      vs.append(v)
      ts.append(t)
    t += 1
  return xs, ys, vs, ts

def dist(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

if __name__ == "__main__":
  trials = 10
  sum_dists = 0.0
  for j in range(trials):
    dists = 0.0
    xs, ys, vs, ts = rand()
    n = len(xs)
    for i in range(n - 1):
      d = dist(xs[i], ys[i], xs[i + 1], ys[i + 1])
      dists += d
    sum_dists += dists / (n - 1)
  print sum_dists / trials

'''
with open("rand.csv", "w") as f:
  t = 0
  first = True
  while t <= T_MAX:
    if random.randint(1, 30) == 1:
      x = random.randint(1, 10)
      y = random.randint(1, 10)
      v = 1
      if first:
        t = 0
        first = False
      f.write(",".join(map(str, (x, y, v, t))) + "\n")
    t += 1
'''
