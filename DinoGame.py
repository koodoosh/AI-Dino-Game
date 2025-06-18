import pygame
import os
import random

SPEED = 10

run1 = pygame.image.load(os.path.join("img", "run1.png"))
run2 = pygame.image.load(os.path.join("img", "run2.png"))
jump = pygame.image.load(os.path.join("img", "jump.png"))
low1 = pygame.image.load(os.path.join("img", "low1.png"))
low2 = pygame.image.load(os.path.join("img", "low2.png"))
floor = pygame.image.load(os.path.join("img", "floor-1.png"))
cloud = pygame.image.load(os.path.join("img", "1x-cloud.png"))
cactuses = [pygame.image.load(os.path.join("img", "CACTUS" + str(i) + ".png")) for i in range(1, 6)]
enemy1 = pygame.image.load(os.path.join("img", "enemy1.png"))
enemy2 = pygame.image.load(os.path.join("img", "enemy2.png"))


class Dino:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.duck_y = 0
        self.y_vel = 0
        self.y_accel = 3
        self.jumping = False
        self.ducking = False
        self.counter = 0
        self.max_speed = 27

        self.img = run1
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def collision_detection(self, cactuses, enemies):
        x = self.x
        y = self.y
        w = self.img.get_width() + 5
        h = self.img.get_height()

        for cactuse in cactuses:
            cx = cactuse.x
            cy = cactuse.y
            cw = cactuse.img.get_width()
            ch = cactuse.img.get_height()

            if x < cx + cw and x + w > cx and y < cy + ch and y + h > cy:
                return True

        for enemy in enemies:
            ex = enemy.x
            ey = enemy.y
            ew = enemy.img1.get_width()
            eh = enemy.img1.get_height()

            if self.ducking:
                if x < ex + ew and x + w > ex and y + 17 < ey + eh and y + h > ey:
                    return True
            else:
                if x < ex + ew and x + w > ex and y < ey + eh and y + h > ey:
                    return True

        return False

    def move(self):
        if self.jumping:
            self.jump()
            self.img = jump

            if self.y_vel >= self.max_speed:
                self.y_vel = 0
                self.jumping = False

            self.y += self.y_vel
        else:
            self.y = 140
            if self.img == run1:
                self.img = run2
            else:
                self.img = run1

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_vel = -1 * self.max_speed
        else:
            self.y_vel += self.y_accel

    def duck(self):
        self.ducking = True

    def stop_ducking(self):
        if self.ducking:
            self.ducking = False

    def draw(self, win):
        if self.ducking:
            if self.counter == 0:
                self.img = pygame.transform.scale(low1.convert_alpha(), (60, 30))
                self.counter += 1
            else:
                self.img = pygame.transform.scale(low2.convert_alpha(), (60, 30))
                self.counter = 0
            win.blit(self.img, (self.x, self.y + 17))
        else:
            win.blit(self.img, (self.x, self.y))



class Cactus:

    def __init__(self, width, height):
        self.img = cactuses[random.randint(0, 4)]
        self.x = width
        self.y = height - floor.get_height() * 2 - self.img.get_height() + 10

    def check_dino_collision(self, dinos, networks, genomes):
        x = self.x
        y = self.y

        w = self.img.get_width()
        h = self.img.get_height()

        for dino in dinos:
            collided = False

            dx = dino.x
            dy = dino.y
            dw = dino.width
            dh = dino.height

            if y <= dy + dh / 2 <= y + h:
                if x <= dx <= x + w:
                    collided = True

                if x <= dx + dw <= x + w:
                    collided = True

            if y <= dy + dh <= y + h:
                if x <= dx <= x + w:
                    collided = True

                if x <= dx + dw <= x + w:
                    collided = True

            if collided:
                del networks[dinos.index(dino)]
                del genomes[dinos.index(dino)]
                dinos.remove(dino)

    def move(self):
        self.x -= SPEED

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def disappear(self):
        if self.x <= -1 * self.img.get_width():
            return True
        return False


class BG:

    def __init__(self, width, height):
        self.win_width = width
        self.win_height = height
        self.img = pygame.transform.scale(floor.convert_alpha(), (1000, 30))

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = 0
        self.y = height - self.height + 5
        self.clouds_x = []
        self.clouds_y = []
        self.cloud_img = cloud
        self.clouds_x.append(width)
        self.clouds_y.append(random.randint(10, 100))
        self.tick = 0

    def move(self):
        if self.x <= -1 * self.width:
            self.x = 0
        self.x -= SPEED

        for index, x in enumerate(self.clouds_x):
            if x <= -1 * self.cloud_img.get_width():
                del self.clouds_x[index]
                del self.clouds_y[index]

            self.clouds_x[index] -= (SPEED / 3)

        if self.tick >= 100:
            self.tick = 0
            self.clouds_x.append(self.win_width)
            self.clouds_y.append(random.randint(10, 100))

        self.tick += 1

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        win.blit(self.img, (self.x + self.width, self.y))

        for index, x in enumerate(self.clouds_x):
            # print("X: " + str(pos) + "   Y: " + str(self.clouds[index + 1]))
            win.blit(self.cloud_img, (x, self.clouds_y[index]))


class Pterodactyl:

    def __init__(self, width):
        self.x = width
        rand = random.randint(1, 3)
        if rand == 1:
            self.y = 102
        elif rand == 2:
            self.y = 130
        else:
            self.y = 70

        self.img1 = pygame.transform.scale(enemy1.convert_alpha(), (50, 40))
        self.img2 = pygame.transform.scale(enemy2.convert_alpha(), (50, 40))
        self.counter = 0

    def check_dino_collision(self, dinos, networks, genomes):
        x = self.x
        y = self.y

        w = self.img1.get_width()
        h = self.img1.get_height()

        for dino in dinos:
            collided = False

            dx = dino.x
            dy = dino.y
            dw = dino.width
            dh = dino.height

            if y <= dy + dh / 2 <= y + h:
                if x <= dx <= x + w:
                    collided = True

                if x <= dx + dw <= x + w:
                    collided = True

            if y <= dy <= y + h:
                if x <= dx <= x + w:
                    collided = True

                if x <= dx + dw <= x + w:
                    collided = True

            if collided:
                del networks[dinos.index(dino)]
                del genomes[dinos.index(dino)]
                dinos.remove(dino)

    def move(self):
        self.x -= SPEED

    def draw(self, win):
        image = self.img2

        if self.counter >= 10:
            image = self.img1
        if self.counter >= 15:
            self.counter = 0

        self.counter += 1

        win.blit(image, (self.x, self.y))

    def disappear(self):
        if self.x <= -1 * self.img1.get_width():
            return True
        return False