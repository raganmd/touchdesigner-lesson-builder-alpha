import urllib

lister      = parent.Explorer.op('container_left/lister')
webBrowser 	= parent.Explorer.op('container_left/webBrowser')
view 		= parent.Explorer.op('container_right/container_view')
loadingView = parent.Explorer.op('container_right/container_loading')
transTimer  = parent.Explorer.op('container_right/container_loading/timer1')

def selectionHandler(info):
    webPage 	= info.get('rowData').get('rowObject').get('webPage')
    remoteTox 	= info.get('rowData').get('rowObject').get('tox')
    
    parent.Explorer.store('selectedWebPage', webPage)
    parent.Explorer.store('selectedRemoteTox', remoteTox)

    loadNewSelection()

    pass


def loadNewSelection():
    loadingView.par['display'] = True
    displayLoadingScreen()

def displayLoadingScreen():
    transTimer.par.start.pulse()

def updateBrowser():
    url = parent.Explorer.fetch('selectedWebPage')
    webBrowser.par['Address'] = url

def loadRemoteTox():
    remoteTox = parent.Explorer.fetch('selectedRemoteTox')

    try:

        asset 	= urllib.request.urlopen(remoteTox)
        tox 	= asset.read()
        view.loadByteArray(tox)
        updateBrowser()

    except Exception as e:
        print(e)

def clearView():
    for each in view.findChildren(depth=1):
        each.destroy()

def setTimerPlay(playVal):
    transTimer.par['play'] = playVal
    print("called")

#####################################################
## Timer Functions
#####################################################

def timerSegmentEnter(**kwargs):
    timerOp = kwargs.get('timerOp')
    segment = kwargs.get('segment')
    interrupt = kwargs.get('interrupt')

    if segment > 0:
        timerOp.par.play = False
        clearView()
        run(loadRemoteTox(), delayFrames = 1)
        timerOp.par.play = True

def onTimerDone(**kwargs):
    loadingView.par['display'] = False
    pass

