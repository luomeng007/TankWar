#-*-coding:utf-8-*-
#import the library we will use in this project
import pygame

# regard pygame.display as _display
_display = pygame.display

class MainGame():
    # when we use __ before varibles, it means these varibles could not be changed
    # give two parameters as the size of our display window
    __SCREEN_WIDTH = 600
    __SCREEN_HEIGHT = 400

    #
    __window = None

    # start game function
    def startGame(self):
        # initialize the game window
        _display.init()

        # display the window
        MainGame.__window = _display.set_mode([MainGame.__SCREEN_WIDTH,MainGame.__SCREEN_HEIGHT])

        # set the title of the game window
        _display.set_caption('坦克大战v1.0')

        while True:
            # render background, RGB(0,0,0) represents black color
            MainGame.__window.fill(pygame.Color(0,0,0))

            # call getEvent function
            self.getEvent()

            # update the screen
            _display.update()

    def getEvent(self):
        # get all event
        eventList = pygame.event.get()

        for event in eventList:
            # use type character to judge which event
            if event.type == pygame.QUIT:
                print("quit the game")
                self.gameOver()

    # creat a quit method, when we click the cross button, the window closes
    def gameOver(self):
        exit()

if __name__ == "__main__":
    # creat a MainGame() class
    game = MainGame()
    # use the startGame function in class MainGame
    game.startGame()

'''
Judgement: perfect run!
'''