from collections import deque


class LockForrest:
	""" has a LockTree for each thread"""
	def __init__ (self):
		self.trees = {}
	
	def acquire(self,thread_id,lock_id):
		if thread_id not in self.trees:
			self.trees[thread_id] = LockTree(thread_id)
		self.trees[thread_id].acquire(lock_id)
	
	def release(self,thread_id,lock_id):
		if thread_id not in self.trees:
			print("ERROR? thread never acqired lock but releases it")
			self.trees[thread_id] = LockTree(thread_id)
		self.trees[thread_id].release(lock_id)
	def check(self):
		warnings = ""
		for t1 in self.trees.values():
			for t2 in self.trees.values():
				if t1 != t2:
					warnings += self.__checkTreePair(t1,t2)
		print(warnings)

	def __checkTreePair(self,t1,t2):
		warnings = ""
		allLocks = t1.getAllLocksBelow(t1.root.value)
		for lock_id in allLocks:
			t1below = t1.getAllLocksBelow(lock_id)
			t1above = t1.getAllHoldLocks(lock_id)
			t2above = t2.getAllHoldLocks(lock_id)
			possible_deadlocks = t1below & t2above
			if len(possible_deadlocks)	!= 0:
				#check for gatelock
				gatelocks = t1above & t2above
				if len(gatelocks) > 0:
					#print("prevented by gatelock"+str(gatelocks))
					warnings += "possible deadlock between "+str(t1.threadID)+" and "+str(t2.threadID)+": "+str(possible_deadlocks)
					warnings += " prevented by gatelock"+str(gatelocks)+"\n"
				else:
					#print("possible deadlock between "+str(t1.threadID)+" and "+str(t2.threadID)+": "+str(possible_deadlocks))
					warnings += "possible deadlock between "+str(t1.threadID)+" and "+str(t2.threadID)+": "+str(possible_deadlocks)+"\n"
		return warnings
	def getThreadList(self):
		return self.trees.keys()
	def printTree(self,thread_id):
		if thread_id not in self.trees:
			print("no LockTree for Thread "+str(thread_id))
		else:
			self.trees[thread_id].printTree()

class LockTree: 
	"""  represents lockTree of one Thread"""
	def __init__ (self,threadID):
		self.threadID = threadID
		self.root = Node(None)
		self.currentNode = self.root
	def size(self):
		return len([x for x in self.root.getAllChildrenBFS_G()])
	def acquire(self,lock_id):
		if lock_id == None:
			return
		if self.currentNode.isAbove(Node(lock_id)):
			print("reentrant lock: Lock "+str(lock_id)+" is still acquired")
			# reentrant locks get added again
		if Node(lock_id) in self.currentNode.children:
			# follow given path if already taken in the past
			self.currentNode = self.currentNode.getChild(Node(lock_id))
			self.currentNode.value.addCallLoc(lock_id.callLocations)
		else:
			childnode = Node(lock_id)
			self.currentNode.addChild(childnode)
			self.currentNode = childnode

	def release(self,lock_id):
		if lock_id == None:
			return
		if self.currentNode.value == lock_id:
			self.currentNode.value.addCallLoc(lock_id.callLocations)
			self.currentNode = self.currentNode.parent
		else:
			path = self.__getPathFromUpTo(self.currentNode,lock_id)
			if path == None:
				print("ERROR? release not acquired lock"+str(lock_id))
			else:
#				add a copy of all still acquired Locks as childs to the Lock above the released one
				releasedNode = path[-1]
				releasedNode.value.addCallLoc(lock_id.callLocations)
				path = path[:-1]
				path.reverse()
				newsubtreeRoot = releasedNode.parent
				for node in path:
					self.acquire(node.value)

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
		hold_locks = hold_locks - set([lock_id,None])
		return hold_locks
	
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
	def getChild(self,query):
		for child in self.children:
			if child == query:
				return child
		#not found
		return None
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


