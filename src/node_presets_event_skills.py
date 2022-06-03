
from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
import math, random, pickle
import binascii
from src.skeletons.weapon_types import weaponTypes

class event_(QWidget):
    def __init__(self, title, desc, scene, hexe, width):
        QObject.__init__(self)
        self.scene = scene
        self.title=title
        self.desc=desc
        self.inputs = [S_BOOLEAN]
        self.outputs=[S_BOOLEAN]
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

        label1 = QLabel("T/F")
        label1.setAlignment(Qt.AlignLeft)
        self.line1_layout.addWidget(label1)
        
        label2 = QLabel(self.desc)
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)

        label2 = QLabel("T/F")
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
    
class n_percent_chance(QWidget):
    def __init__(self, scene, desc, hexe, full_name):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.desc = desc
        self.full_name = full_name
        self.title="N% Chance"
        self.inputs = [S_NUMBER]
        self.outputs=[S_TRIGGER]
        self.hex_output = self.hexe+""
        self.chain = 0
        self.width=640
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("Skill has % chance of triggering")
        label2.setAlignment(Qt.AlignCenter)
        self.line1_layout.addWidget(label2)
        
        self.bonus_amount = QDoubleSpinBox()
        self.bonus_amount.setRange(00,100)
        self.bonus_amount.setValue(0.0)
        self.bonus_amount.setSingleStep(1.0)
        self.bonus_amount.valueChanged.connect(self.change_chance)
        
        self.contents = [self.line1, self.bonus_amount]
        self.socket_content_index = 0
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 200)
        self.n.node_preset = self
        
        self.n.sw = ["self.bonus_amount"]
        self.n.storage = [0]
    
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
    
    def change_chance(self,i):
        self.hex_output = "nchance." ":" +str(round(self.bonus_amount.value(),1)) + ":"

        self.n.storage = [round(self.bonus_amount.value(),1)]

class percent_chance(n_percent_chance):
    def __init__(self, scene,full_name="N% Chance", hexe="npc", desc = "N% chance"):
            super().__init__(scene, full_name, desc, hexe)

class foe_misses(event_):
    def __init__(self, scene, hexe="efh", title = "Unit Takes Damage", desc = "(T: Foe Hits / F: Foe Misses)", width = 620):
            super().__init__(title, desc, scene, hexe, width)
            
class unit_misses(event_):
    def __init__(self, scene, hexe="euh", title = "Foe Takes Damage", desc = "(T: Unit Hits / F: Unit Misses)", width = 620):
            super().__init__(title, desc, scene, hexe, width)

class unit_would_die(event_):
    def __init__(self, scene, hexe="uwd", title = "Unit Would Die", desc = "T: Unit Receives a Killing Blow (this skill will intervene)", width = 620):
            super().__init__(title, desc, scene, hexe, width)

class foe_would_die(event_):
    def __init__(self, scene, hexe="fwd", title = "Foe Will Die", desc = "T: Foe Receives a Killing Blow (this skill will occur after foe's death)", width = 620):
            super().__init__(title, desc, scene, hexe, width)

            
class unit_is_close_to_any(QWidget):
    def __init__(self, scene, spaces, hexe, l=False):
        QObject.__init__(self)
        self.scene = scene
        self.hexe = hexe
        self.spaces = spaces
        self.l = l
        self.title="Unit is "+self.spaces+" Any Unit"
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
        
        self.n = Node(self.scene, self.title, self.inputs, self.outputs, self.contents, self.socket_content_index, 160, 520)
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

class unit_is_near_any(unit_is_close_to_any):
    def __init__(self, scene, hexe="ane", spaces = "Within N of", l =True):
            super().__init__(scene, spaces, hexe, l)

class take_another_action(event_):
    def __init__(self, scene, hexe="taa", title = "Take Another Action", desc = "T: Take Another Action", width = 640):
            super().__init__(title, desc, scene, hexe, width)