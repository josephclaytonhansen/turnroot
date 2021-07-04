import pygame
from src.GAME_battle_map_graphics_backend import C
def Fade(parent):
    d = parent.music_fade[1]
    animation_frames = round(parent.music_max_volume*100/12)
    frames = 0
    if d == "in":
        rain_s = parent.music_max_volume
        thunder_s = 0.0
        now = pygame.time.get_ticks()
        parent.music_fade[0] = True
        #PULL UP NEW SCREEN
        increment = int(12 * ((parent.clock.get_fps()/60)))
        fc = 0
        tf = parent.music_max_volume /100

        while thunder_s < parent.music_max_volume:
            if pygame.time.get_ticks() - now > increment:
                rain_s -=.01
                thunder_s += .01
                frames += 1
                parent.rain.set_volume(rain_s)
                parent.thunder.set_volume(thunder_s)
                now = pygame.time.get_ticks()
    elif d == "out":
        thunder_s = parent.music_max_volume
        rain_s = 0.0
        now = pygame.time.get_ticks()
        parent.music_fade[0] = True
        #PULL UP NEW SCREEN
        increment = int(12 * ((parent.clock.get_fps()/60)))
        while rain_s < parent.music_max_volume:
            if pygame.time.get_ticks() - now > increment:
                thunder_s -=.01
                rain_s += .01
                frames += 1
                parent.rain.set_volume(rain_s)
                parent.thunder.set_volume(thunder_s)
                now = pygame.time.get_ticks()
    elif d == "init":
        rain_s = 0.0
        now = pygame.time.get_ticks()
        parent.music_fade[0] = True
        increment = int(12 * ((parent.clock.get_fps()/60)))
        while rain_s < parent.music_max_volume:
            if pygame.time.get_ticks() - now > increment:
                rain_s += .01
                parent.rain.set_volume(rain_s)
                now = pygame.time.get_ticks()

    
def initMusic(parent,s):
    parent.rain = pygame.mixer.Sound("app/app_sounds/music/"+s+"_rain"+".mp3")
    parent.thunder = pygame.mixer.Sound("app/app_sounds/music/"+s+"_thunder"+".mp3")
    parent.special_music1 = None
    parent.special_music2 = None
    parent.special_music3 = None
    parent.special_music4 = None
    #these blank slots allow for a boss theme- rain/thunder- and two other songs, which should be enough?
    parent.rain.play(-1)
    parent.thunder.play(-1)
    
    parent.rain.set_volume(0)
    parent.thunder.set_volume(0)
    parent.menu_move = pygame.mixer.Sound("app/app_sounds/menu_move.wav")
    parent.menu_confirm = pygame.mixer.Sound("app/app_sounds/menu_confirm.wav")
    parent.transition_sound_combat = pygame.mixer.Sound("app/app_sounds/Swoosh.mp3")
    
def updateVolumes(parent):
    #Call this on volume settings change!
    for s in [parent.menu_move, parent.menu_confirm, parent.transition_sound_combat]:
        s.set_volume(parent.sfx_max_volume)
    for m in [parent.rain]:
        m.set_volume(parent.music_max_volume)
    C.sfx_max_volume = round(parent.sfx_max_volume,3)
    C.music_max_volume = round(parent.music_max_volume,3)
    C.max_voices_volume = round(parent.voices_max_volume,3)
    C.pack()


