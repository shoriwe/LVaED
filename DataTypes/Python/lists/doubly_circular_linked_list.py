import double_linked_list

from lists import list_node


class DoublyCircularLinkedList(object):
	def __init__(self):
		self.length = 0
		self.content = double_linked_list.DoublyLinkedList()

	def update(self):
		if self.content.start is not None:
			self.content.start.before = self.content.end
		if self.content.end is not None:
			self.content.end.next = self.content.start
		self.length = self.content.length

	def clear(self):
		self.content.clear()
		self.update()

	def append(self, obj: object):
		self.content.append(obj)
		self.update()

	def insert(self, index: int, obj: object):
		self.content.insert(index, obj)
		self.update()

	def remove(self, obj: object):
		self.content.remove(obj)
		self.update()

	def remove_node(self, node: list_node.ListNode):
		self.content.remove_node(node)

	def index(self, obj: object) -> int:
		return self.content.index(obj)

	def to_list(self):
		return [node.value for node in self]

	def reverse_iterator(self):
		current = self.content.start
		while current is not None:
			yield current
			current = current.before

	def __iter__(self):
		yield from self.content

	def __contains__(self, item):
		return item in self.content

	def __setitem__(self, index, value):
		self.content.__setitem__(index, value)

	def __getitem__(self, index):
		return self.content.__getitem__(index)
