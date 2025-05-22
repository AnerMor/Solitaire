import pygame
import os

CARD_SIZE = (70, 140)
CARD_NAMES = {  # dictionary to convert card symbols to numbers
    1: 'ace',
    11: 'jack',
    12: 'queen',
    13: 'king'
}


class Card:
    def __init__(self, value, type, show):
        self.value = value
        self.type = type
        if type in ["heart", "diamond"]:
            self.color = 1  # red
        else:
            self.color = 2  # black

        # sets correct image to each card
        if self.value in CARD_NAMES:
            self.image_path = f"images/{CARD_NAMES[self.value]}_of_{self.type}s2.png"
        else:
            self.image_path = f"images/{self.value}_of_{self.type}s.png"
        self.hidden = not show
        if show:
            self.image = pygame.image.load(self.image_path)
        else:
            self.image = pygame.image.load('images/hidden.jpg')

        self.image = pygame.transform.scale(self.image, CARD_SIZE)

    def __repr__(self):
        return f"{self.type}-{self.value}: {'hidden' if self.hidden else 'shown'}"

    def printCard(self, screen, pos):
        screen.blit(self.image, pos)

    def show(self):
        self.hidden = False
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, CARD_SIZE)
