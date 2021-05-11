import pygame
import pygame_menu
from pygame.locals import *
import sys
import os
from random2 import *

# define display surface
from pygame_menu import Theme

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

per = pygame.image.load('per.png')
bkgd = pygame.image.load("back.png").convert()

X_vermelho = 0
Y_vermelho = 0
RED = (255, 0, 0)
criar = True
possible_Y = [250, 350, 450]


def set_difficulty(value, difficulty):
    # Do the job here !
    pass


def start_the_game():
    global criar, X_vermelho, Y_vermelho
    x = 0
    jumpping = False
    jumpCount = 10
    perx = 200
    pery = 300
    RED = (0, 255, 0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        rel_x = x % bkgd.get_rect().width

        DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
        if rel_x < W:
            DS.blit(bkgd, (rel_x, 0))

        x -= 4

        if not (jumpping):
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                jumpping = True
        else:
            if jumpCount >= -10:
                pery -= (jumpCount * abs(jumpCount)) * 0.5
                jumpCount -= 1
            else:
                jumpCount = 10
                jumpping = False
        if criar == True:
            X_vermelho = 600
            Y_vermelho = possible_Y[randint(0, 2)]
            criar = False

        X_vermelho -= 5

        # Valores da bola vermelha é atribuido
        posicaoBolasVermelhas = [X_vermelho, Y_vermelho]

        # Desenha o círculo vermelho
        pygame.draw.circle(DS, RED, posicaoBolasVermelhas, 10)

        # Se o círculo vermelho ultapassar a  tela ela é reiniciada
        if X_vermelho < 30:
            criar = True
        DS.blit(per, (perx, pery))
        pygame.display.update()
        CLOCK.tick(FPS)


font = pygame_menu.font.FONT_8BIT
mytheme = Theme(background_color=(0, 0, 0, 0), title_font=font, widget_font=pygame_menu.font.FONT_MUNRO,
                widget_font_size=30)
menu = pygame_menu.Menu(
    height=300,
    theme=mytheme,
    title='FOREST RUN',
    width=400
)

menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(DS)
