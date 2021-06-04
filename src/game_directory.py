import os, json
class gameDirectory():
    def __init__(self):
        self.path = None
        self.path_can_change = True
    
    def changePath(self, path):
        self.path = path
        dirs = ["classes", "exp_types","sheets","units","weapon_types","weapons", "objects"]
        for d in dirs:
            working_path = os.path.join(self.path, d)
            os.makedirs(working_path)
    
    def getPath(self):
        try:
            with open("src/tmp/game_dir.etmf", "r") as f:
                data = json.load(f)
                self.path = data["current_game_directory"]
        except:
            #get game directory from game editor"
            pass
            
        
