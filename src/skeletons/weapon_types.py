import json

class expTypes():
    def __init__(self):
        with open("src/skeletons/extra_exp_types.json", "r") as weapons_file:
            weapon_types = json.load(weapons_file)
        self.data = weapon_types
        for wt in self.data:
            w = weaponType(wt)
            try:
                w.Load()
            except:
                print("no existing data for type" + wt)
            with open("src/skeletons/exp_types/"+w.name+".json", "w") as f:
                json.dump(w.data,f)

class weaponTypes():
    def __init__(self):
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            weapon_types = json.load(weapons_file)
        self.data = weapon_types
        for wt in self.data:
            w = weaponType(wt)
            try:
                w.Load()
            except:
                print("no existing data for type" + wt)
            with open("src/skeletons/weapon_types/"+w.name+".json", "w") as f:
                json.dump(w.data,f)

class weaponType():
    def __init__(self, wtype):
        self.type = wtype
        self.skills = {}
        self.objects = []
        self.desc = ""
        self.name = self.type
        self.icon = None
        
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        
    def Save(self):
        with open("src/skeletons/weapon_types/"+self.name+".json", "w") as f:
            json.dump(self.data,f)
    
    def Load(self):
        with open("src/skeletons/weapon_types/"+self.name+".json", "r") as f:
            self.data = json.load(f)
    
    def addSkill(self,name,skill):
        self.skills[name] = skill
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()
    
    def removeSkill(self,name):
        self.skills.pop(name)
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()
    
    def changeIcon(self,icon):
        self.icon = icon
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()

    def addObject(self,name,obj):
        self.objects[name] = obj
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()

class expType():
    def __init__(self, wtype):
        self.type = wtype
        self.skills = {}
        self.objects = []
        self.desc = ""
        self.name = self.type
        self.icon = None
        
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        
    def Save(self):
        with open("src/skeletons/exp_types/"+self.name+".json", "w") as f:
            json.dump(self.data,f)
    
    def Load(self):
        with open("src/skeletons/exp_types/"+self.name+".json", "r") as f:
            self.data = json.load(f)
    
    def addSkill(self,name,skill):
        self.skills[name] = skill
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()
    
    def removeSkill(self,name):
        self.skills.pop(name)
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()
    
    def changeIcon(self,icon):
        self.icon = icon
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()

    def addObject(self,name,obj):
        self.objects[name] = obj
        self.data = {"name":self.type,"skills":self.skills,"objects":self.objects,"desc":self.desc,"icon":self.icon}
        self.Save()