class Behavior():
    descriptions = {
        "foot_soldier":"A simple soldier whose goal is to attack.\nMoves with their group (influenced by Soldier/Lone Wolf).\nStopped by walls, slight chance to avoid slow and danger tiles (influenced by Cautious/Brash).\nHas no movement restrictions, gains normal terrain advantages.",
        "airborne_knight":"A flying unit that travels alone (influenced by Soldier/Lone Wolf).\nIs only stopped by Tall Walls.\nIs not affected by slow or danger tiles.\nDoes not receive terrain advantages.\nAvoids dangerous encounters (influenced by Strategic/Mindless).",
        "mindless_creature":"A mindless creature that attacks whatever it can reach.\nGenerally does not travel in groups or think strategically (influenced by sliders.)\nGenerally does not avoid slow and danger tiles (influenced by Cautious/Brash).\nIs stopped by walls and receives terrain advantages.",
        "cautious_healer":"A cautious unit that avoids being alone and hangs behind the front lines.\nAvoids combat, preferring to heal (influenced by Soldier/Lone Wolf).\nIs stopped by walls, receives terrain advantages.\nAvoids slow and damage tiles generally (influenced by Cautious/Brash).",
        "strategic_assassin":"A skillful killer who fights alone and slips into the darkness.\nGenerally avoids groups and dangerous encounters (influenced by sliders).\nGenerally avoids damage tiles, does not avoid slow tiles.\nStopped by walls, normal terrain advantages.\nGenerally prefers attacks where it has weapon advantage.",
        "distance_sniper":"A cautious unit that avoids being alone (influenced by Soldier/Lone Wolf) and hangs behind.\nIs stopped by walls, recieves terrain advantages.\nGenerally prefers attacks where it has weapon advantage (influenced by Strategic/Mindless).\nAvoids damage tiles, does not avoid slow tiles generally.",
        "strategic_leader":"Prefers attacks where it has weapon advantage.\nPrefers a group (influenced by Soldier/Lone Wolf).\nIs stopped by walls, avoids slow and damage tiles generally.\nGains terrain advantages",
        "cowardly_villager":"Avoids fighting at all costs.\nIs stopped by walls and receives terrain advantages.\nGenerally does not avoid damage or slow tiles (influenced by Strategic/Mindless).",
    }
    behaviors = {
        "foot_soldier":"",
        "airborne_knight":"",
        "mindless_creature":"",
        "cautious_healer":"",
        "strategic_assassin":"",
        "distance_sniper":"",
        "strategic_leader":"",
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
strategic_leader = Behavior("strategic_leader")
cowardly_villager = Behavior("cowardly_villager")

behavioral_presets = [foot_soldier, airborne_knight, mindless_creature, cautious_healer, strategic_assassin,
                      distance_sniper, strategic_leader, cowardly_villager]
