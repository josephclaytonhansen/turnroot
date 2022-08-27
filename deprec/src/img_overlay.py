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

def overlayTileWithoutScaling(image, overlay, size, size2, pos,transform=None):
    image = QPixmap(image)
    overlay = QPixmap(overlay)
    painter = QPainter()
    result = QPixmap(size, size2)
    result.fill(Qt.transparent)
    painter.begin(result)
    painter.drawPixmap(0, 0, image)
    painter.drawPixmap(pos[0], pos[1], overlay)
    painter.end()
    return result

def createClippingMask(image, overlay, c, size, size2):
    background = image
    color = QPixmap(size,size2)
    color.fill(QColor(c))
    mask = overlay  

    painter = QPainter(color)
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, mask.width(), mask.height(), mask)
    painter.end()

    new_painter = QPainter(background)
    new_painter.drawPixmap(0, 0, size, size2, color)
    new_painter.end()
    return background
    