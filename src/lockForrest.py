from collections import deque

class LockForrest:
	""" has a LockTree for each thread"""
	def __init__ (self):
		self.trees = {}
	
	def acquire(self,lock_id,thread_id):
		if thread_id not in self.trees:
			self.trees[thread_id] = LockTree(thread_id)
		self.trees[thread_id].acquire(lock_id)
	
	def release(self,lock_id,thread_id):
		if thread_id not in self.trees:
			print("ERROR? thread never acqired lock but releases it")
			self.trees[thread_id] = LockTree(thread_id)
		self.trees[thread_id].release(lock_id)

		
class LockTree: 
	"""  represents lockTree of one Thread"""

	def __init__ (self,threadID):
		self.threadID = threadID
		self.root = Node(None)
		self.actualNode = self.root
	def size(self):
		return len([x for x in self.root.getAllChildrenBFS_G()])
	def acquire(self,lock_id):
		if lock_id == None:
			return
		if self.actualNode.isAbove(Node(lock_id)):
			print("reentrant lock: Lock "+str(lock_id)+" is still acquired")
			return
		childnode = Node(lock_id)
		self.actualNode.addChild(childnode)
		self.actualNode = childnode
		
	def release(self,lock_id):
		if lock_id == None:
			return
		if self.actualNode.value == lock_id:
			self.actualNode = self.actualNode.parent
		else:
			path = self.__getPathFromUpTo(self.actualNode,lock_id)
			if path == None:
				print("ERROR? release not acquired lock"+str(lock_id))
			else:
#				add a copy of all still acquired Locks as childs to the Lock above the released one
				releasedNode = path[-1]
				path = path[:-1]
				path.reverse()
				newsubtreeRoot = releasedNode.parent
				for node in path:
					newnode = Node(node.value)
					newsubtreeRoot.addChild(newnode)
					newsubtreeRoot = newnode
				self.actualNode = newsubtreeRoot

	def __getPathFromUpTo(self,node,lock_id):
		path = []
		for n in node.getAllParents_G():
			path.append(n)
			if n.value == lock_id:
				return path
		# reached root Node but requested value not found
		return None
		
	def getAllHoldLocks(self,lock_id):
		"""returns set of all Locks that are ever acquired when the given node is acquired"""
		query = Node(lock_id)
		hold_locks = set()
		for lockid_node in self.root.findAll(query):
			for node in lockid_node.getAllParents():
				hold_locks.add(node.value)
		return hold_locks - set([lock_id,None])
	
	def getAllLocksBelow(self,lock_id):
		""" returns set of all locks for which the given lock is acquired at some time"""
		query = Node(lock_id)
		descendant_locks = set()
		for lockid_node in self.root.findAll(query):
			for descendant in lockid_node.getAllChildrenBFS_G():
				descendant_locks.add(descendant.value)
		return descendant_locks - set([lock_id])

	def printTree(self):
		print(self.root.printNode())


class Node:
	def __init__(self,value,parent=None):
		self.parent = parent
		self.children = []
		self.value = value
	def __eq__(self, other):		
		if other == None:
			return False 
		if type(other) != Node:
			return False 
		return self.value == other.value
	def isRoot(self):
		return self.parent == None
	def isLeaf(self):
		return len(self.children) == 0
	def getNumChildren(self):
		return len(self.children)
	def addChild(self,childnode):
		childnode.parent = self
		self.children.append(childnode)
		
	def getAllChildrenBFS_G(self):
		""" a Generator that returns all children of this node in BFS order
				this node as first"""	
		queue = deque([self])
		while len(queue) > 0:
			n = queue.popleft()
			yield n
			queue.extend(n.children)
			
			
	def find(self,query,order = getAllChildrenBFS_G):
		"""find first occurence of query; Breadth First Search """
		for node in order(self):
			if node == query:
				return node
		
	def findAll(self,query,order = getAllChildrenBFS_G):
		"""find all occurence of query; Breadth First Search """
		occurences = []
		for node in order(self):
			if node == query:
				occurences.append(node)
		return occurences

	def getAllParents(self):
		"""returns list of all parents of this node up to the Root element"""
		return [node for node in self.getAllParents_G() ]

	def getAllParents_G(self):
		"""a Generator which returns all parents of this node up to the Root element
				this node as first"""
		yield self
		if not self.isRoot():
			yield from self.parent.getAllParents_G()

	def getAllChildrenDFS_G(self):
		""" a Generator that returns all children of this node in DFS order
				this node as first"""	
		yield self
		for child in self.children:
			yield from child.getAllChildrenDFS_G()
			
	def isAbove(self,query):
		"""returns True if this Node or any parent Node has requested value"""
		for p in self.getAllParents_G():
			if p == query:
				return True
		return False
	def isBelow(self,query):
		"""returns True if this Node or any descendent Node has requested value (wrapper for find)"""
		r = self.find(query)
		if r == None:
			return False
		else:
			return True
	def printNode(self,prefix=""):
		""" returns string representation of the subTree starting in self"""
		res = prefix+"|--"+str(self.value)+"\n"
		for n in self.children:
			res += n.printNode(prefix=prefix+"|  ")
		return res
	def __str__(self):
		return self.printNode()



# Class Lock
#  abstraktion eines Locks
#  jedes obj hat eine eindeutige ID die es einem Lock im Inferior zuweist
