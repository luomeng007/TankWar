#-*-coding:utf-8-*-
import pygame,time,random

_display = pygame.display
COLOR_RED = pygame.Color(255,0,0)
version = 'v1.13'

class MainGame():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    window = None
    P1_TANK = None

    enermy_tank_list = []
    enermy_tank_count = 5

    # v1.10新增敌方坦克子弹存储列表
    enermy_bullet_list = []

    bullet_list = []

    # v1.12存放爆炸效果的列表
    explode_list = []

    def startGame(self):
        pygame.display.init()

        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])

        pygame.display.set_caption('坦克大战'+version)

        MainGame.P1_TANK = Tank(300,200)

        self.creatEnermyTank()

        while True:
            MainGame.window.fill(pygame.Color(0,0,0))

            self.getEvent()

            MainGame.window.blit(self.writeText('remain tanks {}'.format(len(MainGame.enermy_tank_list))),(5,5))

            # v1.11调用展示我方坦克的方法
            self.displayP1Tank()

            # v1.11调用展示敌方坦克的方法
            self.displayEnermyTank()

            # v1.11调用展示我方子弹的方法
            self.displayP1TankBullet()

            # v1.11调用展示敌方子弹的方法
            self.displayEnermyTankBullet()

            # v1.12调用爆炸效果方法
            self.displayTankExplode()

            _display.update()

            time.sleep(0.015)

    def creatEnermyTank(self):
        for i in range(MainGame.enermy_tank_count):
            random_left = random.randint(1,8)

            random_speed = random.randint(1,2)

            enermy_tank = EnermyTank(random_left * 100,150,random_speed)

            MainGame.enermy_tank_list.append(enermy_tank)

    # v1.11 优化我方坦克展示
    def displayP1Tank(self):
        # v1.13 修改我方坦克展示逻辑
        # 下面的话为判断对象存在和坦克是否存活
        if MainGame.P1_TANK and MainGame.P1_TANK.live:
            MainGame.P1_TANK.displayTank()
            if not MainGame.P1_TANK.stop:
                MainGame.P1_TANK.move()
        else:
            # del 表示删除
            del MainGame.P1_TANK
            MainGame.P1_TANK = None

    # v1.11 优化敌方坦克展示
    def displayEnermyTank(self):
        for eTank in MainGame.enermy_tank_list:
            eTank.displayEnermyTank()
            eTank.randomMove()

            if eTank.live:
                eTank.displayEnermyTank()
            else:
                MainGame.enermy_tank_list.remove(eTank)

            # v1.10 敌方坦克射击方法
            eBullet = eTank.randomFire()
            # 在random fire()返回值为None，只有不为None时，再将子弹存储起来
            if eBullet:
                MainGame.enermy_bullet_list.append(eBullet)

    # v1.11 优化我方子弹展示
    def displayP1TankBullet(self):
        for bullet in MainGame.bullet_list:
            bullet.bulletMove()
            if bullet.live:
                bullet.displayBullet()
                # v1.11 调用子弹碰撞方法
                bullet.attackEnermyTank()

            else:
                MainGame.bullet_list.remove(bullet)

    # v1.11 优化敌方子弹展示
    def displayEnermyTankBullet(self):
        # v1.10新增敌方坦克的渲染
        for eBullet in MainGame.enermy_bullet_list:
            eBullet.bulletMove()
            if eBullet.live:
                eBullet.displayBullet()
                # v1.13 调用敌方子弹与我方坦克的碰撞
                eBullet.attackPlayerTank()
            else:
                MainGame.enermy_bullet_list.remove(eBullet)

    # v1.12 展示爆炸效果的方法
    def displayTankExplode(self):
        for explode in MainGame.explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explode_list.remove(explode)

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                print("quit the game")
                self.gameOver()
            if event.type == pygame.KEYDOWN:
                # # v1.13 优化坦克控制，增加前提条件，坦克得活着
                if MainGame.P1_TANK and MainGame.P1_TANK.live:
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
                        if len(MainGame.bullet_list) < 3:
                            bullet = MainGame.P1_TANK.fire()
                            # v1.10优化射击方案
                            MainGame.bullet_list.append(bullet)
                if event.key == pygame.K_1 and not MainGame.P1_TANK:
                    print('我胡汉三又回来了！')
                    # 设定坦克再一次的出生地
                    MainGame.P1_TANK = Tank(400,300)
            if event.type == pygame.KEYUP:
                # v1.13 新增判断处理，
                if event.key != pygame.K_SPACE and MainGame.P1_TANK and MainGame.P1_TANK.live:
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

        # v1.11新增坦克存活属性
        self.live = True

    def displayTank(self):
        self.image = self.images[self.direction]

        MainGame.window.blit(self.image,self.rect)

    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT-self.rect.height:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH-self.rect.width:
                self.rect.left += self.speed

    def fire(self):
        bullet = Bullet(self)

        # MainGame.bullet_list.append(bullet)
        return bullet

class EnermyTank(Tank):
    def __init__(self,left,top,speed):
        # picture
        self.images = {
            'U': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1U.gif'),
            'D': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1D.gif'),
            'L': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1L.gif'),
            'R': pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\enemy1R.gif')
        }
        self.direction = self.randomDirection()
        self.image = self.images[self.direction]

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.speed = speed

        self.stop = True

        self.step = 30

        # v1.11新增坦克存活属性
        self.live = True

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

    # v1.10新增随机射击方法
    def randomFire(self):
        num = random.randint(1,100)
        if num == 1:
            eBullet = self.fire()
            # 得到一个子弹
            return eBullet

    def displayEnermyTank(self):

        self.image = self.images[self.direction]

        MainGame.window.blit(self.image,self.rect)

class Bullet(BaseItem):
    def __init__(self,tank):
        self.image = pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\Bullet.gif')
        self.direction = tank.direction

        self.speed = 5 * 1.5

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

        self.live = True

    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
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

    # v1.11新增子弹与坦克的碰撞方法
    def attackEnermyTank(self):
        for eTank in MainGame.enermy_tank_list:
            result = pygame.sprite.collide_rect(eTank,self)
            if result:
                self.live = False
                eTank.live = False
                # v1.12打中产生爆炸效果，装进爆炸列表中
                explode = Explode(eTank.rect)
                MainGame.explode_list.append(explode)

    #v 1.13新增地方子弹与我方坦克的碰撞
    def attackPlayerTank(self):
        # 遍历敌方子弹
        for eBullet in MainGame.enermy_bullet_list:
            if MainGame.P1_TANK and MainGame.P1_TANK.live:
                result = pygame.sprite.collide_rect(eBullet,MainGame.P1_TANK)
                if result:
                    # 创建一个爆炸，加入爆炸效果列表
                    explode = Explode(MainGame.P1_TANK.rect)
                    MainGame.explode_list.append(explode)
                    # change the nenermy bullet state and player tank state
                    eBullet.live = False
                    MainGame.P1_TANK.live = False

            else:
                break

    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)

class Explode(BaseItem):
    #爆炸效果其实就是多张不同大小的图片的连续显示
    def __init__(self,rect):
        self.images =[
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast0.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast1.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast2.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast3.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast4.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast5.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast6.gif'),
            pygame.image.load(r'D:\python\pythonProgram\tankWar\tank\img\blast7.gif')
        ]
        self.rect = rect
        self.image = self.images[0]
        # 爆炸完成要消失,展示到最后一个状态时删除
        self.live = True
        # 记录当前图片的索引
        self.step = 0

# v1.12新增爆炸效果类
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image,self.rect)
            self.step += 1
        else:
            self.live = False
            self.step = 0

if __name__ == "__main__":
    game = MainGame()
    game.startGame()

'''
Judgement: perfect run!
'''

