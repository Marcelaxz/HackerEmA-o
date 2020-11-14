import pygame
from moviepy.editor import *
import os

icon = pygame.image.load('imagens/icon.png')
pygame.display.set_icon(icon)


class Video():
    pygame.display.set_caption('Hacker em Ação')
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    clip = VideoFileClip('videos/intro.mp4')
    clip.preview()
    os.system('game.py')