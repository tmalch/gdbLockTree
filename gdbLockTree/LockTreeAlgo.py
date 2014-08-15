from .Node import Node

def acquire(tid,lock_id,thread_info="", lock_info="",call_location=""):
	forrest.acquire(Thread(tid,thread_info),Lock(lock_id,lock_info,"acquired: "+call_location))

def release(tid,lock_id,thread_info="", lock_info="",call_location=""):
	forrest.release(Thread(tid,thread_info),Lock(lock_id,lock_info,"released: "+call_location))

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

class Lock:
	def __init__(self,lockid,lock_location,call_location):
		self.ID = lockid
		self.info = lock_location
		self.callLocations = set([call_location])
	def addCallLoc(self,call_loc):
		self.callLocations.update(call_loc)
	def __eq__(self, other):
		if other == None:
			return False 
		if type(other) != Lock:
			return False
		return self.ID == other.ID
	def __hash__(self):
		return int(self.ID)
	def __str__(self):
		call_loc_str = ""
		for x in self.callLocations:
			call_loc_str += x+"\n"
		return " "+str(self.ID)+"\n"+call_loc_str

class DeadLock:
	"""represents all information about a possible deadlock
		involvedlocks: the locks that have triggered the warning, list of Lock objects
		involvedthreads: the Threads that are involved, list of Thread objects """
	def __init__(self,involvedlocks,involvedthreads,gatelock=None):
		pass
class LockForrest:
	""" has a LockTree for each thread"""
	def __init__ (self):
		self.trees = {}
	
	def acquire(self,thread,lock):
		if thread not in self.trees:
			self.trees[thread] = LockTree(thread)
		self.trees[thread].acquire(lock)
	
	def release(self,thread,lock):
		if thread not in self.trees:
			print("ERROR? thread never acqired lock but releases it")
			self.trees[thread] = LockTree(thread)
		self.trees[thread].release(lock)
		
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

	def release(self,lock):
		if lock == None:
			return
		if self.currentNode.value == lock:
			self.currentNode.value.addCallLoc(lock.callLocations)
			self.currentNode = self.currentNode.parent
		else:
			path = self.__getPathFromUpTo(self.currentNode,lock)
			if path == None:
				print("ERROR? release not acquired lock"+str(lock))
			else:
#				add a copy of all still acquired Locks as childs to the Lock above the released one
				releasedNode = path[-1]
				releasedNode.value.addCallLoc(lock.callLocations)
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

forrest = LockForrest()


