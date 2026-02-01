import pygame

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((500, 400))

# Set the title of the window
pygame.display.set_caption("Simple Window")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()
