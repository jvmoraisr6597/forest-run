import pygame
import pygame_menu
from pygame_functions import *
from pygame.locals import *
import sys
import os
import math
from random2 import *

# define display surface
from pygame_menu import Theme


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('per.png')
        self.rect = self.image.get_rect()
        self.jumpping = False
        self.jumpCount = 10
        self.life = 100
        self.alive = True
        self.score = 0
        self.agachando = False
        self.agacharCount = 12
        self.mask = pygame.mask.from_surface(self.image)

    def pular(self):
        self.jumpping = True
        self.updateImage(False)

    def updateImage(self, url):
        if url:
            self.image = pygame.image.load('per_agachado.png')
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = 397
        else:
            self.image = pygame.image.load('per.png')
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = 300
        self.mask = pygame.mask.from_surface(self.image)

    def agachar(self):
        if self.agachando:
            if self.agacharCount >= -12:
                self.updateImage(True)
                self.agacharCount -= 1
            else:
                self.agacharCount = 12
                self.agachando = False
                self.updateImage(False)

    def hit(self):
        self.life -= 25

    def recover(self):
        if self.life <= 85:
            self.life += 15
        else:
            self.life = 100

    def kill(self):
        self.alive = False

    def update(self):
        if self.jumpping:
            if self.jumpCount >= -10:
                self.rect.y -= (self.jumpCount * abs(self.jumpCount)) * 0.65
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.jumpping = False
                self.rect.y = 300


class Food(pygame.sprite.Sprite):
    def __init__(self, url, type_of_food):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(url)
        self.type = type_of_food
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


W, H = 576, 640
HW, HH = W / 2, H / 2
AREA = W * H

os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

# setup pygame
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("FOREST RUN")
FPS = 40

bkgd = pygame.image.load("back.png").convert()
all_sprites = pygame.sprite.Group()
food_group = pygame.sprite.Group()

criar = True
possible_Y = [150, 300, 550]
possible_healthy_foods = ['maca.png']
possible_fat_food = ['burg.png', 'pizza.png']
game_over = False
best_score = 0

font = pygame.font.SysFont('sans', 20)


def start_the_game():
    global criar, food, foodRect, sort, best_score
    x = 0
    per = Player()
    all_sprites.add(per)
    per.rect.x = 100
    per.rect.y = 300
    jumpCount = 8
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        rel_x = x % bkgd.get_rect().width

        DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
        if rel_x < W:
            DS.blit(bkgd, (rel_x, 0))

        x -= 10

        if not per.jumpping:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                per.pular()
        if not per.agachando:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_DOWN]:
                per.agachando = True
                per.agachar()
        else:
            per.agachar()
        print(per.life)
        if criar == True:
            sort = randint(0, 1)
            if sort:
                food = Food(possible_fat_food[randint(0, 1)], "fat")
            else:
                food = Food(possible_healthy_foods[0], "healthy")
            all_sprites.add(food)
            food_group.add(food)
            food.rect.x = 600
            food.rect.y = possible_Y[randint(0, 2)]
            criar = False

        food.rect.x -= 10
        all_sprites.draw(DS)

        if food.rect.x < -60:
            criar = True
        collide = pygame.sprite.spritecollide(per, food_group, False, pygame.sprite.collide_mask)
        if len(collide) > 0:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('eating.mp3'))
            if food.type == "fat":
                per.hit()
                if per.life <= 0:
                    if per.score > best_score:
                        best_score = per.score
                    all_sprites.remove(per)
                    menu_iniciar(best_score)
                    break
            else:
                per.recover()
            all_sprites.remove(food)
            food_group.remove(food)
            criar = True
        per.score += 1
        pygame.draw.rect(DS, (255,0,0), (30,30,200,10))
        pygame.draw.rect(DS, (0,255,0), (30,30,per.life * 2,10))
        score1 = font.render('Tempo de vida', True, ((0, 0, 0)))
        score2 = font.render(str(per.score), True, ((0, 0, 0)))
        DS.blit(score1, (430, 15))
        DS.blit(score2, (485, 35))
        all_sprites.update()
        pygame.display.update()
        CLOCK.tick(FPS)


def menu_iniciar(score):
    print(score)
    fonte = pygame_menu.font.FONT_8BIT
    mytheme = Theme(title_font=fonte, widget_font=pygame_menu.font.FONT_MUNRO,
                    widget_font_size=30)
    myimage = pygame_menu.baseimage.BaseImage(
        image_path="back_menu.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    menu = pygame_menu.Menu(
        height=640,
        theme=mytheme,
        title='FOREST RUN',
        width=576
    )
    menu.add_label("Maior tempo de vida: " + str(score), font_size=20, margin=(160, 100))
    menu.add.vertical_margin(160)
    menu.add.button("Iniciar", start_the_game, background_color=(0, 255, 0), border_width=0)
    menu.add.vertical_margin(250)
    menu.mainloop(DS)

pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('trilha.mp3'), -1)
menu_iniciar(best_score)

