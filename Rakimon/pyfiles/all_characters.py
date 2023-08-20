import pygame
from entity import Entity
import rakimons
from rakimons import Rakimon


# la classe Hero indépendante


class Hero(Entity):

    def __init__(self):
        super().__init__("hero", 0, 0, "down")
        self.speed = 5


class PNJ(Entity):

    def __init__(self, name, x, y, direction, dialog, nb_points=1, want_battle=False, monster=None):
        super().__init__(name, x, y, direction)
        if monster is None:
            monster = []
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.nb_points = nb_points
        self.dialog = dialog
        self.want_battle = want_battle
        self.rakimons = monster
        self.points = []
        self.current_point = 0
        self.feet = pygame.Rect(x, y, self.rect.width * 0.5, 35)
        self.is_moving = True

    def load_path(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def move(self):
        if self.is_moving:
            current_point = self.current_point
            target_point = self.current_point + 1
            if target_point >= self.nb_points:
                target_point = 0
            current_rect = self.points[current_point]
            target_rect = self.points[target_point]
            #  move depending on the positions
            if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.move_down()
                self.change_direction('down')
            elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.move_up()
                self.change_direction('up')
            elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.move_left()
                self.change_direction('left')
            elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.move_right()
                self.change_direction('right')
            if self.rect.colliderect(target_rect):
                self.current_point = target_point


# list of all PNJ's, if they want to battle and their rakimons team !

starting_toon = [PNJ("pnj1", 0, 0, "right", ["J'adore faire des allez-retours !"], nb_points=2),
                 PNJ("pnj2", 0, 0, "right", ["Salut ! bienvenue dans Rakimon !", "Amuse-toi bien :)"]),
                 PNJ("pnj0", 0, 0, "right", ["Bonjour Reiikar", "Je suis le Professeur Duquet",
                                                     "Tu ne peux pas t'aventurer plus loin", "Du moins pas sans Rakimon !",
                                                     "Je peux t'en prêter un pour le moment", "Choisis celui que tu préfères."])
                 ]
road1 = [PNJ("pnj3", 0, 0, "down", ["Salut !", "Je serai ton premier adversaire !"], want_battle=True,
             monster=[rakimons.Rakimon('Twixi', 5, 21, [])])]

poke_center = [PNJ("pnj4", 0, 0, "down", ["Bonjour, voulez-vous soigner vos Rakimons ?"])]

shop = [PNJ("pnj3", 0, 0, "down", ["Bonjour, comment puis-je vous aider ?"])]

forest1 = [PNJ("pnj5", 0, 0, "down",["Salut !", "Il y a parfois des objets au sol !", "Sois toujours attentif."])]

road2 = [PNJ("pnj7", 0, 0, "down", ["Je débute ! Sois sympa avec moi"], want_battle=True,
             monster=[rakimons.Rakimon('Crabinou', 4, 18, [])]),
         PNJ("pnj6", 0, 0, "down", ["La ville approche !"], want_battle=True,
             monster=[rakimons.Rakimon('Toaster', 4, 16, [])])
         ]
# starfall PNJs

starfall_poke_center = [PNJ("pnj4", 0, 0, "down", ["Bonjour, voulez-vous soigner vos Rakimons ?"])]

starfall_shop = [PNJ("pnj3", 0, 0, "down", ["Bonjour, comment puis-je vous aider ?"])]

school = [PNJ("pnj7", 0, 0, "left", ["Hey, regardes le tableau !", "Il y a des infos intéressantes"])]