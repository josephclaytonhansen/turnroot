import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.slider_value1 = 0
        self.slider_value2 = 0
        self.slider_value3 = 0
        
        self.column_colors = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)
        
        if role == Qt.BackgroundRole and index.column() == 0:
            return QtGui.QColor(self.column_colors[0])
        
        if role == Qt.BackgroundRole and index.row() % 2 == 0 and index.column() != 0:
            value = self._data[index.row()][index.column()]
            self.slider_value4 = 100 - self.slider_value1
            self.slider_value5 = 100 - self.slider_value2
            self.slider_value6 = 100 - self.slider_value3
            if value.startswith("SOLDIER"):
                return QtGui.QColor(self.colorizeCell(self.slider_value1))
            elif value.startswith("LONE WOLF"):
                return QtGui.QColor(self.colorizeCell(self.slider_value4))
            elif value.startswith("STRATEGIC"):
                return QtGui.QColor(self.colorizeCell(self.slider_value2))
            elif value.startswith("MINDLESS"):
                return QtGui.QColor(self.colorizeCell(self.slider_value5))
            elif value.startswith("COWARDLY"):
                return QtGui.QColor(self.colorizeCell(self.slider_value3))
            elif value.startswith("BRASH"):
                return QtGui.QColor(self.colorizeCell(self.slider_value6))
            elif value.startswith("ALWAYS!"):
                return QtGui.QColor("black")
            else:
                return QtGui.QColor("white")
        
        elif role == Qt.BackgroundRole and index.row() % 2 != 0 and index.column() != 0:
            value = self._data[index.row()][index.column()]
            if value.startswith("SOLDIER"):
                return QtGui.QColor(self.colorizeCell(self.slider_value1))
            elif value.startswith("LONE"):
                return QtGui.QColor(self.colorizeCell(self.slider_value4))
            elif value.startswith("STRATEGIC"):
                return QtGui.QColor(self.colorizeCell(self.slider_value2))
            elif value.startswith("MINDLESS"):
                return QtGui.QColor(self.colorizeCell(self.slider_value5))
            elif value.startswith("COWARDLY"):
                return QtGui.QColor(self.colorizeCell(self.slider_value3))
            elif value.startswith("BRASH"):
                return QtGui.QColor(self.colorizeCell(self.slider_value6))
            elif value.startswith("ALWAYS!"):
                return QtGui.QColor("black")
            else:
                return QtGui.QColor("#efefef")

        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]
            if value.startswith("ALWAYS!") == False and index.column() != 0:
                return QtGui.QColor('black')
            elif self.column_colors[1] == "black" and index.column() == 0:
                return QtGui.QColor('black')
            elif self.column_colors[1] == "white" and index.column() == 0:
                return QtGui.QColor('white')
            else:
                return QtGui.QColor('white')
            
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
        
    def colorizeCell(self, v):
        v = v / 100
        color_left = QColor(active_theme.node_outliner_label_0)
        color_right = QColor(active_theme.node_outliner_label_1)
        color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
        color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
        distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
        
        new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
        
        return(QColor(new_color[0],new_color[1],new_color[2]).name())