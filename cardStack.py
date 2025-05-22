from card import CARD_SIZE
import pygame

START_Y = 190
START_X = 50
X_DISTANCE = 90
Y_DISTANCE = 30
FOUNDATION_SPACE = 110
FOUNDATION_Y = 20
FOUNDATION_START_X = 300
TYPES = ["heart", "spade", "diamond", "club"]


class Stack:
    def __init__(self, index, cards, isFoundation=False, foundType=None):
        self.index = index
        self.cards = cards
        if len(self.cards) > 0:
            self.cards[-1].show()

        self.isFoundation = isFoundation
        self.foundationType = foundType
        if self.isFoundation:
            self.image = pygame.image.load(f'images/{self.foundationType}-foundation.png')
            self.image = pygame.transform.scale(self.image, CARD_SIZE)
            print(self.foundationType)
            self.leftX = FOUNDATION_START_X + FOUNDATION_SPACE * index
        else:
            self.leftX = START_X + X_DISTANCE * index

        self.rightX = self.leftX + CARD_SIZE[0]

    def __repr__(self):
        return str(self.cards)

    def printStack(self, screen):
        if self.isFoundation:
            if len(self.cards) != 0:
                self.cards[-1].printCard(screen, (FOUNDATION_START_X + self.index * FOUNDATION_SPACE, FOUNDATION_Y))
            else:
                screen.blit(self.image, (FOUNDATION_START_X + self.index * FOUNDATION_SPACE, FOUNDATION_Y))
        else:
            for i in range(len(self.cards)):
                self.cards[i].printCard(screen, (START_X + self.index * X_DISTANCE, START_Y + i * Y_DISTANCE))

    def getCardIndex(self, y):
        print(f"y: {y}")
        if y < START_Y:
            return -10
        if (len(self.cards)-1)*Y_DISTANCE + START_Y + CARD_SIZE[1] < y:
            return -20
        if len(self.cards) == 0:
            return 0

        y -= START_Y
        for i in range(1, len(self.cards)):
            if y < i*Y_DISTANCE:
                return i-1

        return len(self.cards)-1

    def removeCards(self, num):  # num - amount of cards to remove
        size = len(self.cards)
        if size >= num:
            l = self.cards[num:]  # cards tp remove
            self.cards = self.cards[:num]  # update stack
            if len(self.cards) > 0:
                self.cards[-1].show()
            print(f"current {self.cards}")
            return l
        print(f" remove cards: {self.cards} {num}")


    def addCards(self, l):
        print(f"{self.cards}  {l}")
        self.cards += l






