import pygame
import math
import random
from pygame import mixer

# initialize the game

pygame.init()

# creating display

screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
# background
bg = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# show score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
over_font = pygame.font.Font('freesansbold.ttf', 64)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render('SCORE : ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game is Over!", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


# player
playerImg = pygame.image.load('spaceship.png')
playerX = 365
playerY = 520
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('space-invaders.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(10, 100))
    enemyX_change.append(3)
    enemyY_change.append(30)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# bullet in ready state
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 520
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB stands for red , green, blue
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if a keystroke is pressed whether it is right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change += -5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking boundary limit.
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement

    for i in range(num_of_enemies):
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosive_sound = mixer.Sound('explosion.wav')
            explosive_sound.play()
            bulletY = 520
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(10, 100)

        enemy(enemyX[i], enemyY[i], i)

    # bullet move
    if bulletY <= 0:
        bulletY = 520
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
