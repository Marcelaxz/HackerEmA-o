import pygame
from pygame.locals import *
from pygame import mixer

# TELA
SCREEN_SIZE = (1300, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Hacker em Ação")
icon = pygame.image.load('imagens/icon.png')
pygame.display.set_icon(icon)

# IMAGENS
background = pygame.image.load('imagens/tela.png')
menina = pygame.image.load('imagens/lya.png')

# ÁUDIOS
pygame.mixer.init()
soundtrack = "audios/fase.mp3"
pygame.mixer.music.load(soundtrack)
pygame.mixer.music.play(-1)

# PLAYER
def player(x, y):
    screen.blit(menina, (x, y))

mX = 0
mY = 250

Jogo = True

while Jogo:
    screen.blit(background, (0, 0))
    for evento in pygame.event.get():
        if evento.type == QUIT:
            Jogo = False
        if evento.type == KEYDOWN:
            if evento.key == K_RIGHT:
                mX += 50
            if evento.key == K_LEFT:
                mX -= 50
            if evento.key == K_UP:
                mY -= 50
            if evento.key == K_DOWN:
                mY += 50

    if mX >= 1200:
        mX = 1200
    if mX <= 0:
        mX = 0
    if mY >= 440:
        mY = 440
    if mY <= 0:
        mY = 0

    # MOVIMENTO
    player(mX, mY)
    pygame.display.flip()

pygame.quit()