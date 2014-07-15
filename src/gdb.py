
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
	handler = StopHandler()
	connected = False
	breakpoints = ()
#	lockforrest = LockForrest()
	
	
	def __init__ (self):
		super (LockTreeCommand, self).__init__ ("locktree", gdb.COMMAND_USER)
		self.dont_repeat()

	def invoke (self, arg, from_tty):
		print("Hello, World!")
#		argv = gdb.string_to_argv(arg)
#		register breakpoints with bpPlugin stated in arg
		if self.connected:
			gdb.events.stop.disconnect(self.handler)
			print("disconnected")
			self.connected = False
		else:
			gdb.events.stop.connect(self.handler)
			self.connected = True
			print("connected")


#	def registerLockBreakpoints(self):
#	def deleteLockBreakpoints(self):




LockTreeCommand()



#register handler for stop event (breakpoint or signal)
#gdb.events.stop.connect (StopHandler())

#list of all threads existing at the moment
#gdb.inferiors()[0].threads()
