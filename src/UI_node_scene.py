from src.UI_node_graphics_scene import QDMGraphicsScene
from PyQt5.QtWidgets import *
import json
import qtmodern.styles
import qtmodern.windows
from collections import OrderedDict
from src.UI_node_serializable import Serializable
from src.UI_Dialogs import infoClose
from src.UI_node_node import Node
from src.UI_node_edge import Edge


class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.path = None
        
        self.scene_width = 64000
        self.scene_height = 64000
        
        self.initUI()
    
    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)
    
    def addNode(self, node):
        self.nodes.append(node)
    
    def addEdge(self, edge):
        self.edges.append(edge)
        
    def removeNode(self, node):
        self.nodes.remove(node)
        
    def removeEdge(self, edge):
        self.edges.remove(edge)
    
    def saveToFile(self):
        print(self.path)
        if self.path == None or self.path == '':
            self.saveFileDialog()
            if self.path == None or self.path == '':
                c = infoClose("No file selected")
                c.exec_()
            else:
                with open(self.path, "w") as file:
                    file.write( json.dumps( self.serialize(), indent=4 ) )
        else:
            with open(self.path, "w") as file:
                file.write( json.dumps( self.serialize(), indent=4 ) )

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Open", "","Turnroot Node File (*.trnep)", options=options)
        if fileName:
            self.path = fileName

    def loadFromFile(self):
        if self.path == None:
            self.openFileDialog()
            if self.path == None:
                c = infoClose("No file selected")
                c.exec_()
            else:
                with open(self.path, "r") as file:
                    raw_data = file.read()
                    data = json.loads(raw_data)
                    self.deserialize(data)
        else:
            with open(self.path, "r") as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                self.deserialize(data)
    
    def saveFileDialog(self):
        q = QFileDialog()
        options = q.Options()
        options |= q.DontUseNativeDialog
        fileName, _ = q.getSaveFileName(None,"Save","","Turnroot Node File (*.trnep)", options=options)
        if fileName:
            self.path = fileName+".trnep"
    
    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

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

    def deserialize(self, data, hashmap={}):
        print("deserializating data", data)
        self.clear()
        hashmap = {}

        # create nodes
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)

        return True

