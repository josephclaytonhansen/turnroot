from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN


class NumberMathLineEdit(QLineEdit):
    def __init__(self,place,parent=None):
        QObject.__init__(self) 
        self.v = 0
        self.parent = parent
        self.place = place
    def keyPressEvent(self,event):
        super().keyPressEvent(event)
        self.v = float(self.text())
        self.parent.values[self.place] = self.v

        if self.parent.current_operation == "Add":
            self.parent.values[2] = self.parent.values[0] + self.parent.values[1]
            
        print(self.parent.values)

#node naming convention: scope_data_name
class number_number_math():
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.title="Math"
        self.inputs = [S_NUMBER, S_NUMBER]
        self.outputs=[S_NUMBER]
        
        self.values = [0,0,0]
        self.current_operation = "Add"
        
        self.math_operation_choose = QComboBox()
        self.math_operation_choose.addItems(["Add", "Subtract", "Multiply", "Divide", "Greater Than",
                                             "Less Than", "Power", "Modulo", "A Percent of B", "B Percent of A",
                                             "Minimum", "Maximum", "Absolute Value A", "Round A", "Ceiling A", "Floor A"])
        
        self.math_value_a = NumberMathLineEdit(0,self)
        self.math_value_a.setValidator(QDoubleValidator(0.0, 10000.0, 100))
        self.math_value_a.setPlaceholderText("0")
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1_layout.addWidget(QLabel("Number"))
        self.line1_layout.addWidget(self.math_value_a)
        self.line1_layout.addWidget(QLabel("Number"))
        self.line1.setLayout(self.line1_layout)
        
        self.math_value_b = NumberMathLineEdit(1,self)
        self.math_value_b.setValidator(QDoubleValidator(0.0, 10000.0, 100))
        self.math_value_b.setMaximumWidth(220)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.line2_layout.addWidget(QLabel("Number"))
        self.line2_layout.addWidget(self.math_value_b)
        self.line2_layout.addSpacerItem(QSpacerItem(86, 2))
        self.line2.setLayout(self.line2_layout)
        
        self.contents = [self.math_operation_choose, self.line1, self.line2]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 220)
        self.n.node_preset = self
        self.n_a = self.n.inputs[0]
        self.n_b = self.n.inputs[1]
        self.n_out = self.n.outputs[0]
        