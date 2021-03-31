# cola

class ArrayQueue:

    def __init__(self):
        self.items = []
        self.reversed = False

    def enqueue(self, item):
        if len(self.items) == 0:
            self.items.append(item)
        else:
            if self.reversed:
                self.items.append(item)
            else:
                self.items.insert(0, item)

    def dequeue(self):
        if len(self.items) == 0:
            raise IndexError("La lista esta vacía")
        else:
            if self.reversed:
                result = self.items[0]
                self.items = self.items[1:]
            else:
                result = self.items.pop()

        return result

    def len(self):
        return len(self.items)

    def reverse(self):
        if self.reversed:
            self.reversed = False
        else:
            self.reversed = True

    def isEmpty(self):
        return len(self.items) ==0

    def clear(self):
        self.items.clear()

    def sort(self):
        self.items.sort()

    def search(self, value):
        return value in self.items

    def toString(self):
        return str(self.items)


