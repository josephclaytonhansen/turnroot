import pygame
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
                if frames == animation_frames:
                    #advance transition animation by 1
                    pass
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
                if frames == animation_frames:
                    #advance transition animation by 1
                    pass
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

