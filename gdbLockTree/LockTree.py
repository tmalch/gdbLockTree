from .Node import Node
from .Utils import Thread as Thread
from .Utils import Lock as Lock
from threading import Lock as Mutex

def acquire(tid,lock_id,thread_info="", lock_info="",call_location=None):
	forrest.acquire(Thread(tid,thread_info),Lock(lock_id,lock_info),call_location)

def release(tid,lock_id,thread_info="", lock_info="",call_location=None):
#	forrest.executeCommand(lambda trees: release(trees,Thread(tid,thread_info),Lock(lock_id,lock_info),call_location))
	forrest.release(Thread(tid,thread_info),Lock(lock_id,lock_info),call_location)


class LockNode(Node):
	def __init__(self,lock,call_location=None,parent=None):
		Node.__init__(self, lock, parent)
		self.attributes['callLocations'] = set([call_location])
		
	def addCallLoc(self,call_loc):
		if call_loc is not None:
			self.attributes['callLocations'].update(call_loc)

class ThreadNode(Node): 
	"""  represents lockTree of one Thread"""
	def __init__ (self,thread):
		Node.__init__(self, thread, None)
		self.currentNode = self
	
class LockForrest:
	""" has a ThreadNode for each thread 
		represents the data/information storage"""
	def __init__ (self):
		self.mutex = Mutex()
		self.listeners = dict()
		self.listeners['newNode'] = list()
		self.trees = dict()
	
	def acquire(self,thread,lock,call_location=None):
		with self.mutex:
			if lock is None or thread is None:
				return
			if thread not in self.trees:
				self.trees[thread] = ThreadNode(thread)
				
			treeroot = self.trees[thread]
			currentNode = self.trees[thread].currentNode
			if currentNode.isAbove(lock):
				print("reentrant lock: Lock "+str(lock)+" is still acquired")
				# reentrant locks get added again
			if currentNode.findChild(lock) != None:
				# follow given path if already taken in the past
				treeroot.currentNode = currentNode.findChild(lock)
			else:
				childnode = LockNode(lock,call_location)
				currentNode.addChild(childnode)
				treeroot.currentNode = childnode
			treeroot.currentNode.addCallLoc(call_location)
	
	def release(self,thread,lock,call_location=None):
		with self.mutex:
			if lock is None or thread is None:
				return		
			if thread not in self.trees:
				print("ERROR? thread never acquired lock but releases it")
				self.trees[thread] = ThreadNode(thread)
			treeroot = self.trees[thread]
			currentNode = treeroot.currentNode
			
			if currentNode.value == lock:
				currentNode.addCallLoc(call_location)
				treeroot.currentNode = currentNode.parent
			else:# locks are not nested properly
				if currentNode.isAbove(lock):
					still_acquired = []
					for n in currentNode.getAllParents_G(): 
						still_acquired.append(n)
						if n.value == lock: 
							releasedNode = n
							break
					releasedNode.addCallLoc(call_location)
					treeroot.currentNode = releasedNode.parent
					still_acquired.reverse()
	#				add a copy of all still acquired Locks as children to the Lock above the released one
					for node in still_acquired:
						self.acquire(thread,node.value)
				else:
					print("ERROR? release not acquired lock"+str(lock))

	def registerListener(self,event,listener):
		if event not in self.listeners:
			return
		self.listeners[event].append(listener)
	
	def triggerNewNodeEvent(self,node):
		""" calls the event for all registered listeners"""
		for listener in self.listeners['newNode']:
			if callable(listener):
				with self.mutex:
					listener(self.trees.values(),node)

	def executeCommand(self,command,args=(),kwargs={}):
		"""executes the command with self.trees as argument
		command has to be callable"""
		with self.mutex:
			return command(self.trees.values(),*args,**kwargs)


forrest = LockForrest()


