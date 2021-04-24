from src.UI_node_graphics_scene import QDMGraphicsScene
from PyQt5.QtWidgets import *
import json
from collections import OrderedDict
from src.UI_node_serializable import Serializable

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
        if self.path == None:
            self.saveFileDialog()
            with open(self.path, "w") as file:
                file.write( json.dumps( self.serialize(), indent=4 ) )
        else:
            with open(self.path, "w") as file:
                file.write( json.dumps( self.serialize(), indent=4 ) )

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"Save","","Turnroot Node File (*.trnep)", options=options)
        if fileName:
            self.path = fileName+".trnep"

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
        return False
