import time

class AVLTreeNode:
    def __init__(self, chunk_idx, start, length):
        self.chunk_idx = chunk_idx
        self.start = start
        self.length = length
        self.height = 1
        self.left = None
        self.right = None
        
class AVLTree:
    def insert(self, root, chunk_idx, start, length):
        if not root:
            return AVLTreeNode(chunk_idx, start, length)
        
        if length < root.length:
            root.left = self.insert(root.left, chunk_idx, start, length)
        else:
            root.right = self.insert(root.right, chunk_idx, start, length)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and length < root.left.length:
            return self.right_rotate(root)
        if balance < -1 and length >= root.right.length:
            return self.left_rotate(root)
        if balance > 1 and length >= root.left.length:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and length < root.right.length:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, length):
        if not root:
            return root

        if length < root.length:
            root.left = self.delete(root.left, length)
        elif length > root.length:
            root.right = self.delete(root.right, length)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.chunk_idx = temp.chunk_idx
            root.start = temp.start
            root.length = temp.length
            root.right = self.delete(root.right, temp.length)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # 16KB
        self.arena = []
        self.free_tree = None  # AVL tree root node
        self.avl_tree = AVLTree()
        self.allocation_table = {}
        self.total_alloc_time = 0
        self.total_free_time = 0
        self.alloc_count = 0
        self.free_count = 0

    def _allocate_chunk(self):
        new_chunk = bytearray(self.chunk_size)
        self.arena.append(new_chunk)
        self.free_tree = self.avl_tree.insert(self.free_tree, len(self.arena) - 1, 0, self.chunk_size)

    def malloc(self, id, size):
        start_time = time.time()
        current = self.free_tree
        suitable_node = None
        while current:
            if current.length >= size:
                suitable_node = current
                break
            if size < current.length:
                current = current.left
            else:
                current = current.right

        if suitable_node:
            chunk_idx, start, length = suitable_node.chunk_idx, suitable_node.start, suitable_node.length
            self.allocation_table[id] = (chunk_idx, start, size)
            self.free_tree = self.avl_tree.delete(self.free_tree, length)
            if length > size:
                self.free_tree = self.avl_tree.insert(self.free_tree, chunk_idx, start + size, length - size)
        else:
            self._allocate_chunk()
            self.malloc(id, size)  # Retry malloc after allocating new chunk

        self.total_alloc_time += (time.time() - start_time)
        self.alloc_count += 1

    def free(self, id):
        if id in self.allocation_table:
            chunk_idx, start, size = self.allocation_table.pop(id)
            self.free_tree = self.avl_tree.insert(self.free_tree, chunk_idx, start, size)
        else:
            print(f"Warning: Trying to free non-existing block with id {id}")

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
