import pygame
import os
import random


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Bossfighters v0.1.2")
FPS = 40
clock = pygame.Clock()
characters_list = ['knight','archer','axe','druid','potion_zaku','emerald_zaku_young','emerald_zaku_old','combustighoul','velocighoul',
                   'diamond_zaku','chars','gouf','bobbins']
in_game_character_list = []


STAGE = 1
characters_attacks = {
    characters_list[0] :1,
    characters_list[1]:1,
    characters_list[2]:1,
    characters_list[3]:1,
    characters_list[4]:2,
    characters_list[5]:1,
    characters_list[6]:2,
    characters_list[7]:1,
    characters_list[8]:1,
    characters_list[9]:3,
    characters_list[10]:2,
    characters_list[11]:1,
    characters_list[12]:1,
}

characters_speed = {
    characters_list[0]:2,
    characters_list[1]:3,
    characters_list[2]:2.5,
    characters_list[3]:1.7,
    characters_list[4]:3.5,
    characters_list[5]:4,
    characters_list[6]:4.3,
    characters_list[7]:1.3,
    characters_list[8]:7,
    characters_list[9]:2.5,
    characters_list[10]:3.15,
    characters_list[11]:2.8,
    characters_list[12]:2.95
}

characters_health = {
    characters_list[0]:500,
    characters_list[1]:200,
    characters_list[2]:350,
    characters_list[3]:600,
    characters_list[4]:150,
    characters_list[5]:550,
    characters_list[6]:560,
    characters_list[7]:100,
    characters_list[8]:100,
    characters_list[9]:590,
    characters_list[10]:330,
    characters_list[11]:440,
    characters_list[12]:100
    
}
bosses_list = ['bot']
bosses_health = {
    bosses_list[0]:2000
}
bosses_speed = {
    bosses_list[0]:1.5
}
bosses_attacks = {
    bosses_list[0]:1
}
running = True
game_started = False
mouse_pos_x = 0
mouse_pos_y = 0

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, health, max_health):
        super().__init__()
        self.x, self.y = x, y
        self.health, self.max_health = health, max_health

    def draw(self, health):
        self.health = health # update the current health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0,0,0), (self.x - 2, self.y - 2, 104, 24)) # black border
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, 100, 20)) # red background
        green_width = int(100 * ratio)
        if green_width < 0:
            green_width = 0
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y, green_width, 20)) # green foreground

class Character(pygame.sprite.Sprite):
    def __init__(self,x,y,identity ,number):
        super().__init__()
        self.identity = identity
       
        self.number = number
        
        self.num_of_attacks = characters_attacks.get(identity)
        self.animation_types = ['idle','walk']
        self.action_index = 0
        self.frame_index = 0
        self.action = 1   #0 = idle, 1 = walk, 2 = attack, 3 = attack2
        self.x = x
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.speed = characters_speed.get(identity)
        self.health = characters_health.get(identity)
        self.y = y
        if self.num_of_attacks == 1:
            self.animation_types.extend(['attack1'])
        elif self.num_of_attacks == 2:
            self.animation_types.extend(['attack1','attack2'])
        self.animation_list = []
        for animation in self.animation_types:
            temp_list = []
            path = f"images/characters/{identity}/{animation}"
            for file in os.listdir(path):
                if file.lower().endswith('.png'):
                    image_path = os.path.join(path,file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image_resized = pygame.transform.scale(image,(image.get_width()*0.7,image.get_height()*0.7))
                    temp_list.append(image_resized)
                    
                    
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action_index][self.frame_index]
        self.frect = self.image.get_frect(center = (x,y))
        self.rect = self.frect
        
    
    def reload_identity(self,identity):
        self.num_of_attacks = characters_attacks.get(identity)
        self.animation_types = ['idle','walk']
        self.action_index = 0
        self.frame_index = 0
        if self.num_of_attacks == 1:
            self.animation_types.extend(['attack1'])
        elif self.num_of_attacks == 2:
            self.animation_types.extend(['attack1','attack2'])
        self.animation_list = []
        for animation in self.animation_types:
            temp_list = []
            path = f"images/characters/{identity}/{animation}"
            for file in os.listdir(path):
                if file.lower().endswith('.png'):
                    image_path = os.path.join(path,file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image_resized = pygame.transform.scale(image,(image.get_width()*0.7,image.get_height()*0.7))
                    temp_list.append(image_resized)
      
            self.animation_list.append(temp_list)
            self.action_index = 0
            self.frame_index = 0
            self.image = self.animation_list[self.action_index][self.frame_index]
            self.frect = self.image.get_frect(center = (self.x,self.y))
            self.rect = self.frect
            self.speed = characters_speed.get(identity)
            self.health = characters_health.get(identity)
            
        
    def draw(self):
        self.frect.center = self.rect.center
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.frect)   
    def move(self):
        dx = mouse_pos_x - self.rect.centerx
        dy = mouse_pos_y - self.rect.centery
        
        if abs(dx) > self.speed or abs(dy) > self.speed:  # only move if far enough away
            self.update_new_action(1)  # walk
            if dx > 0:
                self.rect.x += self.speed
                self.flip = False
            if dx < 0:
                self.rect.x -= self.speed
                self.flip = True
            if dy < 0 and self.rect.y >= 140:
                self.rect.y -= self.speed
            if dy > 0:
                self.rect.y += self.speed
        else:
            self.rect.centerx = mouse_pos_x  # snap to exact position
            self.rect.centery = mouse_pos_y
            self.update_new_action(0)  # idle
        
    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > 100:
            if len(self.animation_list[self.action]) > 1:
                
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            else:
                pass
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
    def update_new_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def update(self):
        self.update_animation()
        self.update_new_action(self.action)
       
        if self.health <= 0:
            self.kill()
    def change_character(self,event):
        if game_started == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.number == 1:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                if event.key == pygame.K_2:
                    if self.number == 2:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                if event.key == pygame.K_3:
                    if self.number == 3:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                if event.key == pygame.K_4:
                    if self.number == 4:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                if event.key == pygame.K_5:
                    if self.number == 5:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                elif event.key == pygame.K_r:
                    self.identity = random.choice(characters_list)
                    self.reload_identity(self.identity)                
        else:
            pass
        
        
            
            
        
class Boss(pygame.sprite.Sprite):
    def __init__(self,x,y,stage):
        super().__init__()
        self.identity = bosses_list[stage-1]
        self.animation_types = ['attack1','attack2','idle','walk']
        self.action_index = 0
        self.frame_index = 0
        self.action = 1   #0 = idle, 1 = walk, 2 = attack, 3 = attack2
        self.x = x
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.attack_time = pygame.time.get_ticks()
        self.speed = bosses_speed.get(self.identity)
        self.health = bosses_health.get(self.identity)
        
        self.animation_list = []
        for animation in self.animation_types:
            temp_list = []
            path = f"images/bosses/{self.identity}/{animation}"
            for file in os.listdir(path):
                if file.lower().endswith('.png'):
                    image_path = os.path.join(path,file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image_resized = pygame.transform.scale(image,(image.get_width()*0.7,image.get_height()*0.7))
                    temp_list.append(image_resized)
                    
                    
            self.animation_list.append(temp_list)
        print(self.animation_list)
        self.image = self.animation_list[self.action_index][self.frame_index]
        self.frect = self.image.get_frect(center = (x,y))
        self.rect = self.frect
        self.melee_attacking = False
        self.ranged_attacking = False
    def draw(self):
        if game_started == True:
            
            self.frect.center = self.rect.center
            screen.blit(pygame.transform.flip(self.image,self.flip,False),self.frect)
        else:
            pass
    def move(self):
        if self.melee_attacking == False and self.ranged_attacking == False:
            self.update_new_action(3)  # walk
            dx = mouse_pos_x - self.rect.centerx
            dy = mouse_pos_y - self.rect.centery
            
            if abs(dx) > self.speed or abs(dy) > self.speed:  # only move if far enough away
                  # walk
                if dx > 0:
                    self.rect.x += self.speed
                    self.flip = False
                if dx < 0:
                    self.rect.x -= self.speed
                    self.flip = True
                if dy < 0 and self.rect.y >= 140:
                    self.rect.y -= self.speed
                if dy > 0:
                    self.rect.y += self.speed
            else:
                self.rect.centerx = mouse_pos_x  # snap to exact position
                self.rect.centery = mouse_pos_y
                self.update_new_action(0)  # idle
        else:
            pass
            
            
    def melee_attack(self):
        
        self.update_new_action(0)  # attack1
        self.melee_attacking = True
        return self.melee_attacking
        
    def ranged_attack(self):
        
        self.update_new_action(1)  # attack2
        self.ranged_attacking = True
        return self.ranged_attacking
    def choose_attack(self):
        for c in in_game_character_list:
            distance = ((self.rect.centerx - c.rect.centerx) ** 2 + (self.rect.centery - c.rect.centery) ** 2) ** 0.5
            if distance < 200:
                 print('melee attack chosen')
                 return self.melee_attack()
              
            else:
          
                print('ranged attack chosen')
                return self.ranged_attack()
    def attack_timer(self):
        
        if pygame.time.get_ticks() - self.attack_time > random.uniform(900,1500):  # attack duration
               
                self.melee_attacking = False
                self.update_new_action(3)  # back to walk after attack
                self.update_time = pygame.time.get_ticks()
        if self.ranged_attacking == True:
            if pygame.time.get_ticks() - self.attack_time > random.uniform(1500,2500):  # attack duration
             
                self.ranged_attacking = False
                self.update_new_action(3)  # back to walk after attack
                
                self.update_time = pygame.time.get_ticks()
    def when_to_attack(self):
        if not self.melee_attacking and not self.ranged_attacking:
            
            if pygame.time.get_ticks() - self.attack_time > random.uniform(2000,5000):  # time between attacks
                self.choose_attack()
                print('attack chosen')
                self.attack_time = pygame.time.get_ticks()
    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > 100:
            if len(self.animation_list[self.action]) > 1:
                
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            else:
                pass
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
    def update_new_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def update(self):
        self.update_animation()
        self.update_new_action(self.action)
        
        if self.health <= 0:
            self.kill()
        
characters = pygame.sprite.Group()
bosses = pygame.sprite.Group()

for i in range(5):
    
    c = Character(150+(i*170),SCREEN_HEIGHT//2,characters_list[i],i+1)
    characters.add(c)
    in_game_character_list.append(c)#
 
# create persistent health bars for the 5 slots (not attached to Character)
health_bars = []
for idx, c in enumerate(in_game_character_list):
    x = (idx + 1) * 170 - 60
    hb = HealthBar(x, 90, c.health, characters_health.get(c.identity))
    health_bars.append(hb)

boss = Boss(random.uniform(0, SCREEN_WIDTH), random.uniform(500, SCREEN_HEIGHT - 100), STAGE)
bosses.add(boss)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_started == False:
            for character in characters:
                
                character.change_character(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game_started = True
            
    
    
    pygame.display.flip()
    
    
        
    
    
    
    
    
    if game_started == False:
        
        screen.fill((255,255,0))
    else:
        screen.fill((0,255,0))
        
    if game_started == True:
        pygame.draw.rect(screen,pygame.Color('cyan'),(0,0,SCREEN_WIDTH,130))
        # update and draw persistent health bars (do not attach to Character)
        for idx, hb in enumerate(health_bars):
            if idx < len(in_game_character_list):
                char = in_game_character_list[idx]
                hb.max_health = characters_health.get(char.identity)
                hb.draw(char.health)
            
    else:
        pass
    font = pygame.font.Font(None,36)
    small_font = pygame.font.Font(None,20)
    title = font.render('WELCOME TO BOSSFIGHTERS',False,pygame.Color('red'))
    instruction1 = font.render('CHOOSE YOUR CHARACTERS TO BUILD YOUR TEAM,\n  PRESS S TO START \n PRESS R FOR RANDOM TEAM',False,pygame.Color('blue'))
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos_x = mouse_pos[0]
    mouse_pos_y = mouse_pos[1]
    for c in characters:
        c.draw()
    for b in bosses:
        b.draw()
    
    if game_started == False:
        
        screen.blit(title,(SCREEN_WIDTH//2 - 200,100))
        screen.blit(instruction1,(SCREEN_WIDTH//2 - 200,200))   
        
        for c in in_game_character_list:
            
            screen.blit(small_font.render(f'character :{c.identity} \n press {in_game_character_list.index(c)+1} to change',False,pygame.Color('red')),c.rect.bottomleft)
            
        
    else:
        pass
    if game_started == True:
        characters.update()
        bosses.update()
        for c in characters:
            c.move()
        for b in bosses:
            b.move()
            b.when_to_attack()
            b.attack_timer()
    clock.tick(FPS)
    
pygame.quit()