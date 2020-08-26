import pygame
import random
import math

from pygame import mixer

pygame.font.init()

#Crate screen
w_height = 600
w_width = 800
screen = pygame.display.set_mode((w_width, w_height))

#Set Icon
icon = pygame.image.load("icon.jpeg")
pygame.display.set_icon(icon)

#Set Caption
pygame.display.set_caption("Shoot Bitch")

#Set background
background = pygame.image.load("back.jpg")

# Background music
# mixer.music.load(<music file>)
# mixer.music.play(-1)

# Create player
player_Img = pygame.image.load("fighter.png")
playerX = 370
playerY = 480
playerX_change = 0

#Create enemy
enemy_Img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_Img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

#Create bullet
bullet_Img = pygame.image.load("bullet.png")
bulletX = 0 # not needed as x-coord isn’t gonna change
bulletY = 480 # bulletY is the same as that of playerY
bulletX_change = 0 # always
bulletY_change = 10 # any integer
bullet_state = "ready"

# enemy_Img = pygame.image.load("enemy.png")
# enemyX = random.randint(0,736)
# enemyY = random.randint(50, 150)
# enemyX_change = 3
# enemyY_change = 0

score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#GAme Over
game_over_font=pygame.font.Font('freesansbold.ttf',64)

#Player function
def player(x,y):
    # Drawing player’s image onto screen, blit() requires 2 parameters
    screen.blit(player_Img, (x, y))

# Enemy function
def enemy(x, y):
    screen.blit(enemy_Img[i], (x, y))

# Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"

    screen.blit(bullet_Img, (x + 36, y - 16))

# Detecting Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    # collision detected
    if distance < 27:
        return True
    else:
        return False

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0,0,0))
    screen.blit(score, (x, y))

#Game over
def game_over_text():
    game_over_text = game_over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(game_over_text, (200, 250))

#GAME LOOP
running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    #Check for boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movememnt
    for i in range(num_of_enemies):

        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
           enemyX_change[i] = 3
           enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
           enemyX_change[i] = -3
           enemyY[i] += enemyY_change[i]

            # COllision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosion_sound = mixer.Sound("explosion.mp3")
            # explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            # respawn the enemy
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)

    #update the screen
    pygame.display.update()


pygame.quit()
