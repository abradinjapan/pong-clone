import sys
import pygame
import random
import time

class sprite:
    def __init__(self, img_address, xy, wh):
        self.img = pygame.image.load(img_address)
        self.xy = xy
        self.wh = wh
        self.cxcy = [0, 0]

    def draw(self, display):
        display.blit(pygame.transform.scale(self.img, self.wh), self.xy)

    def hit(self, collidee):
        return self.as_rect().colliderect(collidee)

    def as_rect(self):
        return pygame.rect.Rect(self.xy, self.wh)

class wall(sprite):
    def __init__(self, img_address, xy, wh):
        sprite.__init__(self, img_address, xy, wh)

class paddle(sprite):
    def __init__(self, img_address, xy):
        sprite.__init__(self, img_address, xy, [10, 100])

    def move(self, screen_wh):
        self.xy[1] += self.cxcy[1]

        if self.xy[1] < 0 - self.wh[1]:
            self.xy[1] = screen_wh[1]
        elif self.xy[1] > self.wh[1] + screen_wh[1]:
            self.xy[1] = 0

class puck(sprite):
    def __init__(self, img_address, xy):
        sprite.__init__(self, img_address, xy, [10, 10])
        self.cxcy = [random.randint(-15, 15), random.randint(-15, 15)]

    def move(self, walls, paddles):
        scores = [0, 0]
        
        for i in range(len(walls)):
            if walls[i].hit(self.as_rect()):
                self.cxcy[i % 2] *= -1

                if i == 0:
                    scores[1] = 1
                if i == 2:
                    scores[0] = 1
        for i in range(len(paddles)):
            if paddles[i].hit(self.as_rect()):
                self.cxcy[0] *= -1
        self.xy[0] += self.cxcy[0]
        self.xy[1] += self.cxcy[1]

        return scores


class game:
    def __init__(self):
        self.display = None
        self.running = True
        self.started = False
        self.wh = [1000, 600]
        self.fps = 60
        self.title = "Pong!"
        self.bc = [0, 0, 0]
        self.walls = []
        self.pucks = []
        self.paddles = [None, None]
        self.scores = [0, 0]
        self.max_score = 10

    def display_text(self, msg, color, xy):
        self.display.blit(pygame.font.SysFont("Comic Sans MS", 30).render(str(msg), 0, color), xy)

    def play(self, puck_count, wall_asset_file_path, ball_asset_file_path):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        random.seed(time.time())
        t = 10
        ts = [0, 0]

        self.display = pygame.display.set_mode(self.wh)
        pygame.display.set_caption(self.title)

        moves = [[-10, 10, -10, 10], [0, 0, 0, 0]]
        held = [pygame.KEYDOWN, pygame.KEYUP]
        keys = [pygame.K_w, pygame.K_s, pygame.K_UP, pygame.K_DOWN]

        self.walls.append(wall(wall_asset_file_path, [0, 0], [t, self.wh[1]]))
        self.walls.append(wall(wall_asset_file_path, [0, 0], [self.wh[0], t]))
        self.walls.append(wall(wall_asset_file_path, [self.wh[0] - t, 0], [t, self.wh[1]]))
        self.walls.append(wall(wall_asset_file_path, [0, self.wh[1] - t], [self.wh[0], t]))

        for i in range(puck_count):
            self.pucks.append(puck(ball_asset_file_path, [100, 100]))

        self.paddles[0] = paddle(wall_asset_file_path, [100, self.wh[1] / 2])
        self.paddles[1] = paddle(wall_asset_file_path, [900, self.wh[1] / 2])

        while self.running and self.scores[0] < self.max_score and self.scores[1] < self.max_score:
            self.display.fill(self.bc)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False

                for i in range(2):
                    for j in range(4):
                        if e.type == held[i] and e.key == keys[j]:
                            self.paddles[int(j / 2)].cxcy[1] = moves[i][j]

            for w in self.walls:
                w.draw(self.display)
            for p in self.paddles:
                p.move(self.wh)
                p.draw(self.display)

            for p in self.pucks:
                ts = p.move(self.walls, self.paddles)
                p.draw(self.display)
                self.scores[0] += ts[0]
                self.scores[1] += ts[1]

            self.display_text(str(self.scores[0]) + ":" + str(self.scores[1]), [255, 255, 255], [self.wh[0] / 2, t])

            pygame.display.update()
            clock.tick(self.fps)
        print(str(self.scores[0]) + ":" + str(self.scores[1]))
        pygame.quit()

# run game
game = game()
game.play(4, "./assets/wall.png", "./assets/ball.png")
