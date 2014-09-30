
from .Utils import Thread as Thread
from .Utils import Lock as Lock
from . import Utils
from .commands import AcquireRelease as AcquireRelease
from threading import Lock as Mutex

def acquire(tid,lock_id,thread_info="", lock_info="",call_location=None):
	forrest.executeCommandonForrest(AcquireRelease.acquire,(Thread(tid,thread_info),Lock(lock_id,lock_info),call_location))

def release(tid,lock_id,thread_info="", lock_info="",call_location=None):
	forrest.executeCommandonForrest(AcquireRelease.release,(Thread(tid,thread_info),Lock(lock_id,lock_info),call_location))
	
class LockForrest:
	""" has a ThreadNode for each thread 
		represents the data/information storage"""
	def __init__ (self):
		self.mutex = Mutex()
		self.listeners = dict()
		self.listeners['newNode'] = list()
		self.trees = list()

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

	def executeCommandonForrest(self,command,args=(),kwargs={}):
		"""executes the command with self.trees as argument
		command has to be callable """
		with self.mutex:
			return command(self.trees,*args,**kwargs)
	def executeCommandonTree(self,command,thread,args=(),kwargs={}):
		"""executes the command with self.trees as argument
		command has to be callable """
		with self.mutex:
			tree = Utils.getTreeForThread(self.trees,thread)
			if tree is not None:
				return command(tree,*args,**kwargs)
			else:
				print("thread "+str(thread)+" does not exist")
				return None

forrest = LockForrest()


