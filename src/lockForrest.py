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
			path = self.getPathUpTo(self.actualNode,lock_id)
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
				
	def __getPathUpTo(self,node,value):
		path = []
		while node.value != value:
			path.append(node)
			if node.isRoot():
				return None # reached top Node with requested value not found
			node = node.parent
			
		path.append(node)	
		return path
		
	def getAllHoldLocks(self,lock_id):
		"""returns set of all Locks that are ever acquired when the given node is acquired"""
		query = Node(lock_id)
		hold_locks = set()
		for lockid_node in self.root.findAllBFS(query):
			for node in lockid_node.getAllParents():
				hold_locks.add(node.value)
	def getAllLocksBelow(self,lock_id):
		""" returns set of all locks for which the given lock is acquired at any time"""
		query = Node(lock_id)
		child_locks = set()
		for lockid_node in self.root.findAllBFS(query):
			lockid_node.getAllChildren()
# methods
#  addLock(Lock)
#  unlock
#  getAllChilds(Lock): set



class Node:
	def __init__(self):
		self.parent = None
		self.children = []
		self.value = None
	def __init__(self,parent,value):
		self.parent = parent
		self.children = []
		self.value = value
	def __init__(self,value):
		self.parent = None
		self.children = []
		self.value = value
	def __eq__(self, other):
		return self.value == other.value
	def isRoot(self):
		return self.parent == None
	def isLeaf(self)
		return len(self.children) == 0
	def getNumChildren(self):
		return len(self.children)
	def addChild(self,childnode):
		childnode.parent = self
		self.children.append(childnode)
		
	def findDFS(self,query):
	"""find first occurence of query; Deepth First Search """
		if self == query
			return self
		for child in self.children:
			r = child.findDFS(query)
			if r != None:
				return r
		return None

	def findAllDFS(self,query,res = []):
	"""find all occurence of query; Deepth First Search """
		if self == query
			res.append(self)
		for child in self.children:
			child.findAllDFS(query,res)
		return res
	
	def findBFS(self,query):
	"""find first occurence of query; Breadth First Search """
		queue = deque(self)
		while len(queue) > 0:
			n = queue.popLeft()
			if n == query
				return n
			queue.extend(n.children)
		return None
		
	def findAllBFS(self,query):
	"""find all occurence of query; Breadth First Search """
		occurences = []
		queue = deque(self)
		while len(queue) > 0:
			n = queue.popLeft()
			if n == query
				occurences.append(n)
			queue.extend(n.children)
		return None

#	def getPathUpTo(self,value): # use allParents generator in a loop
#	"""returns list of Nodes representing the path to the Node with the requested value 
#			or None if no Node above has this value"""
#		if self.value == value:
#			return [self]
#		elif self.isRoot(): 
#			return None
#		else:
#			upperpath = self.parent.getPathUpTo(value)
#			if upperpath == None: #value not found above
#				return None
#			return [self].extend(upperpath)
			
	def getAllParents(self):
		"""returns list of all parents of this node up to the Root element"""
		return [node in self.getAllParentsG() ]

	def getAllParentsG(self):
		"""a Generator which returns all parents of this node up to the Root element
				this node as first"""
		yield self
		if not self.isRoot():
			yield from self.parent.getAllParentsG()
		
	def getAllChildrenBFS_G(self):
		""" a Generator that returns all children of this node in BFS order
				this node as first"""	
		queue = deque(self)
		while len(queue) > 0:
			n = queue.popLeft()
			yield n
			
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
