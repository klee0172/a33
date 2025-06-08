from __future__ import annotations
from collections.abc import Callable
from typing import Tuple, TypeVar
from data_structures import *
from algorithms.mergesort import mergesort

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: ArrayList[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements ArrayList.

        As such you can assume the length of elements to be non-zero.
        The elements ArrayList will contain tuples of key, item pairs.

        First sort the elements ArrayList and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(ArrayList[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case: O(n log n)
            Worst Case: O(n log n)

        Justification:
            The initialization involves __sort_elements (O(n log n)) and __build_balanced_tree 
            (O(n log n)), both of which contribute to the overall O(n log n) complexity.
        """
        super().__init__()
        new_elements: ArrayList[Tuple[K, I]] = self.__sort_elements(elements)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: ArrayList[Tuple[K, I]]) -> ArrayList[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (ArrayList[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            ArrayList(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case: O(n log n)
            Worst Case: O(n log n)

        Justification:
            mergesort is a comparison-based divide-and-conquer algorithm with guaranteed O(n log n) complexity.
        """
        return mergesort(elements, key=lambda x: x[0])

    def __build_balanced_tree(self, elements: ArrayList[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (ArrayList[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case: O(n log n)
            Worst Case: O(n log n)

        Justification:
            Performs n inserts into the BST. Each insert is O(log n) since the tree is balanced.
        """
        def build(left: int, right: int) -> None:
            if left > right:
                return
            mid = (left + right) // 2
            key, item = elements[mid]
            self[key] = item  
            build(left, mid - 1)
            build(mid + 1, right)

        build(0, len(elements) - 1)

    def filter_keys(self, filter_func1: Callable[[K], bool], filter_func2: Callable[[K], bool]) -> ArrayList[Tuple[K, I]]:
        """
        Filters the keys in the tree based on two criteria.

        Args:
            filter_func1 (callable): A function that takes a value and returns True if the key is more than criteria1.
            filter_func2 (callable): A function that takes a value and returns True if the key is less than criteria2.
        Returns:
            ArrayList[Tuple[K, I]]: An ArrayList of tuples containing Key,Item pairs that match the filter.

        Complexity:
            Best Case: O(log n * f), where f is the combined cost of filter_func1 and filter_func2 and n refers to the number of nodes in the tree.
            Worst Case: O(n * f), where f is the combined cost of filter_func1 and filter_func2 and n refers to the number of nodes in the tree.

        Justification:
            - Best case: If pruning or early stopping were possible, only a small portion of the tree is visited.
            - Worst case: All n nodes must be visited (in-order traversal), and both filters applied to each.
        """
        result = ArrayList[Tuple[K, I]]()

        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            key = node.key
            if filter_func1(key) and filter_func2(key):
                result.append((key, node.item))
            traverse(node.right)

        traverse(self.root)
        return result
