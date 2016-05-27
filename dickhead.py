import pygame
import math
import random



class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y

    def __add__(self, v):
        return Vec2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vec2(self.x - v.x, self.y - v.y)

    def __mul__(self, alpha):
        return Vec2(self.x * alpha, self.y * alpha)

    def __rmul__(self, alpha):
        return Vec2(self.x * alpha, self.y * alpha)

    def intpair(self):
        return (int(self.x), int(self.y))

    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y)


class Ball:
    def __init__(self, pos = Vec2(0,0), speed = Vec2(0,0), g = 100, rad =1 , k = 0.0 , i=1, color = (255,255,255)):
        self.pos, self.speed, self.g, self.rad, self.k, self.i, self.color = \
                pos, speed, g, rad, k, i, color

    def update(self, game):
        self.pos.x += self.speed.x * game.delta
        self.pos.y += self.speed.y * game.delta-0.5*self.g * game.delta * game.delta
        self.speed.y += self.g * game.delta
        self.i += 1

        if self.pos.x < self.rad:
            if self.speed.x < 0:
                self.speed.x = -self.speed.x
                self.pos.x = self.rad
        if self.pos.y < self.rad:
            if self.speed.y < 0:
                self.speed.y = -self.speed.y
                self.pos.y = -self.rad
        if self.pos.x > 1000-self.rad:
            if self.speed.x > 0:
                self.speed.x = -self.speed.x
                self.pos.x = 1000-self.rad

        if self.pos.y > 1000-self.rad:
            if self.speed.y > 0:
                self.speed.y = -self.k*self.speed.y
                self.pos.y = 1000-self.rad

    def render(self, game):
        pygame.draw.circle(game.screen,self.color,
                (int(self.pos.x), int(self.pos.y)), int(self.rad))

class Block:
    color = (50, 130, 50)
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1, self.y1, self.x2, self.y2 = \
            x1, y1, x2, y2

    def render(self, game):
        pygame.draw.rect(game.screen, self.color, (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1,))



def collideWithBlock(block, ball):
    blockMiddle = (block.y1 + block.y2) / 2
    if (ball.pos.x>block.x1)and(ball.pos.x<block.x2)and(ball.pos.y>block.y1-ball.rad)and(ball.pos.y<block.y2+ball.rad)and(ball.pos.y<blockMiddle):
        ball.speed.x = 10*random.random()*(-1)**ball.i
        ball.speed.y = 0
        ball.pos.y -= 3 
    if (ball.pos.x>block.x1)and(ball.pos.x<block.x2)and(ball.pos.y>block.y1-ball.rad)and(ball.pos.y<block.y2+ball.rad)and(ball.pos.y>blockMiddle):
        ball.speed.x = 10*random.random()*(-1)**ball.i
        ball.speed.y = 0
        ball.pos.y += 3 


def liquidInfluence(c, d):
    connectingVector = d.pos - c.pos
    try:
        if connectingVector.len() > 75:
            d.speed -= (connectingVector * (1 / connectingVector.len() ** 2)) * 25
            c.speed += (connectingVector * (1 / connectingVector.len() ** 2)) * 25
        else:
            d.speed += (connectingVector * (1 / connectingVector.len() ** 2)) * (30 + d.color[0]) * 3
            c.speed -= (connectingVector * (1 / connectingVector.len() ** 2)) * (30 + c.color[0]) * 3
    except:
        pass

    if connectingVector.len() < 80:
        if c.color[0] <= 239:
            c.color = (c.color[0] + 15, c.color[1], c.color[2] - 15)
    else:
        if c.color[0] >= 1:
            c.color = (c.color[0] - 1, c.color[1], c.color[2] + 1)

class Game:
    def tick(self):
        self.delta = self.clock.tick(50) / 1000.0

    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 1000, 1000
        # create main display - 640x400 window
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('Game')
        # get object to help track time
        self.clock  = pygame.time.Clock()

        # set default tool
        self.tool = 'run'
        self.ball = Ball()
        self.balls = []
        for j in range(35):
            self.balls.append(Ball(Vec2(1000*random.random(),random.random()*50),Vec2(0,0),  rad=40, color = (0, 0, 255)))

        self.block = Block()
        self.blocks = []
        self.blocks.append(Block(500,100,600,200))
        self.blocks.append(Block(200,400,450,450))
        self.blocks.append(Block(50,200,300,250))
        self.blocks.append(Block(0,500,300,540))
        self.blocks.append(Block(400,550,550,600))
        self.blocks.append(Block(800,200,1000,250))
        self.blocks.append(Block(600,750,800,800))
        self.blocks.append(Block(200,900,700,950))
        self.blocks.append(Block(500,750,600,800))
        self.blocks.append(Block(700,600,1000,650))
        #self.blocks.append(Block(30,23,90,21))
        #self.blocks.append(Block(50,10,20,200))
        #self.blocks.append(Block(120,90,67,30))
        #self.blocks.append(Block(40,37,78,41))
        self.units = self.balls + self.blocks
        #self.units = self.balls
        #self.units = self.blocks
        #for b in self.balls:
        #    self.units.append(b)
        #for c in self.blocks:
        #    self.units.append(c)



    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        elif event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

    def update(self):
        """Here game objects update their positions"""
        self.tick()

        self.ball.update(self)
        for c in self.balls:
            print("updated ball")
            c.update(self)
        for c in self.balls:
            for z in self.blocks:
                print("updated ball/block")
                collideWithBlock(z,c)
        for c in self.balls:
            for d in self.balls:
                if not c == d:
                    print("updated ball/ball")
                    liquidInfluence(c, d)


    def render(self):
        """Render the scene"""
        self.screen.fill((0, 0, 0))
        '''self.ball.render(self)
        self.block.render(self)'''



        '''for b in self.blocks:
            b.render(self)
        for c in self.balls:
            c.render(self)'''

        for n in self.units:
            n.render(self)






        pygame.display.flip()

    def exit(self):
        """Exit the game"""
        self._running = False

    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                self.event_handler(event)
            self.update()
            self.render()
        self.cleanup()





if __name__ == "__main__":
    game = Game()
    game.execute()
