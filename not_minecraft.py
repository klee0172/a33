from __future__ import annotations
from cave_system import CaveSystem, CaveNode
from data_structures import *
from minecraft_block import MinecraftBlock, MinecraftItem
from minecraft_checklist import MinecraftChecklist
from random_gen import RandomGen
from miner import Miner
from data_structures.linked_stack import LinkedStack
from typing import Tuple

class NotMinecraft:
    """
    A class representing a NotMinecraft game.
    """

    def __init__(self, cave_system: CaveSystem, checklist: MinecraftChecklist) -> None:
        """
        Initializes the NotMinecraft game.
        Args:
            cave_system (CaveSystem): The cave system for the game.
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        Justification:
            Initialization involves setting attributes and creating a Miner object, all of which are constant time operations.
        """
        self.cave_system = cave_system
        self.checklist = checklist
        self.miner = Miner("Steve")

    def dfs_explore_cave(self) -> ArrayList[MinecraftBlock]:
        """
        Performs a depth-first search (DFS) to explore the cave system and collect blocks.
        Returns:
            ArrayList[MinecraftBlock]: A list of collected blocks.
        Complexity:
            Not required
        """
        if self.cave_system.entrance is None:
            return ArrayList()

        blocks_found = ArrayList[MinecraftBlock]()
        visited_nodes = ArraySet[str](self.cave_system.number_of_nodes)
        stack = LinkedStack[CaveNode]()

        stack.push(self.cave_system.entrance)
        visited_nodes.add(self.cave_system.entrance.name)

        while not stack.is_empty():
            current_node = stack.pop()

            for i in range(len(current_node.blocks)):
                blocks_found.append(current_node.blocks[i])

            for i in range(len(current_node.neighbours) - 1, -1, -1):
                neighbor = current_node.neighbours[i]
                if neighbor.name not in visited_nodes:
                    visited_nodes.add(neighbor.name)
                    stack.push(neighbor)
        
        return blocks_found

    def objective_mining_filter(self, blocks: ArrayList[MinecraftBlock], block1: MinecraftBlock,
                                block2: MinecraftBlock) -> ArrayList:
        """
        Given a list of blocks, filter the blocks that should be considered according to scenario 1.
        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
            block1 (MinecraftBlock): Filtered blocks should have a ratio of value to mining time > block1.
            block2 (MinecraftBlock): Filtered blocks should have a ratio of value to mining time < block2.
        Complexity:
            Best Case Complexity: O(N * C + N * logM)
            Worst Case Complexity: O(N * C + N * logM)
            Where N is the number of blocks discovered, M is the number of blocks in the checklist, and C is the complexity of block comparison/ratio calculation.
            (Since checklist.__contains__ is O(log M), and ArrayList append is amortized O(1)).
        
        Justification:
            Iterating through all discovered blocks (N) and for each checking if it's in the checklist (O(log M)), and then doing constant time ratio comparisons.
        """
        filtered_blocks = ArrayList[MinecraftBlock]()
        
        ratio1 = block1.item.value / block1.hardness
        ratio2 = block2.item.value / block2.hardness

        lower_bound_ratio = min(ratio1, ratio2)
        upper_bound_ratio = max(ratio1, ratio2)

        for i in range(len(blocks)):
            current_block = blocks[i]

            if current_block in self.checklist: 
                current_ratio = current_block.item.value / current_block.hardness

                if lower_bound_ratio < current_ratio < upper_bound_ratio:
                    filtered_blocks.append(current_block)
        
        return filtered_blocks

    def objective_mining(self, blocks: ArrayList[MinecraftBlock]) -> None:
        """
        Mines the cave system to achieve the objective of collecting blocks.
        Complexity:
            Best Case Complexity: O(n log n), where n is the number of blocks to be mined.
            Worst Case Complexity: O(n log n), where n is the number of blocks to be mined.

        Justification:
            The primary operation is sorting the blocks based on their value-to-mining-time ratio, 
            which dominates the complexity. Using a comparison sort like mergesort or a heap sort (via MaxHeap) 
            would yield O(n log n). Then, iterating through the sorted blocks and mining them is O(n).
        """
        max_heap = MaxHeap[Tuple[float, MinecraftBlock]](len(blocks))

        for i in range(len(blocks)):
            block = blocks[i]
            ratio = block.item.value / block.hardness
            max_heap.add((ratio, block))

        while len(max_heap) > 0:
            _, block_to_mine = max_heap.get_max()
            self.miner.mine(block_to_mine)

    def objective_mining_summary(self, blocks: ArrayList[MinecraftBlock], block1: MinecraftBlock,
                                 block2: MinecraftBlock) -> None:
        """
        Returns the summary of the objective mining.
        This is to explain how objective mining will be called and tested.
        Complexity:
            Not Required
        """
        filtered_blocks = self.objective_mining_filter(blocks, block1, block2)

        self.chicken_jockey_attack(filtered_blocks)

        self.objective_mining(filtered_blocks)

    def profit_mining(self, blocks: ArrayList[MinecraftBlock], time_in_seconds: int) -> None:
        """
        Mines the cave system casually.
        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
            time_in_seconds (int): The time in seconds to mine.
        Complexity:
            Best Case Complexity: O(n), where n is the number of blocks.
            Worst Case Complexity: O(n log n), where n is the number of blocks.
            
        Justification:
           Adding 'n' blocks to the MaxHeap is O(n log n). Iterating through the heap to select blocks 
           can be O(k log n) where k is the number of mined blocks. In the best case, if only a few items 
           are processed, it might be O(log n). If the heapify operation is used, it could be O(N) for building 
           the heap and O(K log N) for extractions. The justification O(n) best case should probably clarify if 
           it assumes an input where all items fit perfectly or if the best case for adding to heap is considered. 
           However, typically, O(N log N) for heap construction and extraction is the dominant factor. The provided 
           justification focuses on the dominant heap operations. It is possible the "best case O(N)" refers to the 
           heapify stage if heapify was used, but individual add operations are log N. The provided complexity aligns 
           with typical heap-based greedy algorithms.
        """
        profit_heap = MaxHeap[Tuple[float, MinecraftBlock]](len(blocks))

        for i in range(len(blocks)):
            block = blocks[i]
            ratio = block.item.value / block.hardness
            profit_heap.add((ratio, block))
        
        current_time = 0
        while len(profit_heap) > 0:
            _, block_to_mine = profit_heap.get_max()
            
            if current_time + block_to_mine.hardness <= time_in_seconds:
                self.miner.mine(block_to_mine)
                current_time += block_to_mine.hardness
    
    def chicken_jockey_attack(self, blocks: ArrayList[MinecraftBlock]) -> None:
        """
        Chicken Jockey Attack
        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
        Complexity:
            Not required
        """
        RandomGen.random_shuffle(blocks)

    def main(self, scenario: int, **criteriaArgs) -> None:
        """
        Main function to run the NotMinecraft game.
        Args:
            scenario (int): The scenario number to run.
            criteriaArgs (dict): Additional arguments for the scenario.
        Complexity:
            Not required
        Sample Usage:
            not_minecraft = NotMinecraft(cave_system, checklist)
            not_minecraft.main(1, block1=block1, block2=block2)
            not_minecraft.main(2, time_in_seconds=60)
        """
        if scenario == 1:
            blocks = self.dfs_explore_cave()
            self.objective_mining_summary(blocks, **criteriaArgs)
        elif scenario == 2:
            blocks = self.dfs_explore_cave()
            self.profit_mining(blocks, **criteriaArgs)
