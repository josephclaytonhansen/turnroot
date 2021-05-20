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
        
        self.n.storage = [s_dict[s], round(self.bonus_amount.value(),1)]
    
    def change_bonus(self,i):
        s_dict = {"Add ("+self.short_name+"+X)":"add", "Multiply ("+self.short_name+" * X)":"mul"}
        self.hex_output = self.hexe + "." + s_dict[self.current_operation] + ":" +str(round(self.bonus_amount.value(),1)) + ":"
        
        self.n.storage = [s_dict[self.current_operation], round(self.bonus_amount.value(),1)]

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
        
        self.n.storage = ["umd", self.bonus_amount.value()]

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