class weaponExperience():
    def __init__(self):
        self.weapon_type = None
        self._exp_to_level = 0
        self._exp = 0
        
    @property
    def exp_to_level(self):
        return self._exp_to_level
       
    @exp_to_level.setter
    def exp_to_level(self, e):
        self._exp_to_level = e

    @property
    def exp(self):
        return self._exp
       
    @exp.setter
    def exp(self, e):
        self._exp = e