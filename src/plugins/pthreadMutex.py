
from pluginBase import PluginBase
import gdbHelper as GDBHelper
import LockInterface

class pthreadMutex(PluginBase):
	def __init__(self,location,function):
		PluginBase.__init__(self,location,"pthreadMutex",LockInterface)
		self.interface = function
	def handleStopEvent(self):
		tid = GDBHelper.getGDBThreadID()
		lock_ptr = GDBHelper.getVariableValue("mutex")
		lid = lock_ptr
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		linfo = lock_name + "defined at "+GDBHelper.getDefinitionLocationOfVariable(lock_name)
		call_location = GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
		self.interface(tid,lid,linfo,call_location)


pthreadMutex("pthread_mutex_lock",LockInterface.acquire)
pthreadMutex("pthread_mutex_unlock",LockInterface.release)


