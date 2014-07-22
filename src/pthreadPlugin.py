import gdb

class BaseLockDesc:
	ACQ = "lock"
	REL = "unlock"
	def __init__ (self,location="",typ=None):
		self._location = location
		self.typ = typ
	def location(self):
		""" returns the location at which the breakpoint should be set"""
		return self._location
	def getType(self):
		""" returns ACQ or REL"""
		return self.typ
	def getThreadID(self):
		""" to be implemented in child"""
		return None
	def getLockID(self):
		""" to be implemented in child"""
		return None
	def getLockInfo(self):
		""" to be implemented in child"""
		return "Unkown"
	def getCallInfo(self):
		""" to be implemented in child"""
		return "Unkown"
	
## HELPER METHODS ## to be used for implementing  	
	def getGDBThreadID():
		return gdb.selected_thread().ptid[1]
		#return gdb.selected_thread().num

	def getVariableValue(name):
		frame = gdb.newest_frame()
		if not frame.is_valid():
			print("frame not valid")
			return
		try:
			frame = gdb.newest_frame()
			value = frame.read_var(name)
		#	value = value.cast(gdb.lookup_type("unsigned int"))
			return value
		except Exception as e:
			print(e)
	def getVariableNameForPointer(variable_ptr):
		"""returns the name of the Variable the pointer variable_ptr points to """
		if variable_ptr.type.code != gdb.TYPE_CODE_PTR:
			return
		ptr = hex(int(variable_ptr))
		varname = gdb.execute("info symbol "+ptr,False,True)
		if varname[:len("No symbol matches")] != "No symbol matches":
			varname = varname.split(" ")
			if len(varname) > 0:
				return varname[0]
	def getDefinitionLocationOfVariable(name):
		r = gdb.lookup_symbol(name)
		sym = r[0]
		if sym != None:
			return str(sym.symtab.filename)+":"+str(sym.line)
	def getCallingFunctionName():
		try:
			frame = gdb.newest_frame().older()
			if frame.function() != None:
				return frame.function().print_name
			else:
				return frame.name()
		except Exception as e:
			print(e)
			return "Unkown"	
	def getFunctionName():
		try:
			frame = gdb.newest_frame()
			if frame.function() != None:
				return frame.function().print_name
			else:
				return frame.name()
		except Exception as e:
			print(e)
			return "Unkown"	
	def getCallingLocation():
		try:
			frame = gdb.newest_frame().older()
			res = str(frame.find_sal().symtab.filename)
			res += ":"+str(frame.find_sal().line)
			return res
		except Exception as e:
			print(e)

class PthreadLockDesc(BaseLockDesc):
	def __init__ (self):
		BaseLockDesc.__init__ (self,"pthread_mutex_lock",BaseLockDesc.ACQ)

	def getThreadID(self):
		return BaseLockDesc.getGDBThreadID();
	def getLockID(self):
		return BaseLockDesc.getVariableValue("mutex")
	def getLockInfo(self):
		lock_ptr = BaseLockDesc.getVariableValue("mutex")
		lock_name = BaseLockDesc.getVariableNameForPointer(lock_ptr)
		def_location = BaseLockDesc.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallInfo(self):
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()
		
class QMutexLockDesc(BaseLockDesc):
	def __init__ (self):
		BaseLockDesc.__init__ (self,"QMutex::lock",BaseLockDesc.ACQ)
	def getThreadID(self):
		return BaseLockDesc.getGDBThreadID();
	def getLockID(self):
		return BaseLockDesc.getVariableValue("this")
	def getLockInfo(self):
		lock_ptr = BaseLockDesc.getVariableValue("this")
		lock_name = BaseLockDesc.getVariableNameForPointer(lock_ptr)
		def_location = BaseLockDesc.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallInfo(self):
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()
		
class QMutexUnlockDesc(BaseLockDesc):
	def __init__ (self):
		BaseLockDesc.__init__ (self,"QMutex::unlock",BaseLockDesc.REL)
	def getThreadID(self):
		return BaseLockDesc.getGDBThreadID();
	def getLockID(self):
		return BaseLockDesc.getVariableValue("this")
	def getLockInfo(self):
		lock_ptr = BaseLockDesc.getVariableValue("this")
		lock_name = BaseLockDesc.getVariableNameForPointer(lock_ptr)
		def_location = BaseLockDesc.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallInfo(self):
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()

class PthreadUnlockDesc(BaseLockDesc):
	def __init__(self):
		BaseLockDesc.__init__(self,"pthread_mutex_unlock",BaseLockDesc.REL)
	def getThreadID(self):
		return BaseLockDesc.getGDBThreadID();
	def getLockID(self):
		return BaseLockDesc.getVariableValue("mutex")
	def getLockInfo(self):
		lock_ptr = BaseLockDesc.getVariableValue("mutex")
		lock_name = BaseLockDesc.getVariableNameForPointer(lock_ptr)
		def_location = BaseLockDesc.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallInfo(self):
		return BaseLockDesc.getFunctionName()+" called from "+BaseLockDesc.getCallingFunctionName()+ " at "+BaseLockDesc.getCallingLocation()
	
