# le fichier qui gère l'apparition du boss à partir d'un certain round: 5 par exemple

import pygame
import random as rd



class Boss(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/boss.png')
        self.image = pygame.transform.scale(self.image, (300, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 0
        # les stats du boss
        self.attack = 20
        self.health = 600
        self.max_health = 600
        self.points = 300
        self.speed = 10
        self.points = 300
        # pour les mouvements
        self.delay = 500
        self.laps = 0
        self.move_right = True
        # ses projectiles
        self.all_fireballs = pygame.sprite.Group()

    def update_health_bar(self, surface):  # on va dessiner la barre de PV sur une surface, elle doit être en argument
        pygame.draw.rect(surface, (60, 63, 60),
                         [(740 - self.max_health) / 2, 770, self.max_health, 5])  # la barre en plein
        pygame.draw.rect(surface, (110, 210, 45),
                         [(740 - self.max_health) / 2, 770, self.health, 5])  # la barre en HP actuel

    # le mouvement horizontal du boss



# une nouvelle classe qui gère les attaques du boss

class Fireball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.boss = Boss()  # on en a besoin pour placer les attaques
        self.image = pygame.image.load('assets/fireball.png')
        self.image = pygame.transform.scale(self.image, (45, 30))
        self.rect = self.image.get_rect()
        self.rect.x = self.boss.rect.x + self.boss.image.get_width() / 2 - rd.randint(-100, 100)
        self.rect.y = self.boss.rect.y + self.boss.image.get_height() / 2 - rd.randint(0,30)
        self.speed_y = 5
        self.speed_x = 10
        # le qui va gérer les tirs
        # self.clock = pygame.time.Clock()
        self.delay = 1000  # delay de 1 seconde
        self.laps = 0

    # une méthode qui tire des boules de feu de manière pas trop rapide

    def Fire(self):
        self.laps += 20
        if self.laps >= self.delay:
            self.boss.all_fireballs.add(Fireball())
            self.laps = 0
            return True
        else:
            return False

    # la méthode de déplacement du boss (auto avec delay)
    def move(self):
        if rd.randint(0, 1) > 1 / 2:
            self.move_right()
        else:
            self.move_left()

    def move_right(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

    def move_left(self):
        self.rect.y += self.speed_y
        self.rect.x -= self.speed_x