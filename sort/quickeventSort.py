def quickEvenSort(A, p, r): 
    if p < r: 
        q = partition(A, p, r)
        quickEvenSort(A, p, q-1)
        quickEvenSort(A, q+1, r)

def partition(A, p, r):
    x = A[r]
    i = p
    j = p
    while j < r:
        if A[j] < x:
            A[i], A[j] = A[j], A[i]
            i += 1
        elif A[j] == x:
            A[j], A[r] = A[r], A[j]
            j -= 1
        j += 1
    A[i], A[r] = A[r], A[i]
    return i
