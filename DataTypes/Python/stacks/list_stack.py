import lists.double_linked_list


class ListStack(object):
    def __init__(self):
        self.length = 0
        self.content = lists.double_linked_list.DoublyLinkedList()
        self.reversed = False

    def update(self):
        self.length = self.content.length

    def reverse(self):
        self.reversed = not self.reversed

    def clear(self):
        self.content.clear()

    def is_empty(self) -> bool:
        return self.content.length == 0

    def peek(self):
        if self.length == 0:
            raise IndexError("The stack is empty")
        if self.reversed:
            return self.content[self.content.length - 1]
        return self.content[0]

    def pop(self):
        if self.length == 0:
            raise IndexError("The stack is empty")
        if self.reversed:
            value = self.content[self.content.length - 1]
            del self.content[self.content.length - 1]
            self.update()
            return value
        value = self.content[0]
        del self.content[0]
        self.update()
        return value

    def push(self, obj: object):
        if self.reversed:
            self.content.append(obj)
        else:
            if self.length == 0:
                self.content.append(obj)
            else:
                self.content.insert(0, obj)
        self.update()

    def size(self):
        return self.length

    def search(self, obj: object) -> bool:
        return obj in self.content
