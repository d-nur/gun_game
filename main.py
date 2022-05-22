import time
import pygame
import math
from random import randint

pygame.init()

W = 800
H = 600
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 30
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
sc = pygame.display.set_mode((W, H))

pygame.font.init()
font = pygame.font.SysFont('Consolas', 14)


class Ball:
    def __init__(self, sc, deg):
        self.sc = sc
        self.deg = math.radians(deg)
        self.b_pos = (math.cos(self.deg) * 100 + 25, (570 - math.sin(self.deg) * 100))
        self.x = self.b_pos[0]
        self.y = self.b_pos[1]
        self.vx = 0
        self.vy = 0

    def draw(self):
        pygame.draw.circle(self.sc, BLACK, (self.x, self.y), 10)

    def move(self):
        gravity_x = 7
        gravity_y = 3
        if self.x >= W:
            self.vx = -self.vx
            self.vx -= gravity_x
        if self.y >= H:
            self.vy = -self.vy
            self.vy -= gravity_y
        self.vy -= gravity_y
        self.x += self.vx
        self.y -= self.vy

    def is_hit(self, obj):
        if ((self.x - obj.cx_pos) ** 2 + (self.y - obj.cy_pos) ** 2) ** 0.5 <= (10 + obj.rad):
            return True
        else:
            return False


class Gun:
    def __init__(self, sc):
        self.sc = sc
        self.deg = 45
        self.sf = pygame.Surface((100, 30))
        self.p_sf = pygame.Surface((100, 10))
        self.power = 10
        self.an = 1
        self.shoot_on = 0
        self.gun_image = pygame.image.load('images/gun2.png')

    def targeting(self, pos):
        if event:
            if pos[0] != 0:
                self.deg = math.degrees(math.atan((600 - pos[1])/pos[0]))
            else:
                pass

    def start_shoot(self):
        self.shoot_on = 1

    def shoot(self):
        global balls
        ball = Ball(sc, self.deg)
        self.an = math.atan2((pos[1] - ball.y), (pos[0] - ball.x))
        ball.vx = self.power * math.cos(self.an)
        ball.vy = - self.power * math.sin(self.an)

        balls.append(ball)
        self.shoot_on = 0
        self.power = 10

    def power_up(self):
        if self.shoot_on == 1:

            if self.power < 100:
                self.power += 1


    def draw(self):
        if self.shoot_on == 1:
            self.p_sf.fill(SILVER)
            pygame.draw.line(self.p_sf, RED, (0, 5), (self.power, 5), 10)
            self.sc.blit(self.p_sf, (10, 450))
        self.sf.fill(WHITE)
        self.gun_image = pygame.transform.scale(self.gun_image, (100, 50))
        gun_image_rot = pygame.transform.rotate(self.gun_image.convert_alpha(), 5 + self.deg)
        self.sc.blit(gun_image_rot, (15, 540 - self.deg + 5))


class Target:
    def __init__(self, sc):
        self.sc = sc
        self.rad = randint(20, 50)
        self.vx = randint(1, 10)
        self.vy = randint(1, 10)
        self.live = 1
        self.cx_pos = randint(self.rad + 100, W - self.rad)
        self.cy_pos = randint(self.rad + 50, H - self.rad - 100)
        self.points = 0

    def target_init(self):
        self.cx_pos = randint(self.rad + 100, W - self.rad)
        self.cy_pos = randint(self.rad + 50, H - self.rad - 100)
        self.rad = randint(20, 50)
        self.vx = randint(1, 10)
        self.vy = randint(1, 10)
        self.live = 1

    def hit(self):
        self.live = 0
        self.points += 1

    def move(self):
        if 0 >= self.cx_pos - self.rad or self.cx_pos + self.rad >= W:
            self.vx = -self.vx
        if 0 >= self.cy_pos - self.rad or self.cy_pos + self.rad >= H:
            self.vy = -self.vy
        self.cx_pos += self.vx
        self.cy_pos += self.vy

    def draw(self):
        pygame.draw.circle(self.sc, SILVER, (self.cx_pos, self.cy_pos), self.rad)


running = False
running2 = True
running3 = False
counter = 30
counter2 = 5
gun = Gun(sc)
target1 = Target(sc)
target2 = Target(sc)
balls = []
bg_image = pygame.image.load('images/bg1.png').convert()
wheel = pygame.image.load('images/wheel.png').convert_alpha()

while running2:
    sc.blit(bg_image, (0, 0))
    text_sf = font.render('Нажмите на экран, чтобы начать игру', True, BLACK)
    text_sf_rect = text_sf.get_rect(center=(W // 2, H // 2))
    sc.blit(text_sf, text_sf_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            running3 = True
            running2 = False
    pygame.display.update()
    clock.tick(FPS)


while running3:
    sc.blit(bg_image, (0, 0))
    next_text = text_sf = font.render(f'Игра начнется через: {counter2}', True, BLACK)
    text2_sf_rect = next_text.get_rect(center=(W // 2, H // 2))
    sc.blit(next_text, text2_sf_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            counter2 -= 1
            if counter2 < 0:
                running = True
                running3 = False
    pygame.display.update()
    clock.tick(FPS)


while running:
    sc.fill(WHITE)
    sc.blit(bg_image, (0, 0))
    gun.draw()
    sc.blit(wheel, (-50, 530))
    target1.draw()
    target2.draw()
    points_surface = font.render(f'Очки: {target1.points + target2.points}', True, BLACK)
    with open('record.txt', 'r') as f:
        r = f.readline()
    record_sf = font.render(f'Рекорд {r}', True, BLACK)
    time_sf = font.render(f'Время: {counter}', True, BLACK)
    if target1.points + target2.points > int(r) and counter == 0:
        sf_congratulations = font.render(f'Поздравляю! Новый рекорд: {target1.points + target2.points}', True,
                                                BLACK)
        con_rect = sf_congratulations.get_rect(center=(W//2, H//2))
        sc.blit(sf_congratulations, con_rect)

    sc.blit(points_surface, (10, 10))
    sc.blit(time_sf, (600, 10))
    sc.blit(record_sf, (300, 10))
    for b in balls:
        b.draw()
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            counter -= 1
            if counter < 0:
                counter = 30
                if target1.points + target2.points > int(r):
                    with open('record.txt', 'w') as f:
                        print(str(target1.points + target2.points))
                        f.write(str(target1.points + target2.points))
                target1.points = 0
                target2.points = 0
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            gun.targeting(pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.start_shoot()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.shoot()
    for b in balls:
        b.move()
        if b.is_hit(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.target_init()
        if b.is_hit(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.target_init()

    for t in [target1, target2]:
        t.move()

    gun.power_up()
