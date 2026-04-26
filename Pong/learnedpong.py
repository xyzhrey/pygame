import pygame
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

clf= KNeighborsRegressor(n_neighbors=3)

WIDTH=1200
HEIGHT=600
BORDER=20
PWIDTH=30
PHEIGHT=300
fgColor = pygame.Color("white")
bgColor = pygame.Color("black")
RADIUS=15
velocity=-1
FRAMERATE=400

class Ball:
    global RADIUS

    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y=y
        self.vx=vx
        self.vy=vy
    def show(self, color):
        global screen,WIDTH,PWIDTH,BORDER,HEIGHT,PHEIGHT,bgColor, fgColor
        pygame.draw.circle(screen, color, (self.x, self.y), RADIUS)
    def update(self):
        global bgColor, fgColor
        self.show(bgColor)
        newx=self.x+self.vx
        newy=self.y+self.vy
        if newx<BORDER+RADIUS:
            self.vx=-self.vx
        elif newy>HEIGHT-BORDER-RADIUS or newy<BORDER+RADIUS:
            self.vy=-self.vy
            self.y=self.y+self.vy
        elif newx>WIDTH-PWIDTH-RADIUS and newy in range(pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[1]+PHEIGHT):
            self.vx=-self.vx
        else:
            self.show(bgColor)
            self.x=self.x+self.vx
            self.y=self.y+self.vy
            self.show(fgColor)


class Paddle:
    global HEIGHT, WIDTH, BORDER,PWIDTH, PHEIGHT
    def __init__(self, py):
        self.py=py
    def show(self, color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect((WIDTH-PWIDTH,self.py),(BORDER, PHEIGHT)))
    def update(self, prediction):
        if prediction-self.HEIGHT//2>BORDER and prediction+self.HEIGHT//2<HEIGHT-BORDER:
            self.show(bgColor)
            self.py=prediction
            self.show(fgColor)




ballplay= Ball(WIDTH-RADIUS, HEIGHT//2,velocity, velocity)
paddleplay=Paddle(HEIGHT//2)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
ballplay.show(fgColor)
pygame.draw.rect(screen, fgColor, pygame.Rect((0,0), (WIDTH,BORDER)))
pygame.draw.rect(screen, fgColor, pygame.Rect((0,0), (BORDER,HEIGHT)))
pygame.draw.rect(screen, fgColor, pygame.Rect((0,HEIGHT-BORDER), (WIDTH,BORDER)))
clock=pygame.time.Clock()


#sample = open("game.csv", "w")

#print("x, y, vx, vy, Paddle.y", file=sample)
pong=pd.read_csv('game.csv')
pong=pong.drop_duplicates()

X=pong.drop(columns="paddle.y")
Y=pong['paddle.py']
clf.fit(X,Y)


df=pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])
while True:

    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    clock.tick(FRAMERATE)
    pygame.display.flip()
    toPredict=df.append({'x':ballplay.x, 'y':ballplay.y, 'vx':ballplay.vx, 'vy':ballplay.vy}, ignore_index=True)
    shouldMove = clf.predict(toPredict)
    ballplay.update(shouldMove)
    paddleplay.update()

    #print("{}, {}, {}, {}, {}".format(ballplay.x, ballplay.y, ballplay.vx, ballplay.vy, paddleplay.py, file=sample))
pygame.quit()
