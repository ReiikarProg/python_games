import pygame
from player import Player
from boss import Boss
from boss import Fireball
import astéroide
import random as rd


class Game():

    def __init__(self):
        super().__init__()
        # la méthode qui lance le jeu
        self.is_playing = False
        # la méthode qui déclenche l'affichage de l'écran de game_over
        self.set_game_over = False
        self.menu = True
        self.winning_screen = False
        # on récupère ici les objets
        self.player = Player(self)  # self est car le second argument de player est justement game
        self.boss = Boss()
        self.fireball = Fireball()
        self.all_boss = pygame.sprite.Group(self.boss)
        self.all_asteroides = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group(self.player)

        # la méthode qui garde trace des touches appuyées sous forme de dictionnaire
        self.pressed = {}
        self.current_round = 0
        self.last_round = 6 # le dernier round avant le boss
        self.nb_asteroides = 0
        self.current_number_asteroides = 0
        # le score final
        self.final_score_text = None
        self.win_text = None
        self.boss_event = False

    # la méthode qui gère l'évènement du boss
    def start_boss_event(self, screen):
        # on lance le boss_event
        self.boss_event = True
        # on continue d'afficher le score
        font = pygame.font.SysFont("monospace", 24)  # la police de base
        score_text = font.render(f"Score : {self.player.score}", True, (255, 255, 255))  # on créer le texte
        screen.blit(score_text, (20, 20))
        # on met à jour l'écran avec le joueur
        screen.blit(self.player.image, self.player.rect)
        self.player.update_health_bar(screen)
        # on affiche le boss et ses HP
        for boss in self.all_boss:
            screen.blit(boss.image, boss.rect)
            boss.update_health_bar(screen)
        font = pygame.font.SysFont("monospace", 24)  # la police de base
        boss_health = font.render("BOSS HEALTH", True, (255, 255, 255))  # on créer le texte
        screen.blit(boss_health, (280, 775))

        # ajout des fireballs, périodiquement, lorsque le boss est vivant

        if self.fireball.Fire() and len(self.all_boss) != 0:
            self.boss.all_fireballs.add(Fireball())

        # gestion des mouvements et collisions
        for fireball in self.boss.all_fireballs:
            fireball.move()
            # on le supprime s'il sort de l'écran
            if fireball.rect.y >= 800:
                self.boss.all_fireballs.remove(fireball)
            # on fait bouger les lasers
            if collision(fireball, self.all_players):
                self.player.health -= self.boss.attack
                if self.player.health <= 0:
                    self.game_over()
                # on supprime la météorite
                self.boss.all_fireballs.remove(fireball)
            elif collision_remove(self.boss, self.player.all_lasers):
                self.boss.health -= self.player.attack
                if self.boss.health <= 0:
                    self.boss.health = self.boss.max_health
                    # self.boss.kill()
                    self.player.score += self.boss.points
                    self.win()

        for laser in self.player.all_lasers:
            laser.move()

        # on dessine sur l'écran les différentes attaques
        self.player.all_lasers.draw(screen)
        self.boss.all_fireballs.draw(screen)

        # on gère les déplacements du personnage en 2D
        if self.pressed.get(
                pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():  # à droite
            self.player.move_right()
        elif self.pressed.get(pygame.K_q) and self.player.rect.x > 0:  # à gauche
            self.player.move_left()
        elif self.pressed.get(
                pygame.K_s) and self.player.rect.y + self.player.rect.height < screen.get_height():  # en bas
            self.player.move_down()
        elif self.pressed.get(pygame.K_z) and self.player.rect.y > 0:  # en haut
            self.player.move_up()

# la méthode qui détermine les ennemis du 1er round
    def round(self, round):
        amount = 6 + 2 * round
        for i in range(1, amount):
            self.all_asteroides.add(astéroide.Model1(self))
            self.all_asteroides.add(astéroide.Model2(self))
            self.all_asteroides.add(astéroide.Model3(self))
        return self.all_asteroides

    # une méthode qui remet le menu principal après le GO

    def main_menu(self):
        self.menu = True
        self.set_game_over = False
        self.is_playing = False

    # la méthode qui (re)start le jeu : elle reset tous les paramètres

    def start(self):
        self.is_playing = True
        self.menu = False
        self.set_game_over = False
        self.winning_screen = False
        self.all_asteroides = pygame.sprite.Group()
        self.player.all_lasers = pygame.sprite.Group()
        self.boss.all_fireballs = pygame.sprite.Group()
        self.current_round = 0
        self.player.score = 0

    # la méthode qui passe au rang suivant

    def new_round(self):
        self.all_asteroides = self.round(self.current_round)
        self.nb_asteroides = len(self.all_asteroides)
        self.current_round += 1

    # la méthode game_over

    def game_over(self):
        self.is_playing = False
        self.set_game_over = True
        # on reset les HP et la position du vaisseau
        self.player.health = self.player.max_health
        self.player.rect.x = 320
        self.player.rect.y = 560
        self.current_round = 0
        # on charge le text du score final
        font = pygame.font.SysFont("monospace", 24)  # la police de base
        self.final_score_text = font.render(f"Final Score : {self.player.score}", True, (0, 0, 0))

    # la méthode lorsqu'on a tué le boss
    def win(self):
        self.is_playing = False
        self.boss_event = False
        self.winning_screen = True
        # on reset les HP et la position du vaisseau
        self.player.health = self.player.max_health
        self.player.rect.x = 320
        self.player.rect.y = 560
        self.current_round = 0
        # on charge le text du score final
        font = pygame.font.SysFont("monospace", 24)  # la police de base
        self.final_score_text = font.render(f"Final Score : {self.player.score}", True, (0, 0, 0))
        self.win_text = font.render('Press EXIT to MAIN MENU', True, (0, 0, 0))
    # la méthode qui met à jour l'écran

    def update(self, screen):
        # on affiche ici le joueur et ses HP
        screen.blit(self.player.image, self.player.rect)
        self.player.update_health_bar(screen)

        # on affiche les textes à l'écran
        font = pygame.font.SysFont("monospace", 24)  # la police de base
        round_text = font.render(f"Round : {self.current_round}", True, (255, 255, 255))  # on créer le texte
        nb_asteroides_text = font.render(f"Nombre d'astéroides : {self.current_number_asteroides} / {self.nb_asteroides}", True, (255, 255, 255))
        score_text = font.render(f"Score : {self.player.score}", True, (255, 255, 255))
        screen.blit(round_text, (20, 20))  # on l'affiche le round
        screen.blit(nb_asteroides_text, (20, 40))  # on affiche le nombre d'ennemis restant pour le round en cours
        screen.blit(score_text, (20, 60))  # on affiche le score

        # on fait bouger les météorites puis on check s'il touche le joueur
        for astre in self.all_asteroides:
            astre.fall()
            # on le supprime s'il sort de l'écran
            if astre.rect.y >= 800:
                self.all_asteroides.remove(astre)
            astre.update_health_bar(screen)  # peut-être à supprimer plus tard
            # on fait bouger les lasers
            if collision(astre, self.all_players):
                self.player.health -= astre.damage
                if self.player.health <= 0:
                    self.game_over()
                # on supprime la météorite
                self.all_asteroides.remove(astre)
            elif collision_remove(astre, self.player.all_lasers):  # attention, collision_remove est diff de collision
                astre.health -= self.player.attack
                if astre.health <= 0:
                    self.all_asteroides.remove(astre)
                    self.player.score += astre.points
            self.current_number_asteroides = len(self.all_asteroides)

        # gestion des mouvements des lasers
        for laser in self.player.all_lasers:
            laser.move()

        # on commence un nouveau round s'il n'y a plus d'astéroide à l'écran
        if len(self.all_asteroides) == 0:
            self.new_round()

        # la condition de début du boss_event
        if self.current_round >= self.last_round:
            self.boss_event = True
            self.is_playing = False
            self.player.all_lasers =pygame.sprite.Group()

        # on dessine sur l'écran
        self.all_asteroides.draw(screen)
        self.player.all_lasers.draw(screen)

        # on gère les déplacements du personnage en 2D

        if self.pressed.get(
                pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():  # à droite
            self.player.move_right()
        elif self.pressed.get(pygame.K_q) and self.player.rect.x > 0:  # à gauche
            self.player.move_left()
        elif self.pressed.get(
                pygame.K_s) and self.player.rect.y + self.player.rect.height < screen.get_height():  # en bas
            self.player.move_down()
        elif self.pressed.get(pygame.K_z) and self.player.rect.y > 0:  # en haut
            self.player.move_up()


# la méthode de check des collisions

def collision(sprite, group):
    return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


def collision_remove(sprite, group):
    return pygame.sprite.spritecollide(sprite, group, True, pygame.sprite.collide_mask)
