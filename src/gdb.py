
import sys
sys.path.append('/home/cloud/projects/AKBS/gdbPythonLocktree/src')
print(sys.path)

from lockForrest import * 
from lockPlugin import * 


class StopHandler:
	lockseq = "lockseq: "
	def __call__(self,event):
		gdb.write("stop event: "+event.__class__.__name__+"\n")
		if event.__class__.__name__ != "BreakpointEvent":
			return 
		self.lockseq = self.lockseq+str(gdb.selected_thread().num)
		frame = gdb.newest_frame()
		if not frame.is_valid():
			print("frame not valid")
			return
		try:
			block = frame.block()
			if not block.is_valid():
				print("block not valid")
				return

			for sym in block:
				if sym.is_argument:
					print(sym.name)
					print(sym.value(frame).address)
					print(sym.value(frame).cast(gdb.lookup_type("unsigned int")))
		except Exception as e:
			print(e)
		print(self.lockseq)

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

class LockTreeBreakPoint(gdb.Breakpoint):
	def __init__ (self,desc,forrest):
		super(LockTreeBreakPoint,self).__init__ (desc.location(),type=gdb.BP_BREAKPOINT,internal=True)
		self.plugin = desc
		self.forrest = forrest

	def stop (self):
		tid = self.plugin.getThreadID()
		lid = self.plugin.getLockID()
		linfo = self.plugin.getLockInfo()
		cinfo = self.plugin.getCallLocation()
		if self.plugin.getType() == BaseLockDesc.ACQ:
			print("Thread "+str(tid)+" acquires Lock "+str(lid))
			self.forrest.acquire(tid,Lock(lid,linfo,"acquired: "+cinfo))
		else:
			print("Thread "+str(tid)+" releases Lock "+str(lid))
			self.forrest.release(tid,Lock(lid,linfo,"released: "+cinfo))
		return False #don't stop

class LockTreeCommand (gdb.Command):
	"""Greet the whole world."""

	def __init__ (self):
		super (LockTreeCommand, self).__init__ ("locktree", gdb.COMMAND_USER)
		self.dont_repeat()
		self.connected = False
		self.breakpoints = []
		self.registery = {"pthread":(PthreadUnlockDesc(),PthreadLockDesc()),
											"qmutex":(QMutexLockDesc(),QMutexUnlockDesc())}
		self.forrest = LockForrest()
		self.subCommands = {"addlocktype":self.registerLockType, #register a new lockDescription plugin
												"locktypes":self.printLockType,
												"monitore":self.createBreakpoints,# create Breakpoints for all stated lockDescriptions given in a space seperated list
												"stop":self.deleteBreakpoints,# delete all Breakpoints set by LockTree
												"check":self.check, # Run the Deadlock Detection
												"printthreads":self.printThreads,# print the current list of ThreadIDs that have acquired a lock
												"printtree":self.printTree,# print the current locktree for the given ThreadID
													 }
	def invoke (self, arg, from_tty):
		argv = gdb.string_to_argv(arg)
		try:
			command = argv[0].lower()
			self.subCommands[command](argv)
		except Exception as e:
			print(e)
			for command in self.subCommands.keys():
				print(command)

	def registerLockType(self,argv):
		locktypeID = argv[1]
		for locktype in argv[2:]:
			#TODO
			self.registery[locktypeID] = list()
	def printLockType(self,argv):
		for ltype in self.registery.keys():
			print(ltype)
	def createBreakpoints(self,argv):
		for locktype in argv[1:]:
			if locktype in self.registery:
				lockpluginlist = self.registery[locktype]
				try:
					for lockplugin in lockpluginlist:
						self.breakpoints.append(LockTreeBreakPoint(lockplugin,self.forrest))
						print("create locktree monitor at "+lockplugin.location())
				except TypeError as e:
					print(e)
					print("ERROR: Lock "+locktype+" doesn't has any plugins - cannot be monitored")
			else:
				print("ERROR: Lock "+locktype+" is not available - cannot be monitored")
	
	def deleteBreakpoints(self,argv):
		for br in self.breakpoints:
			br.delete()
		self.breakpoints = []
	def check(self,argv):
		"""Run the Deadlock Detection"""
		self.forrest.check()
	def printThreads(self,argv):
		"""print the current list of ThreadIDs that have acquired a lock"""
		res=""
		for x in self.forrest.getThreadList():
			res+=str(x)+" "
		print(res)
	def printTree(self,argv):
		""" print the current locktree for the given ThreadID"""
		if len(argv) > 1:
			self.forrest.printTree(int(argv[1]))
			
LockTreeCommand()



#	lockRegistery	
#		registerLockDesc

# onInit
#	for desc in lockRegistery
#		if desc.isLock:
#			LockBreakPoint(desc.location,desc.retrieveLID,desc.retrieveTID,desc.calledFrom)
#		if desc.isUnlock:
#			UnlockBreakPoint(desc.location,desc.retrieveLID,desc.retrieveTID,desc.calledFrom)

#list of all threads existing at the moment
#gdb.inferiors()[0].threads()
