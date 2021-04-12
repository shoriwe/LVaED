# Priority Queue (Python Implementation)

# Source Code

```python
class PriorityQueueNode(object):
	def __init__(self, value: object, priority: int):
		self.value = value
		self.priority = priority


class PriorityQueue(object):
	def __init__(self):
		self.content = []
		self.length = 0

	def enqueue(self, value: object, priority: int):
		if self.length:
			index = -1
			for element_index, element in enumerate(self.content):
				if element.priority < priority:
					index = element_index
			if index != -1:
				self.content.insert(index, PriorityQueueNode(value, priority))
			else:
				self.content.append(PriorityQueueNode(value, priority))
		else:
			self.content.append(PriorityQueueNode(value, priority))
		self.length += 1

	def dequeue(self) -> object:
		if not self.length:
			raise IndexError("the priority queue is empty")
		node = self.content[0]
		self.content = self.content[1:]
		self.length -= 1
		return node.value

	def __len__(self):
		return self.length

	def __contains__(self, item):
		return item in self.content
```
