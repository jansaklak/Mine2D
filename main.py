from pickle import FALSE
from tkinter import W
import pygame
from sprites import *
from config import *
import sys
from story import *
from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('Arial.ttf', 16)
        self.gameover_background = pygame.image.load('img\gameover.png')
        self.story_bg = pygame.image.load('img\story1.png')
        self.intro_background = pygame.image.load('img\intro_background.png')
        self.playing = True
        self.character_spritesheet = Spritesheet('img/characters.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')

    def createmap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "W":
                    Wall(self, j, i)
                if column == "B":
                    Building(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "V":
                    Villager(self, j, i)
                if column == "C":
                    Road(self,j,i)
                if column == "1":
                    Water(self,j,i)
                if column == "M":
                    Mission_Block(self,j,i)
                else:
                    Grass(self, j, i)
                    
    def new(self):

        self.playing = True
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.mission = pygame.sprite.LayeredUpdates()
        self.warning = pygame.sprite.LayeredUpdates()
        self.terrain = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.gracz = pygame.sprite.LayeredUpdates()
        self.createmap()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.storyrun = False

    def update(self):

        self.all_sprites.update()
        self.terrain.draw(self.screen)
        self.mission.update()


    def draw(self):

        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):

        while self.playing:
                self.events()
                self.update()
                self.draw()
        self.running = True

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))

        restart_button = Button(10, 50, 100, 50, WHITE, YELLOW, 'Restart', 16)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    self.storyrun = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos,mouse_pressed):
                self.new()
                self.main()

            self.screet.blit(self.gameover_background, (0,0))

    def intro_screen(self):
        intro = True

        title = self.font.render('Super gra', True, RED)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 50, 100, 50, WHITE, YELLOW, 'START', 16)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    self.storyrun = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def story(self):
        while self.storyrun:
            text = self.font.render('Story one', True, BLACK)
            text_rect = text.get_rect(center=(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
            self.screen.blit(self.story_bg, (0,0))
            self.screen.blit(text, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing = False
                        self.running = False
                        self.storyrun = False

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.story()
g.game_over()
pygame.quit()
sys.exit()