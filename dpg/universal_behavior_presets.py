class Behavior():
    descriptions = {
        "foot_soldier":"",
        "airborne_knight":"",
        "mindless_creature":"",
        "cautious_healer":"",
        "strategic_assassin":"",
        "distance_sniper":"",
        "vengeful_demon":"",
        "strategic_leader":"",
        "greedy_thief":"",
        "cowardly_villager":"",
    }
    behaviors = {
        "foot_soldier":"",
        "airborne_knight":"",
        "mindless_creature":"",
        "cautious_healer":"",
        "strategic_assassin":"",
        "distance_sniper":"",
        "vengeful_demon":"",
        "strategic_leader":"",
        "greedy_thief":"",
        "cowardly_villager":"",
    }
    def __init__(self, tag):
        self.tag = tag
        tmp = self.tag.split("_")
        self.pretty_name = tmp[0].capitalize() + " " + tmp[1].capitalize() 
        self.desc = self.descriptions[self.tag]
        self.behavior = self.behaviors[self.tag]
    
    def is_me(self, pretty):
        if pretty == self.pretty_name or pretty == self.tag:
            return True
        
foot_soldier = Behavior("foot_soldier")
airborne_knight = Behavior("airborne_knight")
mindless_creature = Behavior("mindless_creature")
cautious_healer = Behavior("cautious_healer")
strategic_assassin = Behavior("strategic_assassin")
distance_sniper = Behavior("distance_sniper")
vengeful_demon = Behavior("vengeful_demon")
strategic_leader = Behavior("strategic_leader")
greedy_thief = Behavior("greedy_thief")
cowardly_villager = Behavior("cowardly_villager")

behavioral_presets = [foot_soldier, airborne_knight, mindless_creature, cautious_healer, strategic_assassin,
                      distance_sniper, vengeful_demon, strategic_leader, greedy_thief, cowardly_villager]
