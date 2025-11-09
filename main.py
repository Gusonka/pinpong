from random import randint
from pygame import *

init()

window = display.set_mode((1000, 800))
clock = time.Clock()

platform = Rect(400, 700, 120, 20)
platform_speed = 10


class Ball:
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.dx = speed
        self.dy = -speed
        self.radius = radius
        self.color = color
        self.rect = Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)
        self.original_speed = abs(speed)

    def reset(self):
        draw.circle(window, self.color, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

        if self.x >= 1000 - self.radius or self.x <= self.radius:
            self.dx *= -1
            self.dx += randint(-1, 1)
        if self.y <= self.radius:
            self.dy *= -1
            self.dy += randint(-1, 1)
        if self.rect.colliderect(platform):
            self.dy *= -1

    @staticmethod
    def load_level_map(filename):
        bricks = []
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):
                if char == '#':
                    x = col_index * 50
                    y = row_index * 30
                    brick = Rect(x, y, 50, 20)
                    bricks.append(brick)
        return bricks


class Boost:
    def __init__(self, x, y, c, boost_type="spawn"):
        self.rect = Rect(x, y, 25, 25)
        self.color = c
        self.boost_type = boost_type
        self.active = True

    def reset(self):
        self.rect.y += 3
        draw.rect(window, self.color, self.rect)



current_level = 1
max_level = 3


def load_current_level():
    filename = f'lvl{current_level}.txt'
    return Ball.load_level_map(filename)


def next_level():
    global current_level, lvl, balls, boosts
    current_level += 1
    if current_level <= max_level:
        lvl = load_current_level()
        balls = [Ball(200, 400, 10, 8, (255, 255, 255))]
        boosts = []
        platform.x = 400
        print(f"Перехід на рівень {current_level}!")
    else:
        print("Вітаємо! Ви пройшли всі 3 рівні!")
        current_level = 1
        lvl = load_current_level()



balls = [Ball(200, 400, 10, 8, (255, 255, 255))]
lvl = load_current_level()
boosts = []


font.init()
level_font = font.SysFont('Arial', 36)

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()


    keys = key.get_pressed()
    if keys[K_d]:
        platform.x += platform_speed
    if keys[K_a]:
        platform.x -= platform_speed


    if platform.left < 0:
        platform.left = 0
    if platform.right > 1000:
        platform.right = 1000

    window.fill((0, 0, 0))


    level_text = level_font.render(f'Рівень: {current_level}/3', True, (255, 255, 255))
    window.blit(level_text, (20, 20))

    draw.rect(window, (0, 255, 255), platform, border_radius=15)


    for brick in lvl:
        draw.rect(window, (255, 0, 0), brick)
        draw.rect(window, (0, 255, 0), [brick.x, brick.y, brick.w, brick.h], 2)

    if not lvl:
        next_level()

    for boost in boosts[:]:
        boost.reset()
        if boost.rect.colliderect(platform):
            balls.append(Ball(boost.rect.x, boost.rect.y, 10, 8, (255, 255, 255)))
            boosts.remove(boost)

    for ball in balls[:]:
        ball.reset()
        ball.update()
        if ball.rect.colliderect(platform):
            ball.dy *= -1

        colliding_indexes = ball.rect.collidelistall(lvl)
        if colliding_indexes:
            ball.dy *= -1
            if not randint(0, 10):
                boosts.append(Boost(ball.rect.x, ball.rect.y, (0, 255, 0)))
            for i in sorted(colliding_indexes, reverse=True):
                lvl.pop(i)

        if ball.y > window.get_height():
            balls.remove(ball)


    if not balls:
        balls.append(Ball(400, 200, 10, 8, (255, 255, 255)))

    display.update()
    clock.tick(60)
