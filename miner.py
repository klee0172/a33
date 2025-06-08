from __future__ import annotations
from typing import Iterable

from data_structures import ArrayList
from minecraft_block import MinecraftBlock, MinecraftItem


class Miner:
    """
    A class representing a miner in a mining simulation.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the miner with a name and an empty inventory.
        Args:
            name (str): The name of the miner.
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            Initialization involves setting a name and creating an empty ArrayList, both constant time operations.
        """
        self.name = name
        self.inventory = ArrayList[MinecraftItem]()

    def mine(self, block: MinecraftBlock) -> None:
        """
        Mines a block and adds the item to the miner's bag.

        Args:
            block (MinecraftBlock): The block to be mined.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N) where N is the current number of items in the inventory.

        Justification:
            Appending an item to an ArrayList is typically O(1) amortized, but can be O(N) in the worst case due to resizing.
        """
        self.inventory.append(block.item)

    def clear_inventory(self) -> Iterable:
        """
        Clears the miner's inventory and returns what he had in the inventory before the clear.

        Complexity:
            Best Case Complexity: O(N), where N is the number of items in the inventory.
            Worst Case Complexity: O(N), where N is the number of items in the inventory.
            
        Justification:
            Iterating through the inventory to collect items and then clearing it takes time proportional to the number of items.
        """
        items_in_inventory = self.inventory
        self.inventory = ArrayList[MinecraftItem]() 
        return items_in_inventory

    def __str__(self) -> str:
        return f"Miner: {self.name}"
