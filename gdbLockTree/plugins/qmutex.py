
import gdbHelper as GDBHelper
from pluginBase import PluginBase
import LockInterface as Interface

#interface.acquire(tid,lock_id,lock_info,call_location)
#interface.release(tid,lock_id,lock_info,call_location)

name = "qmutex"

class QMutextBP(PluginBase):
	def __init__(self,location,function):
		PluginBase.__init__(self,location,name,Interface)
		self.function = function
	def handleStopEvent(self):
		tid = GDBHelper.getGDBThreadID()
		lock_ptr = GDBHelper.getVariableValue("this")
		lid = lock_ptr
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		linfo = lock_name + "defined at "+GDBHelper.getDefinitionLocationOfVariable(lock_name)
		call_loc = GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
		self.function(tid,lid,lock_info=linfo,call_location=call_loc)


QMutextBP("QMutex::lock",Interface.acquire)
QMutextBP("QMutex::unlock",Interface.release)


