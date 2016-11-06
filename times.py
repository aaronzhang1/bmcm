import rand

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def mean(lst):
	return reduce(lambda x, y: x + y, lst) / (len(lst) + 0.0)

def variance(lst):
	mean_ = mean(lst)

	squaredDiffs = []

	# for each number subtract the Mean and square the result.
	for num in lst:
		squaredDiffs.append((num - mean_)**2)

	# take the mean of the squared diffs
	avgSquaredDiff = mean(squaredDiffs)

	return avgSquaredDiff**(.5)

def dist(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def avgPokePerTime():
	poke = []
	times = {}

	for currTime in range(max(ts), -1, -1):
		# subtract 1 from all the pokemon times, and remove the pokemon who have reached
		# zero time
		poke = [p - 1 for p in poke if not p - 1 == 0]
		if currTime in ts:
			poke.append(15)

		times[len(poke)] = times.get(len(poke), 0) + 1
		
  	print times

def varBetweenPokemonTimes():
	diffs = []

	for i in range(0, len(ts) - 1):
		diffs.append(ts[i + 1] - ts[i])

	print mean(diffs)

	print variance(diffs)


def plotHistOfDiffInConsecutivePokemonTimes():
	diffs = []

	for i in range(0, len(ts) - 1):
		diffs.append(ts[i + 1] - ts[i])

	plt.hist(diffs)
	plt.title("Time Diffs Between Consecutive Pokemon (n = " + str(len(xs)) + ")")
	plt.xlabel("Difference (in minutes)")
	plt.ylabel("Frequency")

	plt.show()

def plotHistOfDistBetweenConsecutivePokemons():
	dists = []

	for i in range(0, len(xs) - 1):
		dists.append(dist(xs[i], ys[i], xs[i+1], ys[i+1]))

	plt.hist(dists)
	plt.title("Avg Dist Between Consecutive Pokemon (n = " + str(len(xs)) + ")")
	plt.xlabel("Distance (# of blocks)")
	plt.ylabel("Frequency")

	plt.show()

def plotHistOfDiffInConsecutivePokemonTimesPerCell():

	# in the following we use xs * 10 + ys to hash everything

	mostRecentTime = {}
	diffs = np.zeros((10,10))
	numDiffs = np.zeros((10,10))


	for i in range(0, len(xs)):
		h = xs[i] * 10 + ys[i]
		currTime = ts[i]
		mrt = mostRecentTime.get(h, None)
		if(mrt != None):
			diffs[ys[i] - 1][xs[i] - 1] += currTime - mrt
			numDiffs[ys[i] - 1][xs[i] - 1] += 1
		mostRecentTime[h] = currTime

	sixties = np.empty((10,10))
	sixties[:] = 60

	avgDiff = np.divide(diffs, numDiffs)

	avgDiff = np.divide(avgDiff, sixties)

	plt.imshow(avgDiff, extent=[1,10,1,10], origin='lower', interpolation='none', cmap=np.colormap.Reds)
	plt.colorbar()
	plt.show()



xs = []
ys = []
vs = []
ts = []

with open("Providence_Pokemon_1.csv", "r") as f:
  for line in f:
    x, y, v, t = map(int, line.split(","))
    xs.append(x)
    ys.append(y)
    vs.append(v)
    ts.append(t)

plotHistOfDiffInConsecutivePokemonTimesPerCell()
