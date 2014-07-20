
#script that is called from gdb

#register breakpoints for lock/unlock
#register events for breakpoint hit

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


	

class LockTreeCommand (gdb.Command):
	"""Greet the whole world."""

	def __init__ (self):
		super (LockTreeCommand, self).__init__ ("locktree", gdb.COMMAND_USER)
		self.dont_repeat()
		self.connected = False
		self.breakpoints = []
		self.registery = {}
		self.Lockforrest = LockForrest()
		self.subCommands = {"addLockType":self.registerLockType, #register a new lockDescription plugin
												"monitore":self.createBreakpoints,# create Breakpoints for all stated lockDescriptions given in a space seperated list
												"stop":self.deleteBreakpoints,# delete all Breakpoints set by LockTree
												
													 }
	def invoke (self, arg, from_tty):
		argv = gdb.string_to_argv(arg)
		self.subCommands[argv[0]](argv)

				
		if self.connected:
			gdb.events.stop.disconnect(self.handler)
			print("disconnected")
			self.connected = False
		else:
			gdb.events.stop.connect(self.handler)
			self.connected = True
			print("connected")

	def registerLockType(self,argv):
		locktypeID = argv[1]
		for locktype in argv[2:]:
		
		self.registery[locktypeID] = list()
	
	def createBreakpoints(self,argv):
		for locktype in argv[1:]:
			if locktype in self.registery:
				lockpluginlist = self.registery[locktype]
				try:
					for lockplugin in lockpluginlist:
						self.breakpoints.add(LockTreeBreakPoint(lockplugin))
				except TypeError, e:
  				#object is not actually iterable
					print("ERROR: Lock "+locktype+" doesn't has any plugins - cannot be monitored")
			else:
				print("ERROR: Lock "+locktype+" is not available - cannot be monitored")
	def deleteBreakpoints(self,argv):




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
