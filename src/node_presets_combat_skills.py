from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
import math, random, pickle
import binascii
from src.skeletons.weapon_types import weaponTypes

class grant_to_unit(QWidget):
    def __init__(self, scene,full_name, short_name, desc, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.short_name = short_name
        self.hexe = hexe
        self.desc = desc
        self.full_name = full_name
        self.title="Unit +"+self.full_name
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

        label2 = QLabel("Unit improves "+self.desc)
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.bonus_type = QComboBox()
        self.bonus_type.addItems(["Add ("+self.short_name+"+X)", "Multiply ("+self.short_name+" * X)"])
        self.bonus_type.currentTextChanged.connect(self.change_op)
        
        self.bonus_amount = QDoubleSpinBox()
        self.bonus_amount.setRange(-30,30)
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

class does_less_more_damage(QWidget):
    def __init__(self, scene, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.title="Unit does Less/More Damage"
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = self.hexe+"::"
        self.chain = 0
        self.current_operation = "More"
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("Unit does less/more damage")
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        
        self.bonus_amount = QSpinBox()
        self.bonus_amount.setRange(-30,30)
        self.bonus_amount.setValue(0)
        self.bonus_amount.setSingleStep(1)
        self.bonus_amount.valueChanged.connect(self.change_bonus)
        
        self.contents = [self.line1, self.bonus_amount]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160)
        self.n.node_preset = self
        
        self.n.storage = ["umd", 0]
        self.n.sw = ["", "self.bonus_amount"]
    
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
    
    def change_bonus(self,i):
        s_dict = {"More":"umd", "Less":"uld"}
        self.hex_output = self.hexe + "." + ":" +str(self.bonus_amount.value()) + ":"
        
        self.n.storage = ["", self.bonus_amount.value()]

class grant_bonus_to_unit_hit(grant_to_unit):
    def __init__(self, scene,full_name="Hit Chance", short_name= "Hit", hexe="ubi", desc = "hit chance"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class grant_bonus_to_unit_avo(grant_to_unit):
    def __init__(self, scene,full_name="Dodge Chance", short_name= "Avo", hexe="ubv", desc = "dodge chance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class grant_bonus_to_unit_crt(grant_to_unit):
    def __init__(self, scene,full_name="Critical Chance", short_name= "Crt", hexe="ubt", desc = "critical chance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class unit_does_less_more_damage(does_less_more_damage):
    def __init__(self, scene,hexe="udc"):
            super().__init__(scene, hexe)
            
class can_cannot(QWidget):
    def __init__(self, scene, action, which, direction, hexe, width=None):
        QObject.__init__(self)
        self.scene = scene
        self.title=which+direction+action
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = hexe
        self.hexe = hexe
        self.chain = 1
        if width != None:
            self.width = width
        else:
            self.width = 560
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label1 = QLabel("Event")
        label1.setAlignment(Qt.AlignLeft)
        self.line1_layout.addWidget(label1)

        label2 = QLabel("Event")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        
        self.contents = [self.line1]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160, self.width)
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
        
class foe_cannot_counterattack(can_cannot):
    def __init__(self, scene, hexe="fcc", which = "Foe", direction=" Cannot ", action = " Counter-Attack "):
            super().__init__(scene, action, which, direction, hexe)

class unit_counterattack_first(can_cannot):
    def __init__(self, scene, hexe="ucf", which = "", direction="Counter-Attacks ", action = "Before Foe Attack"):
            super().__init__(scene, action, which, direction, hexe)

class unit_counterattack_distance(can_cannot):
    def __init__(self, scene, hexe="ucd", which = "", direction="Counter-Attacks ", action = "From Any Distance"):
            super().__init__(scene, action, which, direction, hexe)

class unit_will_followup(can_cannot):
    def __init__(self, scene, hexe="uwu", which = "", direction="Will ", action = "Follow-Up Attack"):
            super().__init__(scene, action, which, direction, hexe)

class foe_cannot_followup(can_cannot):
    def __init__(self, scene, hexe="fcu", which = "Foe", direction=" Cannot ", action = "Follow-Up Attack"):
            super().__init__(scene, action, which, direction, hexe)

class unit_cannot_followup(can_cannot):
    def __init__(self, scene, hexe="ucu", which = "", direction="Cannot ", action = "Follow-Up Attack"):
            super().__init__(scene, action, which, direction, hexe)
            
class unit_attacks_twice(can_cannot):
    def __init__(self, scene, hexe="ugt", which = "", direction="Attacks ", action = "Twice"):
            super().__init__(scene, action, which, direction, hexe)

class foe_cannot_attack_twice(can_cannot):
    def __init__(self, scene, hexe="fgo", which = "Foe", direction=" Cannot Attack ", action = "Twice"):
            super().__init__(scene, action, which, direction, hexe)
            
class penalize_foe(QWidget):
    def __init__(self, scene,full_name, short_name, desc, hexe):
        QObject.__init__(self)
        self.scene = scene
        self.short_name = short_name
        self.hexe = hexe
        self.desc = desc
        self.full_name = full_name
        self.title="Foe -"+self.full_name
        self.inputs = [S_TRIGGER]
        self.outputs=[S_TRIGGER]
        self.hex_output = self.hexe+".sub::"
        self.chain = 0
        self.current_operation = "Subtract ("+self.short_name+"-X)"
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("Foe suffers penalty on "+self.desc)
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.bonus_type = QComboBox()
        self.bonus_type.addItems(["Subtract ("+self.short_name+"-X)", "Divide ("+self.short_name+" / X)"])
        self.bonus_type.currentTextChanged.connect(self.change_op)
        
        self.bonus_amount = QDoubleSpinBox()
        self.bonus_amount.setRange(-30,30)
        self.bonus_amount.setValue(0.0)
        self.bonus_amount.setSingleStep(1.0)
        self.bonus_amount.valueChanged.connect(self.change_bonus)
        
        self.contents = [self.line1, self.bonus_type, self.bonus_amount]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 200)
        self.n.node_preset = self
        
        self.n.sw = ["self.bonus_type", "self.bonus_amount"]
        self.n.storage = ["sub", 0]
    
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
        s_dict = {"Subtract ("+self.short_name+"-X)":"sub", "Divide ("+self.short_name+" / X)":"div"}
        self.hex_output = self.hexe + "." + s_dict[s] + ":" + str(round(self.bonus_amount.value(),1)) + ":"
        
        self.n.storage = [s, round(self.bonus_amount.value(),1)]
    
    def change_bonus(self,i):
        s_dict = {"Subtract ("+self.short_name+"-X)":"sub", "Divide ("+self.short_name+" / X)":"div"}
        self.hex_output = self.hexe + "." + s_dict[self.current_operation] + ":" +str(round(self.bonus_amount.value(),1)) + ":"
        
        self.n.storage = [self.current_operation, round(self.bonus_amount.value(),1)]

class penalize_foe_spd(penalize_foe):
    def __init__(self, scene,full_name="Speed", short_name= "Spd", hexe="pfs", desc = "speed"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class penalize_foe_atk(penalize_foe):
    def __init__(self, scene,full_name="Str/Mag", short_name= "Atk", hexe="pfa", desc = "attack"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class penalize_foe_def(penalize_foe):
    def __init__(self, scene,full_name="Defense", short_name= "Def", hexe="pfd", desc = "defense"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class penalize_foe_res(penalize_foe):
    def __init__(self, scene,full_name="Resistance", short_name= "Res", hexe="pfr", desc = "resistance"):
            super().__init__(scene, full_name, short_name, desc, hexe)
    
class penalize_foe_chr(penalize_foe):
    def __init__(self, scene,full_name="Charisma", short_name= "Chr", hexe="pfc", desc = "charisma"):
            super().__init__(scene, full_name, short_name, desc, hexe)
        
class penalize_foe_dex(penalize_foe):
    def __init__(self, scene,full_name="Dexterity", short_name= "Dex", hexe="pfx", desc = "dexterity"):
            super().__init__(scene, full_name, short_name, desc, hexe)
            
class penalize_foe_luc(penalize_foe):
    def __init__(self, scene,full_name="Luck", short_name= "Luc", hexe="pfl", desc = "luck"):
            super().__init__(scene, full_name, short_name, desc, hexe)

class turn_is_odd(can_cannot):
    def __init__(self, scene, hexe="gio", which = "Turn", direction=" is ", action = "Odd"):
            super().__init__(scene, action, which, direction, hexe, width=400)

class turn_is_even(can_cannot):
    def __init__(self, scene, hexe="gie", which = "Turn", direction=" is ", action = "Even"):
            super().__init__(scene, action, which, direction, hexe,width=400)
            
class disable_effective_against(can_cannot):
    def __init__(self, scene, hexe="dea", which = "Disable", direction=" Foe's 'Effective Against X'", action = ""):
            super().__init__(scene, action, which, direction, hexe,width=500)
            
class reset_attack_priority(can_cannot):
    def __init__(self, scene, hexe="rap", which = "Reset", direction=" Attack Priority", action = ""):
            super().__init__(scene, action, which, direction, hexe,width=440)

class disable_counterattack_from_any_distance(can_cannot):
    def __init__(self, scene, hexe="nlc", which = "Disable", direction=" Foe's 'Can Counter-Attack From Any Distance'", action = ""):
            super().__init__(scene, action, which, direction, hexe,width=780)