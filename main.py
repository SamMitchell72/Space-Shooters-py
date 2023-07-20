import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE FIRE")

yellow_total_score = 0
red_total_score = 0

WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255,0 ,0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

HEALTH_FONT = pygame.font.SysFont('bold_arial', 60)
WINNER_FONT = pygame.font.SysFont('arial', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))

FPS = 60
VEL = 8
BULLET_VEL = 11
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

EXPLOSION_WIDTH, EXPLOSION_HEIGHT = 128, 94

BASE_HEALTH_WIDTH, BASE_HEALTH_HEIGHT = 150, 30
YELLOW_HEALTH_X, YELLOW_HEALTH_Y = 10, 10
RED_HEALTH_X, RED_HEALTH_Y = WIDTH - 160, 10

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

EXPLOSION_IMAGE = pygame.image.load(os.path.join('Assets', 'explosion.PNG'))
EXPLOSION = pygame.transform.scale(EXPLOSION_IMAGE, (EXPLOSION_WIDTH,EXPLOSION_HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)

SPACE =  pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, EXPLOSION, red_health_width, yellow_health_width, red_health_x, yellow_total_score, red_total_score):
    WIN.blit(SPACE, (0, 0))
    
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    #red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
    #yellow_health_text = HEALTH_FONT.render("Health: "  + str(yellow_health),1, YELLOW)
    #WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    #WIN.blit(yellow_health_text, (10, 10))

    red_score_text = HEALTH_FONT.render("Score:" + str(red_total_score), 1, RED)
    WIN.blit(red_score_text, (WIDTH - red_score_text.get_width() - 10, 450))
    yellow_score_text = HEALTH_FONT.render("Score:" + str(yellow_total_score), 1, YELLOW)
    WIN.blit(yellow_score_text, (10, 450))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    
    YELLOW_HEALTH_BAR_A = pygame.Rect(YELLOW_HEALTH_X, YELLOW_HEALTH_Y, yellow_health_width, BASE_HEALTH_HEIGHT)
    YELLOW_HEALTH_BAR_B = pygame.Rect(YELLOW_HEALTH_X, YELLOW_HEALTH_Y, BASE_HEALTH_WIDTH, BASE_HEALTH_HEIGHT)
    pygame.draw.rect(WIN, RED, YELLOW_HEALTH_BAR_B)
    pygame.draw.rect(WIN, GREEN, YELLOW_HEALTH_BAR_A)
    
    RED_HEALTH_BAR_A = pygame.Rect(red_health_x, RED_HEALTH_Y, red_health_width, BASE_HEALTH_HEIGHT)
    RED_HEALTH_BAR_B = pygame.Rect(RED_HEALTH_X, RED_HEALTH_Y, BASE_HEALTH_WIDTH, BASE_HEALTH_HEIGHT)
    pygame.draw.rect(WIN, RED, RED_HEALTH_BAR_B)
    pygame.draw.rect(WIN, GREEN, RED_HEALTH_BAR_A)

    if yellow_health <= 0:
        WIN.blit(EXPLOSION, (yellow.x - EXPLOSION_WIDTH/4, yellow.y - EXPLOSION_HEIGHT/4))
    
    if red_health <= 0:
        WIN.blit(EXPLOSION, (red.x - EXPLOSION_WIDTH/4, red.y - EXPLOSION_HEIGHT/4))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        
def draw_winner(winner_text):
    if winner_text == "Yellow Wins!":
        draw_text = WINNER_FONT.render(winner_text, 1, YELLOW)
    if winner_text ==  "Red Wins!":
        draw_text = WINNER_FONT.render(winner_text, 1, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main(yellow_total_score, red_total_score):
    red = pygame.Rect(random.randint(500, 850), random.randint(50, 450), SPACESHIP_HEIGHT, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(random.randint(50,400), random.randint(50, 450), SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    yellow_bullets =[]
    red_bullets = []

    red_health_x = WIDTH - 160
    red_health = 10
    yellow_health = 10

    red_health_width = 150
    yellow_health_width = 150

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                red_health_width -= 15
                red_health_x += 15
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                yellow_health_width -= 15
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            red_health == 0
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, EXPLOSION, red_health_width, yellow_health_width, red_health_x, yellow_total_score, red_total_score)
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            yellow_health == 0
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, EXPLOSION, red_health_width, yellow_health_width, red_health_x, yellow_total_score, red_total_score)
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed,red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, EXPLOSION, red_health_width, yellow_health_width, red_health_x, yellow_total_score, red_total_score)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
    if winner_text == "Red Wins!":
        red_total_score += 1
    if winner_text == "Yellow Wins!":
        yellow_total_score += 1
    main(yellow_total_score, red_total_score)
    

if __name__ == "__main__":
    main(yellow_total_score, red_total_score)
