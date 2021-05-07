import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)
        
        if role == Qt.BackgroundRole and index.row() % 2 == 0:
            value = self._data[index.row()][index.column()]
            return QtGui.QColor('white')
    
        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]
            return QtGui.QColor('black')
        
        elif role == Qt.BackgroundRole and index.row() % 2 != 0:
            value = self._data[index.row()][index.column()]
            return QtGui.QColor('#efefef')
            
    def setData(self, index, value, role):
        if role == Qt.EditRole and value != "" and value != None:
            self._data[index.row()][index.column()] = value
            return True
        else:
            return True

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
    
    def flags(self, index):
        if index.column() != 0:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
        else:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled