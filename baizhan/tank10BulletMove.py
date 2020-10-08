#-*-coding:utf-8-*-
import pygame,time,random

_display = pygame.display
COLOR_RED = pygame.Color(255,0,0)
version = 'v1.9'

class MainGame():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    window = None
    P1_TANK = None

    enermy_tank_list = []
    enermy_tank_count = 5

    # v1.8新增我方子弹列表，方便后期处理
    bullet_list = []

    def startGame(self):
        pygame.display.init()

        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])

        pygame.display.set_caption('坦克大战'+version)

        MainGame.P1_TANK = Tank(300,200)

        self.creatEnermyTank()

        while True:
            MainGame.window.fill(pygame.Color(0,0,0))

            self.getEvent()

            MainGame.window.blit(self.writeText('remain tanks %d' %5),(5,5))

            MainGame.P1_TANK.displayTank()

            for eTank in MainGame.enermy_tank_list:
                eTank.displayEnermyTank()
                eTank.randomMove()

            if not MainGame.P1_TANK.stop:
                MainGame.P1_TANK.move()

            # v1.8新增子弹再屏幕上完成绘制
            for bullet in MainGame.bullet_list:
                # v1.9新增调用子弹移动,仅展示存活的子弹
                bullet.bulletMove()
                if bullet.live:
                    bullet.displayBullet()
                else:
                    # 删除子弹，解除内存占用
                    MainGame.bullet_list.remove(bullet)

            _display.update()

            time.sleep(0.015)

    def creatEnermyTank(self):
        for i in range(MainGame.enermy_tank_count):
            random_left = random.randint(1,8)

            random_speed = random.randint(1,2)

            enermy_tank = EnermyTank(random_left * 100,150,random_speed)

            MainGame.enermy_tank_list.append(enermy_tank)

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

                elif event.key == pygame.K_RIGHT:
                    print("move towards right")
                    MainGame.P1_TANK.direction = 'R'
                    MainGame.P1_TANK.stop = False

                elif event.key == pygame.K_UP:
                    print("move towards up")
                    MainGame.P1_TANK.direction = 'U'
                    MainGame.P1_TANK.stop = False

                elif event.key == pygame.K_DOWN:
                    print("move towards Down")
                    MainGame.P1_TANK.direction = 'D'
                    MainGame.P1_TANK.stop = False

                elif  event.key == pygame.K_SPACE  :
                    print("biu biu biu~~~{}".format(len(MainGame.bullet_list)))
                    # v1.8 我方坦克发射子弹
                    if len(MainGame.bullet_list) < 3:
                        MainGame.P1_TANK.fire()

            if event.type == pygame.KEYUP:
                # v1.9优化弹出的不是空格键再停止
                if event.key != pygame.K_SPACE:
                    MainGame.P1_TANK.stop = True

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
            'U':pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\p1tankU.gif'),
            'D':pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\p1tankD.gif'),
            'L':pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\p1tankL.gif'),
            'R':pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\p1tankR.gif')
        }

        self.direction = 'U'
        self.image = self.images[self.direction]

        self.rect = self.image.get_rect()
        self.rect.left =left
        self.rect.top = top

        self.speed = 5

        self.stop = True

    def displayTank(self):
        self.image = self.images[self.direction]

        MainGame.window.blit(self.image,self.rect)

    def move(self):
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

    # v1.6 fire of tank
    def fire(self):
        # creat bullet target
        bullet = Bullet(self)
        # add bullet into list
        MainGame.bullet_list.append(bullet)


class EnermyTank(Tank):
    def __init__(self,left,top,speed):
        # picture
        self.images = {
            'U': pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\enemy1U.gif'),
            'D': pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\enemy1D.gif'),
            'L': pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\enemy1L.gif'),
            'R': pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\enemy1R.gif')
        }
        self.direction = self.randomDirection()
        self.image = self.images[self.direction]

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.speed = speed

        self.stop = True

        self.step = 30

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

    def randomMove(self):
        if self.step == 0:
            self.randomDirection()
            self.step = 30
        else:
            self.move()
            self.step -= 1

    def displayEnermyTank(self):

        self.image = self.images[self.direction]

        MainGame.window.blit(self.image,self.rect)

class Bullet(BaseItem):
    def __init__(self,tank):
        self.image = pygame.image.load(r'D:\python\pythonProgram\tankWar\tankMaterials\img\Bullet.gif')
        self.direction = tank.direction

        self.speed = MainGame.P1_TANK.speed * 1.5

        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top
            self.rect.top = tank.rect.top - self.rect.height
        # the situation tank towards down
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.width/2 - self.rect.width/2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

        # v1.9为子弹添加一个状态值
        self.live = True

    # v1.9新增子弹的移动
    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            # 为子弹添加一个状态值，判断其打中墙或者超出边界，或者打中敌方坦克
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False

    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''

