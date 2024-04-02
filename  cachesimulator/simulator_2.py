class ListNode: 
    def __init__(self, data, nextNode=None):
        self.data = data
        self.next = nextNode
        
class CircularLinkedListBasic:
    def __init__(self):
        self.tail = ListNode("dummy", None)
        self.tail.next = self.tail 
        # self.numItems = 0
        
class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 1
        self.cache  = {}
        self.head = None
        self.tail = None
    
    def do_sim(self, page):
        #pass
        # Do programming here! 
        self.tot_cnt += 1
        if page in self.cache:
            # Cache hit
            self.cache_hit += 1
            Listnode = self.cache[page]
            if Listnode != self.head:
                #MRU
                if Listnode == self.tail:
                    self.tail = Listnode.prev
                else:
                    Listnode.next.prev = Listnode.prev
                Listnode.prev.next = Listnode.next
                
                Listnode.next = self.head
                Listnode.prev = None
                self.head.prev = Listnode
                self.head = Listnode
        else:
            # Cache miss
            node = ListNode(page)
            self.cache[page] = node
            if len(self.cache) > self.cache_slots:
                # rm LRU
                del self.cache[self.tail.data]
                self.tail = self.tail.prev
                self.tail.next = None
            
            if not self.head:
                self.head = node
                self.tail = node
            else:
                # Add MRU
                node.next = self.head
                self.head.prev = node
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