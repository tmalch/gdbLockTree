

class PluginBase():
	def __init__(self,location,name,interface):
		interface.register(name,self)
		self.location = location
		self.name = name
		self.interface = interface
	def BPlocation(self):
		return self.location
	def interfaceType(self):
		return self.interface.type
	def name(self):
		return self.name
	def handleStopEvent(self):	
		pass

