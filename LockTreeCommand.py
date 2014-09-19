import sys
from os import listdir
import os

import gdb
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)
print(sys.path)
import gdbLockTree.LockInterface as LockInterface
import gdbLockTree.LockTree as LockTreeAlgo
import gdbLockTree.commands.DeadlockDetection as DeadlockDetection
import gdbLockTree.commands.PrintandStuff as PrintandStuff
import gdbLockTree.commands.TreeView as TreeView

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
	pluginlocation = basedir+"/gdbLockTree/plugins/"
	
	def registerPlugin(name,plugin):		
		""" gets called by each BreakPoint Plugin that gets  imported
				name: is the name of the plugin (eg qmutex). one plugin has normally more than one Breakpoint objects (eg one for acquire one for release)
				plugin: the Breakpoint object"""
		if plugin.interfaceType() != LockInterface.type:
			print("Don't know what to do with plugin "+name+" of type "+plugin.interfaceType())
			return
		if name not in LockTreeCommand.registery:
			print("register new plugin "+name)
			LockTreeCommand.registery[name] = [plugin,]
		else:
			LockTreeCommand.registery[name].append(plugin)

	def importPluginFiles(self):
		"""imports all .py files inside the plugin directory 
			prior importing it sets the methods the plugins will use for communication with the application"""
		LockInterface.acquire = LockTreeAlgo.acquire
		LockInterface.release = LockTreeAlgo.release
		LockInterface.register = LockTreeCommand.registerPlugin
		plugin_files = filter(lambda x: x.endswith('.py') and x != '__init__.py', os.listdir(LockTreeCommand.pluginlocation))
		for file in plugin_files:
			__import__("gdbLockTree.plugins."+file[:-3])			
			print("import pluginFile "+file)
			
	def __init__ (self):
		super (LockTreeCommand, self).__init__ ("locktree", gdb.COMMAND_USER)
		self.dont_repeat()
		self.breakpoints = []
		self.subCommands = {		"plugins":self.printPlugins,
									"monitore":self.createBreakpoints,# create Breakpoints for all stated lockDescriptions given in a space seperated list
									"stop":self.deleteBreakpoints,# delete all Breakpoints set by LockTree
									"check":self.check, # Run the Deadlock Detection
									"printthreads":self.printThreads,# print the current list of ThreadIDs that have acquired a lock
									"printtree":self.printTree,# print the current locktree for the given ThreadID
									"printdot":self.printTreeGui,
													 }
		self.importPluginFiles()
	def invoke (self, arg, from_tty):
		try:
			argv = gdb.string_to_argv(arg)
			command = argv[0].lower()
			self.subCommands[command](argv)
		except Exception as e:
			print("ERROR "+format(e))
			for command in self.subCommands.keys():
				print(command)

		
	def printPlugins(self,argv):
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
		LockTreeAlgo.forrest.executeCommand(DeadlockDetection.check)
		
	def printThreads(self,argv):
		threads = LockTreeAlgo.forrest.executeCommand(PrintandStuff.printThreads)
		", ".join(threads)

	def printTree(self,argv):
		""" print the current locktree for the given ThreadID"""
		for arg in argv[1:]:
			thread = LockTreeAlgo.Thread(int(arg))
			LockTreeAlgo.forrest.executeCommand(PrintandStuff.printTree,(thread))
	
	def printTreeGui(self,argv):
		""" print the current locktree for all given ThreadIDs with graphviz"""
		for arg in argv[1:]:
			thread = LockTreeAlgo.Thread(int(arg))
			LockTreeAlgo.forrest.executeCommand(TreeView.generateDotCode,kwargs={"thread":thread})


LockTreeCommand()



#list of all threads existing at the moment
#gdb.inferiors()[0].threads()
