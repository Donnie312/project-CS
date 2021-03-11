import pygame
import random
import os
import math

Width = 800
Height = 600
FPS = 30
ground = Height - 30
slow = 3
fast = 8

player_acc = 0.9
player_friction = -0.12
player_grav = 0.9
vec = pygame.math.Vector2



white = (255, 255, 255)
black = (0, 0 ,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()     
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.direction = random.randit(0,1)
        self.vel.x = random.randit(2,6)
        if self.direction == 0:
          self.pos.x = 0
          self.pos.y = 235
        if self.direction == 1:
          self.pos.x = 700
          self.pos.y = 235



font_name = pygame.font.match_font('arial')
def draw_text (surf, text, size, x, y):
  font= pygame.font.Font(font_name, size)
  text_surface = font.render(text, True, blue)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surf.blit(text_surface, text_rect)

game_folder = os.path.dirname (__file__)
snd_folder = os.path.join(game_folder, "snd")
img_folder = os.path.join(game_folder, "img")

class Player (pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(os.path.join(img_folder,"tank.jpeg")).convert()
    self.image.set_colorkey(black)
    self.image=pygame.transform.scale(self.image,(100,75))
    self.rect = self.image.get_rect()
    self.rect.center = (Width / 2, Height / 2)
    self.y_speed = 5
    self.shield = 100
    self.shoot_delay = 4200
    self.last_shot = pygame.time.get_ticks()

    self.pos = vec(10, ground - 60)
    self.vel = vec(0, 0)
    self.acc = vec (0, 0)


  def shoot (self, mouse_x, mouse_y):
    now = pygame.time.get_ticks()
    if now - self.last_shot > self.shoot_delay:
      self.last_shot = now

      bullet = Bullet(self.rect.right,
                    self.rect.centery,
                    mouse_x,
                    mouse_y)
      all_sprites.add(bullet)
      bullets.add(bullet)
    
      
  def update(self):
    self.acc = vec(0, player_grav)

    keystate = pygame.key.get_pressed()

    if keystate[pygame.K_RIGHT]:
      self.acc.x += player_acc
    if keystate[pygame.K_LEFT]:
      self.acc.x += -player_acc
    if keystate[pygame.K_UP]:
      self.rect.y += -5
    if keystate[pygame.K_DOWN]:  
      self.rect.y += 5
    if self.vel.y == 0 and keystate[pygame.K_SPACE]:
      self.vel.y = -20
  
      
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0] == 1:
      pos = pygame.mouse.get_pos()
      mouse_x = pos[0]
      mouse_y = pos[1]

      self.shoot(mouse_x, mouse_y)

    self.acc.x += self.vel.x * player_friction

    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    if self.pos.x > Width:
        self.pos.x = 0
    if self.pos.x < 0:
        self.pos.x = Width



    if self.pos.y > ground:
        self.pos.y = ground + 1
        self.vel.y = 0
    hits = pygame.sprite.spritecollide(self, platforms, False)
    if hits:
      if self.rect.top > hits[0].rect.top:
        self.pos.y = hits[0].rect.bottom + 25 + 1
        self.vel.y = 0

      else:
        self.pos.y = hits[0].rect.top + 1
        self.vel.y = 0
    self.rect.midbottom = self.pos

class Platform (pygame.sprite.Sprite):
  def __init__ (self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(os.path.join(img_folder,"enemy.png")).convert()
    self.image.set_colorkey(black)
    self.image=pygame.transform.scale(self.image,(90,55))
    self.rect = self.image.get_rect()
    self.rect.center = (Width / 2, ground -22.5)
    self.y_speed = 5
  def update(self):
      self.rect.x += -5
      if self.rect.right <0:
          self.rect.left = Width


def show_start_screen():

  screen.fill(black)
  draw_text(screen, "Hot Tracks", 64, Width / 2, Height / 4)
  draw_text(screen, "press any key to begin",22, Width/ 2, Height / 2)
  pygame.display.flip()

  waiting= True
  while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             pygame.quit()
            if event.type == pygame.KEYUP:
             print ("key pressed to start game")
             waiting = False
            
               
 
def show_end_screen():

  screen.fill(red)
  draw_text(screen, "GAME OVER", 62, Width / 2, Height / 4)
  draw_text(screen, "Play again?", 22, Width / 2, Height/ 2)

  pygame.display.flip()

  waiting= True
  while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             pygame.quit()
            if event.type == pygame.KEYUP:
              if event.key == pygame.K_r:
                print ("key pressed to start game")
                waiting = False
            






            
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(os.path.join(snd_folder, "engine.wav"))
pygame.mixer.music.set_volume(0.4)
                                     
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("stryker")

clock = pygame.time.Clock()
pygame.mixer.music.play(loops = -1)

shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "105.wav"))

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
platform = Platform()
platforms = pygame.sprite.Group()
platforms.add(platform)
all_sprites.add(player)
all_sprites.add(platform)




bkgr_image = pygame.image.load(os.path.join(img_folder ,"Background.jpeg")).convert()
background = pygame.transform.scale(bkgr_image, (Width ,Height))
background_rect = background.get_rect()




class Bullet(pygame.sprite.Sprite):
  def __init__(self, start_x, start_y, dest_x, dest_y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((50,10))
    self.image.fill(red)
    self.image.set_colorkey(black)

    self.rect = self.image.get_rect()
    self.rect.left = start_x
    self.rect.bottom = start_y

        #MAKE STARTING POINT MORE ACCURATE
    self.floating_point_x = start_x
    self.floating_point_y = start_y

        #DIFFERENCE BTW START AND DEST PTS
    x_diff = dest_x - start_x
    y_diff = dest_y - start_y
    angle = math.atan2(y_diff, x_diff)

        #APPLY VELOCITY
    self.speedx = 20
    self.change_x = math.cos(angle) * self.speedx
    self.change_y = math.sin(angle) * self.speedx
  def update(self):
      # The floating point x and y hold our more accurate location.
      self.floating_point_y += self.change_y
      self.floating_point_x += self.change_x

      # The rect.x and rect.y are converted to integers.
      self.rect.y = int(self.floating_point_y)
      self.rect.x = int(self.floating_point_x)


      #DELETE LASER ONCE OFF SCREEN
      # If the bullet flies of the screen, get rid of it.
      if self.rect.x < 0 or self.rect.x > Width or self.rect.y < 0 or self.rect.y > Height:
          self.kill()
end = False
start = True
running = True
while running:

  if start:
    show_start_screen()
    start = False

  if end:
    show_end_screen()
    end = False
  
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_q:
        end = True

      
  all_sprites.update()
  screen.fill(blue)
  all_sprites.draw(screen)

  screen.blit(background, background_rect)
  all_sprites.draw(screen)


  pygame.display.flip()

pygame.quit()
