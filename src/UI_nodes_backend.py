import os
GET_FILES = 1
GET_FOLDERS = 0
NODE_FILE_EXTENSION = ".trnep"

class File(object):
    def __init__(self, path):
        self.path = path
        self.depth = self.path.count("/")
        self.ext = self.path[self.path.rfind("."):]
        self.name = self.path[self.path.rfind("/")+1:self.path.rfind(".")]
        self.dir = self.path[:self.path.rfind("/")]+"/"
        if self.ext == NODE_FILE_EXTENSION:
            self.outliner = True
        else:
            self.outliner = False
        
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
    
