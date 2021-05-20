from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
def overlayTile(image, overlay, size):
    image = image.scaled(size,size, Qt.KeepAspectRatio)
    overlay = QPixmap(overlay)
    overlay = overlay.scaled(size,size, Qt.KeepAspectRatio)
    painter = QPainter()
    result = QPixmap(size, size)
    result.fill(Qt.transparent)
    painter.begin(result)
    painter.drawPixmap(0, 0, image)
    painter.drawPixmap(0, 0, overlay)
    painter.end()
    result = result.scaled(size, size, Qt.KeepAspectRatio)
    return result