import pygame

# temporary check
import rakimons
import moves


class BattleManagement:

    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("../assets/images/battle_bg.jpg")
        self.box = pygame.image.load('../assets/dialogs/dialog_box.png')
        self.box = pygame.transform.rotate(self.box, 90)
        self.box = pygame.transform.scale(self.box, (200, 250))
        # the box where all moves are printed
        self.moves_box = pygame.transform.scale(self.box, (500, 350))
        # creating button titles
        self.font = pygame.font.Font('../assets/dialogs/dialog_font.ttf', 22)
        self.attaque = self.font.render('ATTAQUE', False, [0, 0, 0])
        self.rakimons = self.font.render('RAKIMONS', False, [0, 0, 0])
        self.ball = self.font.render('BALL', False, [0, 0, 0])
        self.run = self.font.render('FUITE', False, [0, 0, 0])
        self.back = self.font.render('RETOUR', False, [0, 0, 0])
        # condition to start pnj battle
        self.in_battle = False
        # condition to start wild battle
        self.wild_battle = False
        # condition to print moves when battle is pressed
        self.print_moves = False

    def print_rakimon_moves(self, rakimon):
        rakimon_moves = rakimon.moves
        if self.print_moves:
            self.screen.blit(self.moves_box, (50, 500))  # box size : (500, 350)
            self.screen.blit(self.back, (249, 775))  # letter size : 17 -> "RETOUR" size = 17*6
            # keep in mind that move is a DataClass
            move_1_name = self.font.render(rakimon_moves[0].name.upper(), False, [0, 0, 0])
            move_2_name = self.font.render(rakimon_moves[1].name.upper(), False, [0, 0, 0])
            move_3_name = self.font.render(rakimon_moves[2].name.upper(), False, [0, 0, 0])
            move_4_name = self.font.render(rakimon_moves[3].name.upper(), False, [0, 0, 0])
            self.screen.blit(move_1_name, (125, 550))
            self.screen.blit(move_2_name, (325, 550))
            self.screen.blit(move_3_name, (125, 625))
            self.screen.blit(move_4_name, (325, 625))

    # an example : rakimons.Rakimon('Taylor', 5, 20, [moves.CHARGE, moves.DIVERSION])

    # managing wild battle
    def start_wild_battle(self):
        if self.wild_battle:
            # print the background
            self.screen.blit(self.background, (0, 0))
            # printing the box
            self.screen.blit(self.box, (600, 600))
            # printing buttons
            self.screen.blit(self.attaque, (630, 630))
            self.screen.blit(self.rakimons, (630, 680))
            self.screen.blit(self.ball, (630, 730))
            self.screen.blit(self.run, (630, 780))
            # blit the first rakimon on your team
            # TODO : here, the moves are default set. It needs to be dynamic.
            taylor = rakimons.Rakimon('Taylor', 5, 20, [moves.CHARGE, moves.DIVERSION])
            taylor.blit_rakimon(self.screen, True)
            # print wild rakimons ?

    # This method print the battle screen if in_battle = True

    def start_pnj_battle(self, enemy_rakimons=None):
        if self.in_battle:
            # print the background
            self.screen.blit(self.background, (0, 0))
            # printing the box
            self.screen.blit(self.box, (600, 600))
            # printing buttons
            self.screen.blit(self.attaque, (630, 630))
            self.screen.blit(self.rakimons, (630, 680))
            self.screen.blit(self.ball, (630, 730))
            self.screen.blit(self.run, (630, 780))
            # blit the first rakimon on your team
            taylor = rakimons.Rakimon('Taylor', 5, 20, [])
            taylor.blit_rakimon(self.screen, True)
            # blit first enemy rakimon : set to default here
            if enemy_rakimons is None:
                enemy_rakimons = [rakimons.Rakimon('Flambil', 3, 15, [])]
            for opponent_rakimons in enemy_rakimons:
                opponent_rakimons.blit_rakimon(self.screen, False)


# self.font = pygame.font.Font('../assets/dialogs/dialog_font.ttf', 20)

# all buttons and their rectangles : the length of the rectangle equals 17* the number of letters
all_buttons = {"battle": pygame.rect.Rect(630, 630, 7 * 17, 25),
               "rakimons": pygame.rect.Rect(630, 680, 8 * 17, 25),
               "ball": pygame.rect.Rect(630, 730, 4 * 17, 25),
               "run": pygame.rect.Rect(630, 780, 5 * 17, 25),
               "back": pygame.rect.Rect(249, 775, 6*17, 25) # the moves return button
               }

