from src.node_presets import Nodes
import json
from src.UI_node_edge import QDMGraphicsEdge, Edge, EDGE_TYPE_BEZIER

class Save(): 
    def saveNode(self, node):
        data = dict()
        self.node = node
        self.inputs = self.node.inputs
        self.outputs = self.node.outputs
        self.contents = self.node.content.contents
        
        edges = []
        
        for x in self.inputs:
            for e in x.edges:
                edges.append(str(e.start_socket.node)[-5:-1] + ":" + str(e.start_socket.index)  + ":" + str(e.end_socket.node)[-5:-1]  + ":" + str(e.end_socket.index))
        
        for x in self.outputs:
            for e in x.edges:
                try:
                    edges.append( str(e.start_socket.node)[-5:-1]  + ":" + str(e.start_socket.index)  + ":" + str(e.end_socket.node)[-5:-1] + ":" + str(e.end_socket.index))
                except:
                    pass
        
        data["edges"] = edges
        data["id"] = str(self.node)[-5:-1]
        
        data["preset"] = str(self.node.title)
        data["pos"] = (self.node.pos.x(), self.node.pos.y())
        
        return data
    
    def saveScene(self, scene):
        all_nodes = {}
        data = {}
        
        count = -1
        
        for n in scene.nodes:
            count += 1
            all_nodes[count] = self.saveNode(n)
            
        data["nodes"] = all_nodes
        data["string"] = scene.long_term_storage
        
        scene.save_data = data
        return data
    
class Load():
    def loadScene(self,scene,path):
        s = json.loads(path)
        scene.clear()
        edges = []
        li = {}
        
        for n in s["nodes"]:
            g = Nodes(scene, s["nodes"][n]["preset"]).node
            g.id = s["nodes"][n]["id"]
            scene.added_nodes.append(g)
            li[g.id] = g
            g.setPos(s["nodes"][n]["pos"][0], s["nodes"][n]["pos"][1])
            for k in s["nodes"][n]["edges"]:
                edge = k
                if edge not in edges:
                    edges.append(edge)
        
        for edge in edges:
            edge = edge.split(":")
            start_node = li[edge[0]]
            end_node = li[edge[2]]
            start_socket = start_node.outputs[int(edge[1])]
            end_socket = end_node.inputs[int(edge[3])]
            new_edge = Edge(scene, start_socket, end_socket, edge_type=EDGE_TYPE_BEZIER)
            scene.edges.append(new_edge)
            

        
    
        
