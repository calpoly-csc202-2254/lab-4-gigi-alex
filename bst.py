import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union["Node", None]

@dataclass
class Node:
    element : Any
    left : BinTree
    right : BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    tree : BinTree
    comes_before : Callable[[Any, Any], bool]

def int_comes_before(int1 : int, int2 : int) -> bool:
    return int1 < int2

def str_comes_before(str1 : str, str2 : str) -> bool:
    return str1 < str2

ex1 = BinarySearchTree(Node(10,Node(5,None,None),None),int_comes_before)
ex2 = BinarySearchTree(Node("a",None,None),str_comes_before)

# Given a binary search tree, return true if the tree is empty, False otherwise 
def is_empty(bst : BinarySearchTree) -> bool: 
    return bst.tree is None 

# helper function for insert function
def insert_helper(tree : BinTree, value : Any, comes_before: Callable[[Any, Any], bool]) -> BinTree: 
    match tree:
        case None: 
            return Node(value, None, None)
        case Node(e, l, r):
            if comes_before(value, tree.element): 
                return Node(tree.element, insert_helper(tree.left, value, comes_before), tree.right)
            else: 
                return Node(tree.element, tree.left, insert_helper(tree.right, value, comes_before))

# given a binary search tree and a value as arguments, adds the value to the tree by using comes_before function to determine which path to take at each node; left if before, right if after.
def insert(bst : BinarySearchTree, value : Any) -> BinarySearchTree: 
    new_tree = insert_helper(bst.tree, value, bst.comes_before)
    return BinarySearchTree(tree = new_tree, comes_before = bst.comes_before)   


# given a binary search tree and a value, return True if the value is stored in the tree and False otherwise 
def lookup(bst : BinarySearchTree, value : Any) -> bool:  
    if bst.tree is None:
        return False
    elif bst.comes_before(value, bst.tree.element) == False and bst.comes_before(bst.tree.element, value) == False:
        return True
    elif bst.comes_before(value, bst.tree.element):
        return lookup(BinarySearchTree(bst.tree.left, bst.comes_before), value)
    else:
        return lookup(BinarySearchTree(bst.tree.right, bst.comes_before), value) 

# given a binary search tree and a value as arguments, removes the value from the tree if present while preserving the binary search tree propertu, that for a given node's value, the values in the left subtree come before, right do not.
# if the tree happens to have multiple nodes containing the value to be removed, only a single such node will be removed

def delete_helper(tree : BinTree, value: Any, comes_before : Callable[[Any, Any], bool]) -> BinTree:
    match tree:
            case None:
                return None
            case Node(e, l, r):
                if comes_before(value, e):
                    return delete_helper(l, value, comes_before)
                elif comes_before(e, value):
                    return delete_helper(r, value, comes_before)
                else:
                    if l is None:
                        return r
                    elif r is None:
                        return l
                    else:
                        current = l
                        while current is not None and current.right is not None:
                            current = current.right
                        new_value = current.element
                        new_left = delete_helper(l, current.element, comes_before)
                        return Node(new_value, new_left, r)
                    

def delete(bst : BinarySearchTree, value : Any) -> BinarySearchTree: 
    new_tree = delete_helper(bst.tree, value, bst.comes_before)
    return BinarySearchTree(new_tree, comes_before=bst.comes_before)

test = BinarySearchTree(Node(5, Node(4, None, None), Node(10, None, None)),int_comes_before)
test_after = delete(test, 5)
print(test_after)


class Tests(unittest.TestCase): 
    #tests for is_empty 
    def test_is_empty_1(self): 
        bst = BinarySearchTree(comes_before = int_comes_before, tree = None)
        self.assertTrue(is_empty(bst)) 
    def test_is_empty_2(self): 
        node = Node(element=5, left=None, right=None)
        bst = BinarySearchTree(comes_before = int_comes_before, tree = node)
        self.assertFalse(is_empty(bst)) 
    #tests for insert
    def test_insert_1(self): 
        bst = BinarySearchTree(comes_before = int_comes_before, tree = None)
        bst2 = insert(bst, 10) 
        self.assertFalse(is_empty(bst2)) 
        self.assertEqual(10, bst2.tree.element) 
    def test_insert_2(self): 
        node = Node(element=10, left=None, right=None)
        bst = BinarySearchTree(comes_before = int_comes_before, tree = node)
        bst2 = insert(bst, 5)
        self.assertEqual(5, bst2.tree.left.element) 
        self.assertIsNone(bst2.tree.right) 
    def test_insert_3(self): 
        node = Node(element=20, left=None, right=None)
        bst = BinarySearchTree(comes_before = int_comes_before, tree = node)
        bst2 = insert(bst, 22) 
        self.assertEqual(22, bst2.tree.right.element)
        self.assertIsNone(bst2.tree.left) 
    def test_insert_4(self): 
        node = Node(element='b', right=Node(element='d', left=None, right=None), left=Node(element='a', left=None, right=None)) 
        bst = BinarySearchTree(comes_before = str_comes_before, tree=node) 
        bst2 = insert(bst, 'c') 
        self.assertEqual('d', bst2.tree.right.element) 
        self.assertEqual('c', bst2.tree.right.left.element) 
    #tests for lookup 
    def test_lookup_1(self): 
        node = Node(element=15, left=Node(element=10, left=None, right=None), right=Node(element=20, left=None, right=None)) 
        bst = BinarySearchTree(comes_before = int_comes_before, tree = node)    
        self.assertTrue(lookup(bst, 15)) 
        self.assertTrue(lookup(bst, 10)) 
        self.assertTrue(lookup(bst, 20)) 
        self.assertFalse(lookup(bst, 100)) 
    def test_lookup_2(self): 
        node = Node(element='g', left=Node(element='a', left=None, right=None), right=Node(element='z', left=None, right=None)) 
        bst = BinarySearchTree(comes_before=str_comes_before, tree = node) 
        self.assertTrue(lookup(bst, 'g')) 
        self.assertTrue(lookup(bst, 'a')) 
        self.assertTrue(lookup(bst, 'z'))
        self.assertFalse(lookup(bst, 'k')) 


if (__name__ == '__main__'):
    unittest.main() 

