
from .. import gdbHelper as GDBHelper
from ..pluginBase import PluginBase
from .. import LockInterface

class pthreadMutex(PluginBase):
	def __init__(self,location,function):
		PluginBase.__init__(self,location,"pthreadMutex",LockInterface)
		self.function = function
	def handleStopEvent(self):
		tid = GDBHelper.getGDBThreadID()
		lock_ptr = GDBHelper.getVariableValue("mutex")
		lid = lock_ptr
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		linfo = lock_name + "defined at "+GDBHelper.getDefinitionLocationOfVariable(lock_name)
		call_loc = GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
		self.function(tid,lid,lock_info=linfo,call_location=call_loc)


pthreadMutex("pthread_mutex_lock",LockInterface.acquire)
pthreadMutex("pthread_mutex_unlock",LockInterface.release)


