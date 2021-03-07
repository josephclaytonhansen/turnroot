import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *

app = QApplication([])
screen = app.primaryScreen()
size = screen.size()
title = "Window"



class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)
    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.label.setText(str(e.pos().x())+ ", "+ str(e.pos().y()))
    
    def context_menu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("option 1", self))
        context.exec_(self.mapToGlobal(pos))

            




window = main()
window.show()
sys.exit(app.exec_())