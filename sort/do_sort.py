from shellSort import *
from insertionSort import * 
from quickSort import * 
from quickeventSort import *
from mergeSort import *

def do_sort(input_file):
    data_file = open(input_file)
    A = []
    for line in data_file.readlines():
        lpn = line.split()[0]
        A.append(lpn)

    #shellSort(A)
    #insertionSort(A)
    quickevenSort(A, 0, len(A)-1)
    #quickEvenSort(A,0, len(A)-1)
    #mergeSort(A, 0, len(A)-1)

    for i in range(1000, 1050, 1):
        print(A[i], end= " ")
    print("")

if __name__ == "__main__":
    import time 

    start = time.perf_counter()
    do_sort("/workspaces/ds_2024/sort/linkbench_short.trc")
    end = time.perf_counter()
    elapsed_time_us = (end - start) * 1000
    print(f"Elapsed time: {elapsed_time_us: .2f} ms")

    


