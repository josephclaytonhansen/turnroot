import pygame
#COMBAT FLOW
#cross-fade music
#start "in combat" timer
#record action to history
#in_combat = True


#load sprites (class + weapon + unit) onto battle surface
#load ground + background onto battle surface
#While in_combat: blit battle_surface onto fake_screen

#load skills / blit skills
#calculate unit + foe current stats (take into account skills, statues, etc)
#roll for crit
#roll for Aegis, Miracle, etc

#determine attack order (attack, counter-attack, follow-up attack)
#perform attacks- reroll each attack and blit attack sprites
#give level/weapon XP to unit

#finalize combat- level up if needed
#cross-fade music
#in_combat = False

class Fader(object):
    instances = []
    def __init__(self, fname):
        super(Fader, self).__init__()
        assert isinstance(fname, str)
        self.sound = pygame.mixer.Sound(fname)
        self.increment = 0.01 # tweak for speed of effect!!
        self.next_vol = 1 # fade to 100 on start
        Fader.instances.append(self)

    def fade_to(self, new_vol):
        # you could change the increment here based on something..
        self.next_vol = new_vol

    @classmethod
    def update(cls):
        for inst in cls.instances:
            curr_volume = inst.sound.get_volume()
            # print inst, curr_volume, inst.next_vol
            if inst.next_vol > curr_volume:
                inst.sound.set_volume(curr_volume + inst.increment)
            elif inst.next_vol < curr_volume:
                inst.sound.set_volume(curr_volume - inst.increment)

sound1 = Fader("1.wav")
sound2 = Fader("2.wav")
sound1.sound.play()
sound2.sound.play()
sound2.sound.set_volume(0)

# fading..
sound1.fade_to(0)
sound2.fade_to(1)


while True:
    Fader.update() # a call that will update all the faders..