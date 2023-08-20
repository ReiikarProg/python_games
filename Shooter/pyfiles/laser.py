import pygame
import math
# from player import Player #on aura besoin de Player pour connaitre sa position
class Laser(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load('assets/laser.png')
        #on redimensionne et rotate le sprite
        self.image = pygame.transform.scale(self.image, (40,60))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        #on le positionne un peu au dessus du vaisseau
        self.rect.x = self.player.rect.x + 12
        self.rect.y = self.player.rect.y - 40
        #la vitesse de base du laser
        self.speed = 8

    def remove(self):
        self.player.all_lasers.remove(self)

    #la méthode qui gère le déplacement du laser
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.remove()

