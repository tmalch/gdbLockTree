import gdb
from .. import gdbHelper as GDBHelper
from ..pluginBase import PluginBase
from .. import LockInterface as Interface

name = "swebmutex"

def getThreadID():
	sym = gdb.lookup_global_symbol("currentThread")
	if int(sym.value()) != 0:
		addr = int(sym.value())
		threadobj = sym.value().dereference()
		name = threadobj['name_'].string()
		return (addr,name)
	else:
		return (None,"locktree wasn't able to identify thread")


class SwebMutextBP(PluginBase):
	def __init__(self,location,function):
		PluginBase.__init__(self,location,name,Interface)
		self.function = function
	def handleStopEvent(self):
		
		tid,thread_name = getThreadID()
		lock_ptr = GDBHelper.getVariableValue("this")
		lid = int(lock_ptr)
		lock_obj = lock_ptr.dereference()
		try:
			lock_name = lock_obj['name_'].string()
		except:
			lock_name = "name Unkown"
		bt = GDBHelper.getBacktrace()
		btstring = ""
		i=0
		while i < min(3,len(bt)):
			btstring += i*" "+bt[i]+"\n"
			i += 1
		self.function(tid,lid,thread_info=thread_name, lock_info=lock_name,call_location=btstring[:-1])


SwebMutextBP("Mutex::acquire",Interface.acquire)
SwebMutextBP("Mutex::release",Interface.release)


