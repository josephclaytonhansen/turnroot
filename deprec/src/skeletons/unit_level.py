class Level():
    def __init__(self):
        self._exp_to_level = 0
        self.level = 0
    @property
    def exp_to_level(self):
        return self._exp_to_level
       
    @exp_to_level.setter
    def exp_to_level(self, e):
        self._exp_to_level = e