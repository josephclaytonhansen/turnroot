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
        self.hex_output = "cps"
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
        self.hex_output = "uic"
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
        self.hex_output = "fic"
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
        self.hex_output = self.hexe+".add::"
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
        
        self.n.sw = ["self.bonus_type", "self.bonus_amount"]
        self.n.storage = ["add", 0]
    
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
        s_dict = {"Add ("+self.short_name+"+X)":"add", "Multiply ("+self.short_name+" * X)":"mul"}
        self.hex_output = self.hexe + "." + s_dict[s] + ":" + str(round(self.bonus_amount.value(),1)) + ":"
        
        self.n.storage = [s, round(self.bonus_amount.value(),1)]
    
    def change_bonus(self,i):
        s_dict = {"Add ("+self.short_name+"+X)":"add", "Multiply ("+self.short_name+" * X)":"mul"}
        self.hex_output = self.hexe + "." + s_dict[self.current_operation] + ":" +str(round(self.bonus_amount.value(),1)) + ":"
        
        self.n.storage = [self.current_operation, round(self.bonus_amount.value(),1)]

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
        self.hex_output = self.hexe+".add::"
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
        
        self.n.sw = ["self.bonus_type", "self.bonus_amount"]
        self.n.storage = ["add", 0]
    
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
        s_dict = {"Add ("+self.short_name+"+X)":"add", "Multiply ("+self.short_name+" * X)":"mul"}
        self.hex_output = self.hexe + "." + s_dict[self.current_operation] + ":" +str(round(self.bonus_amount.value(),1)) + ":" + ".s:" + str(self.spaces_amount.value()) + ":"
        self.n.storage = [self.current_operation, round(self.bonus_amount.value(),1)]
    
    def change_bonus(self,i):
        s_dict = {"Add ("+self.short_name+"+X)":"add", "Multiply ("+self.short_name+" * X)":"mul"}
        self.hex_output = self.hexe + "." + s_dict[self.current_operation] + ":" +str(round(self.bonus_amount.value(),1)) + ":" + ".s:" + str(self.spaces_amount.value()) + ":"
        self.n.storage = [self.current_operation, round(self.bonus_amount.value(),1)]
    
    def change_spaces(self):
        s_dict = {"Add ("+self.short_name+"+X)":"add", "Multiply ("+self.short_name+" * X)":"mul"}
        self.hex_output = self.hexe + "." + s_dict[self.current_operation] + ":" +str(round(self.bonus_amount.value(),1)) + ":" + ".s:" + str(self.spaces_amount.value()) + ":"
        self.n.storage = [self.current_operation, round(self.bonus_amount.value(),1)]
        
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
            self.hex_output = self.hexe + ".s::"
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
        
        self.n.sw = ["self.spaces_amount"]
        self.n.storage = [0]
        
    def change_spaces(self):
        self.hex_output = self.hexe + ".s:" +str(self.spaces_amount.value()) + ":"
        self.n.storage = [self.spaces_amount.value()]
    
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
    def __init__(self, scene,full_name="Str/Mag", short_name= "Atk", hexe="uba", desc = "attack"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_spd(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Speed", short_name= "Spd", hexe="ubs", desc = "speed"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_def(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Defense", short_name= "Def", hexe="ubd", desc = "defense"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_res(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Resistance", short_name= "Res", hexe="ubr", desc = "resistance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_unit_chr(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Charisma", short_name= "Chr", hexe="ubc", desc = "charisma"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_dex(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Dexterity", short_name= "Dex", hexe="ubx", desc = "dexterity"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_unit_luc(grant_bonus_to_unit):
    def __init__(self, scene,full_name="Luck", short_name= "Luc", hexe="abl", desc = "luck"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_ally_atk(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Str/Mag", short_name= "Atk", hexe="aba", desc = "attack"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_spd(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Speed", short_name= "Spd", hexe="abs", desc = "speed"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_def(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Defense", short_name= "Def", hexe="abd", desc = "defense"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_res(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Resistance", short_name= "Res", hexe="abr", desc = "resistance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_ally_chr(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Charisma", short_name= "Chr", hexe="abc", desc = "charisma"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_ally_dex(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Dexterity", short_name= "Dex", hexe="abx", desc = "dexterity"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_ally_luc(grant_bonus_to_ally):
    def __init__(self, scene,full_name="Luck", short_name= "Luc", hexe="abl", desc = "luck"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class unit_is_adjacent_to_ally(unit_is_close_to_ally):
    def __init__(self, scene, hexe="uaa", spaces = "Adjacent to"):
            super().__init__(scene, spaces, hexe)

class unit_is_near_ally(unit_is_close_to_ally):
    def __init__(self, scene, hexe="una", spaces = "Within N of", l =True):
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
        
        self.n.sw = ["self.wt_select"]
        self.n.storage = []
    
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
            self.hex_output = self.hexe + "." + s
            self.n.storage = [s]
        else:
            self.hex_output = self.hexe + ".na"
    
class unit_using_weapon_type(using_weapon_type):
    def __init__(self, scene, hexe="uiw", which = "Unit"):
            super().__init__(scene, which, hexe)

class foe_using_weapon_type(using_weapon_type):
    def __init__(self, scene, hexe="fiw", which = "Foe"):
            super().__init__(scene, which, hexe)
            
class health_percentage(QWidget):
    def __init__(self, scene,which, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.title=which+" Health Percentage"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_BOOLEAN]
        self.hex_output = self.hexe + ".<:100:"
        self.current_operation = "<"
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
        #self.amount_set.setValue(100)
        self.amount_set.valueChanged.connect(self.change_amount)
        self.amount_set.setSingleStep(1)
        
        self.contents = [self.line1, self.direction_select, self.amount_set]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 190)
        self.n.node_preset = self
        
        self.n.sw = ["self.direction_select", "self.amount_set"]
        self.n.storage= [">", 50]
    
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
        self.current_operation = s
        self.hex_output = self.hexe + "." + s + ":" +str(self.amount_set.value()) + ":"
        self.n.storage = [s, self.amount_set.value()]
    def change_amount(self, i):
        s_dict = {"--Select--":"00","<": "3c", ">":"3e","<=":"3c3d",">=":"3e3d"}
        self.hex_output = self.hexe + "." + self.current_operation + ":" +str(self.amount_set.value()) + ":"
        self.n.storage = [self.current_operation, self.amount_set.value()]

class unit_health_percentage(health_percentage):
    def __init__(self, scene, hexe="uhp", which = "Unit"):
            super().__init__(scene, which, hexe)

class foe_health_percentage(health_percentage):
    def __init__(self, scene, hexe="fhp", which = "Foe"):
            super().__init__(scene, which, hexe)

class is_(QWidget):
    def __init__(self, isa,scene, which, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.title=which+" is "+isa
        self.isa = isa
        self.inputs = [S_TRIGGER]
        self.outputs=[S_BOOLEAN]
        self.hex_output = hexe
        self.hexe = hexe
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
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass

class foe_is_mounted(is_):
    def __init__(self, scene, hexe="fim", which = "Foe", isa = "Mounted"):
            super().__init__(isa, scene, which, hexe)
    
class unit_is_mounted(is_):
    def __init__(self, scene, hexe="uim", which = "Unit", isa = "Mounted"):
            super().__init__(isa, scene, which, hexe)
            
class ally_is_mounted(is_):
    def __init__(self, scene, hexe="aim", which = "Ally", isa = "Mounted"):
            super().__init__(isa, scene, which, hexe)

class ally_is_male(is_):
    def __init__(self, scene, hexe="amn", which = "Ally", isa = "Male"):
            super().__init__(isa, scene, which, hexe)

class ally_is_female(is_):
    def __init__(self, scene, hexe="afn", which = "Ally", isa = "Female"):
            super().__init__(isa, scene, which, hexe)
            
class has_bonus_or_penalty(QWidget):
    def __init__(self, scene, which, direction,hexe):
        QObject.__init__(self)
        self.scene = scene
        self.title=which+" has "+direction
        self.inputs = [S_TRIGGER]
        self.outputs=[S_BOOLEAN]
        self.hex_output = hexe
        self.hexe = hexe
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
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass

class foe_has_bonus(has_bonus_or_penalty):
    def __init__(self, scene, hexe="fhb", which = "Foe", direction = "Bonus"):
            super().__init__(scene, which, direction, hexe)
    
class foe_has_penalty(has_bonus_or_penalty):
    def __init__(self, scene, hexe="fhp", which = "Foe", direction = "Penalty"):
            super().__init__(scene, which, direction, hexe)
            
class unit_has_bonus(has_bonus_or_penalty):
    def __init__(self, scene, hexe="uhb", which = "Unit", direction = "Bonus"):
            super().__init__(scene, which, direction, hexe)
    
class unit_has_penalty(has_bonus_or_penalty):
    def __init__(self, scene, hexe="uhp", which = "Unit", direction = "Penalty"):
            super().__init__(scene, which, direction, hexe)
            
class experience_extra(QWidget):
    def __init__(self, scene, desc, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.desc = desc
        self.title="Earn Extra "+self.desc+" EXP"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = self.hexe+".add::"
        self.chain = 0
        self.current_operation = "Add"
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("Earn Extra "+self.desc+" EXP")
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.bonus_type = QComboBox()
        self.bonus_type.addItems(["Add", "Multiply"])
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
        
        self.n.sw = ["self.bonus_type", "self.bonus_amount"]
        self.n.storage = ["Add", 0]
    
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
        s_dict = {"Add":"add", "Multiply":"mul"}
        self.hex_output = self.hexe + "." + s_dict[s] + ":" + round(self.bonus_amount.value(),1) + ":"
        self.n.storage = [s, self.bonus_amount.value()]
    
    def change_bonus(self,i):
        s_dict = {"Add":"add", "Multiply":"mul"}
        self.hex_output = self.hexe + "." + s_dict[s] + ":" + round(self.bonus_amount.value(),1) + ":"
        self.n.storage = [s, self.bonus_amount.value()]
        
class level_experience_extra(experience_extra):
    def __init__(self, scene, hexe="ele", desc = "Level"):
            super().__init__(scene, desc, hexe)
    
class weapon_experience_extra(experience_extra):
    def __init__(self, scene, hexe="ewe", desc = "Weapon"):
            super().__init__(scene, desc, hexe)

class level_is_night(is_):
    def __init__(self, scene, hexe="lin", which = "Level", isa = "Night"):
            super().__init__(isa, scene, which, hexe)
            
class level_is_raining(is_):
    def __init__(self, scene, hexe="lir", which = "Level", isa = "Raining"):
            super().__init__(isa, scene, which, hexe)
            
class level_is_foggy(is_):
    def __init__(self, scene, hexe="lif", which = "Level", isa = "Foggy"):
            super().__init__(isa, scene, which, hexe)
            
class unit_is_flying(is_):
    def __init__(self, scene, hexe="uif", which = "Unit", isa = "Flying"):
            super().__init__(isa, scene, which, hexe)
            
class foe_is_flying(is_):
    def __init__(self, scene, hexe="fif", which = "Foe", isa = "Flying"):
            super().__init__(isa, scene, which, hexe)
            
class unit_is_paired(is_):
    def __init__(self, scene, hexe="uip", which = "Unit", isa = "Paired Up"):
            super().__init__(isa, scene, which, hexe)
            
class damage_type_is_magic(is_):
    def __init__(self, scene, hexe="dtm", which = "Damage Type", isa = "Magic"):
            super().__init__(isa, scene, which, hexe)
            
class damage_type_is_physical(is_):
    def __init__(self, scene, hexe="dtp", which = "Damage Type", isa = "Physical"):
            super().__init__(isa, scene, which, hexe)