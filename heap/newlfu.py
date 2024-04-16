from lfuheap import minHeap

class LPN_Frequency: 
    def __init__(self, lpn, frequency):
        self.lpn = lpn
        self.frequency = frequency


class LFUSimulator:
    def __init__(self):
        self.cache = {}
        self.heap = minHeap([])
        self.cache_hit = 0
        self.tot_cnt = 0
        self.lpn_frequencies = {}  # LPN별 빈도수 저장

    def lfu_sim(self, cache_slots, lpn):
        self.cache_slots = cache_slots
        self.tot_cnt += 1

        if lpn in self.cache:  # cache에 호출된 페이지가 있는 경우
            self.cache_hit += 1
            lpn_frequency = self.cache[lpn]
            lpn_frequency.frequency += 1
            self.heap.update(lpn_frequency)
        else:
            if len(self.cache) < cache_slots:  # cache에 빈 자리가 있다면
                if lpn in self.lpn_frequencies:
                    frequency = self.lpn_frequencies[lpn]  # 이전 빈도수 가져오기
                else:
                    frequency = 1  # 처음 호출되는 경우 frequency를 1로 설정
                lpn_frequency = LPN_Frequency(lpn, frequency)
                self.cache[lpn] = lpn_frequency
                self.heap.insert(lpn_frequency)
            else:
                lfu_heap = self.heap.min()
                del self.cache[lfu_heap.lpn]
                self.heap.deleteMin()
                if lpn in self.lpn_frequencies:
                    frequency = self.lpn_frequencies[lpn]  # 이전 빈도수 가져오기
                else:
                    frequency = 1  # 처음 호출되는 경우 frequency를 1로 설정
                lpn_frequency = LPN_Frequency(lpn, frequency)
                self.cache[lpn] = lpn_frequency
                self.heap.insert(lpn_frequency)

    def print_stats(self):
        hit_ratio = self.cache_hit / self.tot_cnt
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", hit_ratio)



if __name__ == "__main__":
    simulator = LFUSimulator()
    data_file = open("/workspaces/ds_2024/heap/linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1000, 100):
        for line in lines:
            lpn = line.split()[0]
            simulator.lfu_sim(cache_slots, lpn)
        simulator.print_stats()