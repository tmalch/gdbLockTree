

class PluginBase():
	def __init__(self,location,name,interface):
		self.location = location
		self.name = name
		self.interface = interface
		self.interface.register(name,self)
	def BPlocation(self):
		return self.location
	def interfaceType(self):
		return self.interface.type
	def name(self):
		return self.name
	def handleStopEvent(self):	
		pass

