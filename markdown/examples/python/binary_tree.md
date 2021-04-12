# Binary Tree (Python Implementation)

# Source Code

```python
class BinaryTreeNode:
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right

	def insertleft(self, left):
		self.left = left

	def insertright(self, right):
		self.right = right

	def preOrder(self):
		yield self.value
		if self.left is not None:
			yield from self.left.preOrder()
		if self.right is not None:
			yield from self.right.preOrder()

	def posOrder(self):

		if self.left is not None:
			yield from self.left.posOrder()
		if self.right is not None:
			yield from self.right.posOrder()
		yield self.value

	def inOrder(self):
		if self.left is not None:
			yield from self.left.inOrder()
		yield self.value
		if self.right is not None:
			yield from self.right.inOrder()

	def removeleft(self):
		self.left = None

	def removeright(self):
		self.right = None

	def search(self, value):
		for node in self.inOrder():
			if value == node:
				return True
		return False
```