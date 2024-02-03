from csv import Dialect
from tkinter import CURRENT
from typing_extensions import Self
import pygame
from config import *
import math
import random
from random import randint
from story import *
from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_i,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)


class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = VILLAGER_LAYER
        self.groups = self.game.all_sprites, self.game.gracz
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        CURRENT_PLAYER_SPEED = PLAYER_SPEED

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.image = game.character_spritesheet.get_sprite(0,0,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0






    def movement(self):

        drawn = pygame.sprite.spritecollide(self, self.game.water, False)
        if drawn:
            CURRENT_PLAYER_SPEED = PLAYER_SPEED / 2
        else:
            CURRENT_PLAYER_SPEED = PLAYER_SPEED

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += CURRENT_PLAYER_SPEED
            for sprite in self.game.terrain or sprite in self.game.mission:
                    sprite.rect.y += CURRENT_PLAYER_SPEED
            self.y_change -= CURRENT_PLAYER_SPEED
            self.facing = 'up'

        if pressed_keys[K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= CURRENT_PLAYER_SPEED
            for sprite in self.game.terrain or sprite in self.game.mission:
                sprite.rect.y -= CURRENT_PLAYER_SPEED
            self.y_change += CURRENT_PLAYER_SPEED
            self.facing = 'down'

        if pressed_keys[K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= CURRENT_PLAYER_SPEED
            for sprite in self.game.terrain or sprite in self.game.mission:
                sprite.rect.x -= CURRENT_PLAYER_SPEED
            self.x_change += CURRENT_PLAYER_SPEED
            self.facing = 'left'

        if pressed_keys[K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += CURRENT_PLAYER_SPEED
            for sprite in self.game.terrain or sprite in self.game.mission:
                sprite.rect.x += CURRENT_PLAYER_SPEED
            self.x_change -= CURRENT_PLAYER_SPEED
            self.facing = 'right'

    def collide_blocks(self,direction):


        drawn = pygame.sprite.spritecollide(self, self.game.water, False)
        if drawn:
            CURRENT_PLAYER_SPEED = PLAYER_SPEED / 2
        else:
            CURRENT_PLAYER_SPEED = PLAYER_SPEED

        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += CURRENT_PLAYER_SPEED
                    for sprite in self.game.terrain:
                        sprite.rect.x += CURRENT_PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= CURRENT_PLAYER_SPEED
                    for sprite in self.game.terrain:
                        sprite.rect.x -= CURRENT_PLAYER_SPEED

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += CURRENT_PLAYER_SPEED
                    for sprite in self.game.terrain:
                        sprite.rect.y += CURRENT_PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= CURRENT_PLAYER_SPEED
                    for sprite in self.game.terrain:
                        sprite.rect.y -= CURRENT_PLAYER_SPEED




class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        self.image = game.terrain_spritesheet.get_sprite(97,0,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Building(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        self.image = game.terrain_spritesheet.get_sprite(33,0,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Villager(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = VILLAGER_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['down'])
        self.movement_loop = 0
        self.max_travel = randint(4,32)
        self.image = game.character_spritesheet.get_sprite(33,0,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def movement(self):


        if self.facing == 'left':
            hits = [s for s in pygame.sprite.spritecollide(self, self.game.all_sprites, False, pygame.sprite.collide_mask) if s != self]
            if hits:
                self.rect.x -= 4
                self.movement_loop = 0
                self.facing = 'right'


            else:
                self.x_change -= VILLAGER_SPEED
                self.movement_loop -= 2
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['right','down','up'])

        if self.facing == 'up':
            hits = [s for s in pygame.sprite.spritecollide(self, self.game.all_sprites, False, pygame.sprite.collide_mask) if s != self]
            if hits:
                self.rect.y += 4
                self.movement_loop = 0
                self.facing = 'down'


            else:
                self.y_change -= VILLAGER_SPEED
                self.movement_loop -= 2
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['right', 'down', 'left'])

        if self.facing == 'right':
            hits = [s for s in pygame.sprite.spritecollide(self, self.game.all_sprites, False, pygame.sprite.collide_mask) if s != self]
            if hits:
                self.rect.x -= 4
                self.movement_loop = 0
                self.facing = 'left'



            else:
                self.x_change += VILLAGER_SPEED
                self.movement_loop += 2
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left', 'up', 'down'])



        if self.facing == 'down':
            hits = [s for s in pygame.sprite.spritecollide(self, self.game.all_sprites, False, pygame.sprite.collide_mask) if s != self]
            if hits:
                self.movement_loop = 0
                self.rect.x -= 4
                self.facing = 'up'


            else:
                self.x_change += VILLAGER_SPEED
                self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left', 'up', 'right'])




    def update(self):

            self.movement()
            self.rect.x += self.x_change
            self.rect.y += self.y_change
            self.x_change = 0
            self.y_change = 0





class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = TERRAIN_LAYER
        self.groups = self.game.terrain
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA
        getgrass = random.choice([self.game.terrain_spritesheet.get_sprite(0,0,self.width, self.height),
        self.game.terrain_spritesheet.get_sprite(0,34,self.width, self.height),
        self.game.terrain_spritesheet.get_sprite(0,68,self.width, self.height),
        self.game.terrain_spritesheet.get_sprite(0,102,self.width, self.height)])


        self.image = getgrass

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Road(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = TERRAIN_LAYER + 1
        self.groups = self.game.terrain
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        self.image = game.character_spritesheet.get_sprite(65,0,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = TERRAIN_LAYER + 1
        self.groups = self.game.terrain, self.game.water
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        self.image = game.terrain_spritesheet.get_sprite(160,0,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Mission_Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = TERRAIN_LAYER
        self.groups = self.game.mission, self.game.terrain
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * KRATKA
        self.y = y * KRATKA
        self.width = KRATKA
        self.height = KRATKA

        self.image = game.terrain_spritesheet.get_sprite(129,33,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def pressed(self):
        pressed_keys = pygame.key.get_pressed()
        states = [self.game.terrain_spritesheet.get_sprite(129,0,self.width, self.height),
        self.game.terrain_spritesheet.get_sprite(129,33,self.width, self.height)]
        hits = pygame.sprite.spritecollide(self, self.game.gracz, False)
        if hits:
            self.image = states[1]
            restart_button = Button(10, 50, 100, 50, WHITE, YELLOW, 'Restart', 16)
            if pressed_keys[K_i]:
                self.game.playing = False
                self.game.storyrun = True
        else:
            self.image = states[0]
    def update(self):
        self.pressed()








class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, fg, bg, zaw, fontsize):
        self.font = pygame.font.Font('Arial.ttf',fontsize)
        self.zaw = zaw
        self._layer = 10
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.zaw, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False




