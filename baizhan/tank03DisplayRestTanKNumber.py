#-*-coding:utf-8-*-
import pygame

_display = pygame.display
# define red in advance, then we could use COlOR_RED represent RGB red
COLOR_RED = pygame.Color(255,0,0)

class MainGame():
    __SCREEN_WIDTH = 600
    __SCREEN_HEIGHT = 400
    window = None
    P1_TANK = None

    def startGame(self):
        _display.init()
        MainGame.window = _display.set_mode([MainGame.__SCREEN_WIDTH,MainGame.__SCREEN_HEIGHT])
        _display.set_caption('坦克大战v1.2')
        while True:
            MainGame.window.fill(pygame.Color(0,0,0))
            self.getEvent()

            # set the adding postion and write the text
            MainGame.window.blit(self.writeText('remain tanks %d' %5),(5,5))

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
                elif event.key == pygame.K_RIGHT:
                    print("move towards right")
                    MainGame.P1_TANK.direction = 'R'
                elif event.key == pygame.K_UP:
                    print("move towards up")
                    MainGame.P1_TANK.direction = 'U'
                elif event.key == pygame.K_DOWN:
                    print("move towards Down")
                    MainGame.P1_TANK.direction = 'D'
                elif  event.key == pygame.K_SPACE:
                    print("biu biu biu~~~")

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

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''