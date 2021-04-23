LEFT = 0
RIGHT = 1
ANY = 2


def find_most_left_right(node):
	if node is None:
		return None
	if node.right == None:
		return None
	if node.right.right == None:
		result = node.right
		node.right = node.right.left
		return result
	return find_most_left_right(node.right)


def find_most_right_left(node):
	if node is None:
		return None
	if node.left == None:
		return None
	if node.left.left == None:
		result = node.left
		node.left = node.left.right
		return result
	return find_most_right_left(node.left)


class AVLTreeNode(object):
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right
		self.weight = 0

	def pre_order(self):
		yield self.value
		if self.left is not None:
			yield from self.left.pre_order()
		if self.right is not None:
			yield from self.right.pre_order()

	def pos_order(self):

		if self.left is not None:
			yield from self.left.pos_order()
		if self.right is not None:
			yield from self.right.pos_order()
		yield self.value

	def in_order(self):
		if self.left is not None:
			yield from self.left.in_order()
		yield self.value
		if self.right is not None:
			yield from self.right.in_order()

	def remove(self, node, value, parent, direction):
		if node is None:
			return False
		if node.value == value:
			left_target = None
			right_target = None
			is_leaf = True
			append_last = True
			if node.left is not None and node.right is None:
				left_target = node.left
				is_leaf = False
				append_last = False
			elif node.left is None and node.right is not None:
				right_target = node.right
				is_leaf = False
				append_last = False
			elif node.left is not None and node.right is not None:
				left_target = find_most_left_right(node.left)
				if left_target is None:
					right_target = find_most_right_left(node.right)
					if right_target is None:
						left_target = node.left
						node.left = None
				is_leaf = False
			if is_leaf:
				if direction == LEFT:
					parent.left = None
				elif direction == RIGHT:
					parent.right = None
			else:
				if parent is not None:
					if direction == LEFT:
						if right_target is not None:
							parent.left = right_target
						elif left_target is not None:
							parent.left = left_target
						if append_last:
							parent.left.left = node.left
							parent.left.right = node.right
					elif direction == RIGHT:
						if right_target is not None:
							parent.right = right_target
						elif left_target is not None:
							parent.eight = left_target
						if append_last:
							parent.right.left = node.left
							parent.right.right = node.right
				else:
					if left_target is not None:
						left_target.left = node.left
						left_target.right = node.right
					elif right_target is not None:
						right_target.left = node.left
						right_target.right = node.right
			node.left = None
			node.right = None
			return True
		removed_left = self.remove(node.left, value, node, LEFT)
		if not removed_left:
			return self.remove(node.right, value, node, RIGHT)
		return True


def calculate_weight(node):
	if node is None:
		return -1
	return node.weight


def rotate_left(root):
	left = root.left
	root.left = left.right
	left.right = root
	root.weight = max(calculate_weight(root.left), calculate_weight(root.right)) + 1
	root.weight = max(calculate_weight(left.left), root.weight) + 1
	return left


def rotate_right(root):
	right = root.right
	root.right = right.left
	right.left = root
	root.weight = max(calculate_weight(root.left), calculate_weight(root.right)) + 1
	right.weight = max(calculate_weight(right.right), root.weight) + 1
	return right


def rotate_right_left(root):
	root.left = rotate_right(root.left)
	return rotate_left(root)


def rotate_left_right(root):
	root.right = rotate_left(root.right)
	return rotate_right(root)


class AVLTree(object):
	def __init__(self):
		self.root = None

	def search(self, value):
		for node in self.root.in_order():
			if value == node:
				return True
		return False

	def __insert(self, target, value):
		if target is None:
			target = AVLTreeNode(value)
		elif value < target.value:
			target.left = self.__insert(target.left, value)
			if calculate_weight(target.left) - calculate_weight(target.right) == 2:
				if value < target.left.value:
					target = rotate_left(target)
				else:
					target = rotate_right_left(target)
		elif value > target.value:
			target.right = self.__insert(target.right, value)
			if calculate_weight(target.right) - calculate_weight(target.left) == 2:
				if value > target.right.value:
					target = rotate_right(target)
				else:
					target = rotate_left_right(target)
		target.weight = max(calculate_weight(target.left), calculate_weight(target.right)) + 1
		return target

	def insert(self, value):
		new_root = self.__insert(self.root, value)
		if new_root is not None:
			self.root = new_root

	def remove(self, value):
		if self.root is not None:
			self.root.remove(self.root, value, None, ANY)
