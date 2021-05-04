from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN
import math

GLOBAL_VARIABLES = {}

class CreateVariableLineEdit(QLineEdit):
    def __init__(self,parent=None):
        QObject.__init__(self)
        self.parent = parent
        
    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        self.parent.storage.name = self.text()
                
        self.parent.updateEmission()

        self.update()
        
    def keyPressEvent(self,event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            GLOBAL_VARIABLES[self.text()] = VariableStorage(name=self.text(), value = self.parent.storage.value, data_type = None)
            self.parent.storage = GLOBAL_VARIABLES[self.text()]
            self.parent.update_r = True
            self.parent.updateReception()
        else:
            self.parent.update_r = False

class VariableStorage():
    def __init__(self, name, data_type, value):
        self.name = name
        self._data_type = data_type
        self._value = value

        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, a):
        self._value = a
        self._data_type = type(a)
    
    @property
    def data_type(self):
        return self._data_type

    @value.setter
    def data_type(self, t):
        self._data_type = t
         
class create_variable(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Access Variable"
        self.inputs = [S_NUMBER]
        self.outputs=[S_OBJECT, S_NUMBER]
        
        self.update_r = False
        
        GLOBAL_VARIABLES[""] = VariableStorage(name="", value = 0, data_type = None)
        self.storage = GLOBAL_VARIABLES[""]
        self.variable = CreateVariableLineEdit(self)
        self.variable_label = QLabel("Value")
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1_layout.addWidget(self.variable_label)
        self.line1_layout.addWidget(self.variable)
        self.line1.setLayout(self.line1_layout)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.line2_layout.addSpacerItem(QSpacerItem(330, 2))
        self.line2_layout.addWidget(QLabel("Value"))
        self.line2.setLayout(self.line2_layout)
        
        self.line_label =QLabel("Variable")
        self.line_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.contents = [self.line_label, self.line1, self.line2]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 200)
        self.n.node_preset = self
        
    def updateEmission(self):
        self.n.outputs[0].emission = self.n.node_preset.storage
        self.n.outputs[1].emission = self.n.node_preset.storage.value
        
    def updateReception(self):
        if self.update_r:
            try:
                self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            except:
                self.n.inputs[0].reception = None
            self.storage.value = self.n.inputs[0].reception
            self.update_r = False

            

class NumberMathLineEdit(QDoubleSpinBox):
    def __init__(self,place,socket,parent=None):
        QObject.__init__(self)
        self.parent = parent
        self.place = place
        self.socket = socket
        
    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        self.parent.values[self.place] = self.value()
                
        self.parent.updateEmission()
        self.parent.updateReception()

        self.update()

class number_number_math(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Math"
        self.inputs = [S_NUMBER, S_NUMBER]
        self.outputs=[S_NUMBER]
        
        self.values = [0,0,0]
        self.current_operation = "Add"
        
        self.math_operation_choose = QComboBox()
        self.math_operation_choose.addItems(["Add", "Subtract", "Multiply", "Divide", "Power",
                                             "Modulo", "A Percent of B",
                                             "Minimum", "Maximum", "Absolute Value A",
                                             "Round A", "Ceiling A", "Floor A", "Sqrt A"])
        self.math_operation_choose.currentTextChanged.connect(self.change_op)
        
        self.math_value_a = NumberMathLineEdit(0,0,self)
        self.math_value_a.setRange(-10000.00000, 100000.00000)
        self.math_value_a.setDecimals(3)
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1_layout.addWidget(QLabel("Number"))
        self.line1_layout.addWidget(self.math_value_a)
        self.line1_layout.addWidget(QLabel("Number"))
        self.line1.setLayout(self.line1_layout)
        
        self.math_value_b = NumberMathLineEdit(1,1,self)
        self.math_value_b.setRange(-10000.00000, 100000.00000)
        self.math_value_b.setDecimals(3)
        self.math_value_b.setMaximumWidth(220)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.line2_layout.addWidget(QLabel("Number"))
        self.line2_layout.addWidget(self.math_value_b)
        self.line2_layout.addSpacerItem(QSpacerItem(132, 2))
        self.line2.setLayout(self.line2_layout)
        
        self.contents = [self.math_operation_choose, self.line1, self.line2]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 220)
        self.n.node_preset = self
        self.n_a = self.n.inputs[0]
        self.n_b = self.n.inputs[1]
        self.n_out = self.n.outputs[0]
    
    def updateEmission(self):
        self.n.outputs[0].emission = self.n.inputs[0].node.node_preset.values[2]
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.values[0] = self.n.inputs[0].reception
            self.math_value_a.setValue(self.n.inputs[0].reception)
        except:
            self.values[0] = float(self.math_value_a.value())
        try:
            self.n.inputs[1].reception = self.n.inputs[1].edges[0].start_socket.emission
            self.values[1] = self.n.inputs[1].reception
            self.math_value_b.setValue(self.n.inputs[1].reception)
        except:
            self.values[1] = float(self.math_value_b.value())
            
        if self.current_operation == "Add":
            self.values[2] = self.values[0] + self.values[1]
        
        elif self.current_operation == "Subtract":
            self.values[2] = self.values[0] - self.values[1]
        
        elif self.current_operation == "Multiply":
            self.values[2] = self.values[0] * self.values[1]
            
        elif self.current_operation == "Divide":
            try:
                self.values[2] = self.values[0] / self.values[1]
            except:
                pass
        
        elif self.current_operation == "Power":
            self.values[2] = self.values[0] ** self.values[1]
            
        elif self.current_operation == "Modulo":
            try:
                self.values[2] = int(self.values[0]) % int(self.values[1])
            except:
                pass
            
        elif self.current_operation == "A Percent of B":
            self.values[2] = self.values[0]/100 * self.values[1]
        
        elif self.current_operation == "Maximum":
            if self.values[0] >= self.values[1]:
                self.values[2] = self.values[0]
            else:
                self.values[2] = self.values[1]
        
        elif self.current_operation == "Minimum":
            if self.values[0] <= self.values[1]:
                self.values[2] = self.values[0]
            else:
                self.values[2] = self.values[1]
        
        elif self.current_operation == "Absolute Value A":
            self.values[2] = abs(self.values[0])
        
        elif self.current_operation == "Round A":
            self.values[2] = round(self.values[0])
        
        elif self.current_operation == "Floor A":
            self.values[2] = math.floor(self.values[0])
        
        elif self.current_operation == "Celing A":
            self.values[2] = math.ceil(self.values[0])
        
        elif self.current_operation == "Sqrt A":
            self.values[2] = math.sqrt(self.values[0])
        
        self.updateEmission()
    
    def change_op(self,s):
        self.current_operation = s




        