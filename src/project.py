import pygame

pygame.init()

#Main Resolution
screen_width = 1550
screen_height = 790 
screen = pygame.display.set_mode((screen_width, screen_height))
WHITE = (255, 255, 255)

player_model_width = 230 
player_model_height = 170 

#Images for the game
player_model = pygame.image.load("WW1Tank.png").convert_alpha()
player_model = pygame.transform.scale(player_model, (player_model_width, player_model_height))

x_player = screen_width // 3 - player_model_width //2 
y_player = screen_height - 450

#Game Loop
running = True
while running: 
    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    screen.fill(WHITE)

    screen.blit(player_model, (x_player, y_player))

    pygame.display.flip()

    pygame.time.Clock().tick(24)

pygame.quit()