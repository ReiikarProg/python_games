import pygame
import pytmx
import pyscroll
from dataclasses import dataclass
from save import SaveManager
import all_portals
import all_texts
import all_characters
from all_characters import PNJ
from dialogs import DialogBox
from main_menu import MainMenu
from battle import BattleManagement


@dataclass()
class Portal:
    from_world: str  # current world
    origin_point: str  # name of the rect where the TP starts
    target_world: str  # name of the world after TP
    teleport_point: str  # point after TP


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group_layers: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    pnjs: list[PNJ]
    signs: list[pygame.Rect]
    sign_text: str


# the portals parameters is empty if we cannot escape the world
class MapManager:

    def __init__(self, screen, hero, portals=None, pnjs=None):
        if portals is None:
            portals = []
        if pnjs is None:
            pnjs = []
        self.pnjs = pnjs
        self.portals = portals
        self.maps = dict()  # dictionary containing all maps ex: "house" -> Map("house", walls, group)
        self.screen = screen  # local screen
        self.hero = hero  # local hero
        # manage font and box for signs
        self.dialog_box = DialogBox()
        # manage saving
        self.save_manager = SaveManager(".save", "save_data")
        # loading battle management
        self.battle_management = BattleManagement(self.screen)
        # allow to start battle with PNJs
        self.pnj_battle = False
        # allow to start wild battle
        self.wild_encounter = False
        # loading contents
        self.main_menu = MainMenu()
        self.contents = self.main_menu.contents
        # managing current enemy Rakimons
        self.current_enemy = []

        # LOADING ALL MAPS
        self.current_map = "starting_toon"
        # the starting map and its portals
        self.register_map("starting_toon", all_portals.starting_toon, pnjs=all_characters.starting_toon)
        # the 'home' map with the portal
        self.register_map("home", all_portals.home, [])
        # neighbor_house
        self.register_map("neighbor_home", all_portals.neighbor_home, [])
        # loading road1
        self.register_map("road1", all_portals.road1, pnjs=all_characters.road1)
        # loading poke center
        self.register_map("poke_center", all_portals.poke_center, pnjs=all_characters.poke_center)
        # loading shop
        self.register_map('shop', all_portals.shop, pnjs=all_characters.shop)
        # loading forest1
        self.register_map('forest1', all_portals.forest1, pnjs=all_characters.forest1)
        # loading beach1
        self.register_map("beach1", all_portals.beach1, [])
        # loading road2
        self.register_map("road2", all_portals.road2, pnjs=all_characters.road2)
        # loading random house in road2
        self.register_map('random_house', all_portals.random_house, [])

        # loading starfall city and all its maps
        self.register_map('starfall', all_portals.starfall, [])
        self.register_map('starfall_shop', all_portals.starfall_shop, all_characters.starfall_shop)
        self.register_map("starfall_poke_center", all_portals.starfall_poke_center, all_characters.starfall_poke_center)
        self.register_map('school', all_portals.school, all_characters.school)
        # Manage SAVINGS #
        # if the last position is saved, we load it. Else, the default origin point is considered
        origin = self.get_object("starting_point")  # default position value
        last_map = "starting_toon"
        # load last map and position
        self.last_position = self.save_manager.load_game_data(["hero_position"], [[origin.x, origin.y]])
        self.last_map = self.save_manager.load_game_data(["current_map"], last_map)
        # for the moment, we just reset the game before managing save maps.
        self.current_map = self.last_map[0]
        self.hero.position = self.last_position[0]
        # default position : disabled
        # self.hero.position = [origin.x, origin.y]
        # self.current_map = last_map
        self.teleport_pnjs()
        # a list of all possible items : the same for all maps
        self.all_map_items = {"Ball", "Potion", "Money"}

    # text of PNJS by dialog box
    def check_pnj_collision(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.hero.rect) and type(sprite) is PNJ:
                dialog_box.execute(sprite.dialog)
                # reset the battle
                self.pnj_battle = False
                if sprite.want_battle:
                    self.current_enemy = sprite.rakimons
                # checking if the PNJ wants to battle. If yes, print the battle screen after the dialog
            if type(sprite) is PNJ and sprite.want_battle and dialog_box.text_index == len(sprite.dialog):
                # if the PNJ wants to battle and its dialog is over, start the battle
                self.pnj_battle = True


    # method to check collision with items to collect
    def check_item_collision(self, dialog_box):
        all_items = self.get_items()
        for item in all_items:
            item.rect = pygame.Rect(item.x, item.y, item.width, item.height)
            if item.type in self.all_map_items:
                for sprite in self.get_group().sprites():
                    if sprite.feet.colliderect(item.rect):
                        # default need to reset the 'want_battle'
                        self.pnj_battle = False
                        text = [f"Vous avez trouvé {item.name}"]
                        dialog_box.execute(text)
                        self.contents['bag'][item.type] += 0.5

    def check_sign_collision(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_signs()) > -1:
                # default need to reset the 'want_battle'
                self.pnj_battle = False
                text = self.get_map().sign_text
                dialog_box.execute(text)

    def check_collision(self):
        # portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.hero.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
        # checking collisions of the Player with collision object
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

        #  collision with pnjs
        for pnj in self.get_map().pnjs:
            point = pnj.position
            rect = pygame.Rect(point[0]+10, point[1]+10, 20, 20)
            if self.hero.feet.colliderect(rect):
                self.hero.move_back()
                pnj.is_moving = False
                pnj.animation = False
            else:
                pnj.is_moving = True
                pnj.animation = True

    # teleport method

    def teleport_player(self, name):
        point = self.get_object(name)
        self.hero.position[0] = point.x
        self.hero.position[1] = point.y
        self.hero.save_location()

    # method to register map

    def register_map(self, name, portals, pnjs):
        tmx_data = pytmx.util_pygame.load_pygame(f"../assets/maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3  # zooming the map *3
        group_layer = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group_layer.add(self.hero)
        sign_text = []
        if name in all_texts.texts:
            sign_text = all_texts.texts[name]
        for pnj in pnjs:
            group_layer.add(pnj)
        walls = []
        signs = []
        for obj in tmx_data.objects:
            if obj.type == "collision":  # signs are treated differently
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == 'sign':
                signs.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        #  create a map object
        self.maps[name] = Map(name, walls, group_layer, tmx_data, portals, pnjs, signs, sign_text)
        # dictionary

    #  method that return current map from the dictionary

    def get_map(self):
        return self.maps[self.current_map]

    # a few method to get all parameters of the dataclass 'Map'

    def get_group(self):
        return self.get_map().group_layers

    def get_walls(self):
        return self.get_map().walls

    def get_signs(self):
        return self.get_map().signs

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def get_items(self):
        return self.get_map().tmx_data.objects

    def teleport_pnjs(self):
        for map in self.maps:
            map_data = self.maps[map]
            pnjs = map_data.pnjs
            for pnj in pnjs:
                pnj.load_path(map_data.tmx_data)
                pnj.teleport_spawn()

    # method that draw the group of layers and center the camera on the player
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.hero.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collision()
        for pnj in self.get_map().pnjs:
            pnj.move()
            if pnj.nb_points > 1:
                pnj.animate(loop=True)
            else:
                pnj.animation = False
