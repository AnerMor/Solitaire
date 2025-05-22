import pygame

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 700)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the window title
pygame.display.set_caption('My Game')
image = pygame.image.load('card.jpg')
image = pygame.transform.scale(image, (200,200))

image2 = pygame.image.load('card.jpg')
image2 = pygame.transform.scale(image2, (250,250))


# Draw a circle
pygame.draw.circle(screen, (0, 0, 255), (320, 240), 100)


x,y = 0, 0
# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))
    screen.blit(image2, (0, 0))

    screen.blit(image, (x,y))
    x += 1
    y += 1
    if (x > 300):
        x = 300

    if (y > 300):
        y = 300
    # Update the display
    pygame.display.update()


# Quit Pygame
pygame.quit()
