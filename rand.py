import random
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

T_MAX = 42 * 24 * 60

# Distribution of locations and values
num_poke = 0
loc_counts = [0 for loc in range(100)]
value_counts = [0 for v in range(20)]
with open("Providence_Pokemon_1.csv", "r") as f:
  for line in f:
    num_poke += 1
    x, y, v, t = map(int, line.split(","))
    loc_counts[10 * (x - 1) + (y - 1)] += 1
    value_counts[v - 1] += 1
loc_freqs = map(lambda x: 1.0 * x / num_poke, loc_counts)
value_freqs = map(lambda x: 1.0 * x / num_poke, value_counts)

# Generates random data for T_MAX minutes
def rand():
  xs = []
  ys = []
  vs = []
  ts = []
  t = 0
  while t <= T_MAX:
    x, y = rand_loc()
    v = rand_value()
    xs.append(x)
    ys.append(y)
    vs.append(v)
    ts.append(t)
    t = int(t + math.ceil(np.random.normal(30, 3)))
  return xs, ys, vs, ts

# Random Pokemon value using distribution from test data
def rand_value():
  r = random.random()
  for i in range(20):
    if r < value_freqs[i]:
      return i + 1
    r -= value_freqs[i]

# Random location using distribution from test data
def rand_loc():
  r = random.random()
  for i in range(100):
    if r < loc_freqs[i]:
      index = i + 1
      return index / 10, index % 10
    r -= loc_freqs[i]

# Saves random data to file
def rand_file(filename):
  with open(filename, "w") as f:
    xs, ys, vs, ts = rand()
    n = len(xs)
    for i in range(n):
      f.write(",".join(map(str, (xs[i], ys[i], vs[i], ts[i]))) + "\n")

if __name__ == "__main__":
  rand_file("rand.csv")
