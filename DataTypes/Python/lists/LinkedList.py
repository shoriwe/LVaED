# Clase nodo creada
class Node(object):
	def __init__(self, data=None, next_node=None, node_before=None):
		self.data = data
		self.next_node = next_node
		self.node_before = node_before

	def get_data(self):
		return self.data

	def get_next(self):
		return self.next_node

	def get_before(self):
		return self.node_before

	def set_before(self, node_before):
		self.node_before = node_before

	def set_next(self, new_next):
		self.next_node = new_next


# Clase de la lista creada
class LinkedList(object):
	def __init__(self, head=None):
		self.head = head
		self.tail = head
		self.length = 0

	def __iter__(self):
		current_node = self.head
		for _ in range(self.length):
			yield current_node.data
			current_node = current_node.next_node

	# Metodo insertar
	def insert(self, index, data):
		if self.length == 0:
			raise IndexError("The list is empty")
		if index >= self.length:
			raise IndexError("Index out of range")
		if self.length == 1:
			old_head = self.head
			new_head = Node(data)
			new_head.next_node = old_head
			self.head = new_head
			self.tail = old_head
			self.tail.node_before = self.head
		elif index == 0:
			old_head = self.head
			new_head = Node(data, old_head)
			old_head.node_before = new_head
			self.head = new_head
		elif index == self.length - 1:
			new_node = Node(data, self.tail, self.tail.node_before)
			self.tail.node_before.next_node = new_node
			self.tail.node_before = new_node
		else:
			current = self.head
			for list_index in range(self.length):
				if index == list_index:
					new_node = Node(data, current, current.node_before)
					current.node_before.next_node = new_node
					current.node_before = new_node
				current = current.next_node
		self.length += 1

	# Metodo tamaño
	def size(self):
		current = self.head
		count = 0
		while current:
			count += 1
			current = current.get_next()
		return count

	def contains(self, data):
		return self.find(data) != -1

	# Metodo buscar
	def find(self, data):
		if self.length == 0:
			raise IndexError("The list is empty")
		current = self.head
		for list_index in range(self.length):
			if current.data == data:
				return list_index
			current = current.next_node
		return -1

	# Metodo Eliminar
	def remove(self, index):
		if self.length == 0:
			raise IndexError("The list is empty")
		if index >= self.length:
			raise IndexError("Index out of range")
		if self.length == 1:
			self.deleteAll()
			return
		elif index == 0:
			self.head.next_node.node_before = None
			self.head = self.head.next_node
		elif index == self.length - 1:
			self.tail.node_before.next_node = None
			self.tail = self.tail.node_before
		else:
			current_node = self.head
			for list_index in range(self.length):
				if index == list_index:
					current_node.next_node.node_before = current_node.node_before
					current_node.node_before.next_node = current_node.next_node
				current_node = current_node.next_node
		self.length -= 1

	# Metodo Anexar
	def append(self, data):
		if self.length == 0:
			self.head = Node(data)
			self.tail = self.head
		else:
			old_tail = self.tail
			new_tail = Node(data, node_before=old_tail)
			old_tail.next_node = new_tail
			self.tail = new_tail
		self.length += 1

	def get(self, index):
		if self.length == 0:
			raise IndexError("The list is empty")
		if index >= self.length:
			raise IndexError("Index out of range")
		current_node = self.head
		for list_index in range(self.length):
			if list_index == index:
				return current_node.data
			current_node = current_node.next_node

	# Metodo insertar por cabeza
	def insertHead(self, data):
		self.insert(0, data)

	# Metodo insertar por cola
	def insertTail(self, data):
		self.insert(self.length - 1, data)

	# Metodo limpiar
	def deleteAll(self):
		self.head = None
		self.tail = None
		self.length = 0

	def to_list(self):
		return list(n for n in self)

	def set(self, index, data):
		if self.length == 0:
			raise IndexError("The list is empty")
		if index >= self.length:
			raise IndexError("Index out of range")
		current_node = self.head
		for list_index in range(self.length):
			if list_index == index:
				current_node.data = data
				return
			current_node = current_node.next_node

	def sub_list(self, start, stop):
		if self.length == 0:
			raise IndexError("The list is empty")
		if stop > self.length:
			stop = self.length
		if start >= self.length:
			raise IndexError("start is bigger or equal than the length of the list")
		sub_list = LinkedList()
		append_it = False
		node = self.head
		for list_index in range(self.length):
			if list_index == start:
				sub_list.append(node.data)
				append_it = True
				if start == stop:
					break
			elif append_it and list_index < stop:
				sub_list.append(node.data)
			node = node.next_node
		return sub_list
