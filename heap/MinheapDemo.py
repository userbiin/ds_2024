from minheap import minHeap

class LPN_Frequency: 
    def __init__(self, lpn, frequency):
        self.lpn = lpn
        self.frequency = frequency

    def __repr__(self):
        return f"LPN: {self.lpn}, Frequency: {self.frequency}"


# minHeap 클래스 테스트를 위한 테스트 코드
if __name__ == "__main__":
    # minHeap 객체 생성
    h1 = minHeap([])
    
    # 초기 힙 상태 출력
    print("Initial Heap:")
    h1.headPrint()
    
    # 데이터 삽입
    h1.insert(LPN_Frequency(7, 3))
    h1.insert(LPN_Frequency(5, 1))
    h1.insert(LPN_Frequency(9, 2))
    
    # 데이터 삽입 후 힙 상태 출력
    print("Heap after insertions:")
    h1.headPrint()
    
    # 최소값 삭제
    min_value = h1.deleteMin()
    print("Min value deleted:", min_value.lpn, min_value.frequency)
    
    # 최소값 삭제 후 힙 상태 출력
    print("Heap after deletion:")
    h1.headPrint()


