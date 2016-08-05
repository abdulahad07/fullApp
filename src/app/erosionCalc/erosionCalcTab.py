import sys
from PyQt4 import QtGui, QtCore
from core.helper.uiHelper import *
import pandas as pd
from core.helper.tableHelper import pandasTableModel, filterTable
import copy
from itertools import product
Qt = QtCore.Qt
import signal

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.view = getViewForWidget(['..', 'ui', 'erosionCalcTab.ui'])
        self.df = self.load_from_excel(r'F:\abdulahad.momin\projects\erosionCalc\work\dev\erosionCalc\src\databases\Erosion_Database_of_Piping_System.xlsx')
        self.setUp()
        self.setConnectors()
        self.setRightClickOptions()
        self.hideRangeWidget()
        self.updateKeysWidget()

    def setUp(self):
        self.keyWidget = self.view.expKeysLW
        self.valWidget = self.view.expValsLW
        self.expRangeRB = self.view.expRangeRB
        self.expMinLE = self.view.expMinLE
        self.expMaxLE = self.view.expMaxLE
        self.filterCriteria = {}

    def setConnectors(self):
        self.keyWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.keyWidget.itemClicked.connect(self.updatevalWidget)
        self.valWidget.itemClicked.connect(self.updateResult)
        self.valWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.expRangeRB.toggled.connect(self.hideRangeWidget)
        self.expMinLE.textChanged.connect(self.updateResult)
        self.expMaxLE.textChanged.connect(self.updateResult)

    def hideRangeWidget(self):
        hidden = False if self.expRangeRB.isChecked() else True
        self.view.expRangeWidget.setHidden(hidden)
        if hidden == False:
            minimum, maximum = self.getMinMax()
            self.expMinLE.setText(str(minimum))
            self.expMaxLE.setText(str(maximum))
            self.updateDataFrame()

    def setRightClickOptions(self):
        actionRemoveFilters = QtGui.QAction('Remove Filters', self.keyWidget)
        self.keyWidget.addAction(actionRemoveFilters)
        actionRemoveFilters.triggered.connect(self.removeFilters)

    def removeFilters(self):
        key = str(self.keyItem.text())
        if self.filterCriteria.has_key(key):        # remove from filter dictionary
            self.filterCriteria.pop(key)
        for item in self.getSelectedItems():        # remove from GUI
            item.setSelected(False)
        self.updateDataFrame()

    def load_from_excel(self, fileName):
        return pd.read_excel(fileName)

    def getSelectedItems(self):
        return self.valWidget.selectedItems()

    def updateKeysWidget(self):
        items = self.df.keys()
        keyItems = [key for key in items if key not in ['Max Erosion Rate', 'Thickness Loss', 'Location Of Peak Erosion']]
        self.keyWidget.addItems(keyItems)

    def updatevalWidget(self, item):
        self.keyItem = item
        valueItems = [QtGui.QListWidgetItem(str(val)) for val in sorted(self.df[str(item.text())].unique()) if str(val) not in ['nan']]
        self.valWidget.clear()
        for item in valueItems:
            self.valWidget.addItem(item)
            filteredList = self.filterCriteria.get(str(self.keyItem.text()), [])    # set previously selected items
            if str(item.text()) in filteredList:
                self.valWidget.setItemSelected(item, True)

    def getFilterMap(self):
        '''returns all possible permutations
            inputDict = {'param1':[1], 'param2': [3, 4]}
            outputList = [{'param1': 1, 'param2':3}, {'param1': 1, 'param2':4}]
        '''
        result = [dict(zip(self.filterCriteria, v)) for v in product(*self.filterCriteria.values())]
        return result

    def updateDataFrame(self):
        newDataFrameList = []
        for filter in self.getFilterMap():
            newDataFrameList.append(filterTable(self.df, filter))
        df = pd.concat(newDataFrameList) if newDataFrameList else pd.DataFrame()
        self.updateTabel(df)

    def getMinMax(self):
        key = str(self.keyItem.text())
        return [min(self.df[key]), max(self.df[key])]

    def getMinMaxFromView(self):
        return [str(self.expMinLE.text()), str(self.expMaxLE.text())]

    def updateResult(self):
        key = str(self.keyItem.text())
        self.filterCriteria[key] = []
#        if self.expRangeRB.isChecked():
#            self.filterCriteria[key].append(self.getMinMaxFromView())
#        else:
        for selected in self.getSelectedItems():
            self.filterCriteria[key].append(str(selected.text()))
        self.updateDataFrame()

    def updateTabel(self, df):
        model = pandasTableModel(df)
        self.view.resultsTableView.setModel(model)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.view.show()
    sys.exit(app.exec_())
