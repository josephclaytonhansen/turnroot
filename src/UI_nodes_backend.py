import os
GET_FILES = 1
GET_FOLDERS = 0

class File(object):
    def __init__(self, path):
        self.path = path
        self.getDepth()
        self.getExt()
        self.getName()
        self.getDir()

    def getDepth(self):
        self.depth = self.path.count("/")

    def getExt(self):
        self.ext = self.path[self.path.rfind("."):]

    def getName(self):
        self.name = self.path[self.path.rfind("/")+1:self.path.rfind(".")]

    def getDir(self):
        self.dir = self.path[:self.path.rfind("/")]+"/"
        
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
    
