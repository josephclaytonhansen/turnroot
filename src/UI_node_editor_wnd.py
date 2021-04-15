from PyQt5.QtWidgets import *
class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.view = QGraphicsView(self)
        self.layout.addWidget(self.view)
        
        self.show()
        