from collections import deque

class LockForrest:
# has a LockTree for each thread
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
#  represents lockTree of one Thread

	def __init__ (self,threadID):
		self.threadID = threadID
		self.root = Node(None)
		self.actualNode = self.root
		
	def acquire(self,lock_id):
		if lock_id == None:
			return		
		if self.actualNode.isAbove(lock_id):
			print("reentrant lock: is still acquired")
			return
		childnode = Node(self.actualNode,lock_id)
		self.actualNode.addChild(childnode)
		self.actualNode = childnode
		
	def release(self,lock_id):
		if lock_id == None:
			return
		if self.actualNode.value == lock_id:
			self.actualNode = self.actualNode.parent
		else:
			path = self.__getPathFromUpTo(self.actualNode,Node(lock_id))
			if path == None:
				print("ERROR? release not acquired lock")
			else:
#				add all acquired Locks as childs to the Lock above the released one
				path_clone = path[:-1]
				releasedNode = path[-1]
				for node in path_clone:
					node.clearChildren()					
				releasedNode.parent.addChild(path_clone[-1])
				self.actualNode = path_clone[0]
				
	def __getPathFromUpTo(self,node,query):
		path = []
		for n in node.getAllParents_G():
			path.append(n)
			if n == query:
				return path
		# reached top Node with requested value not found
		return None
		
	def getAllHoldLocks(self,lock_id):
		"""returns set of all Locks that are ever acquired when the given node is acquired"""
		query = Node(lock_id)
		hold_locks = set()
		for lockid_node in self.root.findAll(query):
			for node in lockid_node.getAllParents():
				hold_locks.add(node.value)
		return hold_locks
	def getAllLocksBelow(self,lock_id):
		""" returns set of all locks for which the given lock is acquired at some time"""
		query = Node(lock_id)
		descendant_locks = set()
		for lockid_node in self.root.findAll(query):
			for descendant in lockid_node.getAllChildrenBFS_G():
				descendant_locks.add(descendant.value)
		return descendant_locks


class Node:
	def __init__(self,value,parent=None):
		self.parent = parent
		self.children = []
		self.value = value
	def __eq__(self, other):
		if other == None:
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
			
			
	def find(self,query,generator = getAllChildrenBFS_G):
		"""find first occurence of query; Breadth First Search """
		for node in generator(self):
			if node == query:
				return node
		
	def findAll(self,query,generator = getAllChildrenBFS_G):
		"""find all occurence of query; Breadth First Search """
		occurences = []
		for node in generator(self):
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

	def isAbove(self,value):
		"""returns True if this Node or any parent Node has requested value"""
		if self.value == value:
			return True
		else:
			if self.isRoot():
				return False
			else:
				return self.parent.isAbove(value)

# Class Lock
#  abstraktion eines Locks
#  jedes obj hat eine eindeutige ID die es einem Lock im Inferior zuweist
