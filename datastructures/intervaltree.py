from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Tuple, Generic, Optional
from avltree import AVLTree
from iavltree import K, V
import csv
import os

@dataclass
class IntervalNode:
    symbol: str
    name: str
    high: int
    low: int
    max_end: int = 0 #max end is the max price of nodes below
    height: int = 1
    def __post_init__(self):
        self.key = [self.low, self.high]

class IntervalTree:
    def __init__(self):
        self._tree = AVLTree[Tuple[int, int], Optional[List[IntervalNode]]]()

    def insert(self, symbol: str, name: str, low: int, high: int):
        interval = (low, high)
        self._tree._root = self._insert(self._tree._root, interval, symbol, name)

    def _insert(self, node: Optional[AVLTree.AVLNode[Tuple[int, int], IntervalNode]], interval: Tuple[int, int], symbol: str, name: str) -> AVLTree.AVLNode[Tuple[int, int], IntervalNode]:
        if node is None:
            new_node = IntervalNode(symbol=symbol, name=name, low=interval[0], high=interval[1], max_end=interval[1])
            return AVLTree.AVLNode(key=interval, value=new_node)

        if interval[0] < node.key[0] or (interval[0] == node.key[0] and interval[1] < node.key[1]):
            node.left = self._insert(node.left, interval, symbol, name)
        else:
            node.right = self._insert(node.right, interval, symbol, name)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        node.value.max_end = max(node.value.high, self._get_max_end(node.left), self._get_max_end(node.right))

        return self._balance(node)
    
    def _get_height(self, node: Optional[AVLTree.AVLNode[Tuple[int, int], IntervalNode]]) -> int:
        if not node:
            return 0
        return node.height

    def _get_max_end(self, node: Optional[AVLTree.AVLNode[Tuple[int, int], IntervalNode]]) -> int:
        if not node:
            return 0
        return node.value.max_end
    
    def _balance(self, node: AVLTree.AVLNode[Tuple[int, int], IntervalNode]) -> AVLTree.AVLNode[Tuple[int, int], IntervalNode]:
        balance_factor = self._get_balance(node)

        if balance_factor > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance_factor < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_balance(self, node: Optional[AVLTree.AVLNode[Tuple[int, int], IntervalNode]]) -> int:
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_left(self, node: AVLTree.AVLNode[Tuple[int, int], IntervalNode]) -> AVLTree.AVLNode[Tuple[int, int], IntervalNode]:
        reposition = None
        new_root = node.right
        node.right = None
        if new_root.left is not None:
            reposition = new_root.left
        new_root.left = node
        if reposition is not None:
            new_root.left.right = reposition

        if self._tree._root == node:
            self._tree._root = new_root

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        node.value.max_end = max(node.value.high, self._get_max_end(node.left), self._get_max_end(node.right))
        new_root.value.max_end = max(new_root.value.high, self._get_max_end(new_root.left), self._get_max_end(new_root.right))

        return new_root

    def _rotate_right(self, node: AVLTree.AVLNode[Tuple[int, int], IntervalNode]) -> AVLTree.AVLNode[Tuple[int, int], IntervalNode]:
        reposition = None
        new_root = node.left
        node.left = None
        if new_root.right is not None:
            reposition = new_root.right
        new_root.right = node
        if reposition is not None:
            new_root.right.left = reposition

        if self._tree._root == node:
            self._tree._root = new_root

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        node.value.max_end = max(node.value.high, self._get_max_end(node.left), self._get_max_end(node.right))
        new_root.value.max_end = max(new_root.value.high, self._get_max_end(new_root.left), self._get_max_end(new_root.right))

        return new_root
    
    def delete(self, key: K) -> None:
        self._tree._root = self._delete(self._tree._root, key)

    def _delete(self, node: 'AVLTree.AVLNode[K, V]', key: K) -> Optional['AVLTree.AVLNode[K, V]']:
        if node is None:
            return None
        
        if key > node.key:
            node.right = self._delete(node.right, key)
        elif key < node.key:
            node.left = self._delete(node.left, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            successor = self._successor(node.right)
            node.key, node.value = successor.key, successor.value
            node.right = self._delete(node.right, node.key)

        
        node.height = 1 + max(self._tree._height(node.left), self._tree._height(node.right))
        return self._balance(node)

    def _successor(self, node: 'AVLTree.AVLNode[K, V]') -> 'AVLTree.AVLNode[K, V]':
        current = node
        while current.left is not None:
            current = current.left
        return current


    def delete_by_symbol(self, symbol: str):
        nodes_to_delete = self._collect_nodes_by_symbol(self._tree._root, symbol)
        for node in nodes_to_delete:
            self.delete((node.key[0], node.key[1]))

    def _collect_nodes_by_symbol(self, node: Optional[AVLTree.AVLNode[Tuple[int, int], IntervalNode]], symbol: str) -> List[AVLTree.AVLNode[Tuple[int, int], IntervalNode]]:
        if not node:
            return []
        nodes = []
        if node.value.symbol == symbol:
            nodes.append(node)
        nodes.extend(self._collect_nodes_by_symbol(node.left, symbol))
        nodes.extend(self._collect_nodes_by_symbol(node.right, symbol))
        return nodes

    def range_query(self, low: int, high: int) -> List[IntervalNode]:
        result = []
        self._range_query(self._tree._root, low, high, result)
        return result
        

    def _range_query(self, node: Optional[AVLTree.AVLNode[Tuple[int, int], IntervalNode]], low: int, high: int, result: List[IntervalNode]):
        if not node:
            return
        
        if node.key[0] <= high and node.key[1] >= low:
            result.append(f"{node.value.symbol}: {node.key}")

        if node.left and node.left.value.max_end > low:
            self._range_query(node.left, low, high, result)
        self._range_query(node.right, low, high, result)

    
    def __str__(self) -> str:
        def draw_tree(node: Optional[AVLTree.AVLNode], level: int=0) -> None:
            if not node: return 
            draw_tree(node.right, level + 1)
            level_outputs.append(f'{" " * 4 * level} -> {f"{node.value.symbol}: {node.value.key}"}')
            draw_tree(node.left, level + 1)
        level_outputs: List[str] = []
        draw_tree(self._tree._root)
        return '\n'.join(level_outputs)
    

    def stocks_from_csv(self, filepath: str):
        abs_path = os.path.abspath(filepath)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"The file {abs_path} does not exist")
        with open(abs_path, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                symbol, name, low, high = row
                self.insert(symbol=symbol, name=name, low=int(low), high=int(high))

    


if __name__ == '__main__':
    tree = IntervalTree()
    stocks = [
        ("AAPL", "Apple Inc.", 15, 20),
        ("GOOGL", "Alphabet Inc.", 15, 20),
        ("MSFT", "Microsoft Corp.", 21, 30),
        ("AMZN", "Amazon.com Inc.", 5, 20),
        ("FB", "Meta Platforms Inc.", 12, 15),
        ("FB", "Meta Platforms Inc.", 1321, 145),
        ("FB", "Meta Platforms Inc.", 10, 152),
        ("FB", "Meta Platforms Inc.", 3, 10),
        ("TSLA", "Tesla Inc.", 30, 40)
    ]

    for symbol, name, low, high in stocks:
        # Insert the intervals into the tree
        tree.insert(symbol, name, low, high)

    print(f"str: {tree.__str__()}")
    print(tree.range_query(1,14))
    print(f"SIZE: {tree._tree.size()}")
    

    if False:
        print("I am testing github repository linking")