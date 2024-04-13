from lfuheap import minHeap

class LPN_Frequency:
    def __init__(self, lpn, frequency):
        self.lpn = lpn  # LPN (Logical Page Number)
        self.frequency = frequency  # 해당 LPN의 빈도수

    def __lt__(self, other):
        return self.frequency < other.frequency  # 빈도수를 기준으로 비교

class LFUSimulator:
    def __init__(self):
       self.cache = {}
       self.heap = minHeap([])
       self.cache_hit = 0
       self.tot_cnt = 0

    def lfu_sim(self, cache_slots):
        self.cache_slots = cache_slots
        data_file = open("/workspaces/ds_2024/heap/linkbench.trc")
        
        for line in data_file.readlines():
            lpn = line.split()[0]  # LPN을 추출
            self.tot_cnt += 1
            
            if lpn in self.cache:
                self.cache_hit += 1
                lpn_frequency = self.cache[lpn]
                lpn_frequency.frequency += 1  # LPN의 빈도수 증가
                self.heap.update(lpn_frequency)  # 힙 업데이트

            else:
                if len(self.cache) < cache_slots:
                    lpn_frequency = LPN_Frequency(lpn, 1)  # 새로운 LPN과 빈도수 1로 LPN_Frequency 객체 생성
                    self.cache[lpn] = lpn_frequency
                    self.heap.insert(lpn_frequency)  # 힙에 삽입
                else:
                    min_lpn_frequency = self.heap.min()
                    del self.cache[min_lpn_frequency.lpn]
                    self.heap.deleteMin()
                    lpn_frequency = LPN_Frequency(lpn, 1)
                    self.cache[lpn] = lpn_frequency
                    self.heap.insert(lpn_frequency)
        
        hit_ratio = self.cache_hit / self.tot_cnt   
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", hit_ratio)

if __name__ == "__main__":
    simulator = LFUSimulator()
    for cache_slots in range(100, 1000, 100):
        simulator.lfu_sim(cache_slots)
