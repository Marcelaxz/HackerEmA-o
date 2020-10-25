"""
JOGOS DIGITAIS
Beatriz Bertan, TIA: 31955312
Bianca Maciel, TIA: 31936873
Marcela Sousa, TIA: 31958443
Tamiris Maimone, TIA: 31901174
Turma 4H

"""

import pygame
from pygame.locals import *
import random

from pygame import mixer

# TELA
SCREEN_SIZE = (1300, 600)
pygame.display.set_caption("Hacker em Ação")
icon = pygame.image.load('imagens/icon.png')
pygame.display.set_icon(icon)

# IMAGENS
background = pygame.image.load('imagens/tela.png')
menina = pygame.image.load('imagens/lya.png')
inimi = pygame.image.load('imagens/inimi.png')
inimi2 = pygame.image.load('imagens/inimi2.png')

# ÁUDIOS
pygame.mixer.init()
soundtrack = "audios/fase.mp3"
pygame.mixer.music.load(soundtrack)
pygame.mixer.music.play(-1)

# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = menina
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -8)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 8)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-8, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(8, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1300:
            self.rect.right = 1300
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600


# ENEMIES
class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy1, self).__init__()
        self.image = inimi
        self.rect = self.image.get_rect(
            center=(
                random.randint(1300 + 20, 1300 + 100),
                random.randint(0, 600),
            )
        )
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy2, self).__init__()
        self.image = inimi2
        self.rect = self.image.get_rect(
            center=(
                random.randint(1300 + 20, 1300 + 100),
                random.randint(0, 600),
            )
        )
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 3000)

# PLAYER e ENEMIES
player = Player()
player.rect.x = 0
player.rect.y = 250

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# JOGO

Jogo = True
clock = pygame.time.Clock()

while Jogo:

    clock.tick(30)
    screen.blit(background, (0, 0))

    for evento in pygame.event.get():
        if evento.type == QUIT:
            Jogo = False
        if evento.type == ADDENEMY:
            new_enemy = Enemy1()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            new_enemy2 = Enemy2()
            enemies.add(new_enemy2)
            all_sprites.add(new_enemy2)

    # MOVIMENTO
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # COLISÃO
    if pygame.sprite.spritecollideany(player, enemies):
        clock.tick(90)
        pygame.display.update()
        player.kill()
        Jogo = False

    pygame.display.flip()

pygame.quit()
