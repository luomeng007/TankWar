#-*-coding:utf-8-*-
import pygame,time,random

_display = pygame.display
COLOR_RED = pygame.Color(255,0,0)
version = 'v1.6'

class MainGame():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    window = None
    P1_TANK = None
    # v1.6 新增敌方坦克列表，用来存储地方所有坦克
    enermy_tank_list = []
    enermy_tank_count = 5
    #start a game
    def startGame(self):
        # initialize the game window
        pygame.display.init()
        # display the window
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        # set the title of the game window
        pygame.display.set_caption('坦克大战'+version)
        MainGame.P1_TANK = Tank(300,200)

        # v1.6 新增创建敌方坦克
        self.creatEnermyTank()

        while True:
            MainGame.window.fill(pygame.Color(0,0,0))

            self.getEvent()

            MainGame.window.blit(self.writeText('remain tanks %d' %5),(5,5))

            MainGame.P1_TANK.display_tank()

            # v1.6 新增将创建好的敌方坦克加入到屏幕上
            for eTank in MainGame.enermy_tank_list:
                eTank.displayEnermyTank()

            # call the tank move function
            if not MainGame.P1_TANK.stop:
                MainGame.P1_TANK.move()

            _display.update()

            # add the updating time
            time.sleep(0.0025)

    def creatEnermyTank(self):
        for i in range(MainGame.enermy_tank_count):
            random_left = random.randint(1,8)
            random_speed = random.randint(1,3)
            # 创建坦克
            enermy_tank = EnermyTank(random_left * 100,150,random_speed)
            MainGame.enermy_tank_list.append(enermy_tank)

    def getEvent(self):
        # get all event
        eventList = pygame.event.get()
        for event in eventList:
            # use type character to judge which event
            if event.type == pygame.QUIT:
                print("quit the game")
                self.gameOver()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("move towards left")
                    MainGame.P1_TANK.direction = 'L'
                    # change the position of tank
                    MainGame.P1_TANK.stop = False
                    #MainGame.P1_TANK.move()
                elif event.key == pygame.K_RIGHT:
                    print("move towards right")
                    MainGame.P1_TANK.direction = 'R'
                    MainGame.P1_TANK.stop = False
                    #MainGame.P1_TANK.move()
                elif event.key == pygame.K_UP:
                    print("move towards up")
                    MainGame.P1_TANK.direction = 'U'
                    MainGame.P1_TANK.stop = False
                    #MainGame.P1_TANK.move()
                elif event.key == pygame.K_DOWN:
                    print("move towards Down")
                    MainGame.P1_TANK.direction = 'D'
                    MainGame.P1_TANK.stop = False
                    #MainGame.P1_TANK.move()
                elif  event.key == pygame.K_SPACE:
                    print("biu biu biu~~~")
            if event.type == pygame.KEYUP:
                MainGame.P1_TANK.stop = True
    # wirte some word on surface
    def writeText(self,content):
        # initialize the font module
        pygame.font.init()
        # create font object,
        # 'consolas' is the type of font
        # 16 is the size of the font
        font = pygame.font.SysFont('consolas',16)
        # print(font_list)
        # rendet the content
        text_sf = font.render(content,True,COLOR_RED)
        # return the content
        return text_sf
    def gameOver(self):
        exit()

# inherit class sprite
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Tank(BaseItem):
    # use left and top to set position
    def __init__(self,left,top):
        # the picture of tank
        self.images = {
            'U':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankU.gif'),
            'D':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankD.gif'),
            'L':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankL.gif'),
            'R':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankR.gif')
        }
        # initialize the origin tank direction
        self.direction = 'U'
        self.image = self.images[self.direction]
        # the region of tank
        self.rect = self.image.get_rect()
        self.rect.left =left
        self.rect.top = top
        # the velocity of tank
        self.speed = 5
        # add stop variable to contorl whether the tank should move or not
        self.stop = True

    def display_tank(self):
        # set the tank image
        self.image = self.images[self.direction]
        # add tank to the window
        MainGame.window.blit(self.image,self.rect)
    #v1.5新增坦克移动方法
    def move(self):
        #change the coordinate of the tank
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT-MainGame.P1_TANK.rect.height:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH-MainGame.P1_TANK.rect.width:
                self.rect.left += self.speed
class Bullet(BaseItem):
    pass

class MyTank(Tank):
    pass

class EnermyTank(Tank):
    def __init__(self,left,top,speed):
        # picture
        self.images = {
            'U': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1U.gif'),
            'D': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1D.gif'),
            'L': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1L.gif'),
            'R': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1R.gif')
        }
        # initial direction
        self.direction = self.randomDirection()
        self.image = self.images[self.direction]

        # the region of tank
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        # velocity of tank
        self.speed = speed

        # add stop variable to contorl whether the tank should move or not
        self.stop = True

    def randomDirection(self):
        num = random.randint(1,4)
        if num == 1:
            self.direction = 'U'
        elif num == 2:
            self.direction = 'D'
        elif num == 3:
            self.direction = 'L'
        elif num == 4:
            self.direction = 'R'
        return self.direction
    def displayEnermyTank(self):
        # 可直接使用父类
        # super().display_tank()

        # reset image
        self.image = self.images[self.direction]
        # add enermy tank to the window
        MainGame.window.blit(self.image,self.rect)

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''
