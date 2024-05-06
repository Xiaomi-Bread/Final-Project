import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

tank_moving_noise = pygame.mixer.Sound("tank-moving.mp3")
tank_moving_noise.set_volume(0.1)

enemy_shooting_sound = pygame.mixer.Sound("enemy-fire.mp3")
enemy_shooting_sound.set_volume(0.09)

artillery_shooting_sound = pygame.mixer.Sound("artillery-fire.mp3")
artillery_shooting_sound.set_volume(0.2)

tank_damage_sound = pygame.mixer.Sound("tank-damage.mp3")
tank_damage_sound.set_volume(0.3) 

bonus_collect_sound = pygame.mixer.Sound("Collect-noise.mp3")
bonus_collect_sound.set_volume(1.0) #Adjust volume if needed

#Main Resolution
screen_width = 1550
screen_height = 790 
screen = pygame.display.set_mode((screen_width, screen_height))

background_images = {
    "Nomansland": pygame.image.load("Nomansland.png").convert(),
    "Snowland": pygame.image.load("Snowland.png").convert(),
    "Grassland": pygame.image.load("Grassland.png").convert(),
    "Desert": pygame.image.load("Desertland.png").convert()
}
def choose_background_image():
    return random.choice(list(background_images.values()))

background_image = choose_background_image()


WHITE = (255, 255, 255)
RED = (255, 0, 0)
COOPERGOLD = (174, 137, 61)
BLACK = (0, 0, 0)

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

artillery_image = pygame.image.load("artillery.png").convert_alpha()
artillery_image = pygame.transform.scale(artillery_image, (250,108))

player_model = pygame.image.load("WW1Tank.png").convert_alpha()
player_model = pygame.transform.scale(player_model, (player_model_width, player_model_height))

bonus_object_image = pygame.image.load("trenches.png").convert_alpha()
bonus_object_size = (200, 790)
bonus_object_image = pygame.transform.scale(bonus_object_image, bonus_object_size)

tank_exit_image = pygame.image.load("Tank-exit.png").convert_alpha()
tank_exit_image = pygame.transform.scale(tank_exit_image, (465, 392))

x_player = screen_width // 3 - player_model_width //3
y_player = screen_height - 425

hitbox_vertical_shift = 15

player_model_x = x_player
player_model_y = y_player 

player_hitbox_x = x_player + (player_model_width - player_hitbox_width) // 2 
player_hitbox_y = y_player + (player_hitbox_height - player_hitbox_height) //3 + hitbox_vertical_shift

player_rectangle = pygame.Rect(player_hitbox_x, player_hitbox_y, player_hitbox_width, player_hitbox_height)

player_speed = 3

def play_tank_damage_sound(): 
    tank_damage_sound.play()

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
hit_projectiles = set()
hit_spike_objects = set()

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

class EnemyShooter: 
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        self.last_shot_time = 0 
        self.bullets = []

    def update(self, player_rectangle):
        self.rect.x -= self.speed 
        if self.rect.right <= 0: 
            self.rect.x = screen_width + random.randint(100, 100)
            self.rect.y = random.randint(0, screen_height -30) 

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= random.randint(2000, 4000): 
            self.fire(player_rectangle)
            self.last_shot_time = current_time

    def fire(self, player_rect): 
        bullet_x = self.rect.right
        bullet_y = self.rect.centery 

        bullet = Bullet(self.rect.x, self. rect.centery, 8)
        self.bullets.append(bullet)

        enemy_shooting_sound.play()

    def draw(self):
        screen.blit(enemy_shooter_image, self.rect.topleft)

class Bullet: 
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = speed 

    def update(self): 
        self.rect.x -= self.speed

class BonusObject: 
    def __init__(self, x, speed):
        self.rect = pygame.Rect(x,  0, 100, screen_height)
        self.speed = speed
        self.active = True
        self.hit_count = 0 

    def update(self): 
        self.rect.x -= self.speed
    
        if self.rect.right <= 0: 
            self.rect.x = screen_width + random.randint(23, 23)
            self.speed = random.randint(4, 4)
            self.hit_count = 0

    def draw(self):
        screen.blit(bonus_object_image, self.rect) 

class Spikes: 
    def __init__(self, y, speed):
        self.image = pygame.image.load("spike.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = screen_width + random.randint(100, 100)
        self.rect.y = y
        self.speed = speed
    
    def update(self):
        self.rect.x -= self.speed

        if self.rect.right <= 0: 
            self.rect.x = screen_width + random.randint(50, 120)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
        
        self.speed = random.randint(2, 2)

    def draw(self): 
        screen.blit(self.image, self.rect)

class Artillery:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        self.last_shot_time = 0
        self.shells = []  # List to hold shells

    def update(self, player_rect):
        # Move Artillery from right to left
        self.rect.x -= self.speed

        # Check if Artillery needs to respawn
        if self.rect.right <= 0:
            self.rect.x = screen_width + random.randint(500, 1000)
            self.rect.y = random.randint(0, screen_height - 30)

        # Check if Artillery needs to shoot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= random.randint(5000, 7000):
            self.shoot(player_rect)
            self.last_shot_time = current_time

    def shoot(self, player_rect):
        # Calculate the initial position of the shells relative to the shooter's position
        shell_x = self.rect.right
        shell_y = self.rect.centery

        shell = Shells(self.rect.x, self.rect.centery, 15)
        self.shells.append(shell)

        # Play enemy shooting sound
        artillery_shooting_sound.play()

    def draw(self):
        screen.blit(artillery_image, self.rect.topleft)

class Shells:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 10)
        self.speed = speed

    def update(self):
        # Move shells from right to left
        self.rect.x -= self.speed

num_spikes = 5
num_enemy_shooters = 5
num_artillerys = 1
num_bonus_objects = 1 

spikes_speed = 2
enemy_shooter_speeds = [2, 2, 2, 2]
artillery_speeds = [2]
bonus_object_speed =4

spikes = [Spikes (random.randint(0, screen_height -30), spikes_speed) for _ in range(num_spikes)]

enemy_shooters = [EnemyShooter(screen_width + random.randint(100,200), random.randint(0, screen_height -30), 
                               random.choice(enemy_shooter_speeds)) for _ in range(num_enemy_shooters)]

artillerys = [Artillery(screen_width + random.randint(100,200), random.randint(0, screen_height -30),
                         random.choice(artillery_speeds)) for _ in range(num_artillerys)]

bonus_objects = [BonusObject(screen_width + random.randint(100, 200), bonus_object_speed) 
                 for _ in range(num_bonus_objects)]

font = pygame.font.SysFont(None, 36)

score = 0 
last_bonus_time = 0
bonus_time_limit = 1000

score_front = pygame.font.SysFont(None, 50)

game_over = False 

#Game Loop
running = True
while running: 
    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    if game_over: 

        screen.fill((0, 0, 0))

        screen.blit(tank_exit_image, (screen_width//2 - tank_exit_image.get_width()//2, screen_height//2 - 300))

        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("All Crew Knocked Out", True, RED)
        screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2 
                                     - game_over_text.get_height()//2))
        
        final_score_font = pygame.font.SysFont(None, 36)
        final_score_text = final_score_font.render("Career Stats: " + str(score), True, WHITE)
        screen.blit(final_score_text, (screen_width//2 - final_score_text.get_width()//2, screen_height//2 + 120))
        
        final_quote_font = pygame.font.SysFont(None, 30)
        final_quote_text = final_quote_font.render("we did what we did best. Our Job.", True, COOPERGOLD)
        screen.blit(final_quote_text, (screen_width//2 - final_quote_text.get_width()//2, screen_height//2 + 180))

        exit_button_rect = pygame.Rect(screen_width//2 - 100, screen_height//2 +50, 200, 50)
        pygame.draw.rect(screen, RED, exit_button_rect)
        exit_button_font  = pygame.font.SysFont(None, 36)
        exit_button_text = exit_button_font.render("Discharge", True, WHITE)
        screen.blit(exit_button_text, (screen_width//2 - exit_button_text.get_width()/2, screen_height//2 +65))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos): 
                    running =  False 
                    break
        pygame.display.flip()
        continue

    update_player()

    for spike in spikes: 
        spike.update()
        if player_rectangle.colliderect(spike.rect):
            if spike not in hit_spike_objects: 
                player_health -= 1 
                hit_spike_objects.add(spike)
            tank_damage_sound.play()
            if player_health <= 0: 
                game_over = True
                break

    for enemyshooter in enemy_shooters: 
        enemyshooter.update(player_rectangle)
        for bullet in enemyshooter.bullets: 
            bullet.update()
            if player_rectangle.colliderect(bullet.rect) and bullet not in hit_projectiles: 
                player_health -= 1 
                hit_projectiles.add(bullet)
                tank_damage_sound.play()
                if player_health <= 0: 
                    game_over = True
                    break
    
    for artillery in artillerys:
        artillery.update(player_rectangle)
        for shell in artillery.shells:
            shell.update()
            if player_rectangle.colliderect(shell.rect) and shell not in hit_projectiles: #Check if the shells has no already hit the player
                player_health -= 2
                hit_projectiles.add(shell) # Add the shell to the set to track hits
                tank_damage_sound.play() # Play tank damage sound
                if player_health <= 0:
                    game_over = True
                    
                    break

    for bonus_object in bonus_objects: 
        if player_rectangle.colliderect(bonus_object.rect) and bonus_object.hit_count == 0:
            # Player gets a point
            bonus_object.hit_count += 1
            bonus_collect_sound.play()
            score += 1  

    screen.blit(background_image, (0, 0))

    for bonus_object in bonus_objects:
        bonus_object.update()
        screen.blit(bonus_object_image, bonus_object.rect)

    score_text = score_front.render("Trenches: " + str(score), True, BLACK)
    screen.blit(score_text, (550, 20))

    for spike in spikes:
        spike.update()
        spike.draw()

    for enemyshooter in enemy_shooters: 
        enemyshooter.update(player_rectangle)
        enemyshooter.draw()
        for bullet in enemyshooter.bullets: 
            bullet.update()
            pygame.draw.rect(screen, RED, bullet.rect)
    
    for artillery in artillerys:
        artillery.update(player_rectangle)
        artillery.draw()
        for shell in artillery.shells:
            shell.update()
            pygame.draw.rect(screen, COOPERGOLD, shell.rect)
  
    
    screen.blit(player_model, (x_player, y_player))

    draw_hitbox()

    draw_health()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()