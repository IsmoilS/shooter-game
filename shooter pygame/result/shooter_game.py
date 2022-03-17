from distutils.util import change_root
from time import sleep
from turtle import Turtle, update
import pygame
from random import randint

#фоновая музыка
pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound('fire.ogg')

animcount = 0



#шрифты и надписи
pygame.font.init()
font2 = pygame.font.SysFont('Arial', 36)
global img_hero
global pw
pw = 0


font1 = pygame.font.SysFont('Arial',150)
los = font1.render("YOU LOSE", True, (180,0,0))

#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = "bullet.png"

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
live = 5
liv = 5

#класс-родитель для других спрайтов
class GameSprite(pygame.sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       pygame.sprite.Sprite.__init__(self)

       #каждый спрайт должен хранить свойство image - изображение
       self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
       self.images = []
       self.img = 0
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

mx = 80

img_b_fire = "fire_bullet.png"

#класс главного игрока
class Player(GameSprite):
   global mx
   mx = 100
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       global pw
       keys = pygame.key.get_pressed()
       if keys[pygame.K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[pygame.K_d] and self.rect.x < win_width - mx:
           self.rect.x += self.speed
   def change(self):
           global bullet1,bullet2
           bullet1 = Bullet(img_b_fire, self.rect.left, self.rect.top, 20,30,-30)
           bullet2 = Bullet(img_b_fire, self.rect.right, self.rect.top, 20,30,-30)
           global bullet
           bullet = Bullet(img_b_fire, self.rect.centerx, self.rect.top, 20,30,-30)
           bullets.add(bullet)
           bullets.add(bullet1)
           bullets.add(bullet2)
           
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       global bullet
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-30)
       bullets.add(bullet)

mv = 1

class Dragon(GameSprite):
    def update(self):
        global mv 
        if mv > 0:
            self.sprites = []
            self.sprites.append(pygame.image.load("dragon_right1.png"))
            self.sprites.append(pygame.image.load("dragon_right2.png"))
            self.sprites.append(pygame.image.load("dragon_right3.png"))
        if mv < 0:
            self.sprites = []
            self.sprites.append(pygame.image.load("dragon_left1.png"))
            self.sprites.append(pygame.image.load("dragon_left2.png"))
            self.sprites.append(pygame.image.load("dragon_left3.png"))
        self.image = self.sprites[int(self.img)//2]
        self.img += 1
        if self.img >= len(self.sprites):
            self.img = 0
        self.rect.x += self.speed*mv
        if self.rect.x <= -250:
           mv *= -1
        if self.rect.x >= win_width-400:
           mv *= -1 


#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
   
   
   def dell(self):
       self.kill() 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed*1.5

        if self.rect.y < 0:
            self.kill()
        

class Heart(GameSprite):
    def update(self):
        self.kill()


#Создаём окошко
win_width = 1540
win_height = 790
pygame.display.set_caption("Shooter")
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))

#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 50)

monsters = pygame.sprite.Group()
for i in range(1, 11):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3, 10))
   monsters.add(monster)

bulletsl = pygame.sprite.Group()
bullets = pygame.sprite.Group()

walk = False

clock = pygame.time.Clock()
FPS = 40

x = 5
hearts = pygame.sprite.Group()

for i in range(live):
    heart = Heart("heart-org.png", x, win_height-100,50,50,0)
    x+=50
    hearts.add(heart)

def chg():
    global ship
    ship = Player("ship.png", ship.rect.x, ship.rect.y, 80, 100,100)


'''class Explosion(pygame.sprite.Sprite):
    def __init__(self,exp_x,exp_y):
        super().__init__()

        self.img_list = []
        self.length = 7
        for i in range(7):
            self.img_list.append(pygame.image.load(f'exp{i+1}.png'))
        
        self.counter = 0
        
    def update(self):
        self.counter+=1
        if self.counter >= 6:
            self.counter = 0
    
    def dell(self):
        self.kill()
'''
    

class Explosion(GameSprite):
    def update(self):
        for i in range(7):
            self.image.append(f'exp{i+1}.png')
        self.image = self.sprites[int(self.img)//2]
        self.img += 1
        if self.img >= len(self.sprites):
            self.img = 0


lvl = False

dragon = Dragon("dragon_front2.png",win_width/2,0,300,300,20)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run: 
   #событие нажатия на кнопку “Закрыть”
   for e in pygame.event.get():
       if e.type == pygame.QUIT:
           run = False
       
       if e.type == pygame.KEYDOWN:
           if e.key == pygame.K_e and score >= 20: 
               chg()
               lvl = True
               
       elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 :
           fire_sound.play()
           ship.fire()
       if lvl == True and e.type == pygame.MOUSEBUTTONDOWN and e.button :
           ship.change()


           

   hits = pygame.sprite.groupcollide(
            monsters,bullets,True,True
        )

   cols = pygame.sprite.spritecollide(
            ship,monsters, True,False

        )

   

   for hit in hits:
       score +=1
       monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3, 8))
       monsters.add(monster)

   for col in cols:
       live -= 1
       hearts.update()
       x = 5
       for i in range(live):
        heart = Heart("heart-org.png", x, win_height-100,50,50,0)
        x+=50
        hearts.add(heart)



   if not finish:
       #обновляем фон   
       window.blit(background,(0,0))

       
       if(live <= 0):
            finish = True
            window.blit(los,(550,350)) 

       #пишем текст на экране

       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))

       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       #производим движения спрайтов
       ship.update()
       #dragon.update() 
       monsters.update()
       bullets.update()

       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       #dragon.reset()
       monsters.draw(window)
       bullets.draw(window)  
       hearts.draw(window) 
    
       pygame.display.update() 
   #цикл срабатывает каждую 0.05 секунд
   pygame.time.delay(40)

