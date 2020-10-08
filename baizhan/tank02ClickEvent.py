#-*-coding:utf-8-*-
import pygame

_display = pygame.display

class MainGame():
    __SCREEN_WIDTH = 600
    __SCREEN_HEIGHT = 400
    __window = None

    def startGame(self):
        _display.init()
        MainGame.__window = _display.set_mode([MainGame.__SCREEN_WIDTH,MainGame.__SCREEN_HEIGHT])
        _display.set_caption('坦克大战v1.1')

        while True:
            MainGame.__window.fill(pygame.Color(0,0,0))

            # call getEvent function
            self.getEvent()

            _display.update()

    def getEvent(self):
        eventList = pygame.event.get()

        for event in eventList:
            # use type character to judge which event
            if event.type == pygame.QUIT:
                print("quit the game")
                self.gameOver()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("move towards left")
                elif event.key == pygame.K_RIGHT:
                    print("move towards right")
                elif event.key == pygame.K_UP:
                        print("move towards up")
                elif event.key == pygame.K_DOWN:
                    print("move towards Down")
                elif  event.key == pygame.K_SPACE:
                    print("biu biu biu~~~")

    def gameOver(self):
        exit()

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''