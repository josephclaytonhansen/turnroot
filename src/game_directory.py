import os, json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

cd = os.getcwd()
srcd = cd + '/src/tmp/game_dir.etmf'

class gameDirectory():
    def __init__(self, parent):
        self.path = None
        self.path_can_change = True
        self.parent = parent
    
    def pathDialog(self):
        path = str(QFileDialog.getExistingDirectory(self.parent, "Select Folder"))
        return path
    
    def changePath(self, path):
        self.path = path

        if os.path.exists(self.path):
            dirs = ["classes", "exp_types","sheets","units","weapon_types","weapons", "objects", "items", "exp_types",
                    "music", "graphics", "sounds", "dialogues", "events", "skills", "tactics", "skilled_blows", "game_data",
                    "levels"]
            for d in dirs:
                working_path = os.path.join(self.path, d)
                try:
                    os.makedirs(working_path)
                except:
                    pass
                
            with open(srcd, "w") as f:
                json.dump({"current_game_directory":self.path},f)
    
    def getPath(self):
        try:
            with open(srcd, "r") as f:
                data = json.load(f)
                self.path = data["current_game_directory"]
        except:
            #get game directory from game editor"
            pass
            
        
