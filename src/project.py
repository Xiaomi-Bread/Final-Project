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
tank_begin_image = pygame.image.load("Tank-begin.png").convert_alpha()
tank_begin_image = pygame.transform.scale(tank_begin_image, (570, 264))

game_begin_button = pygame.image.load("start-button.png").convert_alpha()
game_begin_button = pygame.transform.scale(game_begin_button, (200, 50))

heart_image = pygame.image.load("heart.png").convert_alpha()
heart_size = (150, 150)
heart_image = pygame.transform.scale(heart_image, heart_size)
heart_damaged_image = pygame.image.load("heart-damaged.png").convert_alpha()
heart_damaged_image = pygame.transform.scale(heart_damaged_image, heart_size)

enemy_shooter_image = pygame.image.load("WW1Shooter.png").convert_alpha()
enemy_shooter_image = pygame.transform.scale(enemy_shooter_image, (120, 55))

player_model = pygame.image.load("WW1Tank.png").convert_alpha()
player_model = pygame.transform.scale(player_model, (player_model_width, player_model_height))

x_player = screen_width // 3 - player_model_width //3
y_player = screen_height - 425

hitbox_vertical_shift = 15

player_model_x = x_player
player_model_y = y_player 

player_hitbox_x = x_player + (player_model_width - player_hitbox_width) // 2 
player_hitbox_y = y_player + (player_hitbox_height - player_hitbox_height) //3 + hitbox_vertical_shift

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

    screen.blit(player_model, (x_player, y_player))

screen.blit(player_model, player_rectangle.topleft)

def draw_hitbox():
    pygame.draw.rect(screen, (255, 0, 0), player_rectangle, 2)

player_max_health = 4 
player_health = player_max_health

def draw_health(): 
    heart_offset = 20 
    for i in range(player_max_health):
        if i < player_health: 
            screen.blit(heart_image, (heart_offset + i * 87, 20))
        else: 
            screen.blit(heart_damaged_image, (heart_offset + i * 87, 20))

def display_start_screen():
    screen.blit(tank_begin_image, (screen_width//2 - tank_begin_image.get_width()//2, screen_height//2 -300))

    start_font = pygame.font.SysFont(None, 70)
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
                    pygame.mixer.Sound.play(tank_moving_noise, loops=- 1)
    
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

    draw_health()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()