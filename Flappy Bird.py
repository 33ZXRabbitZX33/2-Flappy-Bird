import pygame, sys, random
from pygame.locals import *


WINDOWWIDTH = 800
WINDOWHEIGHT = 600

BACKGROUND = pygame.image.load('img2/background.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND,(800,600))

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird')

class Background():
      def __init__(self):
          self.x = 0
          self.y = 0
          self.img = BACKGROUND
          self.img_speed = 3
          self.width = self.img.get_width()
          self.height = self.img.get_height()
      def draw(self):
          DISPLAYSURF.blit(self.img,(int(self.x),int(self.y)))
          DISPLAYSURF.blit(self.img,(self.x + self.width ,self.y))
      def update(self):
          self.x -= self.img_speed
          if self.x < -self.width:
             self.x += self.width

BIRD = pygame.image.load('img2/bird.png')
BIRD = pygame.transform.scale(BIRD,(40,40))
X_MARGIN = 300
bird_speed = 8
FALLSPEED = 0
ACCELERATION = 0.4

class Bird():
      def __init__(self):
          self.x = X_MARGIN
          self.y = 0         
          self.speed_up = bird_speed
          self.speed_fall = FALLSPEED
          self.acc = ACCELERATION
          self.bird_img = BIRD
          self.width = self.bird_img.get_width()
          self.height = self.bird_img.get_height()
      def draw(self,bg):
          DISPLAYSURF.blit(self.bird_img,(self.x,self.y + (bg.height-self.height)/2))
      def update(self,space):
          self.y += self.speed_fall + 0.5*self.acc
          self.speed_fall += self.acc
          if space == True :
             self.y -= self.speed_up
             self.speed_fall -= self.speed_up

OBSTACIESIMG = pygame.image.load('img2/column.png')

DISTANCE = 180
speed_column = 3

class Obstacles():     
      def __init__(self,bg):         
          self.dis = DISTANCE
          self.speed = speed_column
          self.ls = []
          for i in range(7):
              x = (bg.width + 40 + i*self.dis)
              c1 = random.randrange(0,400)
              c2 = 400 - c1
              self.ls.append([x,c1,c2])
     
      def draw(self):
          def column(y):
              img =  pygame.transform.scale(OBSTACIESIMG,(40,y))
              return img
          for i in range(7):
              DISPLAYSURF.blit(column(self.ls[i][1]),  (self.ls[i][0],0)                      )
              DISPLAYSURF.blit(column(self.ls[i][2]),  (self.ls[i][0],self.ls[i][1]+200)      )
      def update(self):
          for i in range(7):
              self.ls[i][0] -= self.speed
          if self.ls[0][0] < -40 :
             del(self.ls[0])
             x = self.ls[5][0] + self.dis
             c1 = random.randrange(0,400)
             c2 = 400 - c1 
             self.ls.append([x,c1,c2])


def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False   
def isGameOver(bird, obs,bg):
    for i in range(7):
        rectBird = [bird.x, bird.y+ (bg.height-bird.height)/2, bird.width, bird.height]
        rectColumn1 = [obs.ls[i][0], 0, 40, obs.ls[i][1]]
        rectColumn2 = [obs.ls[i][0],obs.ls[i][1]+200,40,obs.ls[i][2]]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            return True

    if bird.y + (bg.height-bird.height)/2 < 0 or bird.y + (bg.height-bird.height)/2 + bird.height > WINDOWHEIGHT:
       return True
    return False

class Score():
    def __init__(self):
        self.score = 0
    def draw(self):
        font = pygame.font.SysFont('consolas',30)
        font = font.render("Score :" + str(int(self.score)),True,(255,255,255))
        DISPLAYSURF.blit(font,(0,0))
    def update(self):
        self.score += 0.2  
        
class Score2():
    def __init__(self):
        self.score = 0
        self.addScore = True
    
    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        scoreSuface = font.render(str(self.score), True, (0, 0, 0))
        textSize = scoreSuface.get_size()
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))
    
    def update(self, bird, obs,bg):
        collision = False
        for i in range(7):
            rectColumn = [obs.ls[i][0],obs.ls[i][1],40,200]
            rectBird = [bird.x, bird.y+ (bg.height-bird.height)/2, bird.width, bird.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
            self.addScore = False
        else:
            self.addScore = True


def Gamestart():
    pass

def GamePlay(bg,bird,obs,score,score2):
    bg.__init__()
    bird.__init__()
    obs.__init__(bg)
    score.__init__()
    score2.__init__()
    space = False
    
    while True:
        space = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                  space = True
            

        

        if isGameOver(bird,obs,bg)  :
           return

        bg.draw()
        bg.update()

        bird.draw(bg)
        bird.update(space)

        obs.draw()
        obs.update()

        score.draw()
        score.update()

        score2.draw()
        score2.update(bird, obs,bg)

        pygame.display.update()
        fpsClock.tick(FPS)

def Gameover(bg,bird,obs,score,score2):
    font_over = pygame.font.SysFont("consolas",60)
    font_gover = font_over.render('Game over',True,(255,0,0))
    gover_size = font_gover.get_size()

    font_scor = pygame.font.SysFont("consolas",20)
    font_score = font_scor.render("Score : " + str(int(score.score)) +  " ,Press \"Enter\" to Play",True,(234,120,50))
    score_size = font_score.get_size()

    while True:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
              if event.type == pygame.KEYDOWN:
                 if event.key == K_RETURN:
                    return
                     
          
          bg.draw()
          bird.draw(bg)
          obs.draw()
          
          score2.draw()
          score2.update(bird, obs,bg)

          DISPLAYSURF.blit(font_gover,(int((bg.width-gover_size[0])/2),150))      
          DISPLAYSURF.blit(font_score,(int((bg.width-score_size[0])/2),300))  

          pygame.display.update()
          fpsClock.tick(FPS)
    

def main():
    bg = Background()
    bird = Bird()
    obs = Obstacles(bg)
    score = Score()
    score2 = Score2()
    while True:
          GamePlay(bg,bird,obs,score,score2)
          Gameover(bg,bird,obs,score,score2) 
          
if __name__ == '__main__':
    main()