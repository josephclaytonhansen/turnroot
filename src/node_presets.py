from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
import math, random, pickle
import binascii

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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 260)
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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 260)
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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160)
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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160)
        self.n.node_preset = self
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.hex_output
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 2
            if self.n.inputs[0].reception == False:
                self.chain+=1
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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160)
        self.n.node_preset = self
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.hex_output
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 2
            if self.n.inputs[0].reception == False:
                self.chain+=1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass

class grant_bonus_to_unit(QWidget):
    def __init__(self, scene,full_name, short_name, desc, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.short_name = short_name
        self.hexe = hexe
        self.desc = desc
        self.full_name = full_name
        self.title="Unit +Bonus "+self.full_name
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = self.hexe+"2e6164643a3a"
        self.chain = 0
        self.current_operation = "Add ("+self.short_name+"+X)"
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("Grant bonus to unit "+self.desc)
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.bonus_type = QComboBox()
        self.bonus_type.addItems(["Add ("+self.short_name+"+X)", "Multiply ("+self.short_name+" * X)"])
        self.bonus_type.currentTextChanged.connect(self.change_op)
        
        self.bonus_amount = QDoubleSpinBox()
        self.bonus_amount.setRange(-15,15)
        self.bonus_amount.setValue(0.0)
        self.bonus_amount.setSingleStep(1.0)
        self.bonus_amount.valueChanged.connect(self.change_bonus)
        
        self.contents = [self.line1, self.bonus_type, self.bonus_amount]
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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 2
            if self.n.inputs[0].reception == False:
                self.chain+=1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
    
    def change_op(self,s):
        self.current_operation = s
        s_dict = {"Add ("+self.short_name+"+X)":"616464", "Multiply ("+self.short_name+" * X)":"6d756c"}
        self.hex_output = self.hexe + "2e" + s_dict[s] + "3a" + float.hex(round(self.bonus_amount.value(),1)) + "3a"
    
    def change_bonus(self,i):
        s_dict = {"Add ("+self.short_name+"+X)":"616464", "Multiply ("+self.short_name+" * X)":"6d756c"}
        self.hex_output = self.hexe + "2e" + s_dict[self.current_operation] + "3a" +float.hex(round(self.bonus_amount.value(),1)) + "3a"

class grant_bonus_to_ally(QWidget):
    def __init__(self, scene,full_name, short_name, desc, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.short_name = short_name
        self.hexe = hexe
        self.desc = desc
        self.full_name = full_name
        self.title="Near Allies +Bonus "+self.full_name
        self.inputs = [S_BOOLEAN]
        self.outputs=[S_TRIGGER]
        self.hex_output = self.hexe+"2e6164643a3a"
        self.chain = 0
        self.current_operation = "Add ("+self.short_name+"+X)"
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("Grant bonus to ally "+self.desc)
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.line3 = QWidget()
        self.line3_layout = QHBoxLayout()
        self.line3_layout.setSpacing(8)
        self.line3_layout.setContentsMargins(0,0,0,0)
        self.line3.setLayout(self.line3_layout)
        
        label4 = QLabel("If true")
        label4.setAlignment(Qt.AlignLeft)
        self.line3_layout.addWidget(label4)
        
        self.bonus_type = QComboBox()
        self.bonus_type.addItems(["Add ("+self.short_name+"+X)", "Multiply ("+self.short_name+" * X)"])
        self.bonus_type.currentTextChanged.connect(self.change_op)
        
        self.line4 = QWidget()
        self.line4_layout = QHBoxLayout()
        self.line4_layout.setSpacing(8)
        self.line4_layout.setContentsMargins(0,0,0,0)
        self.line4.setLayout(self.line4_layout)
        
        self.spaces_amount = QSpinBox()
        self.spaces_amount.setRange(-15,15)
        self.spaces_amount.setValue(0)
        self.spaces_amount.setSingleStep(1)
        self.spaces_amount.valueChanged.connect(self.change_spaces)
        
        self.line4_layout.addWidget(QLabel("Within spaces"))
        self.line4_layout.addWidget(self.spaces_amount)
        
        self.bonus_amount = QDoubleSpinBox()
        self.bonus_amount.setRange(-15,15)
        self.bonus_amount.setValue(0.0)
        self.bonus_amount.setSingleStep(1.0)
        self.bonus_amount.valueChanged.connect(self.change_bonus)
        
        self.contents = [self.line1, self.line3, self.line4, self.bonus_type, self.bonus_amount]
        self.socket_content_index = 1
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 320)
        self.n.node_preset = self
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = self.hex_output
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 2
            if self.n.inputs[0].reception == False:
                self.chain+=1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
    
    def change_op(self,s):
        self.current_operation = s
        s_dict = {"Add ("+self.short_name+"+X)":"616464", "Multiply ("+self.short_name+" * X)":"6d756c"}
        self.hex_output = self.hexe + "2e" + s_dict[self.current_operation] + "3a" +float.hex(round(self.bonus_amount.value(),1)) + "3a" + "2e733a" + float.hex(float(self.spaces_amount.value())) + "3a"
    
    def change_bonus(self,i):
        s_dict = {"Add ("+self.short_name+"+X)":"616464", "Multiply ("+self.short_name+" * X)":"6d756c"}
        self.hex_output = self.hexe + "2e" + s_dict[self.current_operation] + "3a" +float.hex(round(self.bonus_amount.value(),1)) + "3a" + "2e733a" + float.hex(float(self.spaces_amount.value())) + "3a"
    
    def change_spaces(self):
        s_dict = {"Add ("+self.short_name+"+X)":"616464", "Multiply ("+self.short_name+" * X)":"6d756c"}
        self.hex_output = self.hexe + "2e" + s_dict[self.current_operation] + "3a" +float.hex(round(self.bonus_amount.value(),1)) + "3a" + "2e733a" + float.hex(float(self.spaces_amount.value())) + "3a"
        
class unit_is_close_to_ally(QWidget):
    def __init__(self, scene, spaces, hexe, l=False):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.spaces = spaces
        self.l = l
        self.title="Unit is "+self.spaces+" Ally"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_BOOLEAN]
        if self.l:
            self.hex_output = self.hexe + "2e6164643a3a"
        else:
            self.hex_output = self.hexe
        self.chain = 0
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)
        
        label1 = QLabel("If True")
        label1.setAlignment(Qt.AlignRight)
        label2 = QLabel("Event")
        label2.setAlignment(Qt.AlignLeft)
        
        if l:
            self.spaces_amount = QSpinBox()
            self.spaces_amount.setRange(-15,15)
            self.spaces_amount.setValue(0)
            self.spaces_amount.setSingleStep(1)
            self.spaces_amount.valueChanged.connect(self.change_spaces)
            
        self.line1_layout.addWidget(label2)
        self.line1_layout.addWidget(label1)
        
        if l:
            self.contents = [self.line1, self.spaces_amount]
        else:
            self.contents = [self.line1]
            
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160)
        self.n.node_preset = self
        
    def change_spaces(self):
        self.hex_output = self.hexe + "3a" +float.hex(float(self.spaces_amount.value())) + "3a"
    
    def updateEmission(self):
        try:
            self.n.outputs[0].emission = True
        except:
            pass
    
    def updateReception(self):
        try:
            self.n.inputs[0].reception = self.n.inputs[0].edges[0].start_socket.emission

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 2
            if self.n.inputs[0].reception == False:
                self.chain+=1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
       

class grant_bonus_to_unit_atk(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Str/Mag", short_name= "Atk", hexe="756261", desc = "attack"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_spd(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Speed", short_name= "Spd", hexe="756273", desc = "speed"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_def(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Defense", short_name= "Def", hexe="756264", desc = "defense"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_res(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Resistance", short_name= "Res", hexe="756272", desc = "resistance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_unit_chr(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Charisma", short_name= "Chr", hexe="756263", desc = "charisma"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_dex(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Dexterity", short_name= "Dex", hexe="756278", desc = "dexterity"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_unit_luc(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Luck", short_name= "Luc", hexe="75626c", desc = "luck"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_ally_atk(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Str/Mag", short_name= "Atk", hexe="616261", desc = "attack"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_spd(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Speed", short_name= "Spd", hexe="616273", desc = "speed"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_def(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Defense", short_name= "Def", hexe="616264", desc = "defense"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_res(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Resistance", short_name= "Res", hexe="616272", desc = "resistance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_ally_chr(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Charisma", short_name= "Chr", hexe="616263", desc = "charisma"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_dex(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Dexterity", short_name= "Dex", hexe="616278", desc = "dexterity"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_ally_luc(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Luck", short_name= "Luc", hexe="61626c", desc = "luck"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class unit_is_adjacent_to_ally(unit_is_close_to_ally):
    def __init__(self, scene, hexe="756161", spaces = "Adjacent to"):
            super().__init__(scene, spaces, hexe)

class unit_is_near_ally(unit_is_close_to_ally):
    def __init__(self, scene, hexe="756161", spaces = "Within N of", l =True):
            super().__init__(scene, spaces, hexe, l)
 
NODES = {"Math": number_number_math, "Compare Numbers": compare_numbers, "Combat Start": combat_start,
         "Unit Initiates Combat": unit_initiates_combat, "Foe Initiates Combat": foe_initiates_combat,
         "Unit +Bonus Strength/Magic": grant_bonus_to_unit_atk, "Unit +Bonus Defense": grant_bonus_to_unit_def,
         "Unit +Bonus Resistance": grant_bonus_to_unit_res,"Unit +Bonus Charisma": grant_bonus_to_unit_chr,
         "Unit +Bonus Dexterity": grant_bonus_to_unit_dex,"Unit +Bonus Luck": grant_bonus_to_unit_luc,
         "Unit is Adjacent to Ally": unit_is_adjacent_to_ally, "Unit is Within N of Ally": unit_is_near_ally,
         "Ally +Bonus Strength/Magic": grant_bonus_to_ally_atk, "Ally +Bonus Defense": grant_bonus_to_ally_def,
         "Ally +Bonus Resistance": grant_bonus_to_ally_res,"Ally +Bonus Charisma": grant_bonus_to_ally_chr,
         "Ally +Bonus Dexterity": grant_bonus_to_ally_dex,"Ally +Bonus Luck": grant_bonus_to_ally_luc}

NODE_KEYS = ["Math", "Compare Numbers", "Combat Start",
             "Unit Initiates Combat", "Foe Initiates Combat",
             "Unit +Bonus Strength/Magic", "Unit +Bonus Defense",
             "Unit +Bonus Resistance", "Unit +Bonus Charisma",
             "Unit +Bonus Dexterity", "Unit +Bonus Luck",
             "Unit is Adjacent to Ally", "Unit is Within N of Ally",
             "Ally +Bonus Strength/Magic", "Ally +Bonus Defense",
             "Ally +Bonus Resistance", "Ally +Bonus Charisma",
             "Ally +Bonus Dexterity", "Ally +Bonus Luck"]
    
class Nodes():
    def __init__(self, scene, name):
        self.scene = scene
        self.node = NODES[name](self.scene).n

        


        