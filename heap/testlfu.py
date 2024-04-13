from lfuheap import minHeap

class LFUSimulator:
    def __init__(self):
        self.cache = {}  # 캐시를 LPN을 키로, [frequency, timestamp]을 값으로 하는 딕셔너리로 표현
        self.heap = minHeap()  # LFU 알고리즘에 사용할 MinHeap
        self.total_requests = 0
        self.cache_hits = 0

    def lfu_sim(self, cache_slots):
        self.cache.clear()
        self.heap.clear()
        self.total_requests = 0
        self.cache_hits = 0

        data_file = open("linkbench.trc", "r")
        for line in data_file.readlines():
            lpn = int(line.split()[0])
            self.total_requests += 1

            # 캐시에 LPN이 이미 있는 경우
            if lpn in self.cache:
                self.cache_hits += 1
                frequency, timestamp = self.cache[lpn]
                frequency += 1
                self.cache[lpn] = [frequency, timestamp]
                self.heap.update((lpn, frequency, timestamp))
            # 캐시에 LPN이 없는 경우
            else:
                # 캐시 크기가 채워지지 않은 경우
                if len(self.cache) < cache_slots:
                    self.cache[lpn] = [1, self.total_requests]
                    self.heap.insert((lpn, 1, self.total_requests))
                # 캐시 크기가 채워진 경우
                else:
                    min_lpn, min_frequency, min_timestamp = self.heap.min()
                    del self.cache[min_lpn]
                    self.heap.deleteMin()
                    self.cache[lpn] = [1, self.total_requests]
                    self.heap.insert((lpn, 1, self.total_requests))

        # 캐시 히트율 출력
        hit_ratio = self.cache_hits / self.total_requests if self.total_requests > 0 else 0
        print(f"Cache slots: {cache_slots}, Cache hits: {self.cache_hits}, Hit ratio: {hit_ratio}")

if __name__ == "__main__":
    simulator = LFUSimulator()
    for cache_slots in range(100, 1001, 100):
        simulator.lfu_sim(cache_slots)
