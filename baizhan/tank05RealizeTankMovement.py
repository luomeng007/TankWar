#-*-coding:utf-8-*-
import pygame

_display = pygame.display
COLOR_RED = pygame.Color(255,0,0)
version = 'v1.4'

class MainGame():
    __SCREEN_WIDTH = 600
    __SCREEN_HEIGHT = 400
    window = None
    P1_TANK = None
    def startGame(self):
        _display.init()

        MainGame.window = _display.set_mode([MainGame.__SCREEN_WIDTH,MainGame.__SCREEN_HEIGHT])

        # set the title of the game window
        _display.set_caption('坦克大战'+version)

        MainGame.P1_TANK = Tank(300,200)

        while True:
            MainGame.window.fill(pygame.Color(0,0,0))

            self.getEvent()

            MainGame.window.blit(self.writeText('remain tanks %d' %5),(5,5))

            MainGame.P1_TANK.display_tank()

            _display.update()
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
                    if MainGame.P1_TANK.rect.left > 0:    #防止坦克走出边界
                        MainGame.P1_TANK.rect.left -= MainGame.P1_TANK.speed
                elif event.key == pygame.K_RIGHT:
                    print("move towards right")
                    MainGame.P1_TANK.direction = 'R'
                    if MainGame.P1_TANK.rect.left < (MainGame.__SCREEN_WIDTH-MainGame.P1_TANK.rect.height):
                        MainGame.P1_TANK.rect.left += MainGame.P1_TANK.speed
                elif event.key == pygame.K_UP:
                    print("move towards up")
                    MainGame.P1_TANK.direction = 'U'
                    if MainGame.P1_TANK.rect.top > 0:
                        MainGame.P1_TANK.rect.top -= MainGame.P1_TANK.speed
                elif event.key == pygame.K_DOWN:
                    print("move towards Down")
                    MainGame.P1_TANK.direction = 'D'
                    if MainGame.P1_TANK.rect.top < (MainGame.__SCREEN_HEIGHT-MainGame.P1_TANK.rect.height):
                        MainGame.P1_TANK.rect.top += MainGame.P1_TANK.speed
                elif  event.key == pygame.K_SPACE:
                    print("biu biu biu~~~")

    def writeText(self,content):
        pygame.font.init()

        font = pygame.font.SysFont('consolas',16)

        text_sf = font.render(content,True,COLOR_RED)

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
    def display_tank(self):
        self.image = self.images[self.direction]

        MainGame.window.blit(self.image,self.rect)

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''