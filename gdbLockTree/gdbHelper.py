import gdb



## HELPER METHODS ## to be used for implementing  	
def getGDBThreadID():
	#return gdb.selected_thread().ptid[1]
	return gdb.selected_thread().num

def getVariableValue(name):
	frame = gdb.newest_frame()
	if not frame.is_valid():
		print("frame not valid")
		return
	try:
		frame = gdb.newest_frame()
		value = frame.read_var(name)
		return value
	except Exception as e:
		print(e)

def getVariableNameForPointer(variable_ptr):
	"""returns the name of the Variable the pointer variable_ptr points to """
	if variable_ptr.type.code != gdb.TYPE_CODE_PTR:
		return
	ptr = hex(int(variable_ptr))
	varname = gdb.execute("info symbol "+ptr,False,True)
	if varname[:len("No symbol matches")] != "No symbol matches":
		varname = varname.split(" ")
		if len(varname) > 0:
			return varname[0]
	return "Unknown"

def getDefinitionLocationOfVariable(name):
	r = gdb.lookup_symbol(name)
	sym = r[0]
	if sym != None:
		return str(sym.symtab.filename)+":"+str(sym.line)
	return "Unknown location"
		
def getCallingFunctionName(frame = None):
		if frame == None:
			frame = gdb.newest_frame()
		frame = frame.older()
		return getFunctionName(frame)
		
def getFunctionName(frame = None):
	try:
		if frame == None:
			frame = gdb.newest_frame()
		name = ""
		if frame.function() != None:
			return str(frame.function().print_name)
		else:
			return str(frame.name())
	except Exception as e:
		print(e)
		return "Unkown"	
		
def getCallingLocation(frame = None):
	if frame == None:
		frame = gdb.newest_frame()
	frame = frame.older()
	return getLocation(frame)

def getLocation(frame = None):
	try:
		if frame == None:
			frame = gdb.newest_frame()
		try:
			filename = str(frame.find_sal().symtab.filename)
			if len(filename) > 23:
				filename = "..."+filename[-20:]
		except:
			filename = ""
		try:
			loc = str(frame.find_sal().line)
		except:
			loc = ""		
		return filename+":"+loc
	except Exception as e:
		print(e)
		return "xx"

def getBacktrace():
	frame = gdb.newest_frame()
	res = list()
	while frame != None and frame.unwind_stop_reason() == gdb.FRAME_UNWIND_NO_REASON:
		frame = frame.older()
		if frame == None or not frame.is_valid():
			break
		callingName = getFunctionName(frame)
		callingLoc = getLocation(frame)
		res.append(callingName+" at "+callingLoc)

	return res






