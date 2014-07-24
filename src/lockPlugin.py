import gdb
from gdbHelper import *

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
	def getCallLocation(self):
		""" to be implemented in child"""
		return "Unkown"

class PthreadLockDesc(BaseLockDesc):
	def __init__ (self):
		BaseLockDesc.__init__ (self,"pthread_mutex_lock",BaseLockDesc.ACQ)

	def getThreadID(self):
		return GDBHelper.getGDBThreadID();
	def getLockID(self):
		return GDBHelper.getVariableValue("mutex")
	def getLockInfo(self):
		lock_ptr = GDBHelper.getVariableValue("mutex")
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		def_location = GDBHelper.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallLocation(self):
		return GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
		
class QMutexLockDesc(BaseLockDesc):
	def __init__ (self):
		BaseLockDesc.__init__ (self,"QMutex::lock",BaseLockDesc.ACQ)
	def getThreadID(self):
		return GDBHelper.getGDBThreadID();
	def getLockID(self):
		return GDBHelper.getVariableValue("this")
	def getLockInfo(self):
		lock_ptr = GDBHelper.getVariableValue("this")
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		def_location = GDBHelper.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallLocation(self):
		return GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
		
class QMutexUnlockDesc(BaseLockDesc):
	def __init__ (self):
		BaseLockDesc.__init__ (self,"QMutex::unlock",BaseLockDesc.REL)
	def getThreadID(self):
		return GDBHelper.getGDBThreadID();
	def getLockID(self):
		return GDBHelper.getVariableValue("this")
	def getLockInfo(self):
		lock_ptr = GDBHelper.getVariableValue("this")
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		def_location = GDBHelper.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallLocation(self):
		return GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()

class PthreadUnlockDesc(BaseLockDesc):
	def __init__(self):
		BaseLockDesc.__init__(self,"pthread_mutex_unlock",BaseLockDesc.REL)
	def getThreadID(self):
		return GDBHelper.getGDBThreadID();
	def getLockID(self):
		return GDBHelper.getVariableValue("mutex")
	def getLockInfo(self):
		lock_ptr = GDBHelper.getVariableValue("mutex")
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		def_location = GDBHelper.getDefinitionLocationOfVariable(lock_name)
		return lock_name+" defined at "+def_location
	def getCallLocation(self):
		return GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
	
