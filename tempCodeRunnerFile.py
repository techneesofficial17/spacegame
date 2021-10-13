import pygame
import os

WIDTH , HEIGHT = 900 , 500
WIN = pygame.display.set_mode((WIDTH , HEIGHT))

VEL = 6
MAX_BULLETS = 3
BULLET_VEL = 20

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

# drawing the yellow spaceship in the game
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# drawing the red spaceship in the game
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


pygame.display.set_caption("Nees Game")  # it will change the title of the pygame window 


def createcanvas(red , yellow, red_bullets , yellow_bullets):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BROWN , BORDER)

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


def main():
    red = pygame.Rect(700, 200 , SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(150, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        yellow_movement_control(keys_pressed, yellow)
        red_movement_control(keys_pressed, red)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

            if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(
                    red.x, red.y + red.height//2 - 2, 10, 5)
                red_bullets.append(bullet)

        

        handle_bullets(yellow_bullets , red_bullets, yellow , red)

        createcanvas(red, yellow, red_bullets , yellow_bullets)
    
    pygame.quit()


if __name__ == "__main__":
    main()