import pygame

pygame.init()

#Main Resolution
screen_width = 1550
screen_height = 790 
screen = pygame.display.set_mode((screen_width, screen_height))
WHITE = (255, 255, 255)

player_model_width = 230 
player_model_height = 170 

player_hitbox_width = 140
player_hitbox_height = 80

#Images for the game
player_model = pygame.image.load("WW1Tank.png").convert_alpha()
player_model = pygame.transform.scale(player_model, (player_model_width, player_model_height))

x_player = screen_width // 3 - player_model_width //2 
y_player = screen_height - 450

hitbox_vertical_shift = 15

player_model_x = x_player
player_model_y = y_player 

player_hitbox_x = x_player + (player_model_width - player_hitbox_width) // 2 
player_hitbox_y = y_player + (player_hitbox_height - player_hitbox_height) //2 + hitbox_vertical_shift

player_rectangle = pygame.Rect(player_hitbox_x, player_hitbox_y, player_hitbox_width, player_hitbox_height)

player_speed = 3

def update_player(): 
    global x_player, y_player, player_rectangle 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y_player -= player_speed 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y_player += player_speed 

    x_player = max(0, min(x_player, screen_width - player_model_width))
    y_player = max(0, min(y_player, screen_height - player_model_height))

    player_hitbox_x  = x_player + (player_model_width - player_hitbox_width) //2 
    player_hitbox_y = y_player +(player_model_height - player_hitbox_height) //2 + hitbox_vertical_shift
    player_rectangle.x = player_hitbox_x
    player_rectangle.y = player_hitbox_y

def draw_hitbox():
    pygame.draw.rect(screen, (255, 0, 0), player_rectangle, 2)

#Game Loop
running = True
while running: 
    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    update_player()

    screen.fill(WHITE)

    screen.blit(player_model, (x_player, y_player))

    draw_hitbox()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()