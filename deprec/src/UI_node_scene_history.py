from src.UI_node_edge import QDMGraphicsEdge


DEBUG = False


class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 32

    def undo(self):
        pass

    def redo(self):
        pass


    def restoreHistory(self):
        pass


    def storeHistory(self, desc, setModified=False):
        pass
    def createHistoryStamp(self, desc):
        pass

    def restoreHistoryStamp(self, history_stamp):
        pass
