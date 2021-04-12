# List Based Stack (Python Implementation)

# Source Code

```python
# colas

import double_linked_list


class ListQueue:

	def __init__(self):
		self.items = double_linked_list.DoublyLinkedList()
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
				del self.items[0]

			else:
				result = self.items[self.items.length - 1]
				del self.items[self.items.length - 1]

		return result

	def len(self):
		return self.items.length

	def reverse(self):
		if self.reversed:
			self.reversed = False
		else:
			self.reversed = True

	def isEmpty(self):
		return self.items.length == 0

	def clear(self):
		self.items.clear()

	def search(self, value):
		return value in self.items

	def toString(self):
		return str(self.items)
```
