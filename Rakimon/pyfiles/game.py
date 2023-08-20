import pygame
from maps import MapManager
from all_characters import Hero
from dialogs import DialogBox
from main_menu import MainMenu
from main_menu import all_sub_menus
# import battle
from battle import BattleManagement
from battle import all_buttons
# import rakimons and moves: temporary
import rakimons
import moves


class Game:

    def __init__(self):
        # create the window, its title and the FPS
        self.screen = pygame.display.set_mode((900, 900))
        pygame.display.set_caption('Rakimon')
        self.fps = 30
        # get the hero Class, at initial location (0, 0)
        self.hero = Hero()
        # the method to manage all maps
        self.map_manager = MapManager(self.screen, self.hero)
        self.dialog_box = DialogBox()
        self.main_menu = MainMenu()
        # the dictionary of all sub menus and their rect
        self.all_sub_menus = all_sub_menus
        # the dictionary of all contents that needs to be saved
        self.contents = self.map_manager.contents
        # managing battles
        self.battle_management = BattleManagement(self.screen)
        # all_buttons are defined in battle file
        self.all_buttons = all_buttons

    def handle_input(self):
        if (not self.main_menu.reading) and (not self.dialog_box.reading):
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_z]:
                self.hero.move_up()
                self.hero.animation = True
                self.hero.change_direction('up')
                self.hero.animate(loop=True)
            elif pressed[pygame.K_s]:
                self.hero.move_down()
                self.hero.animation = True
                self.hero.change_direction('down')
                self.hero.animate(loop=True)
            elif pressed[pygame.K_d]:
                self.hero.move_right()
                self.hero.animation = True
                self.hero.change_direction('right')
                self.hero.animate(loop=True)
            elif pressed[pygame.K_q]:
                self.hero.move_left()
                self.hero.animation = True
                self.hero.change_direction('left')
                self.hero.animate(loop=True)
            else:
                self.hero.image = self.hero.images[0]  # if no key is pressed, we restore initial image

    # the update method

    def update(self):
        self.map_manager.update()
        self.hero.update()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            self.hero.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            # managing dialogs
            self.dialog_box.render(self.screen)
            # print battle with PNJs
            self.battle_management.start_pnj_battle(self.map_manager.current_enemy)
            # print wild battle screen
            self.battle_management.start_wild_battle()

            # printing menus corresponding to battles : atm, we instantiate a fixed rakimon
            my_rakimon = rakimons.Rakimon('Taylor', 5, 20, [moves.CHARGE, moves.DIVERSION, moves.NO, moves.NO])
            self.battle_management.print_rakimon_moves(my_rakimon)

            # start the battle at the end of the dialog with a pnj that wants to
            if self.map_manager.pnj_battle:
                self.battle_management.in_battle = True
            # start wild encounter if the wild_encounter boolean is set to True
            if self.map_manager.wild_encounter:
                self.battle_management.wild_battle = True
            # managing menu and sub-menu
            if self.main_menu.reading:
                self.main_menu.print_menu(self.screen)
                for name in self.all_sub_menus.keys():
                    if self.main_menu.sub_menu == name:
                        if name != 'exit':
                            self.main_menu.open_menu(self.screen, name.upper(), self.contents)
                        else:
                            self.main_menu.reading = False
                            self.main_menu.sub_menu = ""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # save last map and position
                    self.map_manager.save_manager.save_game_data([self.hero.position], ["hero_position"])
                    self.map_manager.save_manager.save_game_data([self.map_manager.current_map], ['current_map'])
                    self.map_manager.save_manager.save_game_data([self.contents], ['contents'])
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.map_manager.check_pnj_collision(self.dialog_box)
                        self.map_manager.check_sign_collision(self.dialog_box)
                        self.map_manager.check_item_collision(self.dialog_box)

                    # manage the main menu

                    if event.key == pygame.K_SPACE:
                        # we print the main menu when pressing 'SPACE'
                        self.main_menu.reading = True
                        # pressing 'x' while menu open close it
                    if event.key == pygame.K_x and self.main_menu.reading:
                        self.main_menu.reading = False
                        # open sub-menu using mouse

                        # managing wild battle (only temporary check)
                    if event.key == pygame.K_b:
                        self.battle_management.wild_battle = True

                elif event.type == pygame.MOUSEBUTTONDOWN and self.main_menu.reading:
                    for name in self.all_sub_menus:
                        if self.all_sub_menus[name].collidepoint(event.pos):
                            self.main_menu.sub_menu = name
                        if self.all_sub_menus['return'].collidepoint(event.pos):
                            self.main_menu.sub_menu = ""
                # managing buttons while in battle (works for PNJ and wild battle)
                elif event.type == pygame.MOUSEBUTTONDOWN and (self.battle_management.in_battle or self.battle_management.wild_battle):
                    # closing battle menu if 'RUN' is pressed
                    if self.all_buttons['run'].collidepoint(event.pos):
                        # reset all booleans if 'run' is pressed
                        # for battle with PNJ
                        self.battle_management.in_battle = False
                        self.map_manager.pnj_battle = False
                        # for wild battle
                        self.battle_management.wild_battle = False
                        self.map_manager.wild_encounter = False
                    # if "RETOUR" is pressed, close all submenus (moves, rakimon, bag, ...)
                    if self.all_buttons['back'].collidepoint(event.pos):
                        self.battle_management.print_moves = False
                    #  if "BATTLE" is pressed, print moves
                    if self.all_buttons['battle'].collidepoint(event.pos):
                        # in this case, we want to print the moves of the current rakimon on the screen, together with a 'return' button
                        self.battle_management.print_moves = True
                        # TODO : cannot press RUN while moves are printed. aka suppress menus while moves are printed ?
                        print("You want to attack !")

            pygame.display.flip()

            clock.tick(self.fps)


