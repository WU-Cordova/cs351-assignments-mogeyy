from abc import abstractmethod
from iavltree import IAVLTree, Comparable, K, V
from typing import Any, Callable, Protocol, TypeVar, Generic, Optional, List, Union

K = TypeVar('K', bound=Comparable)
V = TypeVar('V')

def printing(func):

    def wrapper(*args, **kwargs):
        # print(f'RUNNING {func.__name__.upper()} ON {args[1].key if args and isinstance(args[1], AVLTree.AVLNode) else "unknown"}')
        # print("----BEFORE_BEGIN---")
        # print(args[0].__str__())
        # print(f"SIZE = {args[0].size()}")
        # print("----BEFORE_END---")
        result = func(*args, **kwargs)
        # print("----AFTER_BEGIN---")
        # print(args[0].__str__())
        # print(f"SIZE = {args[0].size()}")
        # print("----AFTER_END---")
        return result

    return wrapper


class AVLTree(Generic[K, V]):
    def __init__(self):
        self._root: Optional[AVLTree.AVLNode[K, V]] = None
        # if self.initial is not None:
            # for key, value in self.initial:
            #     self.insert(key, value)

    class AVLNode(Generic[K, V]):
        def __init__(self, key: K, value: V):
            self.key = key
            self.value = value
            self.height = 1
            self.left: Optional[AVLTree.AVLNode] = None
            self.right: Optional[AVLTree.AVLNode] = None
        
        def set_left(self, node: Optional['AVLTree.AVLNode']) -> None:
            self.left = node

        def set_right(self, node: Optional['AVLTree.AVLNode']) -> None:
            self.right = node

    def insert(self, key: K, value: V) -> None:
        if self._root == None:
            self._root = self.AVLNode(key, value)
        else:
            self._insert(self._root, key, value)
        
    def _insert(self, node, key, value) -> Optional[AVLNode[K, V]]:
        if not isinstance(key, int):
            raise ValueError("Key must be integer value")
        if key == node.key:
            raise ValueError("Key already exists in tree.")
        
        if key > node.key:
            if node.right:
                self._insert(node.right, key, value)
            else:
                node.right = self.AVLNode(key, value)
        else:
            if node.left:
                self._insert(node.left, key, value)
            else:
                node.left = self.AVLNode(key, value)
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        parent = self.get_parent(node.key)
        try:
            if parent.right.key == node.key:
                parent.right = self._balance(node)
            else:
                parent.left = self._balance(node)
        except AttributeError:
            node = self._balance(node)

    def _balance_factor(self, node: AVLNode[K, V]) -> int:
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)
    
    def _balance(self, node: AVLNode[K, V]) -> AVLNode[K, V]: 
        balance = self._balance_factor(node)

        if balance > 1: #left
            inner_balance = self._balance_factor(node.left)
            if inner_balance < 0:
                node.left = self._rotate_right(node.left)
            return self._rotate_left(node)
            
        
        elif balance < -1: #right
            inner_balance = self._balance_factor(node.right)
            if inner_balance > 0:
                node.right = self._rotate_left(node.right)
            return self._rotate_right(node)
        
        return node
    @printing
    def _rotate_right(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        reposition = None
        new_root = node.right
        node.set_right(None)
        if new_root.left is not None:
            reposition = new_root.left
        new_root.set_left(node)
        if reposition is not None:
            new_root.left.set_right(reposition)
        
        if self._root == node:
            self._root = new_root
        
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        new_root.height = 1 + max(self._height(new_root.left), self._height(new_root.right))
        
        return new_root

    @printing    
    def _rotate_left(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        reposition = None
        new_root = node.left
        node.set_left(None)
        if new_root.right is not None:
            reposition = new_root.right
        new_root.set_right(node)
        if reposition is not None:
            new_root.right.set_left(reposition)

        if self._root == node:
            self._root = new_root 
            
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        new_root.height = 1 + max(self._height(new_root.left), self._height(new_root.right))
        
        return new_root

    def get_parent(self, key: int) -> Optional[AVLNode[K, V]]:
        if self._root is None or self._root.key == key:
            return None

        parent = None
        current = self._root

        while current:
            if key == current.key:
                return parent
            elif key < current.key:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right

        return None

    def _height(self, node: AVLNode[K, V]) -> int:
        if node is None:
            return 0
        return node.height
  
    def search(self, key: K) -> Optional[V]:
        return self._search(key, self._root)
  
    def _search(self, key: K, node: AVLNode[K, V]) -> Optional[AVLNode[K, V]]:
        if node is None:
            return "Not found"
        
        if key == node.key:
            return node.value
        
        if key > node.key:
            return self._search(key, node.right)
        else:
            return self._search(key, node.left)
        
    def delete(self, key: K) -> None:
        self._root = self._delete(self._root, key)

    def _delete(self, node: AVLNode[K, V], key: K) -> Optional[AVLNode[K, V]]:
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

        
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return self._balance(node)

    def _successor(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self) -> List[K]: # visit: Callable[[V], None] | None = None
        return self._inorder(self._root, [])

    def _inorder(self, node: AVLNode[K, V], list: List[K]) -> list[K]:
        if node is not None:
            self._inorder(node.left, list)
            list.append(node.key)
            self._inorder(node.right, list)
        return list

    def preorder(self) -> List[K]: #, visit: Callable[[V], None] | None = None
        return self._preorder(self._root, [])
    
    def _preorder(self, node: Optional[AVLNode], list) -> List[K]:
        if node is not None:
            list.append(node.key)
            self._preorder(node.left, list)
            self._preorder(node.right, list)
        return list
    
    def postorder(self) -> List[K]: #, visit: Callable[[V], None] | None = None
        return self._postorder(self._root, [])
    
    def _postorder(self, node: AVLNode[K, V], list: List[K]) -> List[K]:
        if node is not None:
            self._postorder(node.left, list)
            self._postorder(node.right, list)
            list.append(node.key)
        return list
    
    def bforder(self) -> List[K]: #, visit: Callable[[V], None] | None = None
        height = self._height(self._root)
        list = []
        for level in range(1, height+1):
            self._bforder(self._root, level, list)
        return list
            
    
    def _bforder(self, node: AVLNode[K, V], level: int, list: List[K]) -> None:
        if node is None:
            return
        elif level == 1:    
            list.append(node.key)
        elif level > 1:
            self._bforder(node.left, level - 1, list)
            self._bforder(node.right, level - 1, list)


    
    def size(self) -> int:
        return len(self.inorder())


    def __str__(self) -> str:
        def draw_tree(node: Optional[self.AVLNode[K, V]], level: int=0) -> None:
            if not node:
                return
            draw_tree(node.right, level + 1)
            level_outputs.append(f'{" "*4*level} -> {str(node.value)}')
            draw_tree(node.left, level + 1)
        level_outputs: list[str] = []
        draw_tree(self._root)
        return '\n'.join(level_outputs)
 