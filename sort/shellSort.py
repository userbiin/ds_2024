def shellSort(A): 
    H = gapSequence(len(A))
    for h in H:
        for k in range(h):
            stepInsertionSort(A, k, h)

def stepInsertionSort(A, k, h):
    for i in range(k+h, len(A), h):
        j = i - h
        newItem = A[i]
        while ( j >= 0 and newItem < A[j] ):
            A[j+h] = A[j]
            j -= h 
        A[j+h] = newItem 

def gapSequence(n):
    H = [1]; gap = 1
    while gap < n/5:
        gap = gap*3 + 1
        H.append(gap)
    H.reverse()
    return H