import pygame
import os
pygame.font.init()
pygame.mixer.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255,255,255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', '1-01. Opening.mp3'))
YBULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', '001 - Kanto - Bulbasaur.mp3'))
RBULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', '007 - Kanto - Squirtle.mp3'))
YBULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bushhitwav-14661.mp3'))
RBULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'water-splash-46402.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BACKGROUND_MUSIC.play()

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

POKE_WIDTH, POKE_HEIGHT = 125, 115 


GREEN_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2


GREEN_POKE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'bulbasaur (1).png'))
GREEN_POKE = pygame.transform.rotate(pygame.transform.scale(
    GREEN_POKE_IMAGE, (POKE_WIDTH, POKE_HEIGHT)), 0)



BLUE_POKE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'squirtle.png'))
BLUE_POKE = pygame.transform.rotate(pygame.transform.scale(
    BLUE_POKE_IMAGE, (POKE_WIDTH, POKE_HEIGHT)), 0)

GRASS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'unnamed.png')), (WIDTH, HEIGHT))


def draw_window(blue, green, blue_bullets, green_bullets, blue_health, green_health):
    WIN.blit(GRASS, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width() -10, 10))
    WIN.blit(green_health_text, (10, 10))

    WIN.blit(GREEN_POKE, (green.x, green.y))
    WIN.blit(BLUE_POKE, (blue.x, blue.y))

    

    for bullets in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullets)
    for bullets in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullets)

    pygame.display.update()
    


def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VEL > 0: # LEFT
        green.x -= VEL
    if keys_pressed[pygame.K_d] and green.x + VEL + green.width < BORDER.x: # RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_w] and green.y - VEL > 0: # UP
        green.y -= VEL
    if keys_pressed[pygame.K_s] and green.y + VEL + green.height < HEIGHT - 15: # DOWN
        green.y += VEL

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL > BORDER.x + BORDER.width: # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blue.x + VEL + blue.width < WIDTH: # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y - VEL > 0: # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + VEL + blue.height < HEIGHT - 15: # DOWN
        blue.y += VEL

def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    blue = pygame.Rect(700, 300, POKE_WIDTH, POKE_HEIGHT)
    green = pygame.Rect(100, 300, POKE_WIDTH, POKE_HEIGHT)

    blue_bullets = []
    green_bullets = []

    blue_health = 10
    green_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = True
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        green.x + green.width, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    YBULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    RBULLET_FIRE_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                RBULLET_HIT_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                YBULLET_HIT_SOUND.play()

        winner_text = ""
        if blue_health <= 0:
            winner_text = "Squirtle Wins!"

        if green_health <= 0:
            winner_text = "Bulbasaur Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        blue_handle_movement(keys_pressed, blue)

        handle_bullets(green_bullets, blue_bullets, green, blue)

        draw_window(blue, green, blue_bullets, green_bullets, blue_health, green_health)

    main()

if __name__ == "__main__":
    main()
