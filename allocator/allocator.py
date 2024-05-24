import time

class FreeListNode:
    def __init__(self, chunk_idx, start, length):
        self.chunk_idx = chunk_idx
        self.start = start
        self.length = length
        self.next = None

class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # 16KB
        self.arena = []
        self.free_list_head = None  # Free list head node
        self.allocation_table = {}
        self.total_alloc_time = 0
        self.total_free_time = 0
        self.alloc_count = 0
        self.free_count = 0

    def _allocate_chunk(self):
        new_chunk = bytearray(self.chunk_size)
        self.arena.append(new_chunk)
        new_node = FreeListNode(len(self.arena) - 1, 0, self.chunk_size)
        new_node.next = self.free_list_head
        self.free_list_head = new_node

    def malloc(self, id, size):
        start_time = time.time()
        prev = None
        current = self.free_list_head
        while current:
            if current.length >= size:
                self.allocation_table[id] = (current.chunk_idx, current.start, size)
                if current.length > size:
                    current.start += size
                    current.length -= size
                else:
                    if prev:
                        prev.next = current.next
                    else:
                        self.free_list_head = current.next
                self.total_alloc_time += (time.time() - start_time)
                self.alloc_count += 1
                return
            prev = current
            current = current.next

        # No suitable block found, allocate a new chunk
        self._allocate_chunk()
        self.malloc(id, size)  # Retry malloc after allocating new chunk

    def free(self, id):
        start_time = time.time()
        if id in self.allocation_table:
            chunk_idx, start, size = self.allocation_table.pop(id)
            new_node = FreeListNode(chunk_idx, start, size)
            new_node.next = self.free_list_head
            self.free_list_head = new_node
        else:
            print(f"Warning: Trying to free non-existing block with id {id}")
        self.total_free_time += (time.time() - start_time)
        self.free_count += 1

    def print_stats(self):
        total_arena_size = len(self.arena) * self.chunk_size
        used_memory = sum(size for _, _, size in self.allocation_table.values())
        utilization = used_memory / total_arena_size if total_arena_size > 0 else 0
        print(f"Arena: {total_arena_size / (1024 * 1024):.2f} MB")
        print(f"In-use: {used_memory / (1024 * 1024):.2f} MB")
        print(f"Utilization: {utilization:.2f}")
        if self.alloc_count > 0:
            print(f"Average allocation time: {self.total_alloc_time / self.alloc_count:.6f} seconds")
        if self.free_count > 0:
            print(f"Average free time: {self.total_free_time / self.free_count:.6f} seconds")

if __name__ == "__main__":
    allocator = Allocator()
    
    with open("./input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            n += 1
    
    allocator.print_stats()
