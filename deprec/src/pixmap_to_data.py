from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class StoreQPixmap:

    def __init__(self):
        self._qpixmap = {}

    def to_data(self):
        # QPixmap is not pickable so let's transform it into QByteArray that does support pickle
        state = []
        for key, value in self._qpixmap.items():
            qbyte_array = QByteArray()
            stream = QDataStream(qbyte_array, QIODevice.WriteOnly)
            stream << value
            state.append((key, qbyte_array))
        return state

    def from_data(self, state):
        self._qpixmap = {}
        # retrieve a QByteArray and transform it into QPixmap
        for (key, buffer) in state:
            qpixmap = QPixmap()
            stream = QDataStream(buffer, QIODevice.ReadOnly)
            stream >> qpixmap
            self._qpixmap[key] = qpixmap
