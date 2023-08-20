import pygame
from save import SaveManager
from math import floor


class MainMenu:
    X_POSITION = 550
    Y_POSITION = 100

    def __init__(self):
        self.save_manager = SaveManager(".save", "save_data")
        self.box = pygame.image.load('../assets/dialogs/dialog_box.png')
        self.box = pygame.transform.rotate(self.box, 90)
        self.box = pygame.transform.scale(self.box, (300, 700))
        self.sub_menu_box = pygame.transform.scale(self.box, (900, 900))
        self.font = pygame.font.Font('../assets/dialogs/dialog_font.ttf', 22)
        # submenu titles
        self.encyclopedia = self.font.render('ENCYCLOPEDIA', False, [0, 0, 0])
        self.rakimons = self.font.render('RAKIMONS', False, [0, 0, 0])
        self.bag = self.font.render('BAG', False, [0, 0, 0])
        self.status = self.font.render('STATUS', False, [0, 0, 0])
        self.options = self.font.render('OPTIONS', False, [0, 0, 0])
        self.credits = self.font.render('CREDITS', False, [0, 0, 0])
        self.exit = self.font.render('EXIT', False, [0, 0, 0])
        self.quit = self.font.render('RETURN', False, [0, 0, 0])
        self.reading = False
        # TO KEEP ?
        self.sub_menu = ""
        # contents need to come from the MapManager
        self.contents = initial_contents
        # load previous content. Unless it is the default value
        self.contents = self.save_manager.load_game_data(["contents"], initial_contents)[0]

    # print the full menu

    def print_menu(self, screen):
        if self.reading:
            # printing words
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            screen.blit(self.encyclopedia, (self.X_POSITION + 50, self.Y_POSITION + 100))
            screen.blit(self.rakimons, (self.X_POSITION + 50, self.Y_POSITION + 180))
            screen.blit(self.bag, (self.X_POSITION + 50, self.Y_POSITION + 260))
            screen.blit(self.status, (self.X_POSITION + 50, self.Y_POSITION + 340))
            screen.blit(self.options, (self.X_POSITION + 50, self.Y_POSITION + 420))
            screen.blit(self.credits, (self.X_POSITION + 50, self.Y_POSITION + 500))
            screen.blit(self.exit, (self.X_POSITION + 50, self.Y_POSITION + 580))

    # open the menu associated to 'name'

    def open_menu(self, screen, name, contents):
        position = (150, 150)
        position_2 = (450, 150)
        if self.reading:
            screen.blit(self.sub_menu_box, (0, 0))
            maj_name = self.font.render(name.upper(), False, [0, 0, 0])
            screen.blit(maj_name, (400, 100))
            # if we open the bag, we need to print all its items
            if name == "BAG":
                for item in contents[name.lower()]:
                    position = (position[0], position[1] + 50)
                    position_2 = (position_2[0], position_2[1] + 50)
                    item_text = self.font.render(item, False, [0, 0, 0])
                    item_quantity = self.font.render(str(floor(contents[name.lower()][item])), False, [0, 0, 0])
                    screen.blit(item_text, position)
                    screen.blit(item_quantity, position_2)
            screen.blit(self.quit, (700, 800))


# dictionary of all sub_menus and their rect : X_position = 550 and Y_position = 100
all_sub_menus = {"encyclopedia": pygame.rect.Rect(550 + 50, 100 + 100, 12 * 17, 25),
                 "rakimons": pygame.rect.Rect(550 + 50, 100 + 180, 17 * 8, 25),
                 "bag": pygame.rect.Rect(550 + 50, 100 + 260, 17 * 3, 25),
                 "status": pygame.rect.Rect(550 + 50, 100 + 340, 17 * 6, 25),
                 "options": pygame.rect.Rect(550 + 50, 100 + 420, 17 * 7, 25),
                 "credits": pygame.rect.Rect(550 + 50, 100 + 500, 17 * 7, 25),
                 "exit": pygame.rect.Rect(550 + 50, 100 + 580, 17 * 4, 25),
                 "return": pygame.rect.Rect(700, 800, 17 * 6, 25)
                 }

initial_contents = {"encyclopedia": {'#1': 'Bulbizarre', '#2': "Caratank"},
                    "rakimons": {"": ""},
                    "bag": {"Money": 1000, "Potion": 0, "Ball": 0, },
                    "status": {"Nom": "Reiikar", "Badge": 0},
                    "options": {"Vitesse dialogue": "Par défaut", "COMMANDES": "", "Haut": "Z", "Bas": "S",
                                "Gauche": "Q",
                                "Droite": "D", "Ouvrir menu": "ESPACE"},
                    "credits": {"Ce jeu est en cours de développement": ""},
                    "exit": {"": ""}
                    }
