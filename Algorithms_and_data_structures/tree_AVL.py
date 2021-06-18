from copy import copy


class BinaryNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.right = None
        self.left = None
        self.balance = 0


class AvlTree:
    def __init__(self, key=None, value=None):
        self.root = BinaryNode(key, value)

    def search_node(self, key, node=None, start=True):
        if start:
            node = self.root
            if node.key is None:
                return None
            start = False
        if node.key is None:
            return None
        elif key < node.key:
            return self.search_node(key, node.left, start)
        elif key > node.key:
            return self.search_node(key, node.right, start)
        else:
            return node

    def search(self, key):
        return self.search_node(key).value

    def set_balance(self, node):
        left_h = 0 if node.left is None else self.height(node.left.key)
        right_h = 0 if node.right is None else self.height(node.right.key)
        node.balance = left_h - right_h

    def insert(self, key, value, node=None, start=True):
        if start:
            node = self.root
            if node.key is None or node.key == key:
                node.key = key
                node.value = value
                return self
            start = False
        if node is None:
            return BinaryNode(key, value)
        if key < node.key:
            node.left = self.insert(key, value, node.left, start)
            self.set_balance(node)
            self.rotate(node)
            return node
        elif key > node.key:
            node.right = self.insert(key, value, node.right, start)
            self.set_balance(node)
            self.rotate(node)
            return node
        else:
            node.key = key
            node.value = value
            return node

    def delete(self, key, node=None, start=True):
        if start:
            node = self.root
            start = False
        if node is None:
            return node
        if key < node.key:
            node.left = self.delete(key, node.left, start)
            self.set_balance(node)
            self.rotate(node)
        elif key > node.key:
            node.right = self.delete(key, node.right, start)
            self.set_balance(node)
            self.rotate(node)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            node_ptr = node.right
            while node_ptr.left is not None:
                node_ptr = node_ptr.left
            node.key = node_ptr.key
            node.value = node_ptr.value
            node.right = self.delete(node_ptr.key, node.right, start)
            self.set_balance(node)
            self.rotate(node)
        return node

    def preorder_balance(self, node):
        if node is not None:
            self.set_balance(node)
            self.preorder_balance(node.left)
            self.preorder_balance(node.right)

    def print_tree(self):
        def _print_tree(node, lvl):
            if node is not None:
                _print_tree(node.right, lvl + 10)
                print()
                for i in range(10, lvl + 10):
                    print(end=" ")
                print(node.key)
                _print_tree(node.left, lvl + 10)
        print("=====================")
        _print_tree(self.root, 0)
        print("=====================")

    def print_tree_balance(self):
        def _print_tree(node, lvl):
            if node is not None:
                _print_tree(node.right, lvl + 10)
                print()
                for i in range(10, lvl + 10):
                    print(end=" ")
                print(node.balance)
                _print_tree(node.left, lvl + 10)
        print("=====================")
        _print_tree(self.root, 0)
        print("=====================")

    def print_tree_str(self, node=None, lst=None):
        if lst is None:
            node = self.root
            lst = []
        if node is not None:
            self.print_tree_str(node.left, lst)
            lst.append(f"{node.key}: {node.value}")
            self.print_tree_str(node.right, lst)
            return "{" + ", ".join(lst) + "}"

    def __str__(self):
        return self.print_tree_str()

    def height(self, key=None, node=None, start=True):
        if start:
            if key is None:
                node = self.root
            else:
                node = self.search_node(key)
            start = False
        if node is None:
            return 0
        else:
            left_h = self.height(key, node.left, start)
            right_h = self.height(key, node.right, start)
            return max(left_h, right_h) + 1

    def rotate_LL(self, node):
        node_copy = copy(node)
        node_copy.right = node.right.left
        node.key = node.right.key
        node.value = node.right.value
        node.right = node.right.right
        node.left = node_copy
        self.set_balance(node)

    def rotate_RR(self, node):
        node_copy = copy(node)
        node_copy.left = node.left.right
        node.key = node.left.key
        node.value = node.left.value
        node.left = node.left.left
        node.right = node_copy
        self.set_balance(node)

    def rotate_LR(self, node):
        self.rotate_RR(node.right)
        self.rotate_LL(node)
        self.preorder_balance(node)

    def rotate_RL(self, node):
        self.rotate_LL(node.left)
        self.rotate_RR(node)
        self.preorder_balance(node)

    def rotate(self, node):
        if node.key is not None:
            if node.right is not None:
                if node.balance == -2 and node.right.balance == 1:
                    self.rotate_LR(node)
                if node.balance == -2 and node.right.balance == -1:
                    self.rotate_LL(node)
            if node.left is not None:
                if node.balance == 2 and node.left.balance == -1:
                        self.rotate_RL(node)
                if node.balance == 2 and node.left.balance == 1:
                    self.rotate_RR(node)
