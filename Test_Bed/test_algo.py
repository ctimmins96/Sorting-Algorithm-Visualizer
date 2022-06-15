## import statements
import random
from ct_algorithms import BubbleSort
from ct_algorithms import QuickSort
import matplotlib.pyplot as plt
import datetime

## sortTest
"""
sortTest(algoClass)

Parameter(s):
algoClass[] - Array of Class objects (not instances)
 - Class that contains the sorting algorithm to be tested

 Description:
 Takes a class object and runs a full scale stress test pertaining to the number of average swaps performed and time to complete sorting operation.
 Prints plots that detail the performance of the given algorithm with different sized datasets. Writes data obtained from
 sorted data sets pertaining to the number of swap operations and the time to completion for varying sized datasets.

 Returns:
 None
"""

def sortTest(algoClass = None, sizes = None, nSamp = 200):
	if not sizes:
	    sizes = [10 ** i for i in range(1, 5)]
    # Begin looping through the different desired sizes of array
	if algoClass:
		swaps = { 'mean': [], 'min': [], 'max': [] }
		times = { 'mean': [], 'min': [], 'max': [] }
        accry = []
		for size in sizes:
			print(f"Beginning Sort Test using Size: {size}")
            arr_acc = [0]*len(algoClass)
			arr_swap_mean = [0]*len(algoClass)
			arr_swap_max  = [0]*len(algoClass)
			arr_swap_min  = [size ** 2]*len(algoClass)

			arr_time_mean = [0]*len(algoClass)
			arr_time_max  = [0]*len(algoClass)
			arr_time_min  = [size ** 2]*len(algoClass)

			sum_swap = [0]*len(algoClass)
			sum_time = [0]*len(algoClass)
            sum_accy = [0]*len(algoClass)
			for itr in range(nSamp):
				a = list()
				for i in range(size):
					a.append(random.random()*100)

                ref = sorted(a)
				# Create an object and sort it for each entry in the algoClass object
				for j in range(len(algoClass)):
					srt = algoClass[j]
					print(f"Begin Testing {srt.__name__}.")
					b = srt(a.copy())
					c = b.sort()

                    sum_accy[j] += (c == ref)

					# perform stat calculations for swap data
					sum_swap[j] += b.getSwaps()
					if b.getSwaps() > arr_swap_max[j]: arr_swap_max[j] = b.getSwaps()
					if b.getSwaps() < arr_swap_min[j]: arr_swap_min[j] = b.getSwaps()
					# perform stat calculations for time data
					sum_time[j] += b.getTime()
					if b.getTime() > arr_time_max[j]: arr_time_max[j] = b.getTime()
					if b.getTime() < arr_time_min[j]: arr_time_min[j] = b.getTime()
				print(f"Iteration {itr+1} Complete.")
			for idx in range(len(sum_swap)):
				arr_swap_mean[idx] = sum_swap[idx]/nSamp
				arr_time_mean[idx] = sum_time[idx]/nSamp
                arr_acc[idx] = sum_accy[idx]/nSamp

			# Append data to swaps and times dicts
			swaps['mean'].append(arr_swap_mean.copy())
			swaps['min'].append(arr_swap_min.copy())
			swaps['max'].append(arr_swap_max.copy())

			times['mean'].append(arr_time_mean.copy())
			times['min'].append(arr_time_min.copy())
			times['max'].append(arr_time_max.copy())

            accry.append(arr_acc.copy())
		dt = datetime.datetime.now()
		fName = f"Sorting_Tests_{dt.strftime('%y%m%d_%H%M%S')}.csv"
		with open(fName,'w') as f:
			header = 'Array Size'
			for i in range(len(algoClass)):
				header += f", {algoClass[i].__name__} Accuracy [\%], {algoClass[i].__name__} Swap Min, {algoClass[i].__name__} Swap Mean, {algoClass[i].__name__} Swap Max, {algoClass[i].__name__} Time Min [s], {algoClass[i].__name__} Time Mean [s], {algoClass[i].__name__} Time Max [s]"
			f.write(header)
			f.write('\n')
			# For each size case, generate the row data depending on the number of algoClass entries
			for i in range(len(sizes)):
				rowDat = f"{sizes[i]}"
				for j in range(len(algoClass)):
					rowDat += f", {accry[i][j]}, {swaps['min'][i][j]}, {swaps['mean'][i][j]}, {swaps['max'][i][j]}, {times['min'][i][j]}, {times['mean'][i][j]}, {times['max'][i][j]}"
				rowDat += '\n'
				f.write(rowDat)
			f.close()

## main

def main():
    a = []
    # a = [17, 53, 64, 82, 45, 76, 85, 71, 35, 58, 98, 17, 31, 58, 38, 21, 94, 81, 11, 82]

    ## generate random vector of length 20
    for i in range(20):
       a.append(int(float(random.random()*100 + 1)))

    print('Vector prior to sorting:')
    print(a)
    print('\n')

    b = BubbleSort(a)
    c = QuickSort(a)
    d = b.sort()
    e = c.sort()

    print('Vector after sorting:')
    print(d)
    print("BubbleSort and QuickSort Solutions match!" if d == e else "QuickSort needs to be fixed...")
    print(' ')
    print('Bubble Sort')
    print(f"Total swaps for bubble sort: {b.getSwaps()}")
    print(f"Total elapsed time for bubble sort: {b.getTime()}\n")
    print('Quick Sort')
    print(f"Total swaps for quick sort: {c.getSwaps()}")
    print(f"Total elapsed time for quick sort: {c.getTime()}")

def runSortTest():
    sortTest([BubbleSort, QuickSort], [10, 100, 200, 300, 500, 1000, 2000], 500)

if __name__ == '__main__':
    main()
