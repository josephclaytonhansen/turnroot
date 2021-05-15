from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
import math, random, pickle

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
        self.hex_output = "6e6d6f2e616464"
        self.chain = 0
        
        self.values = [0,0,0]
        self.current_operation = "Add"
        
        self.math_operation_choose = QComboBox()
        self.math_operation_choose.addItems(["Add", "Subtract", "Multiply", "Divide", "Power",
                                             "Modulo", "A Percent of B",
                                             "Minimum", "Maximum", "Absolute Value A",
                                             "Round A", "Ceiling A", "Floor A", "Sqrt A"])
        self.math_operation_choose.currentTextChanged.connect(self.change_op)
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1_layout.addWidget(QLabel("Num"))
        label2 = QLabel("Num")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        self.line1.setLayout(self.line1_layout)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        label3 = QLabel("Num")
        label3.setAlignment(Qt.AlignLeft)
        self.line2_layout.addWidget(label3)
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
        except:
            pass
        try:
            self.n.inputs[1].reception = self.n.inputs[1].edges[0].start_socket.emission
            self.values[1] = self.n.inputs[1].reception
        except:
            pass
            
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
        s_dict = {"Add":"616464", "Subtract":"737562", "Multiply":"6d756c",
                  "Divide":"646976", "Power":"706f77","Modulo":"6d6f64",
                  "A Percent of B":"706572", "Minimum":"6d696e", "Maximum":"6d6178",
                  "Absolute Value A":"616273", "Round A":"726f75", "Ceiling A":"636569",
                  "Floor A":"666c6f", "Sqrt A":"737172"}
        self.hex_output = "6e6d6f" + "2e" + s_dict[s]

class compare_numbers(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Compare Numbers"
        self.inputs = [S_NUMBER, S_NUMBER]
        self.outputs=[S_BOOLEAN]
        self.hex_output = "636e6f2e657175"
        self.chain = 0
        
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
        self.label1 = QLabel("Num")
        self.label1.setAlignment(Qt.AlignLeft)
        self.label2 = QLabel("T/F")
        self.label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(self.label1)
        self.line1_layout.addWidget(self.label2)
        self.line1.setLayout(self.line1_layout)
        
        self.line2 = QWidget()
        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(8)
        self.line2_layout.setContentsMargins(0,0,0,0)
        self.label3 = QLabel("Num")
        self.label3.setAlignment(Qt.AlignLeft)
        self.line2_layout.addWidget(self.label3)
        self.line2.setLayout(self.line2_layout)
        
        self.contents = [self.math_operation_choose, self.line1, self.line2]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 300)
        self.n.node_preset = self
        self.n_a = self.n.inputs[0]
        self.n_b = self.n.inputs[1]
        self.n_out = self.n.outputs[0]
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.n.inputs[0].node.node_preset.values[2]
            self.n.outputs[1].emission = self.n.inputs[0].node.node_preset.values[2]
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.values[0] = self.n.inputs[0].reception
        except:
            pass
        try:
            self.n.inputs[1].reception = self.n.inputs[1].edges[0].start_socket.emission
            self.values[1] = self.n.inputs[1].reception
        except:
            pass
            
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
        s_dict = {"Equal":"657175", "Not Equal":"6e6571", "Greater Than":"677274",
                  "Less Than":"6c7274", "Greater Than or Equal":"677465",
                  "Less Than or Equal":"6c7465"}
        self.hex_output = "636e6f" + "2e" + s_dict[s]

class combat_start(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Combat Start"
        self.inputs = []
        self.outputs=[S_TRIGGER]
        self.hex_output = "637073"
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("On event...")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        
        self.contents = [self.line1]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 200)
        self.n.node_preset = self
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.hex_output
        except:
            pass
    
    def updateReception(self):
        pass

class unit_initiates_combat(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Unit Initiates Combat"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = "756963"
        self.chain = 0
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("From event, on event...")
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.contents = [self.line1]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 200)
        self.n.node_preset = self
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.hex_output
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass

class foe_initiates_combat(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Foe Initiates Combat"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = "666963"
        self.chain = 0
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("From event, on event...")
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.contents = [self.line1]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 200)
        self.n.node_preset = self
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.hex_output
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission
            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
    
NODES = {"Math": number_number_math, "Compare Numbers": compare_numbers, "Combat Start": combat_start,
         "Unit Initiates Combat": unit_initiates_combat, "Foe Initiates Combat": foe_initiates_combat}
    
class Nodes():
    def __init__(self, scene, name):
        self.scene = scene
        self.node = NODES[name](self.scene).n

        


        