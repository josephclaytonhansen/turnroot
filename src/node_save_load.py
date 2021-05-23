from src.node_presets import Nodes
import json
from src.UI_node_edge import QDMGraphicsEdge, Edge, EDGE_TYPE_BEZIER
from src.img_overlay import overlayTile

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

data_string = ""

class Save(): 
    def saveNode(self, node):
        data = dict()
        self.node = node
        self.inputs = self.node.inputs
        self.outputs = self.node.outputs
        self.contents = self.node.content.contents
        self.storage = self.node.storage
        self.sw = self.node.sw
        
        edges = []
        
        for x in self.inputs:
            for e in x.edges:
                try:
                    edges.append(str(e.start_socket.node)[-5:-1] + ":" + str(e.start_socket.index)  + ":" + str(e.end_socket.node)[-5:-1]  + ":" + str(e.end_socket.index))
                except:
                    pass
        
        for x in self.outputs:
            for e in x.edges:
                try:
                    edges.append( str(e.start_socket.node)[-5:-1]  + ":" + str(e.start_socket.index)  + ":" + str(e.end_socket.node)[-5:-1] + ":" + str(e.end_socket.index))
                except:
                    pass
        
        data["edges"] = edges
        data["id"] = str(self.node)[-5:-1]
        
        data["preset"] = str(self.node.title)
        data["pos"] = (round(self.node.pos.x(),1), round(self.node.pos.y(),1))
        
        data["storage"] = self.storage
        data["sw"] = self.sw
        
        return data
    
    def saveScene(self, scene):
        all_nodes = {}
        data = {}
        
        count = -1
        
        for n in scene.nodes:
            count += 1
            all_nodes[count] = self.saveNode(n)
            
        data["nodes"] = all_nodes
        data["connection"] = scene.connection_type
        data["desc"] = scene.desc
        data["icon"] = [scene.or_index,scene.ir_index,scene.ic_index]
        
        scene.save_data = data
        
        return data
    
class Load():
    def loadScene(self,scene,path):
        s = json.loads(path)
        scene.save_data = s
        scene.clear()
        edges = []
        li = {}
        
        global data_string
        data_string = ""
        
        for n in s["nodes"]:
            g = Nodes(scene, s["nodes"][n]["preset"]).node
            
            for widget in s["nodes"][n]["sw"]:
                w_index = s["nodes"][n]["sw"].index(widget)
                widget = widget.replace("self.", "")

                try:
                    widget = getattr(g.node_preset, widget)
                    try:
                        widget.setValue(s["nodes"][n]["storage"][w_index])
                    except:
                        try:
                            widget.setCurrentText(s["nodes"][n]["storage"][w_index])
                        except:
                            print("could not set text")
                except:
                    pass
                    
                
            g.id = s["nodes"][n]["id"]
            print(g.id)
            scene.added_nodes.append(g)
            li[g.id] = g
            g.setPos(s["nodes"][n]["pos"][0], s["nodes"][n]["pos"][1])
            for k in s["nodes"][n]["edges"]:
                edge = k
                if edge not in edges:
                    edges.append(edge)
                    data_string+="&"+edge+"&*"
        
        for edge in edges:
            edge = edge.split(":")
            try:
                start_node = li[edge[0]]
                end_node = li[edge[2]]
                start_socket = start_node.outputs[int(edge[1])]
                end_socket = end_node.inputs[int(edge[3])]
                new_edge = Edge(scene, start_socket, end_socket, edge_type=EDGE_TYPE_BEZIER)
                scene.edges.append(new_edge)
            except:
                print("invalid edge")
        
        scene.or_index = s["icon"][0]
        scene.ir_index= s["icon"][1]
        scene.ic_index= s["icon"][2]
        
        pixmap = QPixmap(135,135)
        pixmap.fill(Qt.transparent)
        p = overlayTile(pixmap, scene.preview.outer[scene.or_index], 135)
        g = overlayTile(p, scene.preview.inner[scene.ir_index], 135)
        d = overlayTile(g, scene.preview.inner2[scene.ic_index], 135)
        pixmap = QIcon(d)
        scene.preview.image.setIcon(pixmap)
        
        scene.preview.desc_name.setPlainText(s["desc"])
        
        scene.data_string = data_string
        print(scene.data_string)
        
        for y in scene.preview.radio_buttons:
            if y == s["connection"]:
                scene.preview.radio_buttons[y].setAutoExclusive(False)
                scene.preview.radio_buttons[y].setCheckable(True)
                scene.preview.radio_buttons[y].setChecked(True)
                scene.preview.radio_buttons[y].setAutoExclusive(True)

