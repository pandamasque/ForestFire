import numpy as np
import random
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm



np.set_printoptions(threshold=sys.maxsize)



__gridDim__ = (200,200)


TREE = 1
NOTHING = 0
FIRE = 2
SPREAD_PROBABILITY = 0.8




def getCompleteSurrounding(x, y):
    return [(i,j) for i in range(x-1, x+2) for j in range(y-1, y+2) if (i != x or j !=y)]


def getVonNeumanSurrounding(x, y):
    return [(x-1,y), (x+1, y), (x, y-1), (x, y+1)]


def AustralianFire(grid, x, y):
    return grid.isTree(x,y)


def ProbabilisticFire(grid, x, y):
    if grid.isTree(x,y):
        return random.randrange(1) <= SPREAD_PROBABILITY


def NorthWindFire(grid, x, y):
    if grid.isTree(x,y):
        X = grid._grid.shape[0] - 1
        return random.randrange(1) <= (x/X)



class Grid:
    
    
    _grid= None


    def __init__(self, dim, p, grid=None):
        if grid is not None:
            self._grid = np.copy(grid._grid)
        else:
            self._grid = np.random.choice(TREE +1, (dim[0]+2,dim[1]+2), p=[1-p, p])
            self._grid[0,:] = NOTHING
            self._grid[-1,:] = NOTHING
            self._grid[:,0] = NOTHING
            self._grid[:,-1] = NOTHING


    def setOnFire(self, x, y):
        self._grid[x+1,y+1] = FIRE


    def setDead(self, x, y):
        self._grid[x+1,y+1] = NOTHING


    def isTree(self, x, y):
        return self._grid[x+1,y+1] == TREE


    def isFire(self, x, y):
        return self._grid[x+1,y+1] == FIRE

    def nbTrees(self):
        return np.sum(self._grid)

    def __repr__(self):
        str = ''
        for i in range(1,self._grid.shape[0]-1):
            for j in range(1,self._grid.shape[1]-1):
                if self._grid[i,j] == TREE:
                    str += 'T'
                else:
                    str += " "
            str += '\n'
        return str



class Forest:


    _grid = None
    _burned = 0
    _adjacenceFunction = None
    _transmitionFunction = None


    def __init__(self, p, adjacenceFunction, transmitionFunction):
        self._grid = Grid(__gridDim__, p)
        self._adjacenceFunction = adjacenceFunction
        self._transmitionFunction = transmitionFunction


    def ignite(self):
        toIgnite = self._spread(__gridDim__[0]//2, __gridDim__[1]//2)
        while len(toIgnite) > 0:
            (x,y) = toIgnite.pop(0)
            toIgnite += self._spread(x, y)
        return self._burned


    def _spread(self, x, y):
        if not self._grid.isTree(x,y):
            return []
        self._grid.setOnFire(x,y)
        self._burned +=1
        ret = []
        for (x1,y1) in self._adjacenceFunction(x, y):
            if self._transmitionFunction(self._grid, x1, y1):
                ret.append((x1,y1))
        return ret


    def nbTrees(self):
        return self._grid.nbTrees()


    def __repr__(self):
        return self._grid.__repr__()



class Simulator:


    def __init__(self, sampling, iteration, adjacenceFunction, transmitionFunction):
        self._adjacenceFunction = adjacenceFunction
        self._transmitionFunction = transmitionFunction
        self._densities = []
        self._sampling = sampling
        self._iteration = iteration
        self._probabilities = np.linspace(1, 0, sampling+1)


    def _simulate(self):
        for i in tqdm(range(self._sampling+1)):
            sum = 0
            trees = 1
            for s in tqdm(range(self._iteration)):
                f = Forest(1-(i/self._sampling), self._adjacenceFunction, self._transmitionFunction)
                trees += f.nbTrees()
                sum += f.ignite()
            self._densities.append(1-(sum/trees))
            #print(trees, sum, i, (trees-1)/(self._iteration*__gridDim__[0]*__gridDim__[1]), 1-(i/self._sampling), sum/trees)
        self._densities = np.array(self._densities)


    def display(self):           
        self._simulate()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self._probabilities, self._densities, color='tab:green')

        for i in range(self._densities.shape[0]-1):
            if self._densities[i] <= 0.5 and self._densities[i+1] >= 0.5:
                X = (0.5-((self._probabilities[i]*self._densities[i+1]-self._probabilities[i+1]*self._densities[i])/(self._probabilities[i]-self._probabilities[i+1])))/((self._densities[i]-self._densities[i+1])/(self._probabilities[i]-self._probabilities[i+1]))
                ax.axvline(x=X, ymin=0, ymax=0.5)
                ax.annotate("p = "+ str(X),xy=(X,0))
                break
        ax.set_title('Percentage of forest burned in function of the forest density')
        plt.show()
        from Interface import Selection
        Selection()