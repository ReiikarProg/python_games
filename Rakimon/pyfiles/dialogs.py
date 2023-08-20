import pygame


class DialogBox:
    X_POSITION = 100
    Y_POSITION = 750

    def __init__(self):
        self.box = pygame.image.load('../assets/dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = ['Empty dialog']
        self.text_index = 0
        self.font = pygame.font.Font('../assets/dialogs/dialog_font.ttf', 20)
        self.reading = False

    def execute(self, dialog):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render(self, screen):
        if self.reading:
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index], False, (0, 0, 0))  # triple RGB color
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30))

    def next_text(self):
        self.text_index += 1
        if self.text_index >= len(self.texts):
            # close box
            self.reading = False
