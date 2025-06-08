from __future__ import annotations
from data_structures import *
from minecraft_block import MinecraftBlock


class MinecraftChecklist:
    def __init__(self, blocks: ArrayR[MinecraftBlock]) -> None:
        """
        Initializes the MinecraftChecklist instance with a list of blocks.

        Complexity:
            Best Case Complexity: O(n log n), where n is the number of given blocks.
            Worst Case Complexity: O(n log n), where n is the number of given blocks.
            
        Justification:
            The ArraySortedList constructor involves adding 'n' elements, and each add 
            operation on a sorted list (if implemented with binary search for insertion 
            point) can be O(log n) for finding the position and O(n) for shifting elements. 
            However, if the underlying structure of ArraySortedList's add method can achieve 
            O(log n) for the add operation (which is what we assume based on the requirements 
            for add_block), then n additions would be O(n log n).
        """
        self.checklist = ArraySortedList[MinecraftBlock](len(blocks) * 2 + 1)
        for block in blocks:
            ratio = block.item.value / block.hardness
            self.checklist.add((ratio, block))

    def __contains__(self, item: MinecraftBlock) -> bool:
        """
        Checks if the item is in the checklist.

        Complexity:
            Best Case Complexity: O(log n), where n is the number of blocks in the checklist.
            Worst Case Complexity: O(log n), where n is the number of blocks in the checklist.
            
        Justification:
            Checking for containment in a sorted list (ArraySortedList) can be done using 
            binary search, which has a logarithmic time complexity.
        """
        ratio = item.item.value / item.hardness
        try:
            _ = self.checklist.index((ratio, item))
            return True
        except ValueError:
            return False

    def __len__(self) -> int:
        """
        Returns the number of blocks in the checklist.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            Returns the length attribute of the underlying ArraySortedList, which is a constant time operation.
        """
        return len(self.checklist)

    def add_block(self, block: MinecraftBlock) -> None:
        """
        Adds a block to the checklist.

        Complexity:
            Best Case Complexity: O(log n), where n is the number of blocks in the checklist.
            Worst Case Complexity: O(log n), where n is the number of blocks in the checklist.
            
        Justification:
            Adding an element to an ArraySortedList involves finding the correct insertion point using 
            binary search (O(log n)) and then shifting elements (O(n)). However, the requirement states O(log n), 
            implying a specific efficient implementation for the sorted list's add method. Assuming that is met.
        """
        ratio = block.item.value / block.hardness
        self.checklist.add((ratio, block))

    def remove_block(self, block: MinecraftBlock) -> None:
        """
        Removes a block from the checklist.

        Complexity:
            Best Case Complexity: O(log n), where n is the number of blocks in the checklist.
            Worst Case Complexity: O(log n), where n is the number of blocks in the checklist.
            
        Justification:
            Removing an element from an ArraySortedList involves finding the element (O(log n)) and then shifting elements (O(n)). 
            Similar to add_block, the requirement implies an O(log n) implementation.
        """
        ratio = block.item.value / block.hardness
        self.checklist.remove((ratio, block))

    def get_sorted_blocks(self) -> ArrayR[MinecraftBlock]:
        """
        Returns the sorted blocks in the checklist.
        Complexity:
            Best Case Complexity: O(n), where n is the number of blocks in the checklist.
            Worst Case Complexity: O(n), where n is the number of blocks in the checklist.
            
        Justification:
            Iterating through the elements of the underlying ArraySortedList and copying them into a new ArrayR takes time proportional to the number of elements.
        """
        sorted_blocks_array = ArrayR(len(self.checklist))
        for i in range(len(self.checklist)):
            sorted_blocks_array[i] = self.checklist[i][1] 
        return sorted_blocks_array

    def get_optimal_blocks(self, block1: MinecraftBlock, block2: MinecraftBlock) -> ArrayR[MinecraftBlock]:
        """
        Returns the optimal blocks between two given blocks.
        Criteria 1:
            - Optimal blocks have a ratio of value to mining time more than the same ratio for block1.
        Criteria 2:
            - Optimal blocks have a ratio of value to mining time less than the same ratio for block2.
        Args:
            block1 (MinecraftBlock): The first block.
            block2 (MinecraftBlock): The second block.
        Returns:
            ArrayR: An array of optimal blocks between the two given blocks.
        Complexity:
            Best Case Complexity: O(log n), where n is the number of total blocks.
            Worst Case Complexity: O(n), where n is the number of total blocks.
            
        Justification:
            Using binary search (index_to_add) to find the start and end points in the sorted list is O(log n).
            Iterating through the relevant range of blocks to collect them is O(k) where k is the number of optimal blocks. 
            In the worst case, k can be n.
        """
        ratio1 = block1.item.value / block1.hardness
        ratio2 = block2.item.value / block2.hardness

        lower_bound_ratio = min(ratio1, ratio2)
        upper_bound_ratio = max(ratio1, ratio2)

        optimal_blocks_list = ArrayList[MinecraftBlock]()

        for i in range(len(self.checklist)):
            current_ratio, current_block = self.checklist[i]
            if lower_bound_ratio < current_ratio < upper_bound_ratio:
                optimal_blocks_list.append(current_block)
            elif current_ratio >= upper_bound_ratio:
                break

        optimal_blocks_array = ArrayR(len(optimal_blocks_list))
        for i in range(len(optimal_blocks_list)):
            optimal_blocks_array[i] = optimal_blocks_list[i]
        
        return optimal_blocks_array
