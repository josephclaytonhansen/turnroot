from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
import math, random, pickle
import binascii
from src.skeletons.weapon_types import weaponTypes

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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
                #self.chain+=len(self.n.inputs[0].edges)-1
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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
                #self.chain+=len(self.n.inputs[0].edges)-1
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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
                #self.chain+=len(self.n.inputs[0].edges)-1
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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
                #self.chain+=len(self.n.inputs[0].edges)-1
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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
                #self.chain+=len(self.n.inputs[0].edges)-1
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
            
class using_weapon_type(QWidget):
    def __init__(self, scene, which, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.title=which+" is Using Weapon Type"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_BOOLEAN]
        self.hex_output = self.hexe
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label1 = QLabel("Event")
        label1.setAlignment(Qt.AlignLeft)
        self.line1_layout.addWidget(label1)

        label2 = QLabel("T/F")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        
        self.wt_select = QComboBox()
        self.wt_select.addItem("--Select--")
        self.wt_select.addItems(weaponTypes().data)
        self.wt_select.currentTextChanged.connect(self.change_weapon)
        
        self.contents = [self.line1, self.wt_select]
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

            self.chain = self.n.inputs[0].edges[0].start_socket.node.node_preset.chain + 1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
    
    def change_weapon(self, s):
        if s != "--Select--":
            s_dict = {}
            for x in range(len(weaponTypes().data)):
                s_dict[x] = str(ord(str(x)))
            self.hex_output = self.hexe + "2e" + s_dict[weaponTypes().data.index(s)]
        else:
            self.hex_output = self.hexe + "2e00"
    
class unit_using_weapon_type(using_weapon_type):
    def __init__(self, scene, hexe="757774", which = "Unit"):
            super().__init__(scene, which, hexe)

class foe_using_weapon_type(using_weapon_type):
    def __init__(self, scene, hexe="667774", which = "Foe"):
            super().__init__(scene, which, hexe)
            
class health_percentage(QWidget):
    def __init__(self, scene,which, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.title=which+" Health Percentage"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_BOOLEAN]
        self.hex_output = self.hexe + "2e3c3a35303a"
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label1 = QLabel("Event")
        label1.setAlignment(Qt.AlignLeft)
        self.line1_layout.addWidget(label1)

        label2 = QLabel("T/F")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        
        self.direction_select = QComboBox()
        self.direction_select.addItem("--Select--")
        self.direction_select.addItems([">", "<", ">=", "<="])
        self.direction_select.currentTextChanged.connect(self.change_direction)
        
        self.amount_set = QSpinBox()
        self.amount_set.setSuffix("%")
        self.amount_set.setRange(0,100)
        self.amount_set.setValue(100)
        self.amount_set.setSingleStep(1)
        
        self.contents = [self.line1, self.direction_select, self.amount_set]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 190)
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
    
    def change_direction(self, s):
        s_dict = {"--Select--":"00","<": "3c", ">":"3e","<=":"3c3d",">=":"3e3d"}
        self.hex_output = self.hexe + "2e" + s_dict[s] + "3a" +float.hex(float(self.amount_set.value())) + "3a"

class unit_health_percentage(health_percentage):
    def __init__(self, scene, hexe="756870", which = "Unit"):
            super().__init__(scene, which, hexe)

class foe_health_percentage(health_percentage):
    def __init__(self, scene, hexe="666870", which = "Foe"):
            super().__init__(scene, which, hexe)
