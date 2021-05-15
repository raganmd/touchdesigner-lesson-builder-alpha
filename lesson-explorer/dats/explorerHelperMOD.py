#####################################################
# imports
#####################################################

import urllib.request
from bs4 import BeautifulSoup 
import requests

#####################################################
# module variables
#####################################################

ExplorerCOMP    = parent.Explorer
lister          = ExplorerCOMP.op('container_left/lister')
webBrowser  	= ExplorerCOMP.op('container_left/webBrowser')
view 		    = ExplorerCOMP.op('container_right/container_view')
loadingView     = ExplorerCOMP.op('container_right/container_loading')
settingsView    = ExplorerCOMP.op('container_right/container_settings')
transTimer      = ExplorerCOMP.op('container_right/container_loading/timer1')
linkManifest    = ExplorerCOMP.op('table_manifestBuffer')

#####################################################
# functions
#####################################################

def selectionHandler(info):
    currentRow      = info.get('row')

    if currentRow == -1:
        pass

    else:
        if info is None:
            pass

        else:
            lastRowSelected = ExplorerCOMP.fetch('lastRowSelected', 0)
            webPage 	    = info.get('rowData').get('rowObject').get('webPage')
            remoteTox 	    = info.get('rowData').get('rowObject').get('tox')
            col             = info.get('col')

            ExplorerCOMP.store('selectedWebPage', webPage)
            ExplorerCOMP.store('selectedRemoteTox', remoteTox)

            if col == 0:
                # same row clicked
                if lastRowSelected == currentRow:
                    pass

                else:
                    ExplorerCOMP.store('lastRowSelected', currentRow)
                    ExplorerCOMP.store('selectedWebPage', webPage)
                    ExplorerCOMP.store('selectedRemoteTox', remoteTox)
                    loadNewSelection()        

                pass

            # view URL in browser
            elif col == 1:
                ui.viewFile(webPage)

            # # toggle network COMPs
            # elif col == 2:
            #     networkView.par.display = (1 if not networkView.par.display.eval() else 0)

    pass

def loadLessonFromUrl():
    bufferContents = []
    print("Loading")
    lessonUrl = ExplorerCOMP.par.Lessonurl.eval()

    # GET request from url
    lessonContent = requests.get(lessonUrl).text

    bufferContents = htmlTableToRowsObject(lessonContent)

    buildManifestFromContents(bufferContents)

    ExplorerCOMP.store('lastRowSelected', -1)
    lister.par.Selectedrows = ''

def htmlTableToRowsObject(lessonContent):
    rowsObject = []

    # parse web content
    soup = BeautifulSoup(lessonContent, "html.parser")
    tableContents = soup.find("table")

    # get rows
    tableRows = tableContents.tbody.find_all('tr')

    for each in tableRows:
        if each.th:
            pass
        else:
            row = each.find_all('td')
            outputRow = []
            for eachCell in enumerate(row):
                if eachCell[0] == 0:
                    outputRow.append(eachCell[1].string)
                else:
                    outputRow.append(eachCell[1].find('a')['href'])
            rowsObject.append(outputRow)

    return rowsObject

def buildManifestFromContents(contents):
    # clear old contents
    bufferClear()

    # build manifest from new contents
    for each in contents:
        linkManifest.appendRow(each)

def bufferClear():
    linkManifest.clear(keepFirstRow=True)

def loadNewSelection():
    loadingView.par['display'] = True
    displayLoadingScreen()

def displayLoadingScreen():
    transTimer.par.start.pulse()

def updateBrowser():
    url = ExplorerCOMP.fetch('selectedWebPage')
    webBrowser.par['Address'] = url

def loadRemoteTox():
    remoteTox = ExplorerCOMP.fetch('selectedRemoteTox')

    try:

        asset 	= urllib.request.urlopen(remoteTox)
        tox 	= asset.read()
        loadedTox = view.loadByteArray(tox)
        loadedTox.par['display'] = True
        loadedTox.nodeX = 0
        loadedTox.nodeY = 0
        updateBrowser()

    except Exception as e:
        print(e)

def clearView():
    for each in view.findChildren(depth=1):
        each.destroy()

def setTimerPlay(playVal):
    transTimer.par['play'] = playVal
    print("called")

def toggleSettings():
    settingsView.par.display = (0 if settingsView.par.display else 1)

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

