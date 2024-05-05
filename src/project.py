import pygame
import sys

pygame.init()
pygame.mixer.init()

tank_moving_noise = pygame.mixer.Sound("tank-moving.mp3")
tank_moving_noise.set_volume(0.1)

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
game_begin_button = pygame.image.load("start-button.png").convert_alpha()
game_begin_button = pygame.transform.scale(game_begin_button, (200, 50))

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

def display_start_screen():
    screen.blit(game_begin_button, (screen_width//2 - game_begin_button.get_width()//2, screen_height//2 -300))

    start_font = pygame.font.SysFont(None, 72)
    start_text = start_font.render("Click to Start the Offensive", True, WHITE)
    screen.blit(start_text, (screen_width//2 - start_text.get_width()//2, screen_height//2 - start_text.get_height()//2 ))

    screen.blit(game_begin_button, (screen_width//2 - game_begin_button.get_width()//3 , screen_height//2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_position = pygame.mouse.get_pos()
                if (screen_width//2 -game_begin_button.get_width()//2 < mouse_position[0] < 
                    screen_width//2 + game_begin_button.get_width()//2) and (screen_height//2 +50 < mouse_position[1] < screen_height//2 + 50 + game_begin_button.get_height()):
                    waiting = False
    
display_start_screen()

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