import pygame, sys

loader = "retro"

class retroLoader():
    def __init__(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        super().__init__()
        pygame.init()
        self.initMainWindow(dimensions, title, initial_bg, icon, bar_bg, cursor_speed)
    
    def initInitialValues(self, dimensions, cursor_speed):
        self.cursor_pos = [192,64]
        self.cursor_x_change = 0
        self.cursor_y_change = 0
        self.dimensions = dimensions
        self.last_cursor_move = pygame.time.get_ticks()
        self.cursor_move_cooldown = cursor_speed
        
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                
                #Key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.cursor_y_change = -192
                    if event.key == pygame.K_DOWN:
                        self.cursor_y_change = 192

                #Key release
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        self.cursor_x_change = 0
                        self.cursor_y_change = 0
                        
                #Handle screen size
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((int(event.size[0]), int(event.size[1])), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    self.screen_rect = self.screen.get_rect()
            
            screen.fill(bar_bg)
            self.fake_screen.fill(initial_bg)
            
            #self.show...
            self.showButtons()
            self.showCursor()
            
            #screen.blit(pygame.transform.scale(self.fake_screen, screen.get_rect().size), (0, 0))
            if self.screen_rect.size != self.dimensions:
                fit_to_rect = self.fake_rect.fit(self.screen_rect)
                fit_to_rect.center = self.screen_rect.center
                scaled = pygame.transform.smoothscale(self.fake_screen, fit_to_rect.size)
                self.screen.blit(scaled, fit_to_rect)
            else:
                self.screen.blit(self.fake_screen, (0,0))
            
            pygame.display.update()
    
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

        self.leds = pygame.image.load("app/app_imgs/leds.png")
        self.screen_img = pygame.image.load("app/app_imgs/screen.png")
        self.speaker = pygame.image.load("app/app_imgs/speaker.png")
        self.fake_screen.blit(self.screen_img, (0,46))
        self.fake_screen.blit(self.load_button, (192,64))
        self.fake_screen.blit(self.create_button, (192,256))
        self.fake_screen.blit(self.settings_button, (192,448))
        self.fake_screen.blit(self.leds, (560,500))
        self.fake_screen.blit(self.speaker, (630,10))
    
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

if loader == "retro":
    m = retroLoader((840,640), "Testing", "#DfDfDf", "icon.png", "#000000", 70)