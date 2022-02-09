import pygame
import random
import pickle

from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# Music / Sound

music = mixer.music.load('Bandit.mp3')
mixer.music.play(-1)

bullet_sound = mixer.Sound('laser.wav')
hit_sound = mixer.Sound('explosion.wav')

class Player(object):

    def __init__(self, x, y):
        self.image = pygame.image.load('spaceship.png')
        self.x = int(x)
        self.y = int(y)
        self.vel = 8

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self):
        # Key binding
        keys = pygame.key.get_pressed()
##        if keys[pygame.K_UP]:
##            self.y -= self.vel
##        if keys[pygame.K_DOWN]:
##            self.y += self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        # Set boundaries
        if self.x >= WIDTH - 64:
            self.x = WIDTH - 64
        if self.x <= 0:
            self.x = 0
        if self.y >= HEIGHT - 64:
            self.y = HEIGHT - 64
        if self.y <= 0:
            self.y = 0


class Enemy(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('enemy.png')
        self.vel = 3

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.vel


class Bullet(object):
    def __init__(self, x1, x2, y, radius, color):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x1, self.y), self.radius)
        pygame.draw.circle(surface, self.color, (self.x2, self.y), self.radius)


def collide():
    global score

    for enemy in enemies:
        for bullet in bullets:
            if enemy.x <= bullet.x1 <= enemy.x + 64 and (enemy.y <= bullet.y <= enemy.y + 64):
                enemies.pop(enemies.index(enemy))
                bullets.pop(bullets.index(bullet))
                # hit_sound.play()
                score += 5

            elif enemy.x <= bullet.x2 <= enemy.x + 64 and (enemy.y <= bullet.y <= enemy.y + 64):
                enemies.pop(enemies.index(enemy))
                bullets.pop(bullets.index(bullet))
                # hit_sound.play()
                score += 5


def centralise_text(surface, text, font, size, color, bold=0, italic=0):
    font = pygame.font.SysFont(font, size, bold)
    label = font.render(text, 1, color)
    x = int(WIDTH/2 - label.get_width()/2)
    y = int(HEIGHT/2 - label.get_height()/2)
    surface.blit(label, (x, y))


def is_game_over():
    game_over = False
    for enemy in enemies:
        if enemy.y +32 >= spaceship.y:
            if score >= high_score:
                with open(r"C:\Users\Akuma\Desktop\Codes\Dark Space\score.dat", "wb") as file:
                    pickle.dump(score, file)
            game_over = True
            
            break

    return game_over


WIDTH = 650
HEIGHT = 600
spaceship = Player(WIDTH / 2 - 32, 500)
bullets = []
enemies = []
score = 0
is_valid = False

 # Get the high score.
try:
    with open(r"C:\Users\Akuma\Desktop\Codes\Dark Space\score.dat", "rb") as file:
        high_score = pickle.load(file)
        is_valid = True
except FileNotFoundError:
    with open(r"C:\Users\Akuma\Desktop\Codes\Dark Space\score.dat", "wb") as file:
        pickle.dump(score, file)
finally:
    if not is_valid:
        with open(r"C:\Users\Akuma\Desktop\Codes\Dark Space\score.dat", "rb") as file:
            high_score = pickle.load(file)        


def count_score(surface, high_score):
    # Display current score.
    font = pygame.font.SysFont('monospace', 18, bold=1)
    score_label = font.render('Score: {}'.format(score), 1, (255, 255, 255))
    surface.blit(score_label, (10, 10))
    if score >= high_score:
        high_score = score
    highScore_label = font.render("High Score: {}".format(high_score), 1, (255, 255, 255))
    surface.blit(highScore_label, (10, 30))

    # if score >= high_score:
    #     with open(r"C:\Users\Akuma\Desktop\Codes\Dark Space\score.dat", "wb") as file:
    #         pickle.dump(str(score), file)


def redraw_window(surface, bg):

    surface.blit(bg, (0, 0))

    spaceship.draw(surface)
    count_score(surface, high_score)
    for bullet in bullets:
        bullet.draw(surface)
    for enemy in enemies:
        enemy.draw(surface)
        enemy.move()
    pygame.display.update()
    

def main(bg, win):

    shoot = 1
    # Main Game loop
    run = True
    while run:

        if shoot > 0:
            shoot += 1
        if shoot > 15:
            shoot = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for bullet in bullets:
            if 0 < bullet.y < HEIGHT:
                bullet.y -= bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        spaceship.move()
        if keys[pygame.K_SPACE] and shoot == 0:
            bullet_sound.play()
            if len(bullets) < 5:
                bullets.append(Bullet(round(spaceship.x + 14), round(spaceship.x + 50),
                                      int(spaceship.y), 4, (255, 0, 0)))
            shoot = 1

        # Game difficulty control
        if len(enemies) < 1:
            enemies.append(Enemy(random.randint(0, WIDTH - 64), random.randint(-100, -20)))
        if score >= 20 and len(enemies) < 2:
            enemies.append(Enemy(random.randint(0, WIDTH - 64), random.randint(-100, -20)))
        if score >= 150 and len(enemies) < 3:
            enemies.append(Enemy(random.randint(0, WIDTH - 64), random.randint(-100, -20)))
        if score >= 350 and len(enemies) < 4:
            enemies.append(Enemy(random.randint(0, WIDTH - 64), random.randint(-100, -20)))
        if score >= 500 and len(enemies) < 5:
            enemies.append(Enemy(random.randint(0, WIDTH - 64), random.randint(-100, -20)))
        if score >= 600 and len(enemies) < 6:
            enemies.append(Enemy(random.randint(0, WIDTH - 64), random.randint(-100, -20)))

        collide()

        redraw_window(win, bg)
        game_state = is_game_over()
        if game_state:

            centralise_text(win, 'GAME OVER', 'monospace', 30, (255, 0, 0), bold=1)
            pygame.display.update()
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
            run = False

        pygame.display.update()


def main_menu():
    # setup game window
    icon = pygame.image.load('ufo.png')

    pygame.display.set_caption('Dark Space')
    pygame.display.set_icon(icon)
    bg = pygame.image.load('background.png')
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    while running:
        win.blit(bg, (0, 0))
        centralise_text(win, 'Press Any Key To Play', 'monospace', 30, (255, 255, 255), bold=1)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main(bg, win)
                running = False
            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()


main_menu()
