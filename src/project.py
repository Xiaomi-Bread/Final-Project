import pygame

pygame.init 

screen_width = 1550
screen_height = 790 
screen = pygame.display.set_mode((screen_width, screen_height))

running = True
while running: 
    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

pygame.time.Clock().tick(24)

pygame.quit()