import random

class MemoryBlock:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.process_id = None

class MemoryManager:
    def __init__(self, memory_size, block_size, ):
        self.memory_size = memory_size
        self.block_size = block_size
        self.blocks = []
        for i in range(0, self.memory_size, self.block_size):
            block = MemoryBlock(i, self.block_size)
            self.blocks.append(block)

    def allocate(self, process_id, process_size):
        for block in self.blocks:
            if block.process_id is None and block.size >= process_size:
                block.process_id = process_id
                if block.size > process_size:
                    new_block = MemoryBlock(block.start + process_size, block.size - process_size)
                    self.blocks.insert(self.blocks.index(block) + 1, new_block)
                    block.size = process_size
                return True
        return False

    def deallocate(self, process_id):
        for block in self.blocks:
            if block.process_id == process_id:
                block.process_id = None

    def get_fragmentation(self):
        fragmentation = 0
        unused_blocks = []
        for block in self.blocks:
            if block.process_id is None:
                unused_blocks.append(block)
            else:
                if len(unused_blocks) > 0:
                    fragmentation += sum([block.size for block in unused_blocks])
                    unused_blocks = []
        if len(unused_blocks) > 0:
            fragmentation += sum([block.size for block in unused_blocks])
        return fragmentation

    def get_wasted_blocks(self):
        wasted_blocks = 0
        for block in self.blocks:
            if block.process_id is None:
                wasted_blocks += 1
        return wasted_blocks

# Get simulation parameters from user input
memory_size = int(input("Enter the size of the memory: "))
block_size = int(input("Enter the size of each memory block: "))
num_processes = int(input("Enter the number of processes: "))
process_size_range = tuple(map(int, input("Enter the range of process sizes (e.g. '16 128'): ").split()))
num_time_units = int(input("Enter the number of time units: "))

# Initialize memory manager
memory_manager = MemoryManager(memory_size,block_size)

# Run simulation
for time_unit in range(num_time_units):
    print(f"Time unit: {time_unit}")
    for i in range(num_processes):
        process_id = i
        process_size = random.randint(process_size_range[0], process_size_range[1])
        if memory_manager.allocate(process_id, process_size):
            print(f"process {process_id} of size {process_size} can be allocated.")
        if not memory_manager.allocate(process_id, process_size):
            print(f"Process {process_id} of size {process_size} cannot be allocated.")
    print(f"Fragmentation: {memory_manager.get_fragmentation()}")
    print(f"Wasted blocks: {memory_manager.get_wasted_blocks()}")
    for i in range(num_processes):
        process_id = i
        memory_manager.deallocate(process_id)