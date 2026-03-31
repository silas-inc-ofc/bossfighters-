import pygame
import os
import random
from collections import Counter

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Bossfighters v0.1.8")
FPS = 40
clock = pygame.Clock()
characters_list = ['knight','archer','axe','druid','potion_zaku','emerald_zaku_young','emerald_zaku_old','combustighoul','velocighoul',
                   'diamond_zaku','chars','gouf','bobbins','gogg','guardian']
in_game_character_list = []
turns =[characters_list[0],characters_list[1],characters_list[2],characters_list[3],characters_list[4]]
turn = turns[0]
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
    characters_list[13]:1,
    characters_list[14]:2,
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
    characters_list[12]:2.95,
    characters_list[13]:3.2,
    characters_list[14]:3.85,
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
    characters_list[12]:100,
    characters_list[13]:400,
    characters_list[14]:214,
    
    
    
}

characteres_attacks_stats = {
    characters_list[0]:['melee'],
    characters_list[1]:['non-melee'],
    characters_list[2]:['melee'],
    characters_list[3]:['melee'],
    characters_list[4]:['heal','non-melee'],
    characters_list[5]:['beam'],
    characters_list[6]:['beam','melee'],
    characters_list[7]:['melee'],
    characters_list[8]:['melee'],
    characters_list[9]:['beam','non-melee','melee'],
    characters_list[10]:['melee','melee'],
    characters_list[11]:['melee'],
    characters_list[12]:['heal'],
    characters_list[13]:['melee'],
    characters_list[14]:['melee','melee'],
    
    
    
}


characters_beam_damage = {
    characters_list[5]:5,
    characters_list[6]:3.5,
    characters_list[9]:4.5,
}

characters_projectile_delays = {
    characters_list[1]:600,
    characters_list[4]:100,
    characters_list[9]:300,
}
character_projectile_damage = {
    characters_list[1]:60,
    characters_list[4]:30,
    characters_list[9]:45
}
characters_damage = {
    characters_list[0]:(100,),
    characters_list[1]:(60,),
    characters_list[2]:(120,),
    characters_list[3]:(90,),
    characters_list[4]:(0,50),
    characters_list[5]:(10,),
    characters_list[6]:(20,100),
    characters_list[7]:(150,),
    characters_list[8]:(115,),
    characters_list[9]:(15,75,90),
    characters_list[10]:(110,67),
    characters_list[11]:(130,),
    characters_list[12]:(0,),
    characters_list[13]:(140,),
    characters_list[14]:(200,450),
}
characters_heal_stats = {
    
    characters_list[0]:[False],
    characters_list[1]:[False],
    characters_list[2]:[False],
    characters_list[3]:[False],
    characters_list[4]:['single',False],
    characters_list[5]:[False],
    characters_list[6]:[False,False],
    characters_list[7]:[False],
    characters_list[8]:[False],
    characters_list[9]:[False,False,False],
    characters_list[10]:[False,False],
    characters_list[11]:[False],
    characters_list[12]:['multi'],
    characters_list[13]:[False],
    characters_list[14]:[False,False],
    
}
characters_heal_amounts = {
    characters_list[4]:100,
    characters_list[12]:30,
    
    
    
}



bosses_list = ['bot']
bosses_projectile_attacks_directions = {
    bosses_list[0]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)]
}

bosses_projectiles_attacks = {
    bosses_list[0]:[0,1]
}
bosses_health = {
    bosses_list[0]:2000
}
bosses_speed = {
    bosses_list[0]:1
}
bosses_attacks = {
    bosses_list[0]:1
}
bosses_num_of_bullets = {
    bosses_list[0]:5
}
running = True
game_started = False
mouse_pos_x = 0
mouse_pos_y = 0
character_dict = {
    1:characters_list[0],
    2:characters_list[1],
    3:characters_list[2],
    4:characters_list[3],
    5:characters_list[4]
}

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, health, max_health,colour):
        super().__init__()
        self.x, self.y = x, y
        self.health, self.max_health = health, max_health
        self.colour = colour

    def draw(self, health):
        self.health = health # update the current health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0,0,0), (self.x - 2, self.y - 2, 104, 24)) # black border
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, 100, 20)) # red background
        green_width = int(100 * ratio)
        if green_width < 0:
            green_width = 0
        pygame.draw.rect(screen,self.colour, (self.x, self.y, green_width, 20)) # green foreground
        
 
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
        self.attack_type = 0
        if self.num_of_attacks == 1:
            self.animation_types.extend(['attack1'])
        elif self.num_of_attacks == 2:
            self.animation_types.extend(['attack1','attack2'])
        elif self.num_of_attacks == 3:
            self.animation_types.extend(['attack1','attack2','attack3'])
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
        self.attacking = False
        self.attack_duration = 0
        self.attack_duration_time = pygame.time.get_ticks()
        self.pending_projectiles = []
        self.last_projectile_time = 0
        self.projectile_delay = characters_projectile_delays.get(self.identity, 300)
    
    def reload_identity(self,identity):
        self.num_of_attacks = characters_attacks.get(identity)
        self.animation_types = ['idle','walk']
        self.action_index = 0
        self.frame_index = 0
        if self.num_of_attacks == 1:
            self.animation_types.extend(['attack1'])
        elif self.num_of_attacks == 2:
            self.animation_types.extend(['attack1','attack2'])
        elif self.num_of_attacks == 3:
            self.animation_types.extend(['attack1','attack2','attack3'])
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
            self.pending_projectiles = []
            self.last_projectile_time = 0
            self.projectile_delay = characters_projectile_delays.get(identity, 300)
            
    
    def draw(self):
        self.frect.center = self.rect.center
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.frect)   
    
    def attack(self,attack_no):
        # don't retrigger attack if already attacking
        if self.attacking:
            return False
        index = attack_no-1
        
        self.update_new_action(attack_no+1)
        self.attacking = True
        self.attack_type = characteres_attacks_stats.get(self.identity)[index]
        if self.attack_type == 'melee':
            if pygame.sprite.groupcollide(bosses,characters,False,False):
                for boss in pygame.sprite.groupcollide(bosses,characters,False,False):
                    boss.health -= characters_damage.get(self.identity)[attack_no-1]
        elif self.attack_type == 'non-melee':
            if self.identity == 'potion_zaku':
                projectile_dx = 7 
                projectile_dy = 0
                repetition = 10
                self.pending_projectiles = [(projectile_dx if not self.flip else -projectile_dx, projectile_dy, self.identity, index) for _ in range(repetition)]
                self.last_projectile_time = pygame.time.get_ticks()
            if self.identity == 'archer':
                projectile_dx = 4
                projectile_dy = 0
                repetition = 5
                self.pending_projectiles = [(projectile_dx if not self.flip else -projectile_dx, projectile_dy, self.identity, index) for _ in range(repetition)]
                self.last_projectile_time = pygame.time.get_ticks()
            if self.identity == 'diamond_zaku':
                projectile_dx = 9
                projectile_dy = 0
                repetition = 3
                self.pending_projectiles = [(projectile_dx if not self.flip else -projectile_dx, projectile_dy, self.identity, index) for _ in range(repetition)]
                self.last_projectile_time = pygame.time.get_ticks()
        elif self.attack_type == 'beam':
            beam = Player_beam(self.rect.x,self.rect.y,self.identity,self,self.flip)
            player_beams.add(beam)
            
        healthlist = []
        
        
            
   
        if characters_heal_stats.get(self.identity)[attack_no-1] == 'single':
            for c in in_game_character_list:
                healthlist.append(c.health/characters_health.get(c.identity))
            min_health = min(healthlist)
            
            
            for c in in_game_character_list:
                if c.health/characters_health.get(c.identity) == min_health and c.health < characters_health.get(c.identity)  :
                  
                    c.health += characters_heal_amounts.get(self.identity)
        elif characters_heal_stats.get(self.identity)[attack_no-1] == 'multi':
            for c in in_game_character_list:
                if c.health <= characters_health.get(c.identity):
                    
                    c.health += characters_heal_amounts.get(self.identity)
                else:
                    pass
                
            
        
            
            
            
                 
                
        self.attack_duration_time = pygame.time.get_ticks()
        self.attack_duration = 500  # milliseconds
        return True
    def duration_of_attack(self):
        if not self.attacking:
            return False
        now = pygame.time.get_ticks()
        elapsed = now - self.attack_duration_time
        if elapsed > self.attack_duration:
            self.attacking = False
            self.update_new_action(0)
        return self.attacking
            
    def move(self):
        if self.attacking == False:
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
        else:
            pass
        
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
        # check whether an ongoing attack should finish each frame
        self.duration_of_attack()
        if self.pending_projectiles:
            now = pygame.time.get_ticks()
            if now - self.last_projectile_time >= self.projectile_delay:
                dx, dy, identity, idx = self.pending_projectiles.pop(0)
                projectile = Player_Projectile(self.rect.centerx, self.rect.centery, dx, dy, identity, )
                player_projectiles.add(projectile)
                self.last_projectile_time = now
        self.update_new_action(self.action)
       
        if self.health <= 0:
            self.kill()
    def controls(self,event):
        if game_started == True:
            if event.type == pygame.KEYDOWN and turn == self.identity:
               
                #
                    
                        
                if event.key == pygame.K_a :
                    self.attack(1)
                if self.num_of_attacks == 2:
                    if event.key == pygame.K_s:
                        self.attack(2)
                if self.num_of_attacks == 3:
                    if event.key == pygame.K_s:
                        self.attack(2)
                    if event.key == pygame.K_d:
                        self.attack(3)
                  
    def change_character(self,event):
        if game_started == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.number == 1:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            character_dict.update({1:self.identity})
                            self.reload_identity(self.identity)
                            turns[0] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = characters_list[0]
                            character_dict.update({1:self.identity})
                            self.reload_identity(self.identity)
                            turns[0] = self.identity
                            print(turns)
                if event.key == pygame.K_2:
                    if self.number == 2:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({2:self.identity})
                            turns[1] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                            character_dict.update({2:self.identity})
                            turns[1] = self.identity
                            print(turns)
                if event.key == pygame.K_3:
                    if self.number == 3:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({3:self.identity})
                            turns[2] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                            character_dict.update({3:self.identity})
                            turns[2] = self.identity
                            print(turns)
                if event.key == pygame.K_4:
                    if self.number == 4:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({4:self.identity})
                            turns[3] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                            turns[3] = self.identity
                            character_dict.update({4:self.identity})
                            print(turns)
                if event.key == pygame.K_5:
                    if self.number == 5:
                        try:
                            self.identity = characters_list[characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({5:self.identity})
                            turns[4] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = characters_list[0]
                            self.reload_identity(self.identity)
                            character_dict.update({5:self.identity})
                            turns[4] = self.identity
                            print(turns)
                elif event.key == pygame.K_r:
                    self.identity = random.choice(characters_list)
                    self.reload_identity(self.identity)         
                    turns[self.number-1] = self.identity
                    print(turns)       
        else:
            pass
    def antirepeat(self,event):
        if game_started == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    character_dict.values()
                    repetitives = Counter(character_dict)
                    print(repetitives)
                    
                    
        
        
            

class Player_Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,dx,dy,character):
        super().__init__()
        self.character = character
        self.image = pygame.image.load(f'images/player_projectiles/{self.character}.png').convert_alpha()
        self.dx = dx
        self.dy = dy
        if self.dx < 0:
            self.image = pygame.transform.flip(self.image,True,False)
        else:
            pass
        self.frect = self.image.get_frect(center = (x,y))
        self.rect = self.frect
        
    def draw(self):
        self.frect.center = self.rect.center
        screen.blit(self.image,self.frect)
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
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
        self.shoot_time = pygame.time.get_ticks()
        self.attack_duration_time = pygame.time.get_ticks()
        self.speed = bosses_speed.get(self.identity)
        self.health = bosses_health.get(self.identity)
        self.attack_duration = 0
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
        self.attack_duration_time = pygame.time.get_ticks()
        self.attack_duration = random.uniform(900,1500)
        for c in pygame.sprite.groupcollide(characters, bosses, False, False):
            if c.health > 0:
                c.health -= 100 
        return self.melee_attacking
        
    def ranged_attack(self):
        
        self.update_new_action(1)  # attack2
        
        type = random.choice(bosses_projectiles_attacks.get(self.identity))
        self.attack_duration = random.uniform(1500,2500)
        for i in range(bosses_num_of_bullets.get(self.identity)):
            
           
            direction = random.choice(bosses_projectile_attacks_directions.get(self.identity))
            dx = direction[0]
            dy = direction[1]
            projectile = Projectile(self.rect.centerx,self.rect.centery,dx,dy,bosses_list.index(self.identity)+1,type)
            projectiles.add(projectile)
          
        self.ranged_attacking = True
        self.attack_duration_time = pygame.time.get_ticks()
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
        now = pygame.time.get_ticks()
        elapsed = now - self.attack_duration_time
        if self.melee_attacking:
            if elapsed > self.attack_duration:
                self.melee_attacking = False
                self.update_new_action(3)
                self.attack_time = pygame.time.get_ticks()  # ← cooldown starts after attack ends
        if self.ranged_attacking:
            if elapsed > self.attack_duration:
                self.ranged_attacking = False
                self.update_new_action(3)
                self.attack_time = pygame.time.get_ticks()  # ← cooldown starts after attack ends
        
                
    def when_to_attack(self):
        if not self.melee_attacking and not self.ranged_attacking:
            
            if pygame.time.get_ticks() - self.attack_time > random.uniform(1000,3000):  # time between attacks
                self.choose_attack()
                print('attack chosen')
                
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
        
class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,dx,dy,boss,attack_type):
        super().__init__()
        self.boss = bosses_list[boss-1]
        self.images = []
        for file in os.listdir(f"images/boss_projectiles/{self.boss}"):
            if file.lower().endswith('.png'):
                image_path = os.path.join(f"images/boss_projectiles/{self.boss}",file)
                image = pygame.image.load(image_path).convert_alpha()
                image_resized = pygame.transform.scale(image,(image.get_width()*0.7,image.get_height()*0.7))
                self.images.append(image_resized)
        self.image = self.images[attack_type]
        self.frect = self.image.get_frect(center = (x,y))
        self.rect = self.frect
        self.dx = dx
        self.dy = dy
        
    def draw(self):
        self.frect.center = self.rect.center
        screen.blit(self.image,self.frect)
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
    
    
class Player_beam(pygame.sprite.Sprite):
    def __init__(self,x,y,character,parent,flip):
        super().__init__()
        self.character = character
        self.parent = parent
        self.flip = flip
        self.image = pygame.image.load(f'images/player_beams/{self.character} beam.png').convert_alpha()
        if character == 'emerald_zaku_young':
            self.image = pygame.transform.scale(self.image,(self.image.get_width()*3,self.image.get_height()*0.3))
        if character == 'emerald_zaku_old':
            self.image = pygame.transform.scale(self.image,(self.image.get_width()*3,self.image.get_height()*0.7))
        if character == 'diamond_zaku':
            self.image = pygame.transform.scale(self.image,(self.image.get_width()*3,self.image.get_height()*0.5))
        if self.flip == False:
            pass
        else:
            self.image = pygame.transform.flip(self.image,True,False)
        self.frect = self.image.get_frect(center = (x,y))
        self.rect = self.frect   
    def draw(self):
        screen.blit(self.image,self.rect)
    def update(self):
        if self.parent.flip == True:
            
            self.rect.topright = (self.parent.rect.topright[0] - 70, self.parent.rect.topright[1])
        else:
            self.rect.topleft = (self.parent.rect.topleft[0] + 70, self.parent.rect.topleft[1])
        if not self.parent.attacking:
            self.kill()
characters = pygame.sprite.Group()
bosses = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()
player_beams = pygame.sprite.Group()
boss_health_bars = []
for i in range(5):
    
    c = Character(150+(i*170),SCREEN_HEIGHT//2,characters_list[i],i+1)
    characters.add(c)
    in_game_character_list.append(c)#
 
# create persistent health bars for the 5 slots (not attached to Character)
health_bars = []
for idx, c in enumerate(in_game_character_list):
    x = (idx + 1) * 170 - 60
    hb = HealthBar(x, 10, c.health, characters_health.get(c.identity),(random.uniform(0,255),random.uniform(0,255),random.uniform(0,255)))
    health_bars.append(hb)


boss = Boss(random.uniform(0, SCREEN_WIDTH), random.uniform(500, SCREEN_HEIGHT - 100), STAGE)
bosses.add(boss)
in_game_bosses_list = []
in_game_bosses_list.append(boss)
for b in bosses:
    
    bhb = HealthBar(SCREEN_WIDTH//2,200,bosses_health.get(b.identity),bosses_health.get(b.identity),(0,0,255))
    boss_health_bars.append(bhb)
    


    

            
    
   
   
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_started == False:
            for character in characters:
                
                character.change_character(event)
        if event.type == pygame.KEYDOWN:
            if game_started == False:
                
                if event.key == pygame.K_s:
                    game_started = True
                  
                    turn = turns[0]
            if game_started == True:
                
                if event.key == pygame.K_q:
                    try:
                        turn = turns[turns.index(turn) + 1]
                    except IndexError:
                        turn = turns[0]
                    print(turn)
            
        if game_started == True:
            for character in characters:
                character.controls(event)
        
            
    
    
    pygame.display.flip()
    
    
        
    
    
    
    
    
    if game_started == False:
        
        screen.fill((255,255,0))
    else:
        screen.fill((0,255,0))
        
    if game_started == True:
        pygame.draw.rect(screen,pygame.Color('cyan'),(0,0,SCREEN_WIDTH,160))
        # update and draw persistent health bars (do not attach to Character)
        for idx, hb in enumerate(health_bars):
            if idx < len(in_game_character_list):
                char = in_game_character_list[idx]
                hb.max_health = characters_health.get(char.identity)
                hb.draw(char.health)
            
    else:
        pass
    
    if game_started == True:

        # update and draw persistent health bars (do not attach to Character)
        for idx, hb in enumerate(boss_health_bars):
            if idx < len(in_game_bosses_list):
                char = in_game_bosses_list[idx]
                hb.max_health = bosses_health.get(char.identity)
                hb.draw(char.health)
            
    else:
        pass
    for character in pygame.sprite.groupcollide(characters, projectiles, False, True):
        
        character.health -= 20  # example damage value
    if pygame.sprite.groupcollide(player_projectiles,bosses,False,False):
        for pp in pygame.sprite.groupcollide(player_projectiles,bosses,False,False):
            for b in pygame.sprite.groupcollide(bosses,player_projectiles,False,False):
                b.health -= character_projectile_damage.get(pp.character)
            pp.kill()
            
    if pygame.sprite.groupcollide(player_beams,bosses,False,False):
        for bm in pygame.sprite.groupcollide(player_beams,bosses,False,False):
            for b in pygame.sprite.groupcollide(bosses,player_beams,False,False):
                b.health -= characters_beam_damage.get(bm.character)
            
    font = pygame.font.Font(None,36)
    small_font = pygame.font.Font(None,20)
    title = font.render('WELCOME TO BOSSFIGHTERS',False,pygame.Color('red'))
    instruction1 = font.render('CHOOSE YOUR CHARACTERS TO BUILD YOUR TEAM,\n  PRESS S TO START \n PRESS R FOR RANDOM TEAM',False,pygame.Color('blue'))
    turn_label = font.render(f'using:{turn}',False,pygame.Color('blue'))
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
        screen.blit(turn_label,(SCREEN_WIDTH//2 + 300,100))
    if game_started == True:
        characters.update()
        bosses.update()
        player_beams.update()
        player_beams.draw(screen)
        for c in characters:
            c.move()
         
        for b in bosses:
            b.move()
            
            b.attack_timer()
            b.when_to_attack()
        for p in projectiles:
            p.draw()
            p.move()
        for cp in player_projectiles:
            cp.draw()
            cp.move()
    clock.tick(FPS)
    
pygame.quit()