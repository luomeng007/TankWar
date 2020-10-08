#-*-coding:utf-8-*-
import pygame,time

_display = pygame.display
COLOR_RED = pygame.Color(255,0,0)
# we could change the version here
version = 'v1.5'

class MainGame():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    window = None
    P1_TANK = None

    def startGame(self):
        _display.init()
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        # set the title of the game window
        _display.set_caption('坦克大战'+version)
        MainGame.P1_TANK = Tank(300,200)
        while True:
            MainGame.window.fill(pygame.Color(0,0,0))
            self.getEvent()
            MainGame.window.blit(self.writeText('remain tanks %d' %5),(5,5))
            MainGame.P1_TANK.display_tank()
            if not MainGame.P1_TANK.stop:
                MainGame.P1_TANK.move()
            _display.update()

            # add the updating time
            time.sleep(0.0025)

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
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

    def writeText(self,content):
        pygame.font.init()
        font = pygame.font.SysFont('consolas',16)
        text_sf = font.render(content,True,COLOR_RED)
        return text_sf

    def gameOver(self):
        exit()

class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Tank(BaseItem):
    def __init__(self,left,top):
        self.images = {
            'U':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankU.gif'),
            'D':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankD.gif'),
            'L':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankL.gif'),
            'R':pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\p1tankR.gif')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]

        self.rect = self.image.get_rect()
        self.rect.left =left
        self.rect.top = top

        self.speed = 5

        self.stop = True

    def display_tank(self):
        self.image = self.images[self.direction]
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

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''