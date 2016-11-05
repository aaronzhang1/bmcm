import rand

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def dist(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def plotAppearancesPerLocation():
	
	heatmap, xedges, yedges = np.histogram2d(xs, ys, bins=10) # returns histogram, x edges, y edges
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]] # define min and max values for plot axis

	plt.clf() # clear the current figure
	
	plt.imshow(heatmap.T, extent=extent, origin='lower', interpolation='none')
	plt.title("Pokemon Appearances Per Location")
	plt.colorbar()

	plt.show()

def plotWeightedAppearancesPerLocation():

	heatmap, xedges, yedges = np.histogram2d(xs, ys, bins=10, weights=vs) # returns histogram, x edges, y edges
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]] # define min and max values for plot axis

	plt.clf() # clear the current figure
	
	plt.imshow(heatmap.T, extent=extent, origin='lower', interpolation='none')
	plt.title("Pokemon Weighted Appearances Per Location")
	plt.colorbar()

	plt.show()

# get the expected value for each individual square
# if weighted then each square is assigned the total value of all the pokemon
# that appear in that square, otherwise each square is assigned the total number of appearances
# for the square
# if normalized, the data is normalized
def getExpectedValuePerSquare(normalized, weighted):

	weights = None
	if weighted:
		weights = vs

	# get the normalized expected value using the histogram function
	heatmap, _unused, _unused = np.histogram2d(xs, ys, bins=10, weights=weights, normed = normalized)
	return heatmap


# normalized and weighted conform to the above function
# currRange is the range of the person we are calculating this for
def getTotalExpectedValueForSquaresInRange(normalized, weighted, currRange):

	# create an array of the same shape as the input valueMap
	valueMap = getExpectedValuePerSquare(normalized, weighted)
	output = np.empty_like(valueMap)

	for i in range(0, len(output)):
		for j in range(0, len(output[i]) ):
			output[i][j] = getSumOfSquaresInRange(i, j, currRange, valueMap)

	return output

# returns the sum of the squares in range, valueMap is the expected value for
# individual squares as a 2d array
def getSumOfSquaresInRange(currRow, currCol, currRange, valueMap):
	output = 0

	for i in range(0, len(valueMap)):
		for j in range(0, len(valueMap[i]) ):
			if dist(currRow, currCol, i, j) <= currRange:
				output += valueMap[i][j]

	return output

def plotExpectedValueSums(normalized, weighted, currRange):
	expectedValueMap = getTotalExpectedValueForSquaresInRange(normalized, weighted, currRange)

	plt.imshow(expectedValueMap.T, extent=[1,10,1,10], origin='lower', interpolation='none')
	plt.colorbar()

	Title = "Expected Poke Value per Location (Range: " + str(currRange) + ")"
	plt.title(Title)
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







