class ArrayStack(object):
    def __init__(self, length: int):
        self.max_length = length
        self.current_length = 0
        self.content = [None] * length
        self.reversed = False

    def reverse(self):
        self.reversed = not self.reversed

    def clear(self):
        self.content.clear()

    def is_empty(self) -> bool:
        return self.current_length == 0

    def peek(self):
        if self.current_length == 0:
            raise IndexError("The stack is empty")
        if self.reversed:
            return self.content[self.current_length - 1]
        return self.content[0]

    def pop(self):
        if self.current_length == 0:
            raise IndexError("The stack is empty")
        if self.reversed:
            value = self.content[self.current_length - 1]
            self.content[self.current_length - 1] = None
            self.current_length -= 1
            return value
        value = self.content[0]
        self.content = [*self.content[1:], None]
        self.current_length -= 1
        return value

    def push(self, obj: object):
        if self.current_length == self.max_length:
            raise IndexError("Reached maximum length of stack")
        if self.reversed:
            self.content[self.current_length] = obj
        else:
            self.content = [obj, *self.content[:-1]]
        self.current_length += 1

    def size(self):
        return self.current_length

    def search(self, obj: object) -> bool:
        return obj in self.content
