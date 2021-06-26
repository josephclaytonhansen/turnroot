import pygame, sys, random, json

class Constants():
    def __init__(self):
        super().__init__()
        with open("src/tmp/sc.trecd", "r") as f:
            d = json.load(f)
        self.scale = d[0]
        self.fps = d[1]
        self.cursor_speed = d[2]
        self.grid_dimensions = d[3]
        with open("src/tmp/sc2.trecd", "r") as da:
            g = json.load(da)
        self.CURSOR_OVER = g[0]
        self.GRID_OVER = g[1]
        self.GRID_OPACITY = g[2]
        self.SANS_GAME_FONT= g[3]
        self.SERIF_GAME_FONT = g[4]
        self.OVERLAY_PLACEMENTS64 = g[5]
        self.OVERLAY_PLACEMENTS32 = g[6]
        self.GUARD_ICON = g[7]
        self.AVOID_ICON = g[8]
        self.HEAL_ICON = g[9]
        self.GUARD_ICON32 = g[10]
        self.AVOID_ICON32 = g[11]
        self.HEAL_ICON32 = g[12]
        self.KEY_OVER = g[13]
        self.KEY_OVER_WIDE = g[14]
        self.KEY_OVER32 = g[15]
        self.KEY_OVER_WIDE32 = g[16]
        self.SELECTION_OVERLAY_TYPE = g[17]

C = Constants()

class cursorOver(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            if color == "white":
                self.sprites.append(pygame.image.load('app/app_imgs/64_cursor_over_white.png'))
            if color == "black":
                self.sprites.append(pygame.image.load('app/app_imgs/64_cursor_over_black.png'))
        elif C.scale == 32:
            if color == "white":
                self.sprites.append(pygame.image.load('app/app_imgs/32_cursor_over_white.png'))
            if color == "black":
                self.sprites.append(pygame.image.load('app/app_imgs/32_cursor_over_black.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]

class overlayOver(pygame.sprite.Sprite):
    def __init__(self,image64,image32):
        super().__init__()
        self.sprites = []
        if C.scale == 64:
            self.sprites.append(pygame.image.load(image64))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load(image32))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

class gridOver(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            if color == "white":
                self.sprites.append(pygame.image.load('app/app_imgs/64_grid_white.png'))
            elif color == "black":
                self.sprites.append(pygame.image.load('app/app_imgs/64_grid_black.png'))
        elif C.scale == 32:
            pass
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]
        
class moveOver(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/64move.png'))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load('app/app_imgs/32move.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]
    
class damageOver(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/64damage.png'))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load('app/app_imgs/32damage.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]