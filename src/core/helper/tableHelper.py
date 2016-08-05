from PyQt4 import QtCore
Qt = QtCore.Qt
import copy

class pandasTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

#def filterTable(dataFrame, filters):
#    df = copy.deepcopy(dataFrame)
#    for key, value in filters.iteritems():
#        if df.empty:
#            return df
#        for val in value:
#            if isfloat(val) == True:
#                val = float(val)
#            df = df.loc[(df[key] == val)]
#    return df

def filterTable(df, filterCriteria):
#    df = copy.deepcopy(dataFrame)
    for key, val in filterCriteria.iteritems():
        if df.empty:
            return df
        if isinstance(val, list):
            if isfloat(val[0]) == True and isfloat(val[1]) == True:
                val = [float(val[0]), float(val[1])]
                print 'haa'
            df = df.loc[(df[key] >= val[0]) & (df[key] <= val[1])]
        else:
            if isfloat(val) == True:
                val = float(val)
            df = df.loc[(df[key] == val)]
    return df
