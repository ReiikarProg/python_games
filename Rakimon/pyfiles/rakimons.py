import pygame
import moves


class Rakimon(pygame.sprite.Sprite):

    def __init__(self, name, level, hp_max, moves):
        super().__init__()
        self.name = name
        self.level = level
        self.image = all_starters[name]
        self.hp = hp_max
        self.hp_max = hp_max
        self.moves = moves
        self.exp = 0
        # managing printing on screen
        self.ally_position = (120, 550)
        self.enemy_position = (550, 50)
        pygame.font.init()  # needs to be initialized since we are outside the main pygame.init()
        self.font = pygame.font.Font('../assets/dialogs/dialog_font.ttf', 20)
        self.text_name = self.font.render(self.name.upper(), False, (0, 0, 0))  # triple RGB color
        self.text_level = self.font.render("LVL." + str(self.level), False, (0, 0, 0))
        self.text_hp = self.font.render(str(self.hp) + "/" + str(self.hp_max), False, (0, 0, 0))

    # a function that blit everything related to a Rakimon in battle

    def blit_rakimon(self, screen, is_ally):
        if is_ally:
            blit_with_transparency(screen, self.image, (self.ally_position[0], self.ally_position[1] + 30), [0, 0, 0])
            screen.blit(self.text_name, (self.ally_position[0], self.ally_position[1]))
            screen.blit(self.text_level, (self.ally_position[0], self.ally_position[1] + 25))
            screen.blit(self.text_hp, (self.ally_position[0], self.ally_position[1] + 50))
            blit_health_bar(screen, self.ally_position[0], self.ally_position[1] + 85)
        else:
            blit_with_transparency(screen, self.image, self.enemy_position, [0, 0, 0])
            screen.blit(self.text_name, (self.enemy_position[0], self.enemy_position[1] + 256))
            screen.blit(self.text_level, (self.enemy_position[0], self.enemy_position[1] + 281))
            screen.blit(self.text_hp, (self.enemy_position[0], self.enemy_position[1] + 304))
            blit_health_bar(screen, self.enemy_position[0], self.enemy_position[1] + 334)


# method for update health bar

def blit_health_bar(screen, x, y):
    pygame.draw.rect(screen, (0, 0, 0), [x, y, 256, 8])
    pygame.draw.rect(screen, (51, 51, 255), [x, y, 128, 8])


# method to blit the sprite of the Rakimon with a given color transparency

def blit_with_transparency(target, source, location, transparency):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_colorkey(transparency)
    target.blit(temp, location)


def get_sprite(sheet, x, y, size1=64, size2=64, final_size=(256, 256)):
    image = pygame.Surface([size1, size2])
    image.blit(sheet, (0, 0), (x, y, size1, size2))
    image = pygame.transform.scale(image, final_size)
    return image


starter_sprite = pygame.image.load('../assets/rakimons/starters.png')

all_starters = {'Taylor': get_sprite(starter_sprite, 0, 0),
                'Flambil': get_sprite(starter_sprite, 62, 0),
                'Twixi': get_sprite(starter_sprite, 0, 64),
                'Crabinou': get_sprite(starter_sprite, 256, 66),
                'Toaster': get_sprite(starter_sprite, 0, 192)
                }
