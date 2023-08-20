# Le fichier main du jeu

# on importe les autres fichiers et modules

import pygame
from game import Game

pygame.init()

# on créer la fenêtre du jeu

pygame.display.set_caption('Shooter Game')
screen = pygame.display.set_mode((720, 800))
clock = pygame.time.Clock()
FPS = 60

# on charge les images liées au jeu:

# l'image de fond
background = pygame.image.load('assets/background.png')
background = pygame.transform.rotate(background, 180)
background = pygame.transform.scale(background, (screen.get_size()))
# le bouton play
button = pygame.image.load('assets/button.png')
button = pygame.transform.scale(button, (200, 80))
button_rect = button.get_rect()
button_rect.x = 250
button_rect.y = 370
# Logo pygame
logo = pygame.image.load('assets/pygame_logo.png')
logo = pygame.transform.scale(logo, (500, 160))
logo_rect = logo.get_rect()
logo_rect.x = 120
logo_rect.y = 220
# affichage game_over
GameOverLogo = pygame.image.load('assets/game_over.png')
GameOverLogo = pygame.transform.scale(GameOverLogo, (600, 500))
GameOverLogo_rect = GameOverLogo.get_rect()
GameOverLogo_rect.x = 60
GameOverLogo_rect.y = 0
# win logo
WinLogo = pygame.image.load('assets/win.png')
WinLogo = pygame.transform.scale(WinLogo, (450, 250))
WinLogo_rect = WinLogo.get_rect()
WinLogo_rect.x = 130
WinLogo_rect.y = 150
# exit button
exit_logo = pygame.image.load('assets/exit.png')
exit_logo = pygame.transform.scale(exit_logo, (200, 80))
exit_logo_rect = GameOverLogo.get_rect()
exit_logo_rect.x = 500
exit_logo_rect.y = 700

game = Game()

# Début de la boucle principale

run = True

while run:

    # l'affichage à l'écran, qui se fait toujours : le background

    screen.blit(background, (0, 0))  # on affiche le background

    # l'affichage du jeu quand celui-ci est en cours
    if game.is_playing:
        game.update(screen)
    # on affiche le game over lorsque le joueur a perdu
    elif game.set_game_over:
        screen.fill((118, 56, 39))
        screen.blit(exit_logo, exit_logo_rect)
        screen.blit(GameOverLogo, GameOverLogo_rect)
        screen.blit(game.win_text, (200, 420))
        screen.blit(game.final_score_text, (230, 400))
    # sinon, on affiche l'écran de démarrage
    elif game.menu:
        screen.blit(button, button_rect)
        screen.blit(logo, logo_rect)
    elif game.boss_event:
        game.start_boss_event(screen)
    elif game.winning_screen:
        screen.fill((70, 229, 41))
        screen.blit(exit_logo, exit_logo_rect)
        screen.blit(WinLogo, WinLogo_rect)
        screen.blit(game.win_text, (200, 520))
        screen.blit(game.final_score_text, (230, 500))

    pygame.display.flip()  # on met à jour l'écran
    clock.tick(FPS)  # on gère les FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            print('Fermeture du jeu')

        # les commandes de récupération des touches

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            # sur la touche e, on tire un laser
            if event.key == pygame.K_SPACE:
                game.player.fire_laser()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        # on peut aussi tirer à la souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.player.fire_laser()

            # on regarde si le bouton PLAY est enclenché
            if (button_rect.collidepoint(event.pos)) and (game.is_playing == False) and (game.boss_event == False):
                # on lance le jeu en ce cas
                game.start()
            if exit_logo_rect.collidepoint(event.pos) and (game.set_game_over or game.winning_screen):
                # on relance le jeu
                game.main_menu()

pygame.quit()
