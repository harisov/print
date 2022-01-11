import os
import pygame
from pygame.locals import *
import sys
import random


pygame.init()
size = width, height = 600, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Дудл джамп")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        self.green = load_image("green.png")
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.blue = load_image("blue.png")
        self.red = load_image("red.png")
        self.red_1 = load_image("red_1.png")
        self.playerRight = load_image("right.png")
        self.playerRight_1 = load_image("right_1.png")
        self.playerLeft = load_image("left.png")
        self.playerLeft_1 = load_image("left_1.png")
        self.spring = load_image("spring.png")
        self.spring_1 = load_image("spring_1.png")
        self.direction = 0
        self.gamer_x = 300
        self.gamer_y = 300
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cam = 0
        self.jump = 0
        self.gravity = 0
        self.move_moment = 0

    def updatePlayer(self):
        if not self.jump:
            self.gamer_y += self.gravity
            self.gravity += 1
        elif self.jump:
            self.gamer_y -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.move_moment < 10:
                self.move_moment += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.move_moment > -10:
                self.move_moment -= 1
            self.direction = 1
        else:
            if self.move_moment > 0:
                self.move_moment -= 1
            elif self.move_moment < 0:
                self.move_moment += 1
        if self.gamer_x > 850:
            self.gamer_x = -50
        elif self.gamer_x < -50:
            self.gamer_x = 850
        self.gamer_x += self.move_moment
        if self.gamer_y - self.cam <= 200:
            self.cam -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.gamer_x, self.gamer_y - self.cam))
            else:
                self.screen.blit(self.playerRight, (self.gamer_x, self.gamer_y - self.cam))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.gamer_x, self.gamer_y - self.cam))
            else:
                self.screen.blit(self.playerLeft, (self.gamer_x, self.gamer_y - self.cam))

    def update(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.gamer_x, self.gamer_y, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.gamer_y < (p[1] - self.cam):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for i in self.platforms:
            m = self.platforms[1][1] - self.cam
            if m > 800:
                platform = random.randint(0, 1000)
                if platform < 600:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                cords = self.platforms[-1]
                m = random.randint(0, 1000)
                if m > 900 and platform == 0:
                    self.springs.append([cords[0], cords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if i[2] == 0:
                self.screen.blit(self.green, (i[0], i[1] - self.cam))
            elif i[2] == 1:
                self.screen.blit(self.blue, (i[0], i[1] - self.cam))
            elif i[2] == 2:
                if not i[3]:
                    self.screen.blit(self.red, (i[0], i[1] - self.cam))
                else:
                    self.screen.blit(self.red_1, (i[0], i[1] - self.cam))

        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cam))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cam))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(
                    pygame.Rect(self.gamer_x, self.gamer_y, self.playerRight.get_width(),
                                self.playerRight.get_height())):
                self.jump = 50
                self.cam -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, 800))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (600, x * 12))

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(40)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.gamer_y - self.cam > 500:
                self.cam = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.gamer_x = 400
                self.gamer_y = 400
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.update()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()

DoodleJump().run()