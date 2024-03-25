class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 0
        self.cache = {}
        self.head = None
        self.tail = None

    def do_sim(self, page):
        self.tot_cnt += 1
        if page in self.cache:
            # Cache hit
            self.cache_hit += 1
            node = self.cache[page]
            if node != self.head:
                # Move the accessed node to the head (MRU)
                if node == self.tail:
                    self.tail = node.prev
                else:
                    node.next.prev = node.prev
                node.prev.next = node.next
                
                node.next = self.head
                node.prev = None
                self.head.prev = node
                self.head = node
        else:
            # Cache miss
            node = Node(page)
            self.cache[page] = node
            if len(self.cache) > self.cache_slots:
                # Remove the least recently used node (LRU)
                del self.cache[self.tail.data]
                self.tail = self.tail.prev
                self.tail.next = None
            
            if not self.head:
                self.head = node
                self.tail = node
            else:
                # Add the new node to the head (MRU)
                node.next = self.head
                self.head.prev = node
                self.head = node

    def print_stats(self):
        hit_ratio = self.cache_hit / self.tot_cnt if self.tot_cnt > 0 else 0
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", hit_ratio)

if __name__ == "__main__":
    data_file = open("/workspaces/ds_2024/linkbench.trc")  # Adjust the path to your data file
    lines = data_file.readlines()
    
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()

