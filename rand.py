import random
import math

T_MAX = 12 * 60
counts = [410, 333, 271, 198, 165, 150, 91, 80, 48, 53, 51, 44, 23, 23, 22, 11, 11, 4, 4, 7]
sum_counts = sum(counts)
freqs = map(lambda x: 1.0 * x / sum_counts, counts)

# Generates random data for T_MAX minutes
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
      v = rand_value()
      if first:
        t = 0
        first = False
      xs.append(x)
      ys.append(y)
      vs.append(v)
      ts.append(t)
    t += 1
  return xs, ys, vs, ts

# Random Pokemon value using distribution from test data
def rand_value():
  r = random.random()
  for i in range(20):
    if r < freqs[i]:
      return i + 1
    r -= freqs[i]

# Saves random data to file
def rand_file(filename):
  with open(filename, "w") as f:
    xs, ys, vs, ts = rand()
    n = len(xs)
    for i in range(n):
      f.write(",".join(map(str, (xs[i], ys[i], vs[i], ts[i]))) + "\n")

if __name__ == "__main__":
  rand_file("rand.csv")
