
from .. import gdbHelper as GDBHelper
from ..pluginBase import PluginBase
from .. import LockInterface as Interface
import gdb
#interface.acquire(tid,lock_id,lock_info,call_location)
#interface.release(tid,lock_id,lock_info,call_location)

name = "qmutex"

class QMutextBP(PluginBase):
	def __init__(self,location,function):
		PluginBase.__init__(self,location,name,Interface)
		self.function = function
	def handleStopEvent(self):
		try:
			tid = GDBHelper.getGDBThreadID()
			lock_ptr = GDBHelper.getVariableValue("this")
			lid = int(lock_ptr)
		except:
			print("ERROR was not able to determine LockID or/and ThreadID")
			return
		lock_name = GDBHelper.getVariableNameForPointer(lock_ptr)
		linfo = lock_name + " defined at "+GDBHelper.getDefinitionLocationOfVariable(lock_name)
		call_loc = GDBHelper.getFunctionName()+" called from "+GDBHelper.getCallingFunctionName()+ " at "+GDBHelper.getCallingLocation()
		self.function(tid,lid,lock_info=linfo,call_location=call_loc)


QMutextBP("QMutex::lock()",Interface.acquire)
QMutextBP("QMutex::unlock()",Interface.release)


