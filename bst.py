import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union["Node", None]

@dataclass
class Node:
    element : Any
    right : BinTree
    left : BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    tree : BinTree
    comes_before : Callable[[Any, Any], bool] 

# Given a binary search tree, return true if the tree is empty, False otherwise 
def is_empty(bst : BinarySearchTree) -> bool: 
    return bst.tree is None 

# helper function for insert function
def insert_helper(tree : BinTree, value : Any, comes_before: Callable[[Any, Any], bool]) -> BinTree: 
    if tree is None: 
        return Node(value, None, None)
    if comes_before(value, tree.element): 
        return Node(tree.element, insert_helper(tree.left, value, comes_before), tree.right)
    else: 
        return Node(tree.element, tree.left, insert_helper(tree.right, value, comes_before))

# given a binary search tree and a value as arguments, adds the value to the tree by using comes_before function to determine which path to take at each node; left if before, right if after.
def insert(bst : BinarySearchTree, value : Any) -> BinarySearchTree: 
    new_tree = insert_helper(bst.tree, value, bst.comes_before) 
    return BinarySearchTree(tree=new_tree, comes_before=bst.comes_before)   

class Tests(unittest.TestCase): 
    #tests for is_empty 
    def test_is_empty_1(self): 
        bst = BinarySearchTree(comes_before=lambda x, y: x < y, tree=None)
        self.assertTrue(is_empty(bst)) 
    def test_is_empty_2(self): 
        node = Node(element=5, left=None, right=None)
        bst = BinarySearchTree(comes_before=lambda x, y: x < y, tree=node)
        self.assertFalse(is_empty(bst)) 
    #tests for insert
    def test_insert_1(self): 
        bst = BinarySearchTree(comes_before=lambda x, y: x < y, tree=None)
        bst2 = insert(bst, 10) 
        self.assertFalse(is_empty(bst2)) 
        self.assertEqual(10, bst2.tree.element) 
    def test_insert_2(self): 
        node = Node(element=10, left=None, right=None)
        bst = BinarySearchTree(comes_before=lambda x, y: x < y, tree=node)
        bst2 = insert(bst, 5) 
        self.assertEqual(5, bst2.tree.left.element) 
        self.assertIsNone(bst2.tree.right) 





if (__name__ == '__main__'):
    unittest.main() 