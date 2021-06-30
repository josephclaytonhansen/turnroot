import pygame, sys, random, json
from src.GAME_battle_map_graphics_backend import (cursorOver, gridOver, moveOver, damageOver, C, overlayOver, showTileTexts64, Tile, gUnit, TILE_CONTENTS,
FRIEND, ENEMY, ALLY, TILE, showMenuTiles, showMenuCursor, initMenuItems, CURRENT_MENU_TILES, initGrid, initFont)
from src.GAME_battle_map_sounds_backend import Fade, initMusic, updateVolumes
from src.GAME_battle_map_options_backend import initOptions, showOptions

GRID_COLOR = "white"
COLORS = {"CREAM":(238,238,230),"BLACK":(0,0,0),"WHITE":(255,255,255), "NID_PINK":(255,0,255),"MUTED_NAVY":(57,65,89), "MUTED_FOREST":(53,89,78), "LIGHT_GRASS":(153,207,174)}

class sandbox():
    def __init__(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        super().__init__()
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()
        self.initMainWindow(dimensions, title, initial_bg, icon, bar_bg, cursor_speed)
    
    def initInitialValues(self, dimensions, cursor_speed):
        self.scales=[1.8,2.3,3]
        self.scale = 1
        self.show_grid_at_scale = True
        self.cursor_pos = [0,0]
        self.tile_pos = [0,0]
        self.tile_offset = [0,0]
        self.current_tile = [0,0]
        self.cursor_x_change = 0
        self.cursor_y_change = 0
        self.cursor_history = []
        self.moved = False
        self.unit_selected = False
        self.tmp_cursor = [0,0]
        #get from unit
        self.xp_amount = 1
        self.level_number = 1
        
        self.colors = COLORS
         
        self.toggle_full_key = "Q"
        self.toggle_full_key_text = "Basic overlay"
        
        self.toggle_menu_key = "Z"
        self.toggle_menu_text = "Menu"
        
        self.toggle_danger_key = "W"
        self.toggle_danger_text = "Show danger area"
        
        self.dimensions = dimensions
        self.last_cursor_move = pygame.time.get_ticks()
        self.last_input = pygame.time.get_ticks()
        self.idle = False
        
        self.tiles = {}
        
        self.tile_group = pygame.sprite.Group()
        self.on_screen_units = pygame.sprite.Group()
        self.move_over_group = pygame.sprite.Group()
        self.graphics = pygame.sprite.Group()
        
        self.units_pos = {}
        self.current_unit = None
        
        self.cursor_move_cooldown = cursor_speed
        self.idle_cooldown = 1400
        self.clock = pygame.time.Clock()
        
        self.music_fade = [False, "init"]
        self.music_max_volume = C.music_max_volume
        self.sfx_max_volume = C.sfx_max_volume
        
        self.show_combat = False
        self.combat_transition = False
        self.fc = 0
        
        self.show_menu = False
        self.action_confirmed = False
        self.menu_cursor = False
        self.active_menu_index = 0
        self.menu_cursor_y_change = 0
        self.current_menu_length = 11
        self.menu_sound_played = False
        self.menu_active = False
        
        self.show_options = False
        self.show_overlays = True
        self.active_options_index = 0
        self.option_cursor = False

    def initMainWindow(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        #load variables and constants
        self.initInitialValues(dimensions, cursor_speed)
        initGrid(self)
        initFont(self)
        initOptions(self)
        
        #init screen
        screen = pygame.display.set_mode(self.dimensions, flags=(pygame.RESIZABLE))
        fake_screen = screen.copy()
        self.camera = fake_screen.get_rect()
        self.fake_screen = fake_screen
        self.screen = screen
        self.icon = icon
        running = True
        
        self.c_over = cursorOver(192,192,GRID_COLOR)
        
        if C.scale == 64:
            self.c_img = pygame.image.load("app/app_imgs/64cursor.png")
        
        self.fake_rect = self.fake_screen.get_rect()
        self.screen_rect = self.screen.get_rect()
        
        initMusic(self,"fw")
        Fade(self)
        
        self.initCombat()
        
        pygame.display.set_caption(title)
        #i = pygame.image.load(icon)
        #pygame.display.set_icon(i)

        #Game loop
        while running:
            self.clock.tick(C.fps)
            #idle timer
            now = pygame.time.get_ticks()
            if now - self.last_input >= self.idle_cooldown:
                self.idle = True   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                
                #Key press
                if event.type == pygame.KEYDOWN:
                    self.last_input = pygame.time.get_ticks()
                    self.idle = False
                    if event.key == pygame.K_UP:
                        if self.menu_cursor == False:
                            self.moved = True
                            self.cursor_y_change = -C.scale
                        else:
                            self.menu_cursor_y_change -= 55
                            self.menu_sound_played = False
                    elif event.key == pygame.K_DOWN:
                        if self.menu_cursor == False:
                            self.cursor_y_change = C.scale
                            self.moved = True
                        else:
                            self.menu_cursor_y_change += 55
                            self.menu_sound_played = False
                    elif event.key == pygame.K_LEFT:
                        if self.menu_cursor == False:
                            self.cursor_x_change = -C.scale
                            self.moved = True
                    elif event.key == pygame.K_RIGHT:
                        if self.menu_cursor == False:
                            self.cursor_x_change = C.scale
                            self.moved = True
                    #A key
                    elif event.key == pygame.K_a:
                        t = self.tiles[self.tile_pos[0]][self.tile_pos[1]]
                        
                        if self.unit_selected:
                            #if unit selected, "move" unit (really, confirm unit movement by deselecting the unit)
                            #This line turns on the menu for action selection
                            self.show_menu = True
                            #move cursor off grid and onto menu
                            self.menu_cursor = True
                            #select menu item
                            if self.menu_cursor:
                                if self.menu_active: #based on menu selection, do...
                                    self.show_overlays = False
                                    action = CURRENT_MENU_TILES[self.active_menu_index]
                                    #Attack- Currently put unit down, fade into battle. Eventually it needs to select weapon, enemy, and THEN do all that. 
                                    if action == CURRENT_MENU_TILES[0]:
                                        self.action_confirmed = True
                                        self.transition_sound_combat.play()
                                        self.music_fade[1] = "in"
                                        Fade(self)
                                        self.show_combat = True
                                    #Wait- put unit down and move on
                                    elif action == CURRENT_MENU_TILES[3]:
                                        self.action_confirmed = True
                                    #Options- essentially do the whole menu thing all over again with Options
                                    elif action == CURRENT_MENU_TILES[10]:
                                        self.show_options = True
                                        self.menu_active = False
                                        self.show_menu = False
                                        self.menu_cursor = False
                                        self.option_cursor = True

                            #this line confirms the action and moves on, so it has to be after the menu
                            if self.action_confirmed:
                                self.current_unit = None
                                self.menu_active = False
                                self.show_overlays = True
                            
                        #if a unit is selected, we confirm the movement and ...take an action... but for now we deselect
                        if self.unit_selected == False:
                            self.Select()
                        else:
                            if self.action_confirmed:
                                self.Deselect()
                        
                    #scale map
                    elif event.key == pygame.K_x:
                        self.scale +=1
                        if self.scale == 3:
                            self.scale = 0
                        if self.scale < 2:
                            self.show_grid_at_scale = False
                        else:
                            self.show_grid_at_scale = True
                    #'B' key
                    elif event.key == pygame.K_s:
                        if self.unit_selected:
                            self.menu_active = False
                            self.Deselect()
                        #replace else with elif for different selection cases
                        else:
                            print("nothing selected")
                    #fade out- replace trigger later
                    elif event.key == pygame.K_m:
                        if self.unit_selected:
                            self.show_combat = True
                            self.combat_transition = True
                            self.music_fade[1] = "out"
                            Fade(self)
                    
                    #Shoulder, maybe? Toggle overlay mode
                    elif event.key == pygame.K_q:
                        if self.unit_selected:
                            if C.SELECTION_OVERLAY_TYPE == "full":
                                C.SELECTION_OVERLAY_TYPE = "small"
                                self.toggle_full_key_text = "Full overlay"
                            else:
                                C.SELECTION_OVERLAY_TYPE = "full"
                                self.toggle_full_key_text = "Basic overlay"

                #Key release
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        self.cursor_history = []
                        self.moved = False
                        self.cursor_x_change = 0
                        self.cursor_y_change = 0
                        
                #Handle screen size
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((int(event.size[0]), int(event.size[1])), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    self.screen_rect = self.screen.get_rect()
            
            screen.fill(bar_bg)
            self.fake_screen.fill(initial_bg)
            
            #draw grid
            self.tile_group.draw(self.fullmap)
            #draw units on grid
            self.on_screen_units.draw(self.fullmap)
            
            #draw cursor
            self.showCursor()
                
            #draw map
            self.fullmap_scaled = pygame.transform.scale(self.fullmap, (int(self.scales[self.scale] * self.fake_screen.get_width()), int(self.scales[self.scale] * self.fake_screen.get_height())))
            self.fake_screen.blit(self.fullmap_scaled, (0,0), self.camera)
            
            #draw overlays and overlay text
            if self.show_overlays:
                self.showOverlays()
                showTileTexts64(self)
                        
            #show combat
            if self.show_combat:
                self.combat_transition = True
                last_frame = pygame.time.get_ticks()
                #start transition
                frames = ["00405","00407", "00409","00411", "00413", "00415", "00417", "00419", "00421", "00423", "00425", "00427"]
                
                frame = frames[self.fc]
                foreground = self.fake_screen
                background = self.combat_surface
                mask = pygame.image.load("app/app_imgs/transitions/map_to_combat/scene"+frame+".png").convert_alpha()
                self.fake_screen.blit(foreground, (0,0))
                masked = background.copy()
                masked.set_colorkey((0,0,0))
                masked.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
                self.fake_screen.blit(masked, (0, 0))
                
                #next frame
                if self.combat_transition:
                    if self.music_fade[1] == "in":
                        if pygame.time.get_ticks() - last_frame > 1:
                            self.fc += 1
                            if self.fc == 12:
                                #transition complete
                                self.combat_transition = False
                                self.fc = 11
                            frame = frames[self.fc]
                            last_frame = pygame.time.get_ticks()
                    elif self.music_fade[1] == "out":
                        if pygame.time.get_ticks() - last_frame > 1:
                            self.fc -= 1
                            if self.fc == -1:
                                #transition complete
                                self.combat_transition = False
                                self.fc = 0
                            frame = frames[self.fc]
                            last_frame = pygame.time.get_ticks()
            
            #show menu, if needed
            if self.show_menu:
                showMenuTiles(self)
                #if menu is selected, draw the cursor on it 
                if self.menu_cursor:
                    initMenuItems(self)
                    showMenuCursor(self)
                    self.menu_active = True
                
            #show options, if needed
            if self.show_options:
                showOptions(self)
                
            #fit screen to screen
            if self.screen_rect.size != self.dimensions:
                fit_to_rect = self.fake_rect.fit(self.screen_rect)
                fit_to_rect.center = self.screen_rect.center
                scaled = pygame.transform.smoothscale(self.fake_screen, fit_to_rect.size)
                self.screen.blit(scaled, fit_to_rect)
            else:
                self.screen.blit(self.fake_screen, (0,0))

            pygame.display.update()

    def showOverlays(self):
        ground_desc = overlayOver(image64="app/app_imgs/overlays/64tile_desc_001.png",image32="app/app_imgs/overlays/32tile_desc_001.png")
        tile_name = overlayOver(image64="app/app_imgs/overlays/64tile_name_001.png",image32="app/app_imgs/overlays/32tile_name_001.png")

        self.fake_screen.blit(ground_desc.image, C.OVERLAY_PLACEMENTS64[0])
        self.fake_screen.blit(tile_name.image, C.OVERLAY_PLACEMENTS64[1])

        guard = overlayOver(image64=C.GUARD_ICON,image32=C.GUARD_ICON32)
        avoid = overlayOver(image64=C.AVOID_ICON,image32=C.AVOID_ICON32)
        heal = overlayOver(image64=C.HEAL_ICON,image32=C.HEAL_ICON32)
        
        self.fake_screen.blit(guard.image, C.OVERLAY_PLACEMENTS64[3])
        self.fake_screen.blit(avoid.image, C.OVERLAY_PLACEMENTS64[4])
        self.fake_screen.blit(heal.image, C.OVERLAY_PLACEMENTS64[5])
        
        if self.idle:
            toggle_full_selection = overlayOver(image64=C.KEY_OVER,image32=C.KEY_OVER32)
            toggle_damage = overlayOver(image64=C.KEY_OVER,image32=C.KEY_OVER32)
            show_menu = overlayOver(image64=C.KEY_OVER_WIDE,image32=C.KEY_OVER32)

            self.fake_screen.blit(toggle_full_selection.image, C.OVERLAY_PLACEMENTS64[22])
            self.fake_screen.blit(toggle_damage.image, C.OVERLAY_PLACEMENTS64[23])
            self.fake_screen.blit(show_menu.image, C.OVERLAY_PLACEMENTS64[24])
            
        if self.unit_selected:
            if C.SELECTION_OVERLAY_TYPE == "full":
                unit_info = overlayOver(image64="app/app_imgs/overlays/unit_info_001.png", image32="app/app_imgs/overlays/32unit_info_001.png")

                self.fake_screen.blit(unit_info.image, C.OVERLAY_PLACEMENTS64[10])

                xp_bar = overlayOver(image64="app/app_imgs/overlays/xp_bar_001.png", image32="app/app_imgs/overlays/32xp_bar_001.png")
                xp_crest = overlayOver(image64="app/app_imgs/overlays/xp_crest_001.png", image32="app/app_imgs/overlays/32xp_crest_001.png")
                xp_count = 0
                for x in range(int(((2*self.xp_amount)*(148/244)))):
                    xp_count +=1
                    xp_amount = overlayOver(image64="app/app_imgs/overlays/xp_bar_progress_001.png", image32="app/app_imgs/overlays/32xp_bar_progress_001.png")
                    self.fake_screen.blit(xp_amount.image, (C.OVERLAY_PLACEMENTS64[21][0]+(2*xp_count),C.OVERLAY_PLACEMENTS64[21][1]))
                    self.fake_screen.blit(xp_bar.image, C.OVERLAY_PLACEMENTS64[11])
                    self.fake_screen.blit(xp_crest.image, C.OVERLAY_PLACEMENTS64[11])
            else:
                unit_info = overlayOver(image64="app/app_imgs/overlays/unit_info_small_001.png", image32="app/app_imgs/overlays/32unit_info_small_001.png")
                self.fake_screen.blit(unit_info.image, C.OVERLAY_PLACEMENTS64[17])
        
    #update cursor/selected overlays
    def showCursor(self):
        #move cursor on menu
        if self.menu_cursor:
            if self.menu_sound_played == False:
                self.menu_move.play()
                self.menu_sound_played = True
            #cursor boundaries
            if int(self.menu_cursor_y_change/55) >= self.current_menu_length:
                self.active_menu_index = self.current_menu_length
                self.menu_cursor_y_change = 0
            elif int(self.menu_cursor_y_change/55) <= 0:
                self.active_menu_index = 0
                self.menu_cursor_y_change = 0
            else:
                self.active_menu_index = int(self.menu_cursor_y_change/55)
        #move cursor on options
        elif self.option_cursor:
            pass
        #move cursor on grid
        else:
            now = pygame.time.get_ticks()
            self.current_tile_index = self.tile_pos[0]+(self.tile_pos[1]*C.grid_dimensions[1])
            self.tile_pos[0] = int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]
            self.tile_pos[1] = int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]
            self.tmp_cursor = self.cursor_pos.copy()
            
            for j in self.move_over_group:
                self.fullmap.blit(j.image,(j.x,j.y))
            self.on_screen_units.draw(self.fullmap)
            
            if now - self.last_cursor_move >= self.cursor_move_cooldown:
                self.cursor_pos[0] += self.cursor_x_change
                self.cursor_pos[1] += self.cursor_y_change
                #Move unit if selected
                if self.current_unit != None:
                    #Currently the unit moves with the cursor, this is obviously not ideal but for sandboxing it's much easier than messing with A*
                    tmp_unit = self.current_unit
                    self.units_pos[self.current_unit.x][self.current_unit.y] = None
                    self.current_unit.kill()
                    tmp_unit.x = int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]
                    tmp_unit.y = int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]
                    self.units_pos[int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]][int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]] = tmp_unit
                    tmp_unit.animateSprites()
                    self.on_screen_units.add(tmp_unit)
                    
                if self.moved:
                    self.cursor_history.append([self.cursor_x_change,self.cursor_y_change])
            
                self.tile_pos[0] = int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]
                self.tile_pos[1] = int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]

                if self.cursor_pos[0] < 0:
                    self.cursor_pos[0] = 0
                if self.tile_pos[0] >= C.grid_dimensions[0]-1:
                    self.cursor_pos[0] = int((C.grid_dimensions[0]-1)*C.scale/(self.scales[self.scale]/2))
                if self.cursor_pos[1] < 0:
                    self.cursor_pos[1] = 0
                if self.tile_pos[1] >= C.grid_dimensions[1]-1:
                    self.cursor_pos[1] = int((C.grid_dimensions[1]-1)*C.scale/(self.scales[self.scale]/2))
                    
                if self.unit_selected:
                    t = (self.tile_pos[0], self.tile_pos[1])
                    if t not in self.move_tiles:
                        self.cursor_pos = self.tmp_cursor
                
                if len(self.cursor_history) > 3:
                    camera_pan_direction = self.cursor_history[0]
                    h_speed = C.scale
                    v_speed = C.scale
                    if camera_pan_direction[0] == -C.scale:
                        self.camera.x -=h_speed
                    elif camera_pan_direction[0] == C.scale:
                        self.camera.x +=h_speed
                    if camera_pan_direction[1] == C.scale:
                        self.camera.y +=v_speed
                    elif camera_pan_direction[1] == -C.scale:
                        self.camera.y -=v_speed

                self.last_cursor_move = now
                
            imgX = self.cursor_pos[0]
            imgY = self.cursor_pos[1]
            if C.CURSOR_OVER:
                self.fullmap.blit(self.c_over.image, (self.cursor_pos[0]-(C.scale*3), self.cursor_pos[1]-(C.scale*3)))
            if C.GRID_OVER:
                if self.show_grid_at_scale:
                    self.fullmap.blit(self.grid.image, (self.camera.x, self.camera.y))
            self.fullmap.blit(self.c_img, (imgX,imgY))
    
    def Select(self):
        #Currently you can select a FRIEND but not anything else, fix this later
        self.move_over_group.empty()
        if self.units_pos[self.tile_pos[0]][self.tile_pos[1]] != None:
            if self.units_pos[self.tile_pos[0]][self.tile_pos[1]].status == FRIEND:
                self.current_unit = self.units_pos[self.tile_pos[0]][self.tile_pos[1]]
        if self.current_unit != None:
            self.unit_return = [self.current_unit.x,self.current_unit.y]
            
        #get move and damage from tile contents
        start = self.tile_pos
        s = start.copy()

        move = 4
        damage = 1
        
        #use these to limit cursor movement
        self.move_tiles = [(s[0],s[1])]
        self.damage_tiles = []
        self.unit_selected = True
        self.idle = True
        
        rows = (move* 2) + 1
        for x in range(-move+self.tile_pos[0]-damage,move+1+self.tile_pos[0]+damage):
            for y in range(-move+self.tile_pos[1]-damage, move+1+self.tile_pos[1]+damage):
                distance = abs(self.tile_pos[0] - x) + abs(self.tile_pos[1] - y)
                if distance <= move:
                    #and if tile is movable by unit/tile is empty
                    m = moveOver(x*C.scale, y*C.scale)
                    self.move_tiles.append((x,y))
                    self.move_over_group.add(m)
                elif distance > move and distance <= damage + move:
                    d = damageOver(x*C.scale, y*C.scale)
                    self.damage_tiles.append((x,y))
                    self.move_over_group.add(d)
    
    def Deselect(self):
        self.move_over_group.empty()
        #put unit back
        if self.current_unit != None:
            tmp_unit = self.current_unit
            self.current_unit.kill()
            pygame.display.update()
            self.units_pos[tmp_unit.x][tmp_unit.y] = None
            tmp_unit.x = self.unit_return[0]
            tmp_unit.y = self.unit_return[1]
            tmp_unit.animateSprites()
            self.units_pos[tmp_unit.x][tmp_unit.y] = tmp_unit
            self.on_screen_units.add(tmp_unit)
        self.unit_selected = False
        self.current_unit = None
        #currently this exits the whole menu, which is fine, but obviously once there's more actions this should only go back one level
        #So this block should be something like if self.show_menu == True and self.action_step == False..., haven't got that far yet
        self.show_menu = False
        self.show_options = False
        self.action_confirmed = False
        self.menu_cursor = False
        self.show_overlays = True
        self.option_cursor = False
        self.active_menu_index = 0
        self.menu_cursor_y_change = 0
    
    def initCombat(self):
        self.combat_surface = pygame.Surface((21*C.scale, 14*C.scale))
        self.combat_surface_rect = self.combat_surface.get_rect()
        self.combat_surface.fill(self.colors["NID_PINK"])
        #UNCOMMENT THIS WHEN THERE'S SOMETHING ON THE SURFACE
        #self.combat_surface.set_colorkey(self.colors["NID_PINK"])
        
bc = COLORS[random.choice(["BLACK","MUTED_NAVY","MUTED_FOREST","LIGHT_GRASS"])]            
m = sandbox((21*C.scale,13*C.scale), "Sandbox", bc, "icon.png", bc, C.cursor_speed)