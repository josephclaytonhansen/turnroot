import pygame, sys, random, json

class Constants():
    def __init__(self,constants):
        super().__init__()
        with open(constants, "r") as f:
            d = json.load(f)
        self.scale = d[0]
        self.fps = d[1]
        self.cursor_speed = d[2]
        self.grid_dimensions = d[3]

C = Constants("src/tmp/sc.trecd")

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