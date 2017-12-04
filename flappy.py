#/Users/TsEric/Desktop/ANN/flappybird/Python3
#
# Tsing-Hay Eric Chow
#
# Simple Flappy Bird for ANN


import sys
import pygame
import random
import numpy
import os

# Define Const
CONST_GRAVITY = 10
CONST_BIRDUPSWING = -55
CONST_BACKGROUNDSPEED = 2
CONST_FPS = 20
CONST_IMAGEWIDTH = 568
CONST_SCREENHEIGHT = 512
CONST_SCREENWIDTH = 284
CONST_HOLESIZE = 110
CONST_PATH = os.path.abspath(__file__)
CONST_PATH = CONST_PATH[0:(len(CONST_PATH)-9)]
CONST_PIPEWIDTH = 50
CONST_BIRD_START_X = 50
CONST_BIRD_START_Y = 200
  


class BG():
    
    def __init__(self):
        
        self.reset = 0;
        self.image = pygame.image.load(CONST_PATH+"images/background.png").convert_alpha()
        self.pos = ([0,0])


    def animation(self):
        
        if self.pos[0] <= (-CONST_IMAGEWIDTH):
            self.pos[0] = 0;
            self.reset = 1;

           
        self.pos[0] = self.pos[0] - CONST_BACKGROUNDSPEED

class Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.BirdUp = pygame.image.load(CONST_PATH+"images/bird_wing_up.png").convert_alpha()
        self.BirdDown = pygame.image.load(CONST_PATH+"images/bird_wing_down.png").convert_alpha()
        self.imageList = ([self.BirdUp, self.BirdDown])
        self.animationCount = 0
        self.image = self.imageList[self.animationCount]

        # Starting Position
        self.posX = CONST_BIRD_START_X
        self.posY = CONST_BIRD_START_Y
        
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.posX, self.posY)
    
    def animation(self):
    
        if self.animationCount == 0:
            self.animationCount = 1
        else:
            self.animationCount = 0

        self.image = self.imageList[self.animationCount]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.posX,self.posY)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self,boost):
    
        # set borders
        self.posY = self.posY + boost;
        if (self.posY < 0 ):
            self.posY = 0

        if (self.posY >= 480):
            self.posY = 480

        self.posX = self.posX

    def mask(self):
       return pygame.mask.from_surface(self.image)

    def rect(self):
        return Rect(self.posX, self.posY, 32, 32)

    def flap(self):
        self.move(CONST_BIRDUPSWING)



class Pipe(pygame.sprite.Sprite):
    
    def __init__(self, height, xPos, pNumber):
        
        pygame.sprite.Sprite.__init__(self)
        self.pipebody = pygame.image.load(CONST_PATH+"images/pipe_body.png").convert_alpha()
        self.pipehead = pygame.image.load(CONST_PATH+"images/pipe_end.png").convert_alpha()
        self.pipehead = pygame.transform.scale(self.pipehead,(CONST_PIPEWIDTH , 32));
        self.height = height
        self.number = pNumber

        # bottom pipe
        self.images = pygame.transform.scale(self.pipebody,(CONST_PIPEWIDTH , height));
        self.pipe = ([self.images,self.pipehead])
        
        # top pipe
        self.images = pygame.transform.scale(self.pipebody,(CONST_PIPEWIDTH , CONST_SCREENHEIGHT - height - CONST_HOLESIZE));
        self.pipe.append(self.images)
        self.pipe.append(self.pipehead)
        
        self.images = self.pipe
        
        # PosX = ([Bottom Pipebody, Bottom Pipehead , Top Pipebody, Top Pipehead])
        # 100 = size of hole
        # 32 = height of pipehead
        
        self.posX = ([xPos , xPos , xPos , xPos])
        self.posY = ([CONST_SCREENHEIGHT - height , (CONST_SCREENHEIGHT - height) , (0) ,(CONST_SCREENHEIGHT - height - CONST_HOLESIZE - 32)])
        self.position = ([self.posX , self.posY])
        self.height = ([height , 32 , (CONST_SCREENHEIGHT - height - CONST_HOLESIZE) , 32 ])


        self.image = pygame.Surface((CONST_PIPEWIDTH, 512), 0x00010000)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect();

    def animation(self,backgroundPosition):
        
        self.position = []
        
        for counter in range(4):
            
            array1 = numpy.array([self.posX[counter] , self.posY[counter]])
            array2 = numpy.array(backgroundPosition)
            position = numpy.add(array1, array2)
            self.position.append(position)

    def rect(self):
        
        return Rect(self.posX, self.posY, 512 , 80)

    def collides_with(self, bird):
        
        for counter in range(4):
            
            self.mask = pygame.mask.from_surface(self.images[counter])
            self.rect = pygame.Rect(self.position[counter][0] , self.position[counter][1] , self.height[counter] , 32)

            if pygame.sprite.collide_mask(self, bird) is not None:
                print (self.number)
                return True;

        return False;


def get_distance(obstacle,bird):
    
    # Search for the next Pipe
    length = [obstacle[0].position[0][0] + CONST_BIRD_START_X - CONST_PIPEWIDTH,obstacle[1].position[0][0] + CONST_BIRD_START_X - CONST_PIPEWIDTH,obstacle[2].position[0][0] + CONST_BIRD_START_X - CONST_PIPEWIDTH,obstacle[3].position[0][0] + CONST_BIRD_START_X - CONST_PIPEWIDTH]
    
    horizontal_distance = min(i for i in length if i > 0)
    index = (length.index(horizontal_distance))
    
    
    vertical_distance = int(CONST_SCREENHEIGHT - bird.posY - (obstacle[index].height[0] + (CONST_HOLESIZE/2)))

    print (horizontal_distance , vertical_distance)


def game_start():
    

    # Init the game
    pygame.init()
    size = width,height = (CONST_SCREENWIDTH,CONST_SCREENHEIGHT)
    screen = pygame.display.set_mode(size);
    pygame.display.set_caption("Flappy Bird")
    
    # Init background
    global background
    background = BG()
    
    # Init player
    global player
    player = Bird()
    
    # Init time label
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Init pipe
    global obstacle1
    
    pipeHeight1 = random.randint(50,400)
    obstacle1 = Pipe(pipeHeight1,284,1)
        
    global obstacle2
    pipeHeight2 = random.randint(50,400)
    obstacle2 = Pipe(pipeHeight2, 460,2)
    
    global obstacle3
    global obstacle4
    pipeHeight3 = random.randint(50,400)
    obstacle3 = Pipe(pipeHeight3, (568 + 80),3)
    obstacle4 = Pipe(pipeHeight3, (-80),4)
    
    obstacle = [obstacle1, obstacle2, obstacle3, obstacle4]

    # Init add var
    Bool_HoldKey = 0
    Bool_GameOver = False
    
    while 1:
        # No FPS over 10
        clock.tick(CONST_FPS)
        
        
        # Game Ending
        if Bool_GameOver == True:
            print("Game Over: %i " % int(pygame.time.get_ticks()/1000))
            break;
    
        # Event handeling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Bool_HoldKey == 0:
                    Bool_HoldKey = 1
                    player.flap()
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and Bool_HoldKey == 1:
                    Bool_HoldKey = 0
 
        # Gravity force
        player.move(CONST_GRAVITY)
 
        # Run Animations
        background.animation()
        player.animation()
        
        if (background.reset == 1):
            
            obstacle4 = Pipe(pipeHeight3, 80,4)
        
            background.reset = 0
            pipeHeight1 = random.randint(40,400)
            pipeHeight2 = random.randint(40,400)
            pipeHeight3 = random.randint(40,400)
            pipeHeight4 = random.randint(40,400)
            
            obstacle1 = Pipe(pipeHeight1,284,1)
            obstacle2 = Pipe(pipeHeight2,488,2)
            obstacle3 = Pipe(pipeHeight3, (568 + 80),3)
        
            obstacle = [obstacle1 , obstacle2 , obstacle3 , obstacle4]
    
    
        obstacle1.animation(background.pos)
        obstacle2.animation(background.pos)
        obstacle3.animation(background.pos)
        obstacle4.animation(background.pos)
        
        # Update time
        time = font.render(str(int(pygame.time.get_ticks()/1000)), 10, (0,0,0))
        textpos = time.get_rect()
        
        # check for collision
        pipe_collision = any(p.collides_with(player) for p in obstacle)
        if pipe_collision:
            Bool_GameOver = True;
        
        # Update Blit
        screen.blit(background.image, background.pos)
        
        for counter in range(4):
            screen.blit(obstacle1.images[counter] , obstacle1.position[counter])
        
        for counter in range(4):
            screen.blit(obstacle2.images[counter] , obstacle2.position[counter])
        
        for counter in range(4):
            screen.blit(obstacle3.images[counter] , obstacle3.position[counter])
        
        for counter in range(4):
            screen.blit(obstacle4.images[counter] , obstacle4.position[counter])
        
        screen.blit(player.image, player.rect)
        screen.blit(time, (5,5))
        pygame.display.update()

        get_distance(obstacle,player)






main()


