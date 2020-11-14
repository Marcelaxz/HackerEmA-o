"""
JOGOS DIGITAIS
Beatriz Bertan, TIA: 31955312
Bianca Maciel, TIA: 31936873
Marcela Sousa, TIA: 31958443
Tamiris Maimone, TIA: 31901174
Turma 4H

"""

import pygame, sys
from pygame.locals import *
import random
from pygame import mixer
from video import Video


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
gameO = pygame.image.load('imagens/perdeu.png')
sim = pygame.image.load('imagens/sim.png')
nao = pygame.image.load('imagens/nao.png')


# ÁUDIOS
pygame.mixer.init()
soundtrack = "audios/fase.mp3"
pygame.mixer.music.load(soundtrack)
pygame.mixer.music.play(-1)
dano = "audios/sofreDano.wav"
hitSound = pygame.mixer.Sound(dano)
morte = "audios/mortePersonagem.wav"
deathSound = pygame.mixer.Sound(morte)


#MENU
menu = pygame.image.load('imagens/background.jpg')
titulo = pygame.image.load('imagens/titulo.png')
iniciar = pygame.image.load('imagens/iniciar2.png')
comoJ = pygame.image.load('imagens/comojogar.png')
sair = pygame.image.load('imagens/sair.png')


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


# GAME OVER
def gameOver():
    clock.tick(90)
    mx, my = pygame.mouse.get_pos()
    color = (252, 3, 211)
    pygame.draw.rect(screen, color, pygame.Rect(60, 60, 1200, 500))
    screen.blit(gameO, (300, 200))
    pygame.font.init()
    fonte = pygame.font.SysFont('Arial', 50)
    texto = fonte.render('Deseja jogar novamente?', False, (255, 255, 255))
    screen.blit(texto, (380, 290))
    button_1 = pygame.Rect(480, 380, 200, 50)
    screen.blit(sim, (490, 380))
    button_2 = pygame.Rect(680, 380, 200, 50)
    screen.blit(nao, (690, 380))
    for evento in pygame.event.get():
        if evento.type == MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if button_1.collidepoint((mx, my)):
                main()
            if button_2.collidepoint((mx, my)):
                pygame.quit()
    pygame.display.flip()


# PYGAME.INIT()
pygame.init()


screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False


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


enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


def main():

    Video()

    global floor_x_pos
    player.rect.x = 0
    player.rect.y = 250

    deathSound_cont = 43


    # VIDA
    vida = 3
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


        # VIDA
        for l in range(vida):
            screen.blit(heart, (20 + (l*50), 10))


        # UPDATE
        pygame.display.flip()

    pygame.quit()

def main_menu():

    while True:


        screen.blit(menu, (0, 0))
        screen.blit(titulo, (315, 40))

        screen.blit(iniciar, (570, 225))
        screen.blit(comoJ, (505, 330))
        screen.blit(sair, (595, 440))
        mx, my = pygame.mouse.get_pos()

        #BOTÃO 1
        button_1 = pygame.Rect(570, 225, 200, 50) # Iniciar

        # BOTÃO 2
        button_2 = pygame.Rect(505, 330, 200, 50) # Como Jogar

        # BOTÃO 3
        button_3 = pygame.Rect(595, 440, 200, 50) # Sair

        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                game()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


def game():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False


        pygame.display.update()
        clock.tick(60)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False



        pygame.display.update()
        clock.tick(60)

main_menu()

main()