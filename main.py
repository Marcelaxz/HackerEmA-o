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
janela = pygame.display.set_mode(SCREEN_SIZE)

# IMAGENS
background = pygame.image.load('imagens/tela.png')
menina = pygame.image.load('imagens/lya.png')
inimi = pygame.image.load('imagens/inimi.png')
speaker = pygame.image.load('imagens/speaker.png')
mute = pygame.image.load('imagens/mute.png')
heart = pygame.image.load('imagens/vida.png')


# ÁUDIOS
pygame.mixer.init()
soundtrack = "audios/fase.mp3"
pygame.mixer.music.load(soundtrack)
pygame.mixer.music.play(-1)
dano = "audios/sofreDano.wav"
hitSound = pygame.mixer.Sound(dano)
morte = "audios/mortePersonagem.wav"
deathSound = pygame.mixer.Sound(morte)
deathSound_cont = 43


# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = menina
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(30, 100, 20, 120)
        self.isJump = False
        self.jumpCount = 20

    def jump (self):
        if self.isJump:
            if self.jumpCount >= -20:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.rect.y -= self.jumpCount**2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 20


    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1200:
            self.rect.right = 1200
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 550:
            self.rect.bottom = 550


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
        self.speed = random.randint(7, 15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# BLOCOS
"""class Blocos(pygame.sprite.Sprite):
    def __init__(self):
        super"""


# GAME OVER
def gameOver():
    clock.tick(90)
    color = (252, 3, 211)
    pygame.draw.rect(screen, color, pygame.Rect(60, 60, 1200, 500))
    pygame.display.flip()
    pygame.font.init()
    fonte = pygame.font.SysFont('Arial', 100)
    texto = fonte.render('Você morreu', False, (255, 255, 255))
    screen.blit(texto, (370, 250))


# PYGAME.INIT()
pygame.init()


screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()


# CHÃO
floor_surface = pygame.image.load('imagens/floor.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 280))
    screen.blit(floor_surface, (floor_x_pos + 1300, 280))


# PLAYER e ENEMIES
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2000)

player = Player()
player.rect.x = 0
player.rect.y = 250

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# VIDA
vida = 3

# JOGO
soundtrack = True

Jogo = True
while Jogo:
    clock.tick(30)


    for evento in pygame.event.get():
        if evento.type == QUIT:
            Jogo = False
        if evento.type == ADDENEMY:
            new_enemy = Enemy1()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                player.isJump = True
            if evento.key == pygame.K_x:
                if soundtrack:
                    pygame.mixer.music.pause()
                    soundtrack = False
                else:
                    pygame.mixer.music.unpause()
                    soundtrack = True


    # BACKGROUND
    screen.blit(background, (0, 0))


    # MOVIMENTO DO CHÃO
    floor_x_pos -= 4
    draw_floor()
    if floor_x_pos <= -1300:
        floor_x_pos = 0


    # PAUSE / PLAY
    pygame.font.init()
    fonte = pygame.font.SysFont('Arial', 11)
    texto = fonte.render('Pressione "x" para pausar ou dar play no som', False, (255, 255, 255))
    screen.blit(texto, (1015, 30))

    if soundtrack == True:
        screen.blit(speaker, (1250, 20))
    else:
        screen.blit(mute, (1250, 20))


    # MOVIMENTO
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)


    # PULO
    player.jump()

    enemies.update()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)


    # COLISÃO
    if pygame.sprite.spritecollide(player, enemies, True):
        hitSound.play()
        vida -= 1
    if vida <= 0:
        deathSound.play()
        deathSound_cont -= 1
        if deathSound_cont <= 0:
           hitSound.stop()
           deathSound.stop()
        gameOver()
        pygame.display.update()
        player.kill()


    # VIDA
    for l in range(vida):
        screen.blit(heart, (20 + (l*50), 10))

    # UPDATE
    pygame.display.flip()

pygame.quit()