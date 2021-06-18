
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Linked_list:
    def __init__(self, data=None):
        self.head = Node(data)

    def destroy(self):
        self.head = None

    def add(self, data):
        old_linked_list = self.head
        if self.is_empty():
            old_linked_list.data = data
        else:
            self.head = Node(data)
            self.head.next = old_linked_list

    def remove(self):
        self.head = self.head.next

    def is_empty(self):
        if self.head.data is None and self.head.next is None:
            return True
        else:
            return False

    def length(self):
        node_ptr = self.head
        if self.is_empty():
            return 0
        counter = 1
        while node_ptr.next is not None:
            node_ptr = node_ptr.next
            counter += 1
        return counter

    def get(self):
        return self.head.data

    def __str__(self):
        node_ptr = self.head
        list_to_str = []
        if self.is_empty():
            return "[]"
        else:
            while node_ptr.next is not None:
                list_to_str.append(str(node_ptr.data))
                node_ptr = node_ptr.next
            list_to_str.append(str(node_ptr.data))
        return "[" + ", ".join(list_to_str) + "]"

    def append(self, data):
        node_ptr = self.head
        if self.is_empty():
            node_ptr.data = data
        else:
            while node_ptr.next is not None:
                node_ptr = node_ptr.next
            node_ptr.next = Node(data)

    def erase(self):
        node_ptr = self.head
        while node_ptr.next.next is not None:
            node_ptr = node_ptr.next
        node_ptr.next = None

    def inverse(self):
        node_ptr = self.head
        list_inv = []
        while node_ptr.next is not None:
            list_inv.append(node_ptr.data)
            node_ptr = node_ptr.next
        list_inv.append(node_ptr.data)
        list_inv = list_inv[::-1]
        node_ptr = self.head
        for elem in list_inv[:-1]:
            node_ptr.data = elem
            node_ptr = node_ptr.next
        node_ptr.data = list_inv[-1]
        return self

    def take(self, n):
        if n > self.length():
            n = self.length()
        node_ptr = self.head
        new_node = Linked_list()
        for _ in range(n):
            new_node.append(node_ptr.data)
            node_ptr = node_ptr.next
        return new_node

    def drop(self, n):
        if n > self.length():
            return Linked_list()
        node_ptr = self.head
        new_node = Linked_list()
        for i in range(1, self.length() + 1):
            if i > n:
                new_node.append(node_ptr.data)
            node_ptr = node_ptr.next
        return new_node
