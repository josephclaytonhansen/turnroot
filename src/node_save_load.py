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
        
        incoming_edges = {}
        outgoing_edges = {}
        
        for x in self.inputs:
            for e in x.edges:
                incoming_edges[x.index] = str(e)
        
        for x in self.outputs:
            for e in x.edges:
                outgoing_edges[x.index] = str(e)
        
        data["outgoing edges"] = outgoing_edges
        data["incoming edges"] = incoming_edges
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
        outgoing_edges = {}
        incoming_edges = {}
        li = {}
        
        for n in s["nodes"]:
            g = Nodes(scene, s["nodes"][n]["preset"]).node
            g.load_index = n
            scene.added_nodes.append(g)
            li[g.load_index] = g
            g.setPos(s["nodes"][n]["pos"][0], s["nodes"][n]["pos"][1])
            
            for socket in s["nodes"][n]["incoming edges"]:
                incoming_edge = s["nodes"][n]["incoming edges"][socket]
                
                incoming_edges[n+"."+socket] = incoming_edge
            
            for socket in s["nodes"][n]["outgoing edges"]:
                outgoing_edge = s["nodes"][n]["outgoing edges"][socket]
                
                outgoing_edges[n+"."+socket] = outgoing_edge
        
        for n in s["nodes"]:
            
            for socket in s["nodes"][n]["outgoing edges"]:
                outgoing_edge = s["nodes"][n]["outgoing edges"][socket]
                
                if outgoing_edge in incoming_edges.values():
                    in_ = list(incoming_edges.keys())[list(incoming_edges.values()).index(outgoing_edge)]
                    out_ = list(outgoing_edges.keys())[list(outgoing_edges.values()).index(outgoing_edge)]
                    in_ = in_.split(".")
                    out_ = out_.split(".")
            
            in_node = li[in_[0]]
            in_socket = li[in_[0]].inputs[int(in_[1])]
            
            print(in_, in_node, in_socket, out_)
            
            out_node = li[out_[0]]
            out_socket = li[out_[0]].outputs[int(out_[1])]
            
            new_edge = Edge(scene, in_socket, out_socket, edge_type=EDGE_TYPE_BEZIER)
            scene.edges.append(new_edge)
        
        
        
        
    
        
