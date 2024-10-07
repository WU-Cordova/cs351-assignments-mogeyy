import pytest

from avltree import AVLTree

class TestAVLInserts():
    @pytest.fixture
    # def avltree(self) -> AVLTree: return AVLTree[int, int]([(8, 8), (9, 9), (10, 10), (2, 2), (1, 1), (5, 5), (3, 3), (6, 6), (4, 4), (7, 7)])
    def avltree(self) -> AVLTree[int, int]: 
        tree = AVLTree[int, int]()
        elements = [(8, 8), (9, 9), (10, 10), (2, 2), (1, 1), (5, 5), (3, 3), (6, 6), (4, 4), (7, 7)]
        for key, value in elements:
            tree.insert(key= key, value= value)
        return tree

    def test_insert_empty_tree(self) -> None:
        tree = AVLTree[int, int]()
        tree.insert(1, 1)
        assert tree.inorder() == [1]

    def test_insert_existing_key(self, avltree: AVLTree) -> None:
        with pytest.raises(ValueError):
            avltree.insert(8, 8)

    def test_insert_left_child(self, avltree: AVLTree) -> None:
        avltree.insert(0, 0)
        print(avltree.inorder())
        assert avltree.inorder() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_insert_right_child(self, avltree: AVLTree) -> None:
        avltree.insert(11, 11)
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] 

    def test_insert_left_grandchild(self, avltree: AVLTree) -> None:
        avltree.insert(-1, -1)
        assert avltree.inorder() == [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_insert_right_grandchild(self, avltree: AVLTree) -> None:
        avltree.insert(12, 12)
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]

    
