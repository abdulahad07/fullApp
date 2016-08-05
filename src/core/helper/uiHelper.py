from PyQt4 import uic
import os

def safeLoadUiType(filename):
    '''
    Load the ui file after taking care of full path information
    (Frozen/normal one)
    
    filename : Its a filename or list of full file path components
            e.g. ["interface, "uiReportRegion.ui"]. This is to avoid
            platform specific separators which we can create here
    '''
    if isinstance(filename, list):
        filename = os.path.join(*filename)

    fullPath = filename
    return uic.loadUiType(fullPath)

def getViewForWidget(uiFilePath):

    Base, Form = safeLoadUiType(uiFilePath)
    class basicViewWidget(Base, Form):
        def __init__(self, parent=None):
            super(basicViewWidget, self).__init__(parent)
            self.setupUi(self)

    return basicViewWidget()
