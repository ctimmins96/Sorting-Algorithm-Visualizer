### Import Statements
from time import perf_counter, sleep
from random import randint

### Class Definitions

## SortAlg (Superclass)

class SortAlg:
    _data_set = None 
    _ascending = True
    _piv_idx = 0
    _cmp_idx = 0
    _swaps = 0
    _compares = 0
    _tStart = 0.00
    _elapsed = 0.00
    _is_sorting = False
    _sorted = False
    
    ## Constructor
    def __init__(self, dataSet, ascending:bool = True):
        self._data_set = dataSet.copy()
        self._ascending = ascending

    ## Get / Set Functions
    # get_data
    def getData(self):
        return self._data_set.copy()
    
    # get_pivot
    def getPivot(self) -> int:
        return self._piv_idx

    # get_swap
    def getSwaps(self) -> int:
        return self._swaps
    
    # get_compares
    def getCompares(self) -> int:
        return self._compares

    # get_times
    def getTimes(self) -> float:
        return self._elapsed
    
    # get_compare
    def getCompare(self) -> int:
        return self._cmp_idx
    
    # is_sorted
    def isSorted(self) -> bool:
        return self._sorted
    
    ## Swap function 
    def _swap(self, i, j):
        if i != j:
            tmp = self._data_set[i]
            self._data_set[i] = self._data_set[j]
            self._data_set[j] = tmp
            self._swaps += 1
    
    ## Compare Function
    def _compare(self, i, j, gt:bool) -> bool:
        self._compares += 1
        if gt:
            return i > j
        else:
            return i < j

    ## Iterate function (performs sorting algorithm one comparison at a time)
    def iterate(self) -> list:
        pass

    ## startSort (begins the sorting process)
    def startSort(self):
        self._swaps = 0
        self._compares = 0
        self._piv_idx = 0
        self._cmp_idx = 1
        self._is_sorting = True
        self._tStart = perf_counter()
    
    # finishSort (ends the sorting process)
    def _finishSort(self) -> None:
        self._elapsed = perf_counter() - self._tStart
        self._sorted = True
        self._is_sorting = False
        self._piv_idx = 0
        self._cmp_idx = 0
        
## BubbleSort Class
class BubbleSort(SortAlg):
    ## Iterate method overload
    def iterate(self) -> list:
        # Check if the startSort function has already been called
        if self._is_sorting:
            # Check if the data set is already sorted or not.
            if not self._sorted:
                # Compare the pivot and compare indices
                if self._compare(self._data_set[self._piv_idx], self._data_set[self._cmp_idx],True) == self._ascending:
                    self._swap(self._piv_idx, self._cmp_idx)
                
                    # Update the Pivot and Compare Indexes
                    self._piv_idx = 0
                    self._cmp_idx = 1
                else:
                    if self._cmp_idx == (len(self._data_set) - 1):
                        self._finishSort()
                    else:
                        self._piv_idx += 1
                        self._cmp_idx += 1
        else:
            print('Data set is already sorted.')
        return self._data_set.copy()

    ## String operator
    def __str__(self):
        piv_pos = ' '*(3*(self._piv_idx + 1) - 2)
        msg = f"""
        Data Set: {self._data_set}
        Position: {piv_pos}p  c
        """
        return msg

## Partition Class
class Partition:
    ## Default property
    _curr_part = -1

    ## Constructor
    def __init__(self, dataSet) -> None:
        self._dset = dataSet.copy()
        self._num_elem = len(dataSet)

    ## property
    @property
    def currentPartition(self):
        return self._curr_part
    
    ## Get Row/Col 
    def _get_row_col(self, idx:int):
        col = 0
        row = -1
        if (type(self._dset[0]) == list):
            row = 0
            while idx > 0:
                if col != (len(self._dset[row]) - 1):
                    col += 1
                else:
                    if row != (len(self._dset) - 1):
                        col = 0
                        row += 1
                    else:
                        raise IndexError
                idx -= 1
        else:
            col = idx
        return row, col
    
    ## Get idx
    def _get_idx(self, row:int, col:int) -> int:
        if row == -1:
            return col
        else:
            idx = 0
            while self._get_row_col(idx) != (row, col):
                idx += 1
            return idx

    ## Get Attribute Operator
    def __getitem__(self, idx:int):
        if (type(self._dset[0]) == list):
            row, col = self._get_row_col(idx)
            return self._dset[row][col]
        else:
            return self._dset[idx]
    
    ## Get Attribute Operator
    def __setitem__(self, idx:int, val) -> None:
        if (type(self._dset[0]) == list):
            row, col = self._get_row_col(idx)
            self._dset[row][col] = val
        else:
            self._dset[idx] = val
    
    ## Length operator
    def __len__(self) -> int:
        return self._num_elem

    ## String Operator
    def __str__(self) -> str:
        return str(self._dset)

    def swap(self, i, j) -> None:
        if i != j:
            tmp = self[i]
            self[i] = self[j]
            self[j] = tmp
    
    def split(self, idx) -> None:
        tmp = self._dset.copy()
        res = []
        row, col = self._get_row_col(idx)

        if row < 0:
            if col < (len(tmp) - 1):
                res = [tmp[0:col+1], tmp[col+1:]]
            else:
                res = tmp.copy()
        else:
            for i in range(row):
                res.append(tmp[i].copy())
            # Prevent Insertion of empty arrays and bypass if necessary
            if col < (len(tmp[row])-1):
                res.append(tmp[row][0:col+1].copy())
                res.append(tmp[row][col+1:].copy())
            else:
                res.append(tmp[row].copy())
            for j in range(len(tmp) - (row+1)):
                res.append(tmp[j + row + 1].copy())
        self._dset = res.copy()
        return res.copy()
    
    ## Next Partition
    def nextPart(self):
        if type(self._dset[0]) == list:
            # Check if the current partition is the last partition
            if self._curr_part == len(self):
                # If yes, set back to -1
                self._curr_part = -1
            else:
                if self._curr_part == -1:
                    self._curr_part = 0
                # If Length of partition is 1 move forward unless we are at the end (all partitions are made and the array is sorted.)
                while (len(self._dset[self._curr_part]) == 1) and (self._curr_part < (len(self) - 1)):
                    self._curr_part += 1
                # Else stop
    
    ## Get Partition
    #
    # Returns array of partition indices accessible to the QuickSort Class
    def getPart(self):
        idxs = []
        if self._curr_part == -1:
            for i in range(self._num_elem):
                idxs.append(i)
        else:
            for i in range(len(self._dset[self._curr_part])):
                idxs.append(self._get_idx(self._curr_part, i))
        return idxs
        

    def getArr(self):
        tmp = []
        for i in range(self._num_elem):
            tmp.append(self[i])
        return tmp

## QuickSort Class
class QuickSort(SortAlg):
    __fmt = """
=========================================
=             QuickSort                 =
=========================================
= Sorting:                {}
=
= partition:              {}
= 
= Pivot:                  {}
= Compare:                {}
=
= Current Partition:      {}
=
========================================="""

    ## Overloaded constructor
    def __init__(self, dataSet, ascending: bool = True):
        super().__init__(dataSet, ascending)
        self.__part = Partition(dataSet.copy())
    
    ## Swap method overload
    def _swap(self, i, j):
        if i != j:
            self.__part.swap(i, j)
            super()._swap(i, j)
    
    ## Start Sort overload
    def startSort(self):
        self._piv_idx = randint(0,len(self.__part) - 1)
        self._swap(0, self._piv_idx)
        super().startSort()

    ## String operator
    def __str__(self):
        msg = self.__fmt.format(self._is_sorting, self.__part, self._piv_idx, self._cmp_idx, self.__part.getPart())
        return msg

    ## Iterate method overload
    def iterate(self) -> list:
        # Check if the startSort function has already been called
        if self._is_sorting:
            # Check if the data set is already sorted or not.
            if not self._sorted:
                part = self.__part.getPart()
                if (self.__part.currentPartition == (len(self.__part) - 1)) and len(part) == 1:
                    self._finishSort()
                else:
                    ## Compare
                    if (self._compare(self._data_set[self._piv_idx], self._data_set[self._cmp_idx], True) == self._ascending):
                        ## Swap
                        self._swap(self._piv_idx, self._cmp_idx)
                        self._swap(self._piv_idx + 1, self._cmp_idx)
                        self._piv_idx += 1

                        ## Update _data_set variable with the new variable
                        #self._data_set = self.__part.getArr()

                    ## Figure out how to best update pivot and compare indices
                    if self._cmp_idx == part[-1]:
                        ## Split Partition
                        ## Add a check condition if the partition is len 2
                        if len(self.__part.getPart()) == 2:
                            self.__part.split(part[0])
                        elif self._piv_idx == part[-1]:
                            self.__part.split(part[-2])
                        else:
                            self.__part.split(self._piv_idx)

                        ## Move to the next partition
                        self.__part.nextPart()

                        ## Update compare and pivot idxs
                        part = self.__part.getPart()
                        if (len(part) < len(self.__part)) and len(part) > 1:
                            self._piv_idx = randint(part[0], part[-1])
                            self._swap(part[0], self._piv_idx)
                            self._swap(part[1], self._piv_idx)
                            self._piv_idx = part[0]
                            self._cmp_idx = part[1]
                    else:
                        # Update index
                        self._cmp_idx += 1
        return self._data_set

### Main

def main():
    a = [3, 1, 2, 6, 4, 5, 10, 7, 9, 8]
    b = BubbleSort(a, False)
    b.startSort()
    print(str(b))
    while not b.isSorted():
        b.iterate()
        print(str(b))
    
    print('Sorting Complete')
    print(f"Total Compares: {b.getCompares()}")
    print(f"   Total Swaps: {b.getSwaps()}")
    print(f"  Time Elapsed: {b.getTimes():.5f}")

def main2():
    a = [3, 1, 2, 6, 4, 5, 0, 7, 9, 8]
    b = QuickSort(a)
    b.startSort()
    print(str(b))
    while not b.isSorted():
        #sleep(0.1)
        b.iterate()
        print(str(b))
    
    print('Sorting Complete')
    print(f"Total Compares: {b.getCompares()}")
    print(f"   Total Swaps: {b.getSwaps()}")
    print(f"  Time Elapsed: {b.getTimes():.5f}")

def partitionRobustness():
    a = [3, 1, 2, 6, 4, 5, 0, 7, 9, 8] 

if __name__ == "__main__":
    main2()