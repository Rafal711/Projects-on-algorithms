from random import random

class Skip_list_elem:
    def __init__(self, key=None, value=None, maxLevel=None, head_size=None):
        self.key = key
        self.value = value
        self.maxLevel = maxLevel
        self.next = [None] * head_size


class Skip_list:
    def __init__(self, head_height):
        self.head = Skip_list_elem(None, None, head_height, head_height)

    def randomLevel(self, p, maxLevel):
        lvl = 1
        while random() < p and lvl < maxLevel:
            lvl = lvl + 1
        return lvl

    def insert(self, key, value):
        previous = []
        lvl = self.head.maxLevel - 1
        ptr_copy = None
        while lvl >= 0:
            if ptr_copy is None:
                node_ptr = self.head
            else:
                node_ptr = ptr_copy
            while node_ptr.next[lvl] is not None:
                node_ptr = node_ptr.next[lvl]
                if node_ptr.key == key:
                    node_ptr.value = value
                    return self
                elif node_ptr.key > key:
                    break
                else:
                    ptr_copy = node_ptr
            if ptr_copy is None:
                previous = [self.head] + previous
            else:
                previous = [ptr_copy] + previous
            lvl -= 1
        new_elem = Skip_list_elem(key, value, self.randomLevel(0.5, self.head.maxLevel), self.head.maxLevel)
        for i in range(new_elem.maxLevel):
            new_elem.next[i] = previous[i].next[i]
            previous[i].next[i] = new_elem

    def search(self, key):
        lvl = self.head.maxLevel - 1
        ptr_copy = None
        while lvl >= 0:
            if ptr_copy is None:
                node_ptr = self.head
            else:
                node_ptr = ptr_copy
            while node_ptr.next[lvl] is not None:
                node_ptr = node_ptr.next[lvl]
                if node_ptr.key == key:
                    return  node_ptr.value
                elif node_ptr.key > key:
                    break
                else:
                    ptr_copy = node_ptr
            lvl -= 1
        return None

    def remove(self, key):
        previous = []
        lvl = self.head.maxLevel - 1
        ptr_copy = None
        while lvl >= 0:
            if ptr_copy is None:
                node_ptr = self.head
            else:
                node_ptr = ptr_copy
            while node_ptr.next[lvl] is not None:
                prev_node = node_ptr
                node_ptr = node_ptr.next[lvl]
                if node_ptr.key == key:
                    node_to_del = node_ptr
                    previous = [prev_node] + previous
                elif node_ptr.key > key:
                    break
                else:
                    ptr_copy = node_ptr
            lvl -= 1
        if not previous:
            return None
        for i in range(node_to_del.maxLevel):
            previous[i].next[i] = node_to_del.next[i]
            node_to_del.next[i] = None

    def __str__(self):
        list_str = []
        node_ptr = self.head
        while node_ptr.next[0] is not None:
            node_ptr = node_ptr.next[0]
            list_str.append(f"{node_ptr.key}: {node_ptr.value}")
        return "{" + ', '.join(list_str) + "}"

    def displayList_(self):
        node = self.head.next[0]
        keys = []
        while(node != None):
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.head.maxLevel-1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while(node != None):
                while node.key>keys[idx]:
                    print("  ", end=" ")
                    idx+=1
                idx+=1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")



skip_lst = Skip_list(4)
letter = 97
for i in range(1, 16):
    skip_lst.insert(i, chr(letter))
    letter += 1
print("stan lvl 0:", skip_lst)
print("Display:")
skip_lst.displayList_()
print("key(2) = ", skip_lst.search(2))
print("============================== insert(2, 'x')")
skip_lst.insert(2, 'x')
print("key(2) = ", skip_lst.search(2))
print("============================== remove(5), remove(6), remove(7)")
skip_lst.remove(5)
skip_lst.remove(6)
skip_lst.remove(7)
print("stan lvl 0:", skip_lst)
print("Display:")
skip_lst.displayList_()
print("============================== insert(6, 'y')")
skip_lst.insert(6, 'y')
print("stan lvl 0:", skip_lst)
print("Display:")
skip_lst.displayList_()
print("\n\n==============================================")
print("for od 15 do 1")
print("==============================================\n")
skip_lst_2 = Skip_list(4)
letter = 97
for i in range(15, 0, -1):
    skip_lst_2.insert(i, chr(letter))
    letter += 1
print("stan lvl 0:", skip_lst_2)
print("Display:")
skip_lst_2.displayList_()
print("key(2) = ", skip_lst_2.search(2))
print("============================== insert(2, 'x')")
skip_lst_2.insert(2, 'x')
print("key(2) = ", skip_lst_2.search(2))
print("============================== remove(5), remove(6), remove(7)")
skip_lst_2.remove(5)
skip_lst_2.remove(6)
skip_lst_2.remove(7)
print("stan lvl 0:", skip_lst_2)
print("Display:")
skip_lst_2.displayList_()
print("============================== insert(6, 'y')")
skip_lst_2.insert(6, 'y')
print("stan lvl 0:", skip_lst_2)
print("Display:")
skip_lst_2.displayList_()
