class ListNode: 
    def __init__(self, data, nextNode=None):
        self.data = data
        self.next = nextNode
        
class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 1
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
                # Move the node to the head
                prev_node = self.head
                while prev_node.next != node:
                    prev_node = prev_node.next
                prev_node.next = node.next
                node.next = self.head
                self.head = node
        else:
            # Cache miss
            node = ListNode(page)
            self.cache[page] = node
            if len(self.cache) > self.cache_slots:
                # Remove the LRU node
                prev_node = None
                curr_node = self.head
                while curr_node.next:
                    prev_node = curr_node
                    curr_node = curr_node.next
                del self.cache[curr_node.data]
                if prev_node:
                    prev_node.next = None
                else:
                    self.head = None
            # Add the new node to the head
            node.next = self.head
            self.head = node
        
    def print_stats(self):
        print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":
    data_file = open("/workspaces/ds_2024/linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()
