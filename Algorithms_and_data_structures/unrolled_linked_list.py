#Implementacja rozwinietej listy wiazanej

length = 6

class Unrolled_node:
    def __init__(self):
        self.tab = [None for _ in range(length)]
        self.size = length
        self.next = None

    def emplace(self, idx, data):
        if self.tab[idx] is None:
            self.tab[idx] = data
        else:
            count = 1
            while count != 0:
                count = 0
                for i in range(self.size - 1):
                    if (self.tab[i] is None) and (self.tab[i + 1] is not None):
                        self.tab[i], self.tab[i + 1] = self.tab[i + 1], self.tab[i]
                        count += 1
            while self.tab[idx] is not None:
                for i in range(self.size - 1, idx, -1):
                    if self.tab[i] is None and self.tab[i - 1] is not None:
                        self.tab[i], self.tab[i - 1] = self.tab[i - 1], self.tab[i]
            for i in range(self.size):
                if self.tab[i] is None:
                    self.tab[idx] = data
                    break

    def erase(self, idx):
        self.tab[idx] = None
        count = 1
        while count != 0:
            count = 0
            for i in range(self.size - 1):
                if (self.tab[i] is None) and (self.tab[i + 1] is not None):
                    self.tab[i], self.tab[i + 1] = self.tab[i + 1], self.tab[i]
                    count += 1


class Un_link_lst:
    def __init__(self):
        self.lst = Unrolled_node()
        self.length = length
        self.num_of_elem = 0

    def get(self, idx):
        node_ptr = self.lst
        count = -1
        for i in range(node_ptr.size):
            if node_ptr.tab[i] is not None:
                count +=1
            if count == idx:
                return node_ptr.tab[i]
        while node_ptr.next is not None:
            node_ptr = node_ptr.next
            for i in range(node_ptr.size):
                if node_ptr.tab[i] is not None:
                    count += 1
                if count == idx:
                    return node_ptr.tab[i]
        return None

    def insert(self, idx, data):

        def insert_overflow(idx, data):
            node_ptr = self.lst
            coeff = 1
            while node_ptr.next is not None:
                if idx < node_ptr.size * coeff:
                    break
                coeff += 1
                node_ptr = node_ptr.next
            new_node = Unrolled_node()
            old_next = node_ptr.next
            self.length += new_node.size
            shift_idx = int(node_ptr.size / 2)
            lst_shift = node_ptr.tab[shift_idx:]
            node_ptr.tab[shift_idx:] = [None] * len(lst_shift)
            new_node.tab[:len(lst_shift)] = lst_shift
            node_ptr.next = new_node
            new_node.next = old_next
            node_ptr = self.lst
            count = 0
            if idx > self.num_of_elem:
                idx = self.num_of_elem
            for i in range(node_ptr.size):
                if node_ptr.tab[i] is not None:
                    count += 1
            while node_ptr.next is not None:
                node_ptr = node_ptr.next
                for i in range(node_ptr.size):
                    if count >= idx:
                        node_ptr.emplace(i, data)
                        self.num_of_elem += 1
                        break
                    if node_ptr.tab[i] is not None:
                        count += 1

        if self.num_of_elem < self.length:
            node_ptr = self.lst
            if self.length == self.lst.size or idx < self.lst.size:
                    node_ptr.emplace(idx, data)
                    self.num_of_elem += 1
            else:
                is_not_add = True
                count = -1
                elem_num = 0
                if idx > self.num_of_elem:
                    idx = self.num_of_elem
                for i in range(node_ptr.size):
                    if node_ptr.tab[i] is not None:
                        count += 1
                while node_ptr.next is not None and is_not_add:
                    elem_num = 0
                    node_ptr = node_ptr.next
                    for i in range(node_ptr.size):
                        if node_ptr.tab[i] is not None:
                            count += 1
                            elem_num +=1
                        if count + 1 == idx and node_ptr.tab[i] is None:
                            node_ptr.emplace(i, data)
                            self.num_of_elem += 1
                            is_not_add = False
                            break
                        if count >= idx and count + 1 < node_ptr.size:
                            node_ptr.emplace(i, data)
                            self.num_of_elem += 1
                            is_not_add = False
                            break
                if elem_num == node_ptr.size and is_not_add:
                    insert_overflow(idx, data)
        else:
            insert_overflow(idx, data)

    def delete(self, idx):
        def delete_compression(elem_num, node_ptr):
            if elem_num < int(node_ptr.size / 2):
                if node_ptr.next is not None:
                    node_ptr.emplace(elem_num, node_ptr.next.tab[0])
                    node_ptr.next.erase(0)
                    count_2 = 0
                    emplace_idx = elem_num + 1
                    for i in range(node_ptr.next.size):
                        if node_ptr.next.tab[i] is not None:
                            count_2 += 1
                    if count_2 < int(node_ptr.next.size):
                        for _ in range(node_ptr.next.size):
                            if node_ptr.next.tab[0] is not None:
                                node_ptr.emplace(emplace_idx, node_ptr.next.tab[0])
                                node_ptr.next.erase(0)
                                emplace_idx += 1
                        node_ptr.next = node_ptr.next.next
                        self.length -= node_ptr.next.size

        node_ptr = self.lst
        count = -1
        is_not_deleted = True
        if idx > self.num_of_elem:
            idx = self.num_of_elem - 1
        for i in range(node_ptr.size):
            if node_ptr.tab[i] is not None:
                count += 1
            if idx == count:
                node_ptr.erase(i)
                self.num_of_elem -=1
                is_not_deleted = False
                break
        num_one = 0
        for j in range(node_ptr.size):
            if node_ptr.tab[j] is not None:
                num_one += 1
        if num_one < int(node_ptr.size / 2):
            delete_compression(num_one, node_ptr)
        while node_ptr.next is not None and is_not_deleted:
            elem_num = 0
            node_ptr = node_ptr.next
            for i in range(node_ptr.size):
                if node_ptr.tab[i] is not None:
                    count += 1
                    elem_num += 1
                if idx == count:
                    node_ptr.erase(i)
                    is_not_deleted = False
                    self.num_of_elem -=1
                    delete_compression(elem_num, node_ptr)
                    break

    def __str__(self):
        list_str = []
        node_ptr = self.lst
        if self.num_of_elem > 0:
            for i in range(node_ptr.size):
                if node_ptr.tab[i] is not None:
                    list_str.append(str(node_ptr.tab[i]))
        while node_ptr.next is not None:
            node_ptr = node_ptr.next
            for i in range(node_ptr.size):
                if node_ptr.tab[i] is not None:
                    list_str.append(str(node_ptr.tab[i]))
        return "[" + ", ".join(list_str) + "]"

    def print_tab(self):
        tab_str = []
        node_ptr = self.lst
        for i in range(node_ptr.size):
            if node_ptr.tab[i] is not None:
                tab_str.append(str(node_ptr.tab[i]))
            else:
                tab_str.append("None")
        while node_ptr.next is not None:
            node_ptr = node_ptr.next
            for i in range(node_ptr.size):
                if node_ptr.tab[i] is not None:
                    tab_str.append(str(node_ptr.tab[i]))
                else:
                    tab_str.append("None")
        return "[" + ", ".join(tab_str) + "]"
