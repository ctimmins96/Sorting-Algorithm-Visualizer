"""
TODOs:
-
"""


### Import Statements
from time import perf_counter

### Class definitions

## SortAlgorithm (Superclass)

class SortAlgorithm:
    _dataSet = None
    _swaps = 0
    _compares = 0
    _tElapsed = 0.00
    _ascending = True

    def __init__(self, dataSet, ascending:bool = True):
        self._dataSet = dataSet.copy()
        self._ascending = ascending

    def getSwaps(self) -> int:
        return self._swaps

    def getCompares(self) -> int:
        return self._compares

    def getData(self) -> list:
        return self._dataSet.copy()

    def getTime(self) -> float:
        return self._tElapsed

    def _swap(self,i,j):
        if i != j:
            tmp = self._dataSet[i]
            self._dataSet[i] = self._dataSet[j]
            self._dataSet[j] = tmp
            self._swaps += 1
    
    def _compare(self, i, j, gt:bool) -> bool:
        self._compares += 1
        if gt:
            return i > j
        else:
            return i < j

    def _swapf(self,i,j):
        print(f"\nSwapping items {i} and {j}...")
        self._swap(i,j)
        print(f"Current Vector: {self._dataSet}")

    def _sort(self): # Bubble swap sorting algorithm for example
        pass

    def sort(self) -> list:
        self._swaps = 0
        self._compares = 0
        tStart = perf_counter()
        self._sort()
        self._tElapsed = perf_counter() - tStart
        return self._dataSet.copy()

## BubbleSort

class BubbleSort(SortAlgorithm):
	# Only Method is _sort
	def _sort(self):
		swap = True
		while swap:
			swap = False
			for i in range(len(self._dataSet) - 1):
				if (not self._ascending) != (self._compare(self._dataSet[i], self._dataSet[i+1], True)):
					swap = True
					self._swap(i, i+1)
		return self._dataSet

## QuickSort

class QuickSort(SortAlgorithm):
    _recur = 0

    def _sort(self,low = 0, high = -1):
        if high == -1:
            high = len(self._dataSet) - 1

        if low < high: # if the array has more than one element in it
            ## Pick a pivot and organize depending on the pivot
            self._recur += 1
            piv = self._partition(low, high)
            if piv == low:
                piv = low+1
            self._sort(low, piv - 1)
            self._sort(piv, high)


    def _partition(self,low,high) -> int:
        piv = self._dataSet[high]
        i = low - 1
        for j in range(low, high):
            if (not self._ascending) != (self._compare(self._dataSet[j], piv, False)):
                i += 1
                self._swap(i, j)
        #if (not swap) or ((i == (high - 1)) and swap):
            #self._swap(int(random.random()*high), high)
        if i == high - 1:
            pass
        else:
            self._swap(i+1, high)
        #print(f"Current Pivot index and value: [{i+1}, {self._dataSet[i+1]}]")
        return (i+1)

    def _partitionf(self, low = 0, high = -1) -> int:
        ret = self._partition(low, high)
        print(f"Pivot Position and Value: [{ret}: {self._dataSet[ret]}]")
        print(f"Current State of Partition: {self._dataSet[low:high + 1]}")
        b = input('Press any key to continue...')

        if b == 'i':
            raise KeyboardInterrupt
        return ret
