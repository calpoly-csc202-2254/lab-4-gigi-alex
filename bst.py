import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union["Node", None]

@dataclass
class Node:
    first : any
    rest : BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    tree : BinTree
    
    def comes_before(self, user_val : any) -> bool:
        return self.tree.first < user_val
    
