


class BaseLockDesc():
	ACQ = "lock"
	REL = "unlock"
	def __init__ (self,location="",typ=None):
		self.location = location
		self.type = typ
	def location():
		""" returns the location at which the breakpoint should be set"""
		return self.location
	def getType():
		""" returns ACQ or REL"""
		return self.type
	def getThreadID():
		""" to be implemented in child"""
		return None
	def getLockID():
		""" to be implemented in child"""
		return None
	def getSourceLine():
		""" to be implemented in child"""
		return "Unkown"
	
## HELPER METHODS ## to be used for implementing  	
	def getGDBThreadID(self):
		return gdb.selected_thread().num

	def getVariableValue(self,name):
		frame = gdb.newest_frame()
		if not frame.is_valid():
			print("frame not valid")
			return
		try:
			frame = gdb.newest_frame()
			value = frame.read_var(name)
			value = value.cast(gdb.lookup_type("unsigned int"))
			return value
		except Exception as e:
			print(e)
	def getCallingFunctionName(self):
		try:
			frame = gdb.newest_frame().older()
			if frame.function() != None:
				return frame.function().print_name
			else:
				return frame.name()
		except Exception as e:
			print(e)
			return "Unkown"	
	def getFunctionName(self):
		try:
			frame = gdb.newest_frame()
			if frame.function() != None:
				return frame.function().print_name
			else:
				return frame.name()
		except Exception as e:
			print(e)
			return "Unkown"	
	def getCallingLocation(self):
		try:
			frame = gdb.newest_frame().older()
			res = str(frame.find_sal().symtab.filename)
			res += ":"+str(frame.find_sal().line)
			return res
		except Exception as e:
			print(e)

class PthreadLockDesc(BaseLockDesc):
	def __init__ (self):
		super(self).__init__ ("pthread_mutex_lock",ACQ)

	def getThreadID():
		return BaseLockDesc.getGDBThreadID();
	def getLockID():
		return BaseLockDesc.getVariableValue("mutex")
	def getSourceLine():
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()
		
class QMutexLockDesc(BaseLockDesc):
	def __init__ (self):
		super(self).__init__ ("QMutex::lock",ACQ)
	def getThreadID():
		return BaseLockDesc.getGDBThreadID();
	def getLockID():
		return BaseLockDesc.getVariableValue("this")
	def getSourceLine():
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()
		
class QMutexLockDesc(BaseLockDesc):
	def __init__ (self):
		super(self).__init__ ("QMutex::unlock",ACQ)
	def getThreadID():
		return BaseLockDesc.getGDBThreadID();
	def getLockID():
		return BaseLockDesc.getVariableValue("this")
	def getSourceLine():
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()

class PthreadUnlockDesc(BaseLockDesc):
	def __init__ (self):
		super(self).__init__ ("pthread_mutex_unlock",REL)

	def getThreadID():
		return BaseLockDesc.getGDBThreadID();
	def getLockID():
		return BaseLockDesc.getVariableValue("mutex")
	def getSourceLine():
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()


class LockTreeBreakPoint(gdb.BreakPoint):
	def __init__ (self,desc,forrest):
		super(self).__init__ (desc.location(),gdb.BP_BREAKPOINT,True)
		self.plugin = desc
		self.forrest = forrest
	
	def stop (self):
		tid = self.plugin.getThreadID()
		lid = self.plugin.getLockID()
		src = self.plugin.getSourceLine()
		if self.plugin.getType() == "lock":
			self.forrest.acquire(tid,Lock(lid,src))
		else:
			self.forrest.release(tid,Lock(lid,src))
			
			
			
			
			



