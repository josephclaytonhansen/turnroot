import pygame, sys, random, json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import Go

class Constants():
    def __init__(self,data):
        super().__init__()
        with open(data, "r") as f:
            d = json.load(f)
        self.loader = d[0]
        self.sounds = d[1]
        self.stickers = d[2]
        self.stickers_dict = d[3]
        self.aw = d[4]

C = Constants("src/tmp/alc.trecd")

class retroLoader():
    def __init__(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        self.initMainWindow(dimensions, title, initial_bg, icon, bar_bg, cursor_speed)
    
    def initInitialValues(self, dimensions, cursor_speed):
        self.cursor_pos = [192,64]
        self.cursor_x_change = 0
        self.cursor_y_change = 0
        
        self.dimensions = dimensions
        self.last_cursor_move = pygame.time.get_ticks()
        self.b_pos = {64:"load",256:"create",448:"settings"}
        
        self.move_sound = pygame.mixer.Sound("app/app_sounds/menu_move.wav")
        self.select_sound = pygame.mixer.Sound("app/app_sounds/menu_confirm.wav")
        
        self.cursor_move_cooldown = cursor_speed
        clock = pygame.time.Clock()
        clock.tick(60)
        
    def initMainWindow(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        #load variables and constants
        self.initInitialValues(dimensions, cursor_speed)
        
        #init screen
        screen = pygame.display.set_mode(self.dimensions, flags=(pygame.RESIZABLE))
        fake_screen = screen.copy()
        self.fake_screen = fake_screen
        self.screen = screen
        self.icon = icon
        running = True
        
        self.fake_rect = self.fake_screen.get_rect()
        self.screen_rect = self.screen.get_rect()
        
        pygame.display.set_caption(title)
        #i = pygame.image.load(icon)
        #pygame.display.set_icon(i)

        #Game loop
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        sys.exit()
                    
                    #Key press
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.cursor_y_change = -192
                        elif event.key == pygame.K_DOWN:
                            self.cursor_y_change = 192
                        elif event.key == pygame.K_RETURN:
                            self.select_sound.play()
                            self.buttonPress(self.b_pos[self.cursor_pos[1]])

                    #Key release
                    elif event.type == pygame.KEYUP:
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                            self.move_sound.play()
                            self.cursor_x_change = 0
                            self.cursor_y_change = 0
                    
                    #Mouse
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.select_sound.play()
                        self.buttonPress(self.b_pos[self.cursor_pos[1]])
                    
                    #Mouse move
                    elif event.type == pygame.MOUSEMOTION:
                        x, y = pygame.mouse.get_pos()
                        if y > 64 and y < 200:
                            self.cursor_pos[1] = 64
                        elif y > 200 and y < 336:
                            self.cursor_pos[1] = 256
                        elif y > 336:
                            self.cursor_pos[1] = 448
                            
                    #Handle screen size
                    elif event.type == pygame.VIDEORESIZE:
                        screen = pygame.display.set_mode((int(event.size[0]), int(event.size[1])), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                        self.screen_rect = self.screen.get_rect()
                
                screen.fill(bar_bg)
                self.fake_screen.fill(initial_bg)
                
                #self.show...
                self.showConsole()
                if C.aw == "main":
                    self.showButtons()
                    self.showCursor()
                if C.aw == "settings":
                    self.showSettings()
                
                #screen.blit(pygame.transform.scale(self.fake_screen, screen.get_rect().size), (0, 0))
                if self.screen_rect.size != self.dimensions:
                    fit_to_rect = self.fake_rect.fit(self.screen_rect)
                    fit_to_rect.center = self.screen_rect.center
                    scaled = pygame.transform.smoothscale(self.fake_screen, fit_to_rect.size)
                    self.screen.blit(scaled, fit_to_rect)
                else:
                    self.screen.blit(self.fake_screen, (0,0))
                
                pygame.display.update()
                
            except:
                sys.exit()
            
    def buttonPress(self, s):
        if s == "settings":
            C.aw = "settings"
        if s == "create":
            C.aw = "create"
            pygame.display.quit()
            pygame.quit()
            Go(True)
            running = False
            
    
    def showConsole(self):
        self.leds = pygame.image.load("app/app_imgs/leds.png")
        self.screen_img = pygame.image.load("app/app_imgs/screen.png")
        self.fake_screen.blit(self.leds, (560,500))
        self.fake_screen.blit(self.screen_img, (0,46))
    
    def showSettings(self):
        #loader, sounds Y/N, stickers Y/N, re-arrange stickers
        pass
    
    def showButtons(self):
        if self.cursor_pos[1] == 64:
            self.load_button = pygame.image.load("app/app_imgs/load_game_s.png")
        elif self.cursor_pos[1] != 64:
            self.load_button = pygame.image.load("app/app_imgs/load_game.png")
        if self.cursor_pos[1] == 256:
            self.create_button = pygame.image.load("app/app_imgs/create_game_s.png")
        elif self.cursor_pos[1] != 256:
            self.create_button = pygame.image.load("app/app_imgs/create_game.png")
        if self.cursor_pos[1] == 448:
            self.settings_button = pygame.image.load("app/app_imgs/settings_s.png")
        elif self.cursor_pos[1] != 448:
            self.settings_button = pygame.image.load("app/app_imgs/settings.png")

        self.fake_screen.blit(self.load_button, (192,64))
        self.fake_screen.blit(self.create_button, (192,256))
        self.fake_screen.blit(self.settings_button, (192,448))
        
    
    def showCursor(self):
        img = pygame.image.load("app/app_imgs/cursor.png")
        now = pygame.time.get_ticks()
        if now - self.last_cursor_move >= self.cursor_move_cooldown:
            self.cursor_pos[0] += self.cursor_x_change
            self.cursor_pos[1] += self.cursor_y_change
            if self.cursor_pos[0] < 0:
                self.cursor_pos[0] = 0
            if self.cursor_pos[0] >= self.dimensions[0] - 256:
                self.cursor_pos[0] = self.dimensions[0] - 256
            if self.cursor_pos[1] < 64:
                self.cursor_pos[1] = 64
            if self.cursor_pos[1] >= self.dimensions[1] - 192:
                self.cursor_pos[1] = self.dimensions[1] - 192
            
            self.last_cursor_move = now
            
        imgX = self.cursor_pos[0]
        imgY = self.cursor_pos[1]
        self.fake_screen.blit(img, (imgX,imgY))

if C.loader == "retro":
    m = retroLoader((840,640), "Testing", "#DfDfDf", "icon.png", "#000000", 70)