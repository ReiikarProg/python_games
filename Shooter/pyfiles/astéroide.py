# la class qui gère les astéroides qui tombent du ciel. Pour ceux de base, on en choisit 3 sprites différents


import pygame
import random as rd

class Asteroide(pygame.sprite.Sprite):

    def __init__(self, game, path):
        super().__init__()
        self.game = game
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        #position initiale aléatoire
        self.rect.x = rd.randint(80,640)
        self.rect.y = rd.randint(-2000,0)    #pour ne pas qu'ils tombe en même temps
        # les "stats de base"
        self.speed = 2
        self.damage = 10
        self.health = 50
        self.max_health = 50
        self.points = 20


    #la méthode de gestion de HP: à priori on le l'affichera pas
    def update_health_bar(self, surface): #on va dessiner la barre de PV sur une surface, elle doit être en argument
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 20, self.rect.y, self.max_health, 2])  # la barre en plein
        pygame.draw.rect(surface, (110, 210, 45) , [self.rect.x + 20, self.rect.y, self.health, 2]) #la barre en HP actuel

    #la chute des astéroides
    def fall(self):
        self.rect.y += self.speed

    def set_speed(self, amount):
        self.speed = amount

    def set_dammage(self, amount):
        self.damage = amount


#on créer des classes différentes en fonction du sprite.

class Model1(Asteroide): #basic ennemy

    def __init__(self, game):
        super().__init__(game, 'assets/astéroide1.png')
        self.set_speed(2)
        self.set_dammage(10)
        self.health = 100
        self.max_health = 100
        self.points = 30

class Model2(Asteroide): #un modèle intermédiaire


    def __init__(self, game):
        super().__init__(game, 'assets/astéroide2.png')
        self.set_speed(4)
        self.set_dammage(10)
        self.points = 20

class Model3(Asteroide):     #le modèle boule de feu rapide

    def __init__(self, game):
        super().__init__(game, 'assets/astéroide3.png')
        self.image = pygame.transform.rotate(self.image, 40)
        self.set_speed(6)
        self.set_dammage(20)
        self.health = 25
        self.max_health = 25
        self.points = 50