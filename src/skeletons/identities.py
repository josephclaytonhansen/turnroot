class orientations():
    def __init__(self):
        self.STRAIGHT = 0
        self.BI = 1
        self.GAY = 2
        self.ACE = 3
        self.OTHER = 4

class genders():
    def __init__(self):
        self.MALE = 0
        self.FEMALE = 1
        self.OTHER = 2

class pronouns():
    def __init__(self, gender):
        if gender == 0:
            self.pronouns_direct = "he"
            self.pronouns_indirect = "him"
            self.pronouns_possessive = "his"
        elif gender == 1:
            self.pronouns_direct = "she"
            self.pronouns_indirect = "her"
            self.pronouns_possessive = "hers"
        elif gender == 2:
            self.pronouns_direct = "they"
            self.pronouns_indirect = "them"
            self.pronouns_possessive = "theirs"
        else:
            self.pronouns_direct = "!CUSTOM PRONOUNS NOT ASSIGNED!"
            self.pronouns_indirect = "!CUSTOM PRONOUNS NOT ASSIGNED!"
            self.pronouns_possessive = "!CUSTOM PRONOUNS NOT ASSIGNED!"
            
        self.pronouns = [self.pronouns_direct, self.pronouns_indirect, self.pronouns_possessive]