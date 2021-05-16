from src.UI_node_node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_socket import Socket, S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_LIST, S_BOOLEAN
from src.node_presets_passive_skills import (combat_start, unit_initiates_combat, foe_initiates_combat,
                                             grant_bonus_to_unit, grant_bonus_to_ally, unit_is_close_to_ally,
                                             grant_bonus_to_unit_atk, grant_bonus_to_unit_def,
                                             grant_bonus_to_unit_res,grant_bonus_to_unit_chr,
                                             grant_bonus_to_unit_dex,grant_bonus_to_unit_luc,
                                             unit_is_adjacent_to_ally,unit_is_near_ally,
                                             grant_bonus_to_ally_atk,grant_bonus_to_ally_def,
                                             grant_bonus_to_ally_res,grant_bonus_to_ally_chr,
                                             grant_bonus_to_ally_dex,grant_bonus_to_ally_luc,
                                             unit_using_weapon_type, foe_using_weapon_type,
                                             unit_health_percentage, foe_health_percentage,
                                             foe_is_mounted, unit_is_mounted,foe_has_bonus,
                                             foe_has_penalty,unit_has_bonus,unit_has_penalty)

from src.skeletons.weapon_types import weaponTypes
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

 
class bool_to_event(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Convert T/F to Event"
        self.inputs = [S_BOOLEAN]
        self.outputs=[S_TRIGGER]
        self.hex_output = "627465"
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label2 = QLabel("From T/F to event")
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
                #self.chain+=len(self.n.inputs[0].edges)-1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
        
class and_event(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="And (If X and Y are True)"
        self.inputs = [S_BOOLEAN, S_BOOLEAN]
        self.outputs=[S_TRIGGER]
        self.hex_output = "616e64"
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label1 = QLabel("If True")
        label1.setAlignment(Qt.AlignLeft)
        self.line1_layout.addWidget(label1)

        label2 = QLabel("Event")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        
        label3= QLabel("If True")
        label3.setAlignment(Qt.AlignLeft)
        
        self.contents = [self.line1, label3]
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

class or_event(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="A or B"
        self.inputs = [S_BOOLEAN, S_BOOLEAN]
        self.outputs=[S_TRIGGER]
        self.hex_output = "6f7263"
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label1 = QLabel("If True")
        label1.setAlignment(Qt.AlignLeft)
        self.line1_layout.addWidget(label1)

        label2 = QLabel("Event")
        label2.setAlignment(Qt.AlignRight)
        self.line1_layout.addWidget(label2)
        
        label3= QLabel("If True")
        label3.setAlignment(Qt.AlignLeft)
        
        self.contents = [self.line1, label3]
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

class not_event(QWidget):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene
        self.title="Not (If A is False, True)"
        self.inputs = [S_BOOLEAN]
        self.outputs=[S_BOOLEAN]
        self.hex_output = "6e6f74"
        self.chain = 1
        
        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1_layout.setSpacing(8)
        self.line1_layout.setContentsMargins(0,0,0,0)
        self.line1.setLayout(self.line1_layout)

        label1 = QLabel("If True")
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
                #self.chain+=len(self.n.inputs[0].edges)-1
            self.n.content.eval_order.setValue(self.chain)
            self.n.content.eval_order.setEnabled(False)
        except:
            pass
    
NODES = {"Math": number_number_math, "Compare Numbers": compare_numbers, "Combat Start": combat_start,
         "Unit Initiates Combat": unit_initiates_combat, "Foe Initiates Combat": foe_initiates_combat,
         "Unit +Bonus Strength/Magic": grant_bonus_to_unit_atk, "Unit +Bonus Defense": grant_bonus_to_unit_def,
         "Unit +Bonus Resistance": grant_bonus_to_unit_res,"Unit +Bonus Charisma": grant_bonus_to_unit_chr,
         "Unit +Bonus Dexterity": grant_bonus_to_unit_dex,"Unit +Bonus Luck": grant_bonus_to_unit_luc,
         "Unit is Adjacent to Ally": unit_is_adjacent_to_ally, "Unit is Within N of Ally": unit_is_near_ally,
         "Ally +Bonus Strength/Magic": grant_bonus_to_ally_atk, "Ally +Bonus Defense": grant_bonus_to_ally_def,
         "Ally +Bonus Resistance": grant_bonus_to_ally_res,"Ally +Bonus Charisma": grant_bonus_to_ally_chr,
         "Ally +Bonus Dexterity": grant_bonus_to_ally_dex,"Ally +Bonus Luck": grant_bonus_to_ally_luc,
         "Convert T/F to Event": bool_to_event, "And": and_event, "Unit Using Weapon Type": unit_using_weapon_type,
         "Foe Using Weapon Type": foe_using_weapon_type, "Unit Health Percentage":unit_health_percentage,
         "Foe Health Percentage":foe_health_percentage, "A or B": or_event, "Not (If A is False, True)": not_event,
         "Foe is Mounted":foe_is_mounted, "Unit is Mounted":unit_is_mounted, "Foe Has Bonus":foe_has_bonus,
         "Foe Has Penalty":foe_has_penalty,"Unit Has Penalty":unit_has_bonus,"Unit has Penalty": unit_has_penalty}

        
NODE_KEYS = sorted(["Math", "Compare Numbers", "Combat Start",
             "Unit Initiates Combat", "Foe Initiates Combat",
             "Unit +Bonus Strength/Magic", "Unit +Bonus Defense",
             "Unit +Bonus Resistance", "Unit +Bonus Charisma",
             "Unit +Bonus Dexterity", "Unit +Bonus Luck",
             "Unit is Adjacent to Ally", "Unit is Within N of Ally",
             "Ally +Bonus Strength/Magic", "Ally +Bonus Defense",
             "Ally +Bonus Resistance", "Ally +Bonus Charisma",
             "Ally +Bonus Dexterity", "Ally +Bonus Luck",
             "Convert T/F to Event", "And", "Unit Using Weapon Type",
             "Foe Using Weapon Type", "Unit Health Percentage",
                    "Foe Health Percentage", "Not (If A is False, True)",
                    "A or B", "Foe is Mounted", "Unit is Mounted",
                    "Unit Has Penalty", "Unit Has Bonus", "Foe Has Penalty",
                    "Foe Has Bonus"])
    
class Nodes():
    def __init__(self, scene, name):
        self.scene = scene
        self.node = NODES[name](self.scene).n

        


        