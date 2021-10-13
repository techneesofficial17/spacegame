import pygame
import os

from pygame import draw
from pygame import mixer
pygame.font.init()
pygame.mixer.init()


pygame.display.set_caption("Nees Game")  # it will change the title of the pygame window 
icon = pygame.image.load(os.path.join('Assets', 'logo.jpg'))
pygame.display.set_icon(icon)

mixer.music.load('Assets/background.wav')
mixer.music.set_volume(0.05)
mixer.music.play(-1)

WIDTH , HEIGHT = 900 , 500
WIN = pygame.display.set_mode((WIDTH , HEIGHT))

VEL = 10
MAX_BULLETS = 5
BULLET_VEL = 10

REDHEALTH = 50
YELLOWHEALTH = 50


BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

BULLET_FIRE_SOUND.set_volume(0.1)
BULLET_HIT_SOUND.set_volume(0.1)

WHITE = (255, 255, 255) 
BROWN = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (200, 0 ,0)
YELLOW = (255, 255, 0)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

FPS = 60 
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 50

BORDER = pygame.Rect(WIDTH // 2, 0 , 10, HEIGHT)


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('sans-serif', 150)
PLEASEWAIT = pygame.font.SysFont('monospace', 50)


# drawing the yellow spaceship in the game
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# drawing the red spaceship in the game
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'galaxy.gif')) , (WIDTH, HEIGHT))

def createcanvas(red , yellow, red_bullets , yellow_bullets, red_health , yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK , BORDER)

    red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health), 1, YELLOW)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 20, 10))
    WIN.blit(yellow_health_text, (20, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x , red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED , bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW , bullet)

    # update at the last 
    pygame.display.update()


def yellow_movement_control(keys_pressed , yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL  > 0:
        yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 12:
        yellow.y += VEL

def red_movement_control(keys_pressed , red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width - 8 < WIDTH:
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL  > 0 :
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 12:
        red.y += VEL


def handle_bullets(yellow_bullets , red_bullets, yellow , red):
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

def winner(text):
    draw_text = WINNER_FONT.render(text, 1 , WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2  , HEIGHT / 2 - draw_text.get_height() / 2))
    pleasewait = PLEASEWAIT.render("Please wait a moment !", 0, WHITE)
    WIN.blit(pleasewait, (WIDTH / 2 - pleasewait.get_width() / 2 + 20 , HEIGHT / 2 - pleasewait.get_height() / 2 + 100))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect(700, 200 , SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(150, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_health = REDHEALTH
    yellow_health = YELLOWHEALTH

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            yellow.x + yellow.width - 20, yellow.y + yellow.height//2 - 2, 20, 5)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 20, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if yellow_health <= 0:
            winner_text = "RED WON"
        
        if red_health <= 0:
            winner_text = "YELLOW WON"

        keys_pressed = pygame.key.get_pressed()
        yellow_movement_control(keys_pressed, yellow)
        red_movement_control(keys_pressed, red)
        handle_bullets(yellow_bullets , red_bullets, yellow , red)
        createcanvas(red, yellow, red_bullets , yellow_bullets, red_health, yellow_health)

        
        if winner_text != "":
            winner(winner_text)
            break
        
    main()

if __name__ == "__main__":
    main()