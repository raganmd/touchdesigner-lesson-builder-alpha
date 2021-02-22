# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

import sys
projectDep = f'{project.folder}/td-python-dep'

def checkDeps():
	if projectDep not in sys.path:
		sys.path.append(projectDep)	
		for each in sys.path:
			print(each)

	else:
		pass

def onStart():
	print()
	checkDeps()

def onCreate():
	return

def onExit():
	return

def onFrameStart(frame):
	return

def onFrameEnd(frame):
	return

def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
	return

def onProjectPostSave():
	return

	