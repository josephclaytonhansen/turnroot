import pygame
from src.GAME_battle_map_graphics_backend import overlayOver, C

def initOptions(parent):
    parent.labels = ["SFX volume","Music volume","Voices volume","Cutscene subtitles",
                     "Smart end","Cursor memory","Cursor speed","Cursor overlay","Show grid","HP gauge type","X axis","Y axis"]
    
    parent.labels_to_options =  {"SFX volume":C.sfx_max_volume,
                             "Music volume":C.music_max_volume,
                             "Voices volume":C.max_voices_volume,
                             "Music choice":C.uc_music,
                             "Cutscene subtitles":C.subtitles,
                             "Smart end":C.smart_end,
                             "Cursor memory":C.cursor_memory,
                             "Cursor speed":C.cursor_speed,
                             "Cursor overlay":C.CURSOR_OVER,
                             "Show grid":C.GRID_OVER,
                             "HP gauge type":C.hp_gauge_type,
                             "X Axis":C.x_axis,
                             "Y Axis":C.y_axis}

def showOptions(parent):
    pos = [322,166]
    start_pos = [350,142]
    img = overlayOver(image64="app/app_imgs/overlays/options_back.png",image32="app/app_imgs/overlays/options_back.png")
    parent.fake_screen.blit(img.image, pos)
    count = -1

    for label in parent.labels:
        start_pos[1] += 40
        count += 1

        
        
        if count == parent.active_options_index:
            img = overlayOver(image64="app/app_imgs/overlays/options_active_row.png",image32="app/app_imgs/overlays/options_active_row.png")
            parent.fake_screen.blit(img.image, (start_pos[0]-20, start_pos[1]-8))
            left_arrow = overlayOver(image64="app/app_imgs/overlays/preferences_arrow_left.png",image32="app/app_imgs/overlays/preferences_arrow_left.png")
            right_arrow = overlayOver(image64="app/app_imgs/overlays/preferences_arrow_right.png",image32="app/app_imgs/overlays/preferences_arrow_right.png")
            parent.fake_screen.blit(left_arrow.image,(start_pos[0]+200,start_pos[1]-5))
            parent.fake_screen.blit(right_arrow.image,(start_pos[0]+500,start_pos[1]-5))
        
        text = parent.fonts["SERIF_16"].render(label, 1, parent.colors["CREAM"])
        parent.fake_screen.blit(text,start_pos)
    
        
        
