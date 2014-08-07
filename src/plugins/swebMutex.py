import gdb
import gdbHelper as GDBHelper
from pluginBase import PluginBase
import LockInterface as Interface

name = "swebmutex"

def getThreadID():
	sym = gdb.lookup_global_symbol("currentThread")
	if int(sym.value()) != 0:
		threadobj = sym.value().dereference()
		addr = str(sym.value())
		name = threadobj['name_'].string()
		return (addr,name)


class SwebMutextBP(PluginBase):
	def __init__(self,location,function):
		PluginBase.__init__(self,location,name,Interface)
		self.function = function
	def handleStopEvent(self):
		
		tid,thread_name = getThreadID()
		lock_ptr = GDBHelper.getVariableValue("this")
		lid = lock_ptr
		lock_name = lock_ptr.dereference()['name_']
		bt = GDBHelper.getBacktrace()
		btstring = ""
		for l in bt:
			btstring +=l
		
		self.function(tid,lid,thread_info=thread_name, lock_info=lock_name,call_location=btstring)


SwebMutextBP("Mutex::acquire",Interface.acquire)
SwebMutextBP("Mutex::release",Interface.release)


