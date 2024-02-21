import pygame
import sys
import random
from math import *

pygame.init()
width = 700
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("CopyAssignment - Balloon Shooter Game")
clock = pygame.time.Clock()


white = (230, 230, 230)
darkBlue = (64, 178, 239)


font = pygame.font.SysFont("Snap ITC", 35)

class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(100, width - self.a - 100)
        self.y = height - 100
        self.angle = 90
        self.speed = -speed
        self.proPool= [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([(231, 76, 60), (35, 155, 86), (155, 89, 182), (243, 156, 18), (244, 208, 63), (46, 134, 193)])
    
    def move(self):
        direct = random.choice(self.proPool)
        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10
        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))
        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/5:
                self.x -= self.speed*cos(radians(self.angle)) 
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a/2, self.y + self.b), (self.x + self.a/2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a/2 - 5, self.y + self.b - 3, 10, 10))

    def burst(self):
        global score
        pos = pygame.mouse.get_pos()
        if is_on_balloon(self.x, self.y, self.a, self.b, pos):
            score += 1
            self.reset()

    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(100, width - self.a - 100)
        self.y = height - 100 
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([(231, 76, 60), (35, 155, 86), (155, 89, 182), (243, 156, 18), (244, 208, 63), (46, 134, 193)])

def is_on_balloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False

def draw_start_button():
    start_button = font.render("Start Game", True, white)
    start_button_rect = start_button.get_rect(center=(width // 2, height // 2))
    pygame.draw.rect(display, darkBlue, start_button_rect)
    display.blit(start_button, start_button_rect)
    return start_button_rect

def game():
    global score
    score = 0
    loop = True
    start_button_rect = draw_start_button()
    pygame.display.update()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    loop = False

    game_loop()

def game_loop():
    balloons = []
    no_balloon = 10
    for _ in range(no_balloon):
        obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
        balloons.append(obj)

    start_time = pygame.time.get_ticks()
    one_minute = 60 * 1000  # milliseconds
    while pygame.time.get_ticks() - start_time < one_minute:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(no_balloon):
                    balloons[i].burst()

        display.fill(white)
        for i in range(no_balloon):
            balloons[i].show()
            balloons[i].move()

        pygame.draw.rect(display, darkBlue, (0, 0, 300, 50))
        time_elapsed = pygame.time.get_ticks() - start_time
        time_remaining = max(0, (one_minute - time_elapsed) // 1000)
        timer_text = font.render(f"Time Remaining: {time_remaining} s", True, white)
        display.blit(timer_text, (10, 10))

        pygame.draw.rect(display, darkBlue, (width - 400, 0, 400, 50))
        score_text = font.render(f"Balloons Shot: {score}", True, white)
        display.blit(score_text, (width - score_text.get_width() - 10, 10))

        pygame.display.update()
        clock.tick(60)

    show_result(score)

def show_result(score):
    modal_bg = pygame.Surface((width, height))
    modal_bg.set_alpha(200)
    modal_bg.fill((0, 0, 0))
    display.blit(modal_bg, (0, 0))

    modal_font = pygame.font.SysFont("Arial", 50)
    result_text = modal_font.render(f"Balloons Shot: {score}", True, white)
    display.blit(result_text, ((width - result_text.get_width()) // 2, (height - result_text.get_height()) // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)

game()
