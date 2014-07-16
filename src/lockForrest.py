

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
		if self.actualNode.payload == lock_id:
			self.actualNode = self.actualNode.parent
		else:
			path = self.getPathUpTo(self.actualNode,lock_id)
			if path == None:
				print("ERROR? release not released lock")
			else:
				path_clone = path[:-1]
				releasedNode = path[-1]
				for node in path_clone:
					node.clearChildren()
					
				releasedNode.parent.addChild(path_clone)
				
			
	def getPathUpTo(self,node,payload):
		path = []
		while node.payload != payload:
			path.append(node)
			if node.isRoot():
				return None # reached top Node with requested payload not found
			node = node.parent
			
		path.append(node)	
		return path
		
	def getHoldLocks(self,node):
		"""returns list of Locks that are acquired in the given node"""
		for node in node.getPathUpToRoot():
			path.append(node.payload)
		
# methods
#  addLock(Lock)
#  unlock
#  getAllParents(Lock): set
#  getAllChilds(Lock): set

class Node:
	def __init__(self):
		self.parent = None
		self.children = []
		self.payload = None
	def __init__(self,parent,payload):
		self.parent = parent
		self.children = []
		self.payload = payload
	def __eq__(self, other):
		return self.payload == other.payload
	def isRoot(self):
		return self.parent == None
	def isLeaf(self)
		return len(self.children) == 0
	def getNumChildren(self):
		return len(self.children)
	def addChild(self,childnode):
		childnode.parent = self
		self.children.append(childnode)

	def getPathUpTo(self,payload):
	"""returns list of Nodes representing the path to the Node with the requested payload 
			or None if no Node above has this payload"""
		if self.payload == payload:
			return [self]
		elif self.isRoot(): 
			return None
		else:
			upperpath = self.parent.getPathUpTo(payload)
			if upperpath == None: #payload not found above
				return None
			return [self].extend(upperpath)
			
	def getPathUpToRoot(self):
		"""returns list of nodes up to the Root element"""
		if self.parent == None:
			return [self]
		else:
			return [self].extend(self.parent.getPathUpToRoot())			
			
	def isAbove(self,payload):
		"""returns True if this Node or any parent Node has equal payload"""
		if self.payload == payload:
			return True
		else:
			if self.parent == None:
				return False
			else:
				return self.parent.isAbove(payload)
		
		
# Class Lock
#  abstraktion eines Locks
#  jedes obj hat eine eindeutige ID die es einem Lock im Inferior zuweist
