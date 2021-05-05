from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
import math, random

GLOBAL_VARIABLES = {}

class TestObject():
    def __init__(self):
        self.stat = int(random.random() * 100)
        
class GetAttrLineEdit(QLineEdit):
    def __init__(self,parent=None):
        QObject.__init__(self)
        self.parent = parent

    def keyPressEvent(self,event):
        super().keyPressEvent(event)
        self.parent.attribute = self.text()
        self.parent.updateEmission()

class get_attr_from_object(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Get Attribute of Object"
        self.inputs = [S_OBJECT]
        self.outputs=[S_NUMBER]
        
        self.attribute = ""
        self.object = None
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.label1 = QLabel("Object")
        self.label1.setAlignment(Qt.AlignLeft)
        self.label2 = QLabel("Value")
        self.label2.setAlignment(Qt.AlignRight)
        self.attr_name = GetAttrLineEdit(self)
        self.line1_layout.addWidget(self.label1)
        self.line1_layout.addWidget(self.attr_name)
        self.line1_layout.addWidget(self.label2)
        self.line1.setLayout(self.line1_layout)
        
        self.socket_content_index = 0
        
        self.contents = [self.line1]
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
        self.n.node_preset = self
        
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = getattr(self.object, self.attribute)
        except:
            pass
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.object = self.n.inputs[0].reception
        except:
            self.n.inputs[0].reception = None

class list_tester(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="List Tester"
        self.inputs = []
        self.outputs=[S_LIST]
        
        self.output_list = [TestObject(), TestObject(), TestObject()]
        print(self.output_list)
        print(self.output_list[0].stat, self.output_list[1].stat, self.output_list[2].stat)
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.label1 = QLabel("List")
        self.label1.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(self.label1)
        self.line1.setLayout(self.line1_layout)
        
        self.socket_content_index = 0
        
        self.contents = [self.line1]
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
        self.n.node_preset = self
        
    def updateEmission(self):
        self.n.outputs[0].emission = self.output_list
    def updateReception(self):
        pass

class each(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Each (List to Object)"
        self.inputs = [S_LIST]
        self.outputs=[S_OBJECT, S_NUMBER, S_TRIGGER]
        
        self.list_length = 0
        self.current_index = 0
        self.l = 0
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.label1 = QLabel("List")
        self.label1.setAlignment(Qt.AlignLeft)
        self.label2 = QLabel("Object")
        self.label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(self.label1)
        self.line1_layout.addWidget(self.label2)
        self.line1.setLayout(self.line1_layout)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.label4 = QLabel("List Length")
        self.label4.setAlignment(Qt.AlignRight)
        self.line2_layout.addWidget(self.label4)
        self.line2.setLayout(self.line2_layout)
        
        self.line3 = QWidget()
        self.line3_layout = QHBoxLayout()
        self.line3_layout.setSpacing(8)
        self.line3_layout.setContentsMargins(0,0,0,0)
        self.button = QPushButton("Step")
        self.button.clicked.connect(self.Execute)
        self.label5 = QLabel("Index")
        self.label5.setAlignment(Qt.AlignRight)
        self.line3_layout.addWidget(self.button)
        self.line3_layout.addWidget(self.label5)
        self.line3.setLayout(self.line3_layout)
        
        self.socket_content_index = 0
        
        self.contents = [self.line1, self.line2, self.line3]
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
        self.n.node_preset = self
        self.n.outputs[2].emission = None
        
    def updateEmission(self):
        self.n.outputs[1].emission  = self.list_length

    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.list_length  = len(self.n.inputs[0].reception)
                
        except:
            self.n.inputs[0].reception = self.n.inputs[0].reception
     
    def Execute(self):
        self.l += 1
        if self.l == 3:
            self.l = 0
        self.n.outputs[0].emission = self.n.inputs[0].reception[self.l]
        self.n.outputs[2].emission = self.l

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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
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

class conditional_with_trigger(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Condition (from Numbers)"
        self.inputs = [S_NUMBER, S_NUMBER]
        self.outputs=[S_BOOLEAN, S_TRIGGER]
        
        self.result = False
        self.trigger = False
        self.values = [0,0,0]
        
        self.current_operation = "Equal"
        
        self.math_operation_choose = QComboBox()
        self.math_operation_choose.addItems(["Equal", "Not Equal", "Greater Than", "Less Than", "Greater Than or Equal",
                                             "Less Than or Equal"])
        
        self.math_operation_choose.currentTextChanged.connect(self.change_op)
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.label1 = QLabel("Number")
        self.label1.setAlignment(Qt.AlignLeft)
        self.label2 = QLabel("Boolean")
        self.label2.setAlignment(Qt.AlignRight)
        self.number1 = NumberMathLineEdit(0,0,self)
        self.line1_layout.addWidget(self.label1)
        self.line1_layout.addWidget(self.number1)
        self.line1_layout.addWidget(self.label2)
        self.line1.setLayout(self.line1_layout)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.label3 = QLabel("Number")
        self.label3.setAlignment(Qt.AlignLeft)
        self.label4 = QLabel("Trigger")
        self.label4.setAlignment(Qt.AlignRight)
        self.number2 = NumberMathLineEdit(1,1,self)
        self.line2_layout.addWidget(self.label3)
        self.line2_layout.addWidget(self.number2)
        self.line2_layout.addWidget(self.label4)
        self.line2.setLayout(self.line2_layout)
        
        self.contents = [self.math_operation_choose, self.line1, self.line2]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
        self.n.node_preset = self
        self.n_a = self.n.inputs[0]
        self.n_b = self.n.inputs[1]
        self.n_out = self.n.outputs[0]
    
    def updateEmission(self):
        self.n.outputs[0].emission = self.n.inputs[0].node.node_preset.values[2]
        self.n.outputs[1].emission = self.n.inputs[0].node.node_preset.values[2]
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.values[0] = self.n.inputs[0].reception
            self.number1.setValue(self.n.inputs[0].reception)
        except:
            self.values[0] = float(self.number1.value())
        try:
            self.n.inputs[1].reception = self.n.inputs[1].edges[0].start_socket.emission
            self.values[1] = self.n.inputs[1].reception
            self.number2.setValue(self.n.inputs[1].reception)
        except:
            self.values[1] = float(self.number2.value())
            
        if self.current_operation == "Equal":
            self.values[2] = self.values[0] == self.values[1]
        
        elif self.current_operation == "Not Equal":
            self.values[2] = self.values[0] != self.values[1]
        
        elif self.current_operation == "Less Than":
            self.values[2] = self.values[0] < self.values[1]
        
        elif self.current_operation == "Greater Than":
            self.values[2] = self.values[0] > self.values[1]
        
        elif self.current_operation == "Greater Than or Equal":
            self.values[2] = self.values[0] >= self.values[1]
            
        elif self.current_operation == "Less Than or Equal":
            self.values[2] = self.values[0] <= self.values[1]
            
        self.updateEmission()
        
    def change_op(self,s):
        self.current_operation = s
    
class set_attr_for_object(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Set Attribute of Object"
        self.inputs = [S_OBJECT, S_NUMBER]
        self.outputs=[]
        
        self.attribute = ""
        self.object = None
        self.new_value = 0
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.label1 = QLabel("Object")
        self.label1.setAlignment(Qt.AlignLeft)
        self.attr_name = GetAttrLineEdit(self)
        self.line1_layout.addWidget(self.label1)
        self.line1_layout.addWidget(self.attr_name)
        self.line1.setLayout(self.line1_layout)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.label2 = QLabel("Value")
        self.label2.setAlignment(Qt.AlignLeft)

        self.line2_layout.addWidget(self.label2)
        self.line2.setLayout(self.line2_layout)
        
        
        self.line3 = QWidget()
        self.line3_layout = QHBoxLayout()
        self.line3_layout.setSpacing(8)
        self.line3_layout.setContentsMargins(0,0,0,0)
        self.button = QPushButton("Set")
        self.button.clicked.connect(self.Execute)
        self.line3_layout.addWidget(self.button)
        self.line3.setLayout(self.line3_layout)
        
        self.socket_content_index = 0
        
        self.contents = [self.line1, self.line2, self.line3]
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
        self.n.node_preset = self
        
    def Execute(self):
        self.updateReception()
        setattr(self.object, self.attribute, self.new_value)
        print(self.object, self.object.stat)
        
    def updateEmission(self):
        pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.n.inputs[1].reception = self.n.inputs[1].edges[0].start_socket.emission
            self.object = self.n.inputs[0].reception
            self.new_value = self.n.inputs[1].reception
        except:
            self.n.inputs[0].reception = None
            self.n.inputs[1].reception = None
            
NODES = {"Math":number_number_math, "Variable":create_variable, "Each":each,
                              "Sample List":list_tester, "Get Attribute":get_attr_from_object,"Condition":conditional_with_trigger,
                              "Set Attribute":set_attr_for_object}

class Nodes():
    def __init__(self, scene, name):
        self.scene = scene
        self.node = NODES[name](self.scene)



        