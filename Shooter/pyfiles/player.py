import pygame
import math
from laser import Laser

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.health = 80
        self.max_health = 80
        self.image = pygame.image.load('assets/player.png')
        #on redimensionne le sprite
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        #position initiale : au milieu de l'écran en x, un peu sur le bas en y
        self.rect.x = 320
        self.rect.y = 560
        #les stats : attaque, speed
        self.attack = 25
        self.speed = 10
        #un groupe de sprite contenant tous les tirs
        self.all_lasers = pygame.sprite.Group()
        # une méthode self qui gère le score du joueur
        self.score = 0

    # la barre de HP
    def update_health_bar(self, surface): # on va dessiner la barre de PV sur une surface, elle doit être en argument
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x, self.rect.y, self.max_health, 3])  # la barre en plein
        pygame.draw.rect(surface, (110, 210, 45) , [self.rect.x, self.rect.y, self.health, 3]) #la barre en HP actuel

# on définit 4 méthode pour gerer le movement.
# Attention, il nous faut vérifier que le sprite du perso ne sort pas de l'écran

    def move_right(self):
        self.rect.x += self.speed
    def move_left(self):
        self.rect.x -= self.speed
    def move_up(self):
        self.rect.y -= self.speed
    def move_down(self):
        self.rect.y += self.speed

#la méthode qui tir un laser

    def fire_laser(self):
        self.all_lasers.add(Laser(self))


