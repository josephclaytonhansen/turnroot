import pygame
from src.GAME_battle_map_graphics_backend import overlayOver, C
from src.GAME_battle_map_sounds_backend import updateVolumes

def initOptions(parent):
    parent.labels = ["SFX volume","Music volume","Voices volume","Cutscene subtitles",
                     "End turn","Cursor memory","Cursor speed","Cursor overlay","Show grid","HP gauge type","X axis inverted","Y axis inverted"]
    parent.hp_holder = ["None", "Basic", "Advanced"]

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
            parent.fake_screen.blit(right_arrow.image,(start_pos[0]+570,start_pos[1]-5))
            
            #change value- first three are sliders
            if count == 1:
                parent.music_max_volume += parent.options_cursor_x_change / 100
                if parent.music_max_volume > 1:
                    parent.music_max_volume = 1
                parent.options_cursor_x_change = 0
            elif count == 0:
                parent.sfx_max_volume += parent.options_cursor_x_change / 100
                if parent.sfx_max_volume > 1:
                    parent.sfx_max_volume = 1
                parent.options_cursor_x_change = 0
            elif count == 2:
                parent.voices_max_volume += parent.options_cursor_x_change / 100
                if parent.voices_max_volume > 1:
                    parent.voices_max_volume = 1
                parent.options_cursor_x_change = 0
            
            #I tried making this a loop but for some reason it kept running into issues, I think the game loop conflicted with it, so whatever
            elif count == 3: #cutscene subtitles- the first true/false option
                if parent.options_cursor_x_change != 0:
                    if C.subtitles == True:
                        C.subtitles = False
                    elif C.subtitles == False:
                        C.subtitles = True
                parent.options_cursor_x_change = 0
            
            elif count == 4: #smart end
                if parent.options_cursor_x_change != 0:
                    if C.smart_end == True:
                        C.smart_end = False
                    elif C.smart_end == False:
                        C.smart_end = True
                parent.options_cursor_x_change = 0
            
            elif count == 5: #cursor_memory
                if parent.options_cursor_x_change != 0:
                    if C.cursor_memory == True:
                        C.cursor_memory = False
                    elif C.cursor_memory == False:
                        C.cursor_memory = True
                parent.options_cursor_x_change = 0
            
            elif count == 6: #cursor_speed: this one is not a slider, but a number
                C.cursor_speed -= parent.options_cursor_x_change
                if C.cursor_speed > 100:
                    C.cursor_speed = 100
                if C.cursor_speed < 0:
                    C.cursor_speed = 0
                parent.options_cursor_x_change = 0
                
            elif count == 7: #cursor_overlay
                if parent.options_cursor_x_change != 0:
                    if C.CURSOR_OVER == True:
                        C.CURSOR_OVER = False
                    elif C.CURSOR_OVER == False:
                        C.CURSOR_OVER = True
                parent.options_cursor_x_change = 0
    
            elif count == 8: #GRID_OVER- there's currently no grid
                pass
            
            elif count == 9: #HP gauge- three options
                if parent.options_cursor_x_change != 0:
                    index = int(parent.options_cursor_x_change/5)
                    current_index = parent.hp_holder.index(C.hp_gauge_type)
                    current_index += index
                    if current_index > 2:
                        current_index = 0
                    if current_index < 0:
                        current_index = 2
                    C.hp_gauge_type = parent.hp_holder[current_index]
                parent.options_cursor_x_change = 0
        
            elif count == 10: #x_axis
                if parent.options_cursor_x_change != 0:
                    C.axis_changed = True
                    if C.x_axis == True:
                        C.x_axis = False
                    elif C.x_axis == False:
                        C.x_axis = True
                parent.options_cursor_x_change = 0
            
            elif count == 11: #y_axis
                if parent.options_cursor_x_change != 0:
                    C.axis_changed = True
                    if C.y_axis == True:
                        C.y_axis = False
                    elif C.y_axis == False:
                        C.y_axis = True
                parent.options_cursor_x_change = 0
   
        #for sliders do all the graphics for that
        SELECTED_COLOR = "WHITE"
        NORMAL_COLOR = "LIGHT_GRASS"
        if count < 3:
            img = overlayOver(image64="app/app_imgs/overlays/options_slider_back.png",image32="app/app_imgs/overlays/options_slider_back.png")
            parent.fake_screen.blit(img.image, (start_pos[0]+260, start_pos[1]+3))
            #Use parent.option_slider_edit to lock - currently, these values update all the time, so it's impossible to change the sliders
            if count == 1:
                p = 6
                for x in range(round(parent.music_max_volume*140)):
                    p+= 2
                    bar = overlayOver(image64="app/app_imgs/overlays/options_slider_bar.png",image32="app/app_imgs/overlays/options_slider_bar.png")
                    parent.fake_screen.blit(bar.image, (start_pos[0]+260+p, start_pos[1]+3))
            elif count == 0:
                p = 6
                for x in range(round(parent.sfx_max_volume*140)):
                    p+= 2
                    bar = overlayOver(image64="app/app_imgs/overlays/options_slider_bar.png",image32="app/app_imgs/overlays/options_slider_bar.png")
                    parent.fake_screen.blit(bar.image, (start_pos[0]+260+p, start_pos[1]+3))
            elif count == 2:
                p = 6
                for x in range(round(parent.voices_max_volume*140)):
                    p+= 2
                    bar = overlayOver(image64="app/app_imgs/overlays/options_slider_bar.png",image32="app/app_imgs/overlays/options_slider_bar.png")
                    parent.fake_screen.blit(bar.image, (start_pos[0]+260+p, start_pos[1]+3))
                    
        #tried making this a loop too, the darn thing 
        elif count == 3:
            if C.subtitles == True:
                t = "Yes"
            if C.subtitles == False:
                t = "No"
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+390,start_pos[1]+1))
        elif count == 4:
            if C.smart_end == True:
                t = "Automatically"
                h = 356
            if C.smart_end == False:
                t = "Manually"
                h = 370
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+h,start_pos[1]+1))
        elif count == 5:
            if C.cursor_memory == True:
                t = "Start on last"
                h = 358
            if C.cursor_memory == False:
                t = "Start on leader"
                h = 350
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+h,start_pos[1]+1))
        elif count == 6:
            t = str((100-C.cursor_speed))
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+390,start_pos[1]+1))
        elif count == 7:
            if C.CURSOR_OVER == True:
                t = "Show"
            if C.CURSOR_OVER == False:
                t = "Hide"
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+380,start_pos[1]+1))
        elif count == 8:
            pass
        elif count == 9:
            t = C.hp_gauge_type
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+380,start_pos[1]+1))
        elif count == 10:
            if C.x_axis == True:
                t = "Yes"
            if C.x_axis == False:
                t = "No"
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+380,start_pos[1]+1))
        elif count == 11:
            if C.y_axis == True:
                t = "Yes"
            if C.y_axis == False:
                t = "No"
            if count != parent.active_options_index:
                tf = parent.fonts["SERIF_16"].render(t, 1, parent.colors["LIGHT_GRASS"])
            else:
                tf = parent.fonts["SERIF_16"].render(t, 1, SELECTED_COLOR)
            parent.fake_screen.blit(tf,(start_pos[0]+380,start_pos[1]+1))
                
        text = parent.fonts["SERIF_16"].render(label, 1, parent.colors["CREAM"])
        parent.fake_screen.blit(text,start_pos)
    
        
        
