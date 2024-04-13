from lfuheap import minHeap

class LFUSimulator:
    def __init__(self):
       self.cache = {}
       self.heap = minHeap([])

    def lfu_sim(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 0
        # frequency = 1
        # timestamp = 0
        data_file = open("/workspaces/ds_2024/heap/linkbench.trc")
        for line in data_file.readlines():
            lpn = line.split()[0] # lpn = int(line.split()[0])
            self.tot_cnt += 1
            
            if lpn in self.cache:
               self.cache_hit += 1
               frequency, timestamp = self.cache[lpn]
               frequency += 1
               self.cache[lpn] = [frequency, timestamp]
               self.heap.update((lpn, frequency, timestamp))

            else:
                if len(self.cache) < cache_slots:
                    self.cache[lpn] = [1, self.tot_cnt]
                    self.heap.insert((lpn, 1, self.tot_cnt))
                else:
                    min_lpn, min_frequency, min_timestamp = self.heap.min()
                    del self.cache[min_lpn]
                    self.heap.deleteMin()
                    self.cache[lpn] = [1, self.tot_cnt]
                    self.heap.insert((lpn, 1, self.tot_cnt))
        
        hit_ratio = self.cache_hit / self.tot_cnt   
        print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", hit_ratio)

if __name__ == "__main__":
  simulator = LFUSimulator()
  for cache_slots in range(100, 1000, 100):
    simulator.lfu_sim(cache_slots)