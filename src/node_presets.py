from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN

#node naming convention: scope_data_name
class number_number_math():
    def __init__(self, scene):
        self.scene = scene
        self.title="Math"
        self.inputs = [S_NUMBER, S_NUMBER]
        self.outputs=[S_NUMBER]
        self.math_operation_choose = QComboBox()
        self.math_operation_choose.addItems(["Add", "Subtract", "Multiply", "Divide", "Greater Than",
                                             "Less Than", "Power", "Modulo", "A Percent of B", "B Percent of A"])
        self.math_value_a = QLineEdit()
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1_layout.addWidget(QLabel("Value"))
        self.line1_layout.addWidget(self.math_value_a)
        self.line1_layout.addWidget(QLabel("Value"))
        self.line1.setLayout(self.line1_layout)
        
        self.math_value_b = QLineEdit()
        self.math_value_b.setMaximumWidth(265)
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.line2_layout.addWidget(QLabel("Value"))
        self.line2_layout.addWidget(self.math_value_b)
        self.line2_layout.addSpacerItem(QSpacerItem(62, 2))
        self.line2.setLayout(self.line2_layout)
        
        self.contents = [self.math_operation_choose, self.line1, self.line2]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 240)