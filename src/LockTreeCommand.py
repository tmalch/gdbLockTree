import gdb
import sys
sys.path.append('/home/cloud/projects/AKBS/gdbPythonLocktree/src')
print(sys.path)

import LockTreeAlgo
import LockInterface
from os import listdir

class MyBreakpoint(gdb.Breakpoint):
	def __init__ (self,plugin):
		super(MyBreakpoint,self).__init__ (plugin.BPlocation(),type=gdb.BP_BREAKPOINT,internal=True)
		self.plugin = plugin
	def stop (self):
		self.plugin.handleStopEvent()
		return False #don't stop


class LockTreeCommand(gdb.Command):
	"""Greet the whole world."""
	registery = {}
	
	def registerPlugin(name,plugin):		
		print("register new plugin "+name)
		if name not in LockTreeCommand.registery:
			LockTreeCommand.registery[name] = [plugin,]
		else:
			LockTreeCommand.registery[name].append(plugin)
			
	def __init__ (self):
		super (LockTreeCommand, self).__init__ ("locktree", gdb.COMMAND_USER)
		self.dont_repeat()
		self.breakpoints = []
		self.subCommands = {"addlockplugin":self.registerLockPlugin, #register a new lockDescription plugin
												"locktypes":self.printLockType,
												"monitore":self.createBreakpoints,# create Breakpoints for all stated lockDescriptions given in a space seperated list
												"stop":self.deleteBreakpoints,# delete all Breakpoints set by LockTree
												"check":self.check, # Run the Deadlock Detection
												"printthreads":self.printThreads,# print the current list of ThreadIDs that have acquired a lock
												"printtree":self.printTree,# print the current locktree for the given ThreadID
													 }
		self.importPluginFiles()
	def invoke (self, arg, from_tty):
		try:
			argv = gdb.string_to_argv(arg)
			command = argv[0].lower()
			self.subCommands[command](argv)
		except Exception as e:
			print("ERROR "+str(e))
			for command in self.subCommands.keys():
				print(command)
	def importPluginFiles(self):
		LockInterface.acquire = LockTreeAlgo.acquire
		LockInterface.release = LockTreeAlgo.release
		LockInterface.register = LockTreeCommand.registerPlugin
		for file in listdir("/home/cloud/projects/AKBS/gdbPythonLocktree/src/plugins"):
			if not file.startswith("__") and file.endswith(".py"):
				__import__("plugins."+file[:-3])
				print("import pluginFile "+file)

	def registerLockPlugin(self,argv):
		""" add a plugin from another place than the plugins directory"""
		pass
		
	def printLockType(self,argv):
		for ltype in LockTreeCommand.registery.keys():
			print(ltype)
	def createBreakpoints(self,argv):
		for locktype in argv[1:]:
			if locktype in LockTreeCommand.registery:
				lockpluginlist = LockTreeCommand.registery[locktype]
				try:
					for lockplugin in lockpluginlist:
						print("create locktree monitor at "+lockplugin.location)
						self.breakpoints.append(MyBreakpoint(lockplugin))
				except TypeError as e:
					print(e)
					print("ERROR: Lock "+locktype+" doesn't has any plugins - cannot be monitored")
			else:
				print("ERROR: Lock "+locktype+" is not available - cannot be monitored")
	
	def deleteBreakpoints(self,argv):
		for br in self.breakpoints:
			br.delete()
		self.breakpoints = []
	def check(self,argv):
		"""Run the Deadlock Detection"""
		LockTreeAlgo.forrest.check()
	def printThreads(self,argv):
		"""print the current list of ThreadIDs that have acquired a lock"""
		res=""
		for x in LockTreeAlgo.forrest.getThreadList():
			res+=str(x)+" "
		print(res)
	def printTree(self,argv):
		""" print the current locktree for the given ThreadID"""
		if len(argv) > 1:
			LockTreeAlgo.forrest.printTree(int(argv[1]))
			

LockTreeCommand()



#list of all threads existing at the moment
#gdb.inferiors()[0].threads()
