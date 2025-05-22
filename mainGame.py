# made by Aner Mor
# january 2023
import pygame
import random
from card import Card, CARD_SIZE
from cardStack import Stack, START_Y, Y_DISTANCE, FOUNDATION_Y

TYPES = ["heart", "spade", "diamond", "club"]
CLOSED_PILE_X = 50
CLOSED_PILE_Y = 20
OPEN_PILE_X = 150
OPEN_PILE_Y = 20

INDEX_CLOSED_PILE = 20
INDEX_OPEN_PILE = 21

INDEX_FOUNDATION = 7


class Game:

    def printStacks(self, stacks):
        for stack in stacks:
            print(stack)

    def shuffle(self):
        cards = []
        for type in TYPES:
            for i in range(1, 14):
                cards.append(Card(i, type, False))
        random.shuffle(cards)
        for card in cards:
            print(card)
        return cards

    def draw_rectangle(self):  # creates a rectangle around the selected cards
        height = CARD_SIZE[1]
        if self.selected_card_index[0] == INDEX_OPEN_PILE:
            left, top = OPEN_PILE_X, OPEN_PILE_Y
        elif self.selected_card_index[0] != INDEX_CLOSED_PILE:
            left = self.stacks[self.selected_card_index[0]].leftX
            if self.selected_card_index[0] < INDEX_FOUNDATION:
                top = START_Y + self.selected_card_index[1] * Y_DISTANCE
                height = CARD_SIZE[1] + \
                         Y_DISTANCE * (len(self.stacks[self.selected_card_index[0]].cards) - self.selected_card_index[
                    1] - 1)
            else:
                top = FOUNDATION_Y
        else:
            self.selected_card_index = None
            return
        r = pygame.Rect((left - 2, top - 2, 75, height + 5))
        pygame.draw.rect(self.screen, (255, 0, 0), r, 3, 2)

    def printScreen(self):
        self.screen.fill((0, 160, 0))  # set background color
        if len(self.closed_pile) != 0:
            self.closed_pile[-1].printCard(self.screen, (CLOSED_PILE_X, CLOSED_PILE_Y)) # print last card

        if len(self.open_pile) != 0:
            self.open_pile[-1].printCard(self.screen, (OPEN_PILE_X, OPEN_PILE_Y))
        for stack in self.stacks:
            stack.printStack(self.screen)
        if self.selected_card_index is not None:
            self.draw_rectangle()

        pygame.display.update()

    def handleClick(self, event):
        stack_index = -1
        pos = event.pos  # get mouse click coordinates
        print(pos)

        if CLOSED_PILE_X <= pos[0] <= CLOSED_PILE_X + CARD_SIZE[0] and CLOSED_PILE_Y <= pos[1] <= CLOSED_PILE_Y + \
                CARD_SIZE[1]:
            if len(self.closed_pile) != 0:
                self.open_pile.append(self.closed_pile.pop())
                self.open_pile[-1].show()
            print(f"closed pile {self.closed_pile}")
            print(f"open pile {self.open_pile}")
            return INDEX_CLOSED_PILE, -1

        if OPEN_PILE_Y <= pos[1] <= OPEN_PILE_Y + CARD_SIZE[1]:  # top row
            for i in range(INDEX_FOUNDATION, INDEX_FOUNDATION + 4):
                if self.stacks[i].leftX <= pos[0] <= self.stacks[i].rightX:
                    # print(f"foundation: {i}")
                    return i, len(self.stacks[i].cards) - 1

            if OPEN_PILE_X <= pos[0] <= OPEN_PILE_X + CARD_SIZE[0]:
                return INDEX_OPEN_PILE, len(self.open_pile) - 1

        for stack in self.stacks[:INDEX_FOUNDATION]:
            if stack.rightX >= pos[0] >= stack.leftX:
                stack_index = stack.index
                break

        if stack_index == -1:
            print('no stack was clicked')
            return -1, -1

        card_index = self.stacks[stack_index].getCardIndex(pos[1])

        print('card index ' + str(card_index))
        print(f"stack index: {stack_index}")
        if card_index < 0:
            return -1, -1
        if len(self.stacks[stack_index].cards) != 0 and self.stacks[stack_index].cards[card_index].hidden:
            return -1, -1
        return stack_index, card_index

    def isLegalMove(self, sourceCard, destCard, foundation=None):
        if foundation is not None:
            if sourceCard.type != foundation.foundationType:
                return False
            if len(foundation.cards) == 0:
                return sourceCard.value == 1 # check if ace
            return sourceCard.value == foundation.cards[-1].value + 1 # check if destination card has higher value

        if destCard is None:
            return sourceCard.value == 13  # check if king
        return sourceCard.value == destCard.value - 1 and sourceCard.color != destCard.color

    def moveCards(self, sourceStackIndex, sourceCardIndex, targetStackIndex):
        print(f"source card: {sourceCardIndex} , stack: {sourceStackIndex}, target: {targetStackIndex}")
        if sourceStackIndex == targetStackIndex:
            print("same stack")
            return

        dest_foundation = None
        if targetStackIndex >= INDEX_FOUNDATION:
            dest_foundation = self.stacks[targetStackIndex]
        destcard = self.stacks[targetStackIndex].cards[-1] if len(self.stacks[targetStackIndex].cards) != 0 else None
        if sourceStackIndex == INDEX_OPEN_PILE:
            print("source is INDEX_OPEN_PILE")
            if len(self.open_pile) == 0:
                print('open pile empty')
                return
            card = self.open_pile[-1]
            if self.isLegalMove(card, destcard, dest_foundation):
                self.open_pile.pop()
                self.stacks[targetStackIndex].addCards([card])
            return
        if len(self.stacks[sourceStackIndex].cards) == 0:
            print("removing from empty stack")
            return
        if not self.isLegalMove(self.stacks[sourceStackIndex].cards[sourceCardIndex], destcard, dest_foundation):
            return
        removed_cards = self.stacks[sourceStackIndex].removeCards(sourceCardIndex)
        print(f"removed card: {removed_cards}")
        self.stacks[targetStackIndex].addCards(removed_cards)

    def main(self):
        pygame.init()
        window_size = (800, 700)
        self.screen = pygame.display.set_mode(window_size)

        pygame.display.set_caption('Solitaire')

        cards = self.shuffle()
        self.stacks = list()

        for i in range(1, 8):  # prepare stacks
            l = [cards.pop() for _ in range(i)]
            self.stacks.append(Stack(i - 1, l))

        print("pile: ", cards)
        self.closed_pile = cards  # rest of the cards
        self.open_pile = []

        for i in range(4):
            self.stacks.append(Stack(i, [], True, TYPES[i]))  # prepare foundations

        self.selected_card_index = None
        self.printScreen()

        running = True
        while running:
            # Handle events
            # self.printScreen()
            for event in pygame.event.get():
                self.printScreen()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked_stack, clicked_card = self.handleClick(event)
                    # print(f"here2: {(clicked_stack, clicked_card)}")
                    if clicked_stack == INDEX_CLOSED_PILE:
                        self.selected_card_index = None
                        self.printScreen()
                        continue
                    if clicked_stack < 0:
                        self.printScreen()
                        continue

                    if self.selected_card_index is None:
                        self.selected_card_index = clicked_stack, clicked_card
                        print(f"selected_card_index: {self.selected_card_index}")
                    else:
                        if clicked_stack == INDEX_OPEN_PILE:
                            self.printScreen()
                            continue
                        self.moveCards(self.selected_card_index[0], self.selected_card_index[1], clicked_stack)

                        self.selected_card_index = None

                self.printScreen()
                # printStacks(stacks)

                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
