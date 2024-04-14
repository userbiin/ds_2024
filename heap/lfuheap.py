class minHeap:
    def __init__(self, list):
        if list == None:
            self.__A = []
        else:
            self.__A = list

    def insert(self, x):
        self.__A.append(x)
        self.__percolateUp(len(self.__A)-1)

    def __percolateUp(self, i):
        parent = (i - 1) // 2
        if i > 0 and self.__A[i].frequency < self.__A[parent].frequency:
            self.__A[i], self.__A[parent] = self.__A[parent], self.__A[i]
            self.__percolateUp(parent)


    def deleteMin(self):
        if not self.isEmpty():
            min = self.__A[0]
            self.__A[0] = self.__A.pop()
            self.__percolateDown(0)
            return min
        else:
            return None
        
    def __percolateDown(self, i):
        child = 2 * i + 1
        right = 2 * i + 2

        if child <= len(self.__A)-1:
            if right <= len(self.__A)-1 and self.__A[child].frequency > self.__A[right].frequency:
                child = right 
            if self.__A[i].frequency > self.__A[child].frequency:
                self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
                self.__percolateDown(child)

    def update(self, updated_element):
        for i, lpn_frequency in enumerate(self.__A):
            if lpn_frequency.lpn == updated_element.lpn:
                self.__A[i] = updated_element
                self.__percolateDown(i)
                break
            
    def min(self):
        return self.__A[0]

    def isEmpty(self):
        return len(self.__A) == 0
    
    def clear(self):
        self.__A = []

    def size(self):
        return len(self.__A)