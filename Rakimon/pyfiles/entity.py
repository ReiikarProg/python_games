import pygame


# a first class to animate moves of each entity
class AnimHero(pygame.sprite.Sprite):

    def __init__(self, name, direction):
        super().__init__()
        self.name = name
        self.sprite_sheet = pygame.image.load(f'../assets/sprites/{self.name}.png')
        self.image = all_animations[self.name].get(direction)[0]  # the first image of each direction has y=0
        self.current_image = 0
        self.animation = False
        self.images = all_animations[self.name].get(direction)
        self.delay = 100
        self.laps = 0

    def animate(self, loop=False):
        self.laps += 25
        if self.animation and self.laps >= self.delay:
            self.current_image += 1
            self.laps = 0
        if self.current_image >= len(self.images):
            self.current_image = 0
            if loop is False:
                self.animation = False
        self.image = self.images[self.current_image]


# method that get the image at location (x,y) of size 32*32 px of the given sprite_sheet

def get_image(sprite_sheet, x, y, size1=32, size2=32):
    image = pygame.Surface([size1, size2])
    image.blit(sprite_sheet, (0,0), (x, y, 32, 32))
    return image


# method that load a line of 4 images of the corresponding sprite_sheet associated to sprite_name

def load_animation_images(x, name, size1=32, size2=32):
    images = []
    sprite_sheet = pygame.image.load(f'../assets/sprites/{name}.png')
    # there are 4 images for each direction
    for num in [0, 32, 64, 96]:
        local_image = get_image(sprite_sheet, num, x, size1, size2)
        images.append(local_image)
    return images


all_animations = {"hero": {'down': load_animation_images(0, "hero"), 'up': load_animation_images(96, "hero"),
                           'right': load_animation_images(64, "hero"), 'left': load_animation_images(32, "hero")},
                  "pnj0": {'down': load_animation_images(0, "pnj0"), 'up': load_animation_images(96, "pnj0"),
                           'right': load_animation_images(64, "pnj0"), 'left': load_animation_images(32, "pnj0")},
                  "pnj1": {'down': load_animation_images(0, "pnj1"), 'up': load_animation_images(96, "pnj1"),
                           'right': load_animation_images(64, "pnj1"), 'left': load_animation_images(32, "pnj1")},
                  "pnj2": {'down': load_animation_images(4, "pnj2"), 'up': load_animation_images(100, "pnj2"),
                           'right': load_animation_images(68, "pnj2"), 'left': load_animation_images(36, "pnj2")},
                  "pnj3": {'down': load_animation_images(4, "pnj3"), 'up': load_animation_images(100, "pnj3"),
                           'right': load_animation_images(68, "pnj3"), 'left': load_animation_images(36, "pnj3")},
                  "pnj4":  {'down': load_animation_images(4, "pnj4"), 'up': load_animation_images(100, "pnj4"),
                            'right': load_animation_images(68, "pnj4"), 'left': load_animation_images(36, "pnj4")},
                  "pnj5": {'down': load_animation_images(4, "pnj5"), 'up': load_animation_images(100, "pnj5"),
                           'right': load_animation_images(68, "pnj5"), 'left': load_animation_images(36, "pnj5")},
                  "pnj6": {'down': load_animation_images(4, "pnj6"), 'up': load_animation_images(100, "pnj6"),
                           'right': load_animation_images(68, "pnj6"), 'left': load_animation_images(36, "pnj6")},
                  "pnj7": {'down': load_animation_images(4, "pnj7"), 'up': load_animation_images(100, "pnj7"),
                           'right': load_animation_images(68, "pnj7"), 'left': load_animation_images(36, "pnj7")},
                  }


class Entity(AnimHero):

    # the init class : x, y are integers that represent the initial position of the character

    def __init__(self, name, x, y, direction):
        super().__init__(name, direction)
        self.image.set_colorkey([0, 0, 0])  # release the black background color
        self.rect = self.image.get_rect().move(1000, 1000)
        self.position = [x, y]
        self.speed = 2
        self.feet = pygame.Rect(x, y, self.rect.width*0.5, 12)
        self.old_position = self.position.copy()  # save the position of the player

    def save_location(self):
        self.old_position = self.position.copy()

    # method to change the animation depending on the movement
    def change_direction(self, direction):
        self.images = all_animations[self.name].get(direction)
        self.image = all_animations[self.name].get(direction)[0]
        for img in self.images:
            img.set_colorkey((0, 0, 0))  # removing black background of the picture

    # movement methods

    def move_right(self): self.position[0] += self.speed

    def move_left(self): self.position[0] -= self.speed

    def move_down(self): self.position[1] += self.speed

    def move_up(self): self.position[1] -= self.speed

    # update the position of the player

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        # self.animate_player(loop=True)

    # move back the player before an eventual collision

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
