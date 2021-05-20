from src.UI_node_graphics_scene import QDMGraphicsScene
from PyQt5.QtWidgets import *
import json, os
import qtmodern.styles
import qtmodern.windows
from collections import OrderedDict
from src.UI_node_serializable import Serializable
from src.UI_Dialogs import infoClose
from src.UI_node_node import Node
from src.UI_node_edge import Edge
from src.UI_node_scene_history import SceneHistory
from src.UI_node_scene_clipboard import SceneClipboard

from src.node_save_load import Load, Save

hex_string = ""
orders = {}

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.path = None
        
        self.scene_width = 64000
        self.scene_height = 64000
        
        self._has_been_modified = False
        self._has_been_modified_listeners = []
        
        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)
        
        self.NodeEditorWnd = None
        self.preview = None
        
        self.connection_type = None
        self.desc = None
        self.long_term_storage = ""
        self.or_index = 0
        self.ir_index = 0
        self.ic_index = 0
        
        self.save_data = Save().saveScene(scene=self)
    
    @property
    def has_been_modified(self):
        return False
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value


    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    
    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)
    
    def addNode(self, node):
        self.nodes.append(node)
        self.added_nodes.append(node)
    
    def addEdge(self, edge):
        self.edges.append(edge)
        
    def removeNode(self, node):
        try:
            self.nodes.remove(node)
            self.added_nodes.remove(node)
        except:
            pass
        
    def removeEdge(self, edge):
        self.edges.remove(edge)
    
    def saveToFile(self, dialog = True):
        if self.path == None or self.path == '':
            self.saveFileDialog()
            if self.path == None or self.path == '':
                c = infoClose("No file selected")
                c.exec_()
            else:
                with open(self.path, "w") as file:
                    file.write(json.dumps(self.save_data))
                    self.preview.skill_name.setText(self.path[self.path.rfind("/")+1:self.path.find(".trnep")])
                    self.preview.enable_radio_buttons()
        else:
            with open(self.path, "w") as file:
                file.write(json.dumps(self.save_data))
                self.preview.skill_name.setText(self.path[self.path.rfind("/")+1:self.path.find(".trnep")])
                self.preview.enable_radio_buttons()

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Open", "","Turnroot Node File (*.trnep)", options=options)
        if fileName:
            self.path = fileName
            with open(self.path, "r") as file:
                raw_data = file.read()
                Load().loadScene(scene=self,path=raw_data)

    def loadFromFile(self):
        self.openFileDialog()
        if self.path == None or self.path == '':
            c = infoClose("No file selected")
            c.exec_()
        else:
            with open(self.path, "r") as file:
                raw_data = file.read()
                Load().loadScene(scene=self,path=raw_data)
                self.preview.skill_name.setText(self.path[self.path.rfind(os.sep)+1:self.path.find(".trnep")])
                self.preview.enable_radio_buttons()
    
    def loadFromFileNoDialog(self):
        if self.path == None or self.path == '':
            c = infoClose("No file selected")
            c.exec_()
        else:
            with open(self.path, "r") as file:
                raw_data = file.read()
                Load().loadScene(scene=self,path=raw_data)
                self.preview.skill_name.setText(self.path[self.path.rfind(os.sep)+1:self.path.find(".trnep")])
                self.preview.enable_radio_buttons()        
    
    def saveFileDialog(self):
        q = QFileDialog()
        options = q.Options()
        options |= q.DontUseNativeDialog
        fileName, _ = q.getSaveFileName(None,"Save","","Turnroot Node File (*.trnep)", options=options)
        if fileName:
            self.path = fileName+".trnep"
            with open(self.path, "w") as file:
                file.write(json.dumps(self.save_data))
    
    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()
            self.added_nodes[0].remove()
            
    def update_hex(self):
        l = []
        tmp_used_data = []
        tmp_order = []
        for y in self.added_nodes:
            l.append([y.content.eval_order.value(), y.node_preset.hex_output])
        for x in range(len(l)):
            c = l[x][0]
            tmp_order.append(c)
        tmp_order = sorted(tmp_order)

        for o in tmp_order:
           for x in range(len(l)):
               c = l[x][0]
               d = l[x][1]
               if c == o:
                   if d not in tmp_used_data:
                       tmp_used_data.append(d)
                       
        self.long_term_storage = "".join(tmp_used_data)

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear()
        hashmap = {}

        if restore_id: self.id = data['id']

        # create nodes
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True

