class ListNode(object):
	def __init__(self, value: object):
		self.value = value
		self.next: ListNode
		self.next = None
		self.before: ListNode
		self.before = None

	def update(self, new_value: object):
		self.value = new_value
