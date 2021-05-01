class unitClass():
    def __init__(self):
        self.unit_class_name = None
        self._exp_to_level = 0
        self._exp_in_class = 0
        self._tactics = {}
        self._skills = {}
        self._allowed_weapon_types = []
        self._disallowed_weapon_types = []
        self._minimum_level = 0
        self._is_mounted = False
        
    @property
    def exp_to_level(self):
        return self._exp_to_level
       
    @exp_to_level.setter
    def exp_to_level(self, e):
        self._exp_to_level = e
        
    @property
    def exp_in_class(self):
        return self._exp_in_class
       
    @exp_in_class.setter
    def exp_in_class(self, e):
        self._exp_in_class = e
        
    @property
    def is_mounted(self):
        return self._is_mounted
       
    @is_mounted.setter
    def is_mounted(self, e):
        self._is_mounted = e
        
    @property
    def minimum_level(self):
        return self._exp_to_level
       
    @minimum_level.setter
    def minimum_level(self, e):
        self._minimum_level = e
        
    @property
    def tactics(self):
        return self._tactics
       
    @tactics.setter
    def tactics(self, e, v):
        self._tactics[e] = v
    
    @property
    def skills(self):
        return self._skills
       
    @skills.setter
    def skills(self, e, v):
        self._skills[e] = v
        
    @property
    def allowed_weapon_types(self):
        return self._allowed_weapon_types
       
    @allowed_weapon_types.setter
    def allowed_weapon_types(self, e):
        self._allowed_weapon_types.append(e)
    
    @property
    def disallowed_weapon_types(self):
        return self._disallowed_weapon_types
       
    @disallowed_weapon_types.setter
    def disallowed_weapon_types(self, e):
        self._disallowed_weapon_types.append(e)