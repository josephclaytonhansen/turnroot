import os
GET_FILES = 1
GET_FOLDERS = 0

class File(object):
    def __init__(self, path):
        self.path = path
        self.fullPath = self.path
        self.getDepth()
        self.getExt()
        self.getName()
        self.getDir()
        

    def getDepth(self):
        self.depth = self.path.count("\\")

    def getExt(self):
        self.ext = self.path[self.path.rfind("."):]

    def getName(self):
        self.name = self.path[self.path.rfind("\\")+1:self.path.rfind(".")]

    def getDir(self):
        self.dir = self.path[:self.path.rfind("\\")]
        
def getFiles(path):
    folders = []
    docs = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            p = os.path.join(root, name)
            docs.append(File(p))
        for name in dirs:
            folders.append(os.path.join(root, name))
    return [folders, docs]

def condenseList(file_list, params):
    counter = -1
    pin = None
    i_pin = None
    
    for i in range(len(file_list)):
        item = file_list[params[i]]
        counter +=1
        if item != None and pin == None: #if slot is filled and there's no pin, move to the next row
            pass
            
        elif item == None and pin == None: #if slot is empty and there's not pin, set pin
            pin = params[counter]
            i_pin = counter
        
        elif item != None and pin != None: #if slot is filled and there's a pin, move this item up
            item.grListItem.setY(pin)
            for k in item.flags:
                k.grFlag.setPos(*k.list_item.getFlagPosition(i_pin, k.position))
            item.grListItem.update()
            pin = None
            i_pin = None
        
        elif item == None and pin != None: #if item is empty and there is a pin, move to the next row
            pass
    
#     for item in file_list:
#         if item == None:
#             file_list.remove(item)


            