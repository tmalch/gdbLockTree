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
import gdbLockTree.Utils as Utils

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
			
	def exit_handler(self, event):
		print("recorded Locktrees will be deleted on restart")
		self.exited = True
	def cont_handler(self, event):
		if self.exited:
			LockTreeAlgo.forrest = LockTreeAlgo.LockForrest()
			self.exited = False

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
		super (LockTreeCommand, self).__init__ ("locktree", gdb.COMMAND_USER,prefix=False)
		self.dont_repeat()
		self.breakpoints = []
		self.subCommands = {		"plugins":self.printPlugins,
									"monitore":self.createBreakpoints,# create Breakpoints for all stated lockDescriptions given in a space seperated list
									"stop":self.deleteBreakpoints,# delete all Breakpoints set by LockTree
									"check":self.check, # Run the Deadlock Detection
									"printthreads":self.printThreads,# print the current list of ThreadIDs that have acquired a lock
									"printtree":self.printTree,# print the current locktree for the given ThreadID
									"printgui":self.printTreeGui,
									"useless":self.useless,
									"holdlocks":self.printHoldLocks,
									"lockinfo":self.printLockInfo
													 }
		self.importPluginFiles()
		#necessary to detect a restart of the inferior -- we have to reset the Locktree on restart
		self.exited = False
		gdb.events.exited.connect(self.exit_handler)
		gdb.events.cont.connect(self.cont_handler)
		
	def complete(self,text, word):
		argv = text.split(" ")
		if word == argv[0]:
			return Utils.completeFromList(word, self.subCommands.keys())
		else:
			subcommand = argv[0]
			if subcommand in ["printtree","printgui","holdlocks"]:
				threadids,_ = LockTreeAlgo.forrest.executeCommandonForrest(PrintandStuff.printThreads)
				completion = Utils.completeFromList(word, threadids)
				if completion == [] and word == "":
					completion.append("\"No Thread available\"")
				return completion
			elif subcommand == "monitore":
				completion = Utils.completeFromList(word, LockTreeCommand.registery.keys())
				return completion				
	
	def invoke (self, arg, from_tty):
		try:
			argv = gdb.string_to_argv(arg)
			command = argv[0].lower()
			self.subCommands[command](argv)
		except Exception as e:
			print("ERROR "+str(e))
			for command in self.subCommands.keys():
				print(command)

	def printPlugins(self,argv):
		if len(LockTreeCommand.registery) == 0:
			print("\"No Plugins available\"")
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
		deadlocks = LockTreeAlgo.forrest.executeCommandonForrest(DeadlockDetection.check)
		if not deadlocks:
			print("no possible Deadlocks found")
		for d in deadlocks:
			print(str(d))
	def useless(self,argv):
		useless_locks = LockTreeAlgo.forrest.executeCommandonForrest(PrintandStuff.uselessLocks)
		if not useless_locks:
			print("No useless Locks found")
		else:
			print("These locks seem to get called only by one thread")
			for l,t in useless_locks:
				print(Utils.nicestr(l)+" called only from Thread "+Utils.nicestr(t))
	def printThreads(self,argv):
		(threadids,threadinfos) = LockTreeAlgo.forrest.executeCommandonForrest(PrintandStuff.printThreads)
		if not threadids:
			print("No Threads recorded")
		else:
			res = ""
			for tid,info in zip(threadids,threadinfos):
				res += tid
				if info != "":
					res += " :: "+info
				res += "\n"
			print(res[:-1])

	def printTree(self,argv):
		""" print the current locktree for the given ThreadID"""
		if not argv[1:]:
			print("Usage: printtree <threadid>")
		for arg in argv[1:]:
			thread = Utils.Thread(int(arg,base=16))
			res = LockTreeAlgo.forrest.executeCommandonTree(PrintandStuff.printTree,thread)
			if res is not None:
				print(res)
	def printHoldLocks(self,argv):
		if not argv[1:]:
			print("Usage: holdlocks <threadid>")
		for arg in argv[1:]:
			thread = Utils.Thread(int(arg,base=16))
			res = LockTreeAlgo.forrest.executeCommandonTree(PrintandStuff.printHoldLocks,thread)
			if res is not None:
				print(" \n ".join(res))
	
	def printLockInfo(self,argv):
		if not argv[1:]:
			print("Usage: lockinfo <lockid>")
		for arg in argv[1:]:
			lock = Utils.Lock(int(arg,base=16),None)
			res = LockTreeAlgo.forrest.executeCommandonForrest(PrintandStuff.printLockInfo,(lock,))
			if res is None:
				print("Lock not found")
			else:
				print(res)
		
	def printTreeGui(self,argv):
		""" print the current locktree for all given ThreadIDs with graphviz"""
		if not argv[1:]:
			print("Usage: printgui <threadid>")
		for arg in argv[1:]:
			thread = Utils.Thread(int(arg,base=16))
			LockTreeAlgo.forrest.executeCommandonTree(TreeView.generateDotCode,thread)

LockTreeCommand()
