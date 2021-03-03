# Double Linked List (Python Implementation)

# Description

# Code

```python
"""
clear - Done
append - Done
length - Done
insert - Done
set - Done
contains - Done
index - Done
get - Done
sub-list - Done
to_vanilla_list - Done
head - Done
tail - Done
remove - Done
remove_node - Done
remove_value - Done
"""
import list_node


class DoublyLinkedList(object):
    def __init__(self):
        self.start: list_node.ListNode
        self.start = None
        self.end: list_node.ListNode
        self.end = None
        self.length = 0

    def reverse_iter(self):
        current = self.end
        for _ in range(self.length):
            yield current.value
            current = current.before

    def __len__(self):
        return self.length

    def __iter__(self):
        current = self.start
        for _ in range(self.length):
            yield current
            current = current.next

    def __setitem__(self, index: int, value: object):
        if self.length == 0:
            raise IndexError("The list is empty")
        if self.length <= index:
            raise IndexError("List out of range")
        for list_index, node in enumerate(self):
            if list_index == index:
                node.value = value
                break

    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def index(self, value: object) -> int:
        for index, list_value in enumerate(self):
            if list_value == value:
                return index
        raise ValueError("Value not found")

    def __getitem__(self, index: int or slice) -> object:
        if isinstance(index, int):
            if self.length == 0:
                raise IndexError("The list is empty")
            if self.length <= index:
                raise IndexError("List out of range")
            for list_index, node in enumerate(self):
                if list_index == index:
                    return node.value
        elif isinstance(index, slice):
            start = 0
            stop = self.length
            if index.start is not None:
                start = index.start
            if index.stop is not None:
                stop = index.stop
            if stop >= self.length:
                stop = self.length
            if start >= self.length:
                raise IndexError("start is bigger or equal than the length of the list")
            if stop - 1 >= 0:
                stop -= 1
            sub_list = DoublyLinkedList()
            append_it = False
            for list_index, node in enumerate(self):
                if list_index == start:
                    sub_list.append(node.value)
                    append_it = True
                    if start == stop:
                        break
                elif list_index == stop:
                    sub_list.append(node.value)
                    break
                elif append_it:
                    sub_list.append(node.value)
            return sub_list
        raise IndexError("Index must be int or slice")

    def __delitem__(self, index: int):
        if self.length == 0:
            raise IndexError("The list is empty")
        if self.length <= index:
            raise IndexError("List out of range")
        if index == 0:
            del_target = self.start
            if self.length - 1 == 0:
                self.start = None
                self.end = None
            elif self.length - 1 == 1:
                self.start = self.end
                self.start.before = None
                self.start.next = None
            else:
                next_ = del_target.next
                next_.before = None
                self.start = next_
            del del_target
        elif index == self.length - 1:
            del_target = self.end
            if self.length - 1 == 0:
                self.start = None
                self.end = None
            elif self.length - 1 == 1:
                self.end = self.start
                self.end.before = None
                self.end.next = None
            else:
                before = del_target.before
                before.before = None
                self.end = before
            del del_target
        else:
            del_target = None
            for list_index, node in enumerate(self):
                if list_index == index:
                    del_target = node
                    break
            before = del_target.before
            next_ = del_target.next
            before.next = next_
            next_.before = before
            del del_target
        self.length -= 1

    def remove_node(self, node: list_node.ListNode):
        if self.length == 0:
            raise IndexError("The list is empty")
        if not isinstance(node, list_node.ListNode):
            raise TypeError("node is not a ListNode")
        current = self.start
        found = False
        if self.length == 1 and self.start == node:
            self.start = None
            self.end = None
            found = True
        else:
            for list_index in range(self.length):
                if current == node:
                    if list_index == 0:
                        self.start = self.start.next
                        self.start.before = None
                    elif list_index == self.length - 1:
                        self.end = self.end.before
                        self.end.next = None
                    else:
                        current.next.before = current.before
                        current.before.next = current.next
                    found = True
                    break
                current = current.next
        if not found:
            raise ValueError("Node not in the list")
        self.length -= 1

    def remove(self, value: object):
        if self.length == 0:
            raise IndexError("The list is empty")
        current = self.start
        found = False
        if self.length == 1 and self.start.value == value:
            self.start = None
            self.end = None
            found = True
        else:
            for list_index in range(self.length):
                if current.value == value:
                    if list_index == 0:
                        self.start = self.start.next
                        self.start.before = None
                    elif list_index == self.length - 1:
                        self.end = self.end.before
                        self.end.next = None
                    else:
                        current.next.before = current.before
                        current.before.next = current.next
                    found = True
                    break
                current = current.next
        if not found:
            raise ValueError("Value not in the list")
        self.length -= 1

    def to_list(self):
        return [node.value for node in self]

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return str([node.value for node in self])

    def clear(self):
        self.length = 0
        self.start = None
        self.end = None

    def insert(self, index: int, value: object):
        if self.length == 0:
            raise IndexError("The list is empty")
        if self.length <= index:
            raise IndexError("List out of range")
        new_node = list_node.ListNode(value)
        if index == 0:
            self.start.before = new_node
            new_node.next = self.start
            self.start = new_node
        elif index == self.length - 1:
            self.end.before.next = new_node
            new_node.before = self.end.before
            self.end.before = new_node
            new_node.next = self.end
        else:
            for list_index, node in enumerate(self):
                if list_index == index:
                    new_node.next = node
                    new_node.before = node.before
                    node.before.next = new_node
                    node.before = new_node
                    break
        self.length += 1

    def append(self, value: object):
        new_end = list_node.ListNode(value)
        if self.length == 0:
            self.start = new_end
            self.end = new_end
        else:
            old_end = self.end
            old_end.next = new_end
            new_end.before = old_end
            self.end = new_end
        self.end = new_end
        self.length += 1
```
