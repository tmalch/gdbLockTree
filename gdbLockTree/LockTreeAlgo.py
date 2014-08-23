from .Node import Node

def acquire(tid,lock_id,thread_info="", lock_info="",call_location=None):
	forrest.acquire(Thread(tid,thread_info),Lock(lock_id,lock_info),call_location)

def release(tid,lock_id,thread_info="", lock_info="",call_location=None):
	forrest.release(Thread(tid,thread_info),Lock(lock_id,lock_info),call_location)

class Thread:
	def __init__(self,thread_id,thread_info=""):
		self.ID = thread_id
		self.info = thread_info

	def __eq__(self, other):
		if other == None:
			return False 
		if type(other) != Thread:
			return False
		return self.ID == other.ID
	def __hash__(self):
		return int(self.ID)
	def __str__(self):
		return str(self.info)+":"+str(self.ID)

class LockTreeNode(Node):
	def __init__(self,lock,call_location=None,parent=None):
		Node.__init__(self, lock, parent)
		self.callLocations = set([call_location])
	def addCallLoc(self,call_loc):
		self.callLocations.update(call_loc)
		
class Lock:
	def __init__(self,lockid,lock_location):
		self.ID = lockid
		self.info = lock_location
	def __eq__(self, other):
		if other == None:
			return False 
		if type(other) != Lock:
			return False
		return self.ID == other.ID
	def __hash__(self):
		return int(self.ID)
	def __str__(self):
		return str(self.ID)+"\n"

class DeadLock:
	"""represents all information about a possible deadlock
		involvednodes: two lists of nodes which locks have triggered the warning
		involvedthreads: the Threads that are involved, list of Thread objects """
	def __init__(self,involvedthreads,involvednodes):
		pass
	def __hash__(self):
		pass
	def __eq__(self, other):
		pass
		
class LockForrest:
	""" has a LockTree for each thread"""
	def __init__ (self):
		self.trees = {}
	
	def acquire(self,thread,lock,call_location=None):
		if thread not in self.trees:
			self.trees[thread] = LockTree(thread)
		self.trees[thread].acquire(lock,call_location)
	
	def release(self,thread,lock,call_location=None):
		if thread not in self.trees:
			print("ERROR? thread never acqired lock but releases it")
			self.trees[thread] = LockTree(thread)
		self.trees[thread].release(lock,call_location)
		
	def check(self):
		warnings = ""
		for t1 in self.trees.values():
			for t2 in self.trees.values():
				if t1 != t2:
					warnings += self.__checkTreePair2(t1,t2)
		print(warnings)
	def __checkTreePair2(self,t1,t2):
		""" returns list of all nodes that may cause a deadlock between thread t1 and t2"""
		def intersect(nodeset1,nodeset2,cmp=lambda n1,n2: n1.value == n2.value):
			""" intersect two sets of nodes by there values"""
			intersection1 = []
			intersection2 = []
			for node1 in nodeset1:
				for node2 in nodeset2:
					if cmp(node1,node2):
						intersection1.append(node1)
						intersection2.append(node2)
			return (intersection1,intersection2)
		warnings = ""
		for node1 in t1.root.getAllChildrenDFS_G():
			t1below_node = [ n for n in node1.getAllChildrenDFS_G() if n is not node1 ]
			t1above_node = [n for n in node1.getAllParents_G() if n is not (node1 and t1.root) ]
			for node2 in t2.root.findAll(node1.value):
				t2above_node = [ n for n in node2.getAllParents_G() if n is not (node2 and t2.root)]
				(t1deadlocks,t2deadlocks) = intersect(t1below_node,t2above_node,lambda n1,n2: n1.value == n2.value)
				if len(t1deadlocks)	> 0:
					#check for gatelock
					(t1gatelocks,t2gatelocks) = intersect(t1above_node, t2above_node,lambda n1,n2: n1.value == n2.value)
					stringlist = [str(l.value.info) for l in t1deadlocks]
					stringlist.append(str(node1.value.info))
					if len(t1gatelocks) > 0:
						warnings += "possible deadlock between "+str(t1.thread)+" and "+str(t2.thread)+": "+str(stringlist)
						warnings += " prevented by gatelock"+str([str(l.value.info) for l in t1gatelocks])+"\n"
					else:
						DeadLock((t1.thread,t2.thread),(t1deadlocks,t2deadlocks))
						warnings += "possible deadlock between "+str(t1.thread)+" and "+str(t2.thread)+": "+str(stringlist)+"\n"
		return warnings
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
				stringlist = [str(l.info) for l in possible_deadlocks]
				stringlist.append(str(lock_id.info))
				if len(gatelocks) > 0:
					#print("prevented by gatelock"+str(gatelocks))
					warnings += "possible deadlock between "+str(t1.thread)+" and "+str(t2.thread)+": "+str(stringlist)
					warnings += " prevented by gatelock"+str([str(l.info) for l in gatelocks])+"\n"
				else:
					#print("possible deadlock between "+str(t1.thread)+" and "+str(t2.thread)+": "+str(possible_deadlocks))
					warnings += "possible deadlock between "+str(t1.thread)+" and "+str(t2.thread)+": "+str(stringlist)+"\n"
		return warnings

	def getThreadList(self):
		return self.trees.keys()
	
	def printTree(self,thread):
		if thread not in self.trees:
			print("no LockTree for Thread "+str(thread))
		else:
			self.trees[thread].printTree()

class LockTree: 
	"""  represents lockTree of one Thread"""
	def __init__ (self,thread):
		self.thread = thread
		self.root = LockTreeNode(None,None)
		self.currentNode = self.root
	def size(self):
		return len([x for x in self.root.getAllChildrenBFS_G()])
	def acquire(self,lock,callLocation=None):
		if lock == None:
			return
		if self.currentNode.isAbove(lock):
			print("reentrant lock: Lock "+str(lock)+" is still acquired")
			# reentrant locks get added again
			
		if self.currentNode.findChild(lock) != None:
			# follow given path if already taken in the past
			self.currentNode = self.currentNode.findChild(lock)
			self.currentNode.addCallLoc(callLocation)
		else:
			childnode = LockTreeNode(lock,callLocation)
			self.currentNode.addChild(childnode)
			self.currentNode = childnode

	def release(self,lock,callLocation=None):
		if lock == None:
			return
		if self.currentNode.value == lock:
			self.currentNode.addCallLoc(callLocation)
			self.currentNode = self.currentNode.parent
		else:
			path = self.__getPathFromUpTo(self.currentNode,lock)
			if path == None:
				print("ERROR? release not acquired lock"+str(lock))
			else:
#				add a copy of all still acquired Locks as childs to the Lock above the released one
				releasedNode = path[-1]
				releasedNode.addCallLoc(callLocation)
				path = path[:-1]
				path.reverse()
				self.currentNode = releasedNode.parent
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
		query = lock_id
		hold_locks = set()
		for lockid_node in self.root.findAll(query):
			for node in lockid_node.getAllParents():
				hold_locks.add(node.value)
		hold_locks = hold_locks - set([lock_id,None])
		return hold_locks
	
	def getAllLocksBelow(self,lock_id):
		""" returns set of all locks for which the given lock is acquired at some time"""
		query = lock_id
		descendant_locks = set()
		for lockid_node in self.root.findAll(query):
			for descendant in lockid_node.getAllChildrenBFS_G():
				descendant_locks.add(descendant.value)
		return descendant_locks - set([lock_id])

	def printTree(self):
		print(self.root.printSubTree())

forrest = LockForrest()


