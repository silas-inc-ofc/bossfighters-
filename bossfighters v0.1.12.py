import pygame
import os
import random
from collections import Counter

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Bossfighters v0.1.12")
FPS = 40
clock = pygame.Clock()
characters_list = ['knight','archer','axe','druid','potion_zaku','emerald_zaku_young','emerald_zaku_old','combustighoul','velocighoul',
                   'diamond_zaku','chars','gouf','bobbins','gogg','guardian','neko','nyanko','stickman','V1','NT01','NT02','NT03','NT04','NT05','NT06','NT07','NT08',
                   'NT09','NT10','NT11','NT12','NT13','NT14','NT15','NT16','NT17','NT18','NT19','NT20','NT21','NT22','NT23','NT24',
                   
                   ]
NT_characters_list = [characters_list[19],characters_list[20],characters_list[21],characters_list[22],characters_list[23],characters_list[24],characters_list[25],characters_list[26],
                      characters_list[27],characters_list[28],characters_list[29],characters_list[30],characters_list[31],characters_list[32],characters_list[33],characters_list[34],
                      characters_list[35],characters_list[36],characters_list[37],characters_list[38],characters_list[39],characters_list[40],characters_list[41],
                      characters_list[42]]
current_characters_list = [characters_list[0],characters_list[1],characters_list[2],characters_list[3],characters_list[4]] + NT_characters_list

killed_characters = []
in_game_character_list = []
turns =[characters_list[0],characters_list[1],characters_list[2],characters_list[3],characters_list[4]]
turn = turns[0]
STAGE = 1
global credits
credits = 0
stages_available = [1]

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
    characters_list[15]:2,
    characters_list[16]:1,
    characters_list[17]:2,
    characters_list[18]:3,
    characters_list[19]:1,
    characters_list[20]:1,
    characters_list[21]:1,
    characters_list[22]:1,
    characters_list[23]:1,
    characters_list[24]:1,
    characters_list[25]:1,
    characters_list[26]:1,
    characters_list[27]:1,
    characters_list[28]:1,
    characters_list[29]:1,
    characters_list[30]:1,
    characters_list[31]:1,
    
    
    characters_list[32]:1,
    characters_list[33]:1,
    characters_list[34]:1,
    characters_list[35]:1,
    
    
    characters_list[36]:1,
    characters_list[37]:1,
    characters_list[38]:1,
    characters_list[39]:1,
    characters_list[40]:1,
    characters_list[41]:1,
    characters_list[42]:1,
 
    
}
stage_rewards = {
    1:('characters',[characters_list[5],characters_list[6],characters_list[7],characters_list[8],characters_list[9]]),
    2:('characters',[characters_list[10],characters_list[11],characters_list[12],characters_list[13],characters_list[14]]),
    3:('characters',[characters_list[15],characters_list[16],characters_list[17],characters_list[18]]),
    4:('credits',100),
    5:('credits',200),
    
    
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
    characters_list[15]:4,
    characters_list[16]:4.5,
    characters_list[17]:3.7,
    characters_list[18]:2.3,
    characters_list[19]:2,
    characters_list[20]:2,
    characters_list[21]:2.1,
    characters_list[22]:2.2,
    characters_list[23]:2.3,
    characters_list[24]:2.4,
    characters_list[25]:2.5,
    characters_list[26]:2.6,
    characters_list[27]:2.7,
    characters_list[28]:2.8,
    characters_list[29]:2.9,
    characters_list[30]:3.0,
    characters_list[31]:3.1,
    characters_list[32]:3.2,
    characters_list[33]:3.3,
    characters_list[34]:3.4,
    characters_list[35]:3.5,
    
    characters_list[36]:3.6,
    characters_list[37]:3.7,
    characters_list[38]:3.8,
    characters_list[39]:3.9,
    characters_list[40]:4.0,
    characters_list[41]:4.1,
    characters_list[42]:4.2,
    
    
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
    characters_list[15]:245,
    characters_list[16]:300,
    characters_list[17]:200,
    characters_list[18]:610,
    characters_list[19]:190,
    characters_list[20]:200,
    characters_list[21]:210,
    characters_list[22]:220,
    characters_list[23]:230,
    characters_list[24]:240,
    characters_list[25]:250,
    characters_list[26]:260,
     characters_list[27]:270,
    characters_list[28]:280,
    characters_list[29]:290,
    characters_list[30]:300,
    characters_list[31]:310,
    characters_list[32]:320,
    characters_list[33]:330,
    characters_list[34]:340,
    characters_list[35]:350,
    characters_list[36]:360,
    characters_list[37]:370,
    characters_list[38]:380,
    characters_list[39]:390,
    characters_list[40]:400,
    characters_list[41]:410,
    characters_list[42]:420,
    
    
    
    
    
    
    
    
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
    characters_list[15]:['melee','melee'],
    characters_list[16]:['beam'],
    characters_list[17]:['melee','non-melee'],
    characters_list[18]:['melee','melee','melee'],
    characters_list[19]:['morale'],
    characters_list[20]:['morale'],

    characters_list[21]:['morale'],
    characters_list[22]:['morale'],
    characters_list[23]:['morale'],
    characters_list[24]:['morale'],
    characters_list[25]:['morale'],
    characters_list[26]:['morale'],
    
    
    characters_list[27]:['morale'],

    characters_list[28]:['morale'],
    characters_list[29]:['morale'],
    characters_list[30]:['morale'],
    characters_list[31]:['morale'],
    characters_list[32]:['morale'],
    characters_list[33]:['morale'],
    
    
    characters_list[34]:['morale'],
    characters_list[35]:['morale'],
    characters_list[36]:['morale'],
    characters_list[37]:['morale'],
    
    
    characters_list[38]:['morale'],

    characters_list[39]:['morale'],
    characters_list[40]:['morale'],
    characters_list[41]:['morale'],
    characters_list[42]:['morale'],

    
    
}


characters_beam_damage = {
    characters_list[5]:5,
    characters_list[6]:3.5,
    characters_list[9]:4.5,
    characters_list[16]:6.7,
}

characters_projectile_delays = {
    characters_list[1]:600,
    characters_list[4]:100,
    characters_list[9]:300,
}
character_projectile_damage = {
    characters_list[1]:60,
    characters_list[4]:30,
    characters_list[9]:45,
    characters_list[17]:30,
    
}

characters_morale_strength = {
    characters_list[19]:20,
    characters_list[20]:20,
    characters_list[21]:20,
    characters_list[22]:20,
    characters_list[23]:20,
    characters_list[24]:20,
    characters_list[25]:20,
    characters_list[26]:20,
    
    
    
    
    characters_list[27]:20,
    characters_list[28]:20,
    characters_list[29]:20,
    characters_list[30]:20,
    
    
    characters_list[31]:20,

    characters_list[32]:20,
    characters_list[33]:20,
    
   
    
    
    
    characters_list[34]:20,
    characters_list[35]:20,
    characters_list[36]:20,
    characters_list[37]:20,
    
    
    characters_list[38]:20,

    characters_list[39]:20,
    characters_list[40]:20,
    characters_list[41]:20,
    characters_list[42]:20,
   
    
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
    characters_list[15]:(250,160),
    characters_list[16]:(6.7,),
    characters_list[17]:(300,0,),
    characters_list[18]:(200,150,500),
    characters_list[19]:(0,),
    characters_list[20]:(0,),
    characters_list[21]:(0,),
    characters_list[22]:(0,),
    characters_list[23]:(0,),
    characters_list[24]:(0,),
    characters_list[25]:(0,),
    characters_list[26]:(0,),
    characters_list[27]:(0,),

    characters_list[28]:(0,),
    characters_list[29]:(0,),
    characters_list[30]:(0,),
    characters_list[31]:(0,),
    characters_list[32]:(0,),
    characters_list[33]:(0,),
    
    
    characters_list[34]:(0,),
    characters_list[35]:(0,),
    characters_list[36]:(0,),
    characters_list[37]:(0,),
    
    
    characters_list[38]:(0,),

    characters_list[39]:(0,),
    characters_list[40]:(0,),
    characters_list[41]:(0,),
    characters_list[42]:(0,),
   
    
    
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
    characters_list[15]:[False,False],
    characters_list[16]:[False],
    characters_list[17]:[False,False],
    characters_list[18]:[False,False,False],
    characters_list[19]:[False],
    characters_list[20]:[False],
    characters_list[21]:[False],
    characters_list[22]:[False],
    characters_list[23]:[False],
    characters_list[24]:[False],
    characters_list[25]:[False],
    characters_list[26]:[False],
    
    
    characters_list[27]:[False],

    characters_list[28]:[False],
    characters_list[29]:[False],
    characters_list[30]:[False],
    characters_list[31]:[False],
    characters_list[32]:[False],
    characters_list[33]:[False],
    
    
    characters_list[34]:[False],
    characters_list[35]:[False],
    characters_list[36]:[False],
    characters_list[37]:[False],
    
    
    characters_list[38]:[False],

    characters_list[39]:[False],
    characters_list[40]:[False],
    characters_list[41]:[False],
    characters_list[42]:[False],
   
    
  
    
    
}
characters_heal_amounts = {
    characters_list[4]:100,
    characters_list[12]:30,
    
    
    
}



bosses_list = ['bot','bot Mk2','bot','bot','bot','bot']   ## boss 2 and 3 are placeholder bosses: must replace later! 
bosses_projectile_attacks_directions = {
    bosses_list[0]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)], 
    bosses_list[1]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5),(10,0),(-10,0),(0,10),(0,-10),(10,10),(10,-10),(-10,10),(-10,-10)],
    bosses_list[2]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)],
    bosses_list[3]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)],
    bosses_list[4]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)],
    bosses_list[5]:[(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)],
}
bosses_projectile_speed_multiplier = {
    bosses_list[0]:{0:1,1:0.5},
    bosses_list[1]:{0:1,1:0.5,2:2,3:1.5},
    bosses_list[2]:{0:1,1:0.5},
    bosses_list[3]:{0:1,1:0.5},
    bosses_list[4]:{0:1,1:0.5},
    bosses_list[5]:{0:1,1:0.5},

}

bosses_projectiles_attacks = {
    bosses_list[0]:[0,1],
    bosses_list[1]:[0,1,2,3],
    bosses_list[2]:[0,1],
    bosses_list[3]:[0,1],
    bosses_list[4]:[0,1],
    bosses_list[5]:[0,1],
    
    
}
bosses_health = {
    bosses_list[0]:2000,
    bosses_list[1]:4000,
    bosses_list[2]:2000,
    bosses_list[3]:2000,
    bosses_list[4]:2000,
    bosses_list[5]:2000,
    
}
bosses_speed = {
    bosses_list[0]:1,
    bosses_list[1]:2,
    bosses_list[2]:1,
    bosses_list[3]:1,
    bosses_list[4]:1,
    bosses_list[5]:1,
    
}

bosses_num_of_bullets = {
    bosses_list[0]:5,
    bosses_list[1]:10,
    bosses_list[2]:5,
    bosses_list[3]:5,
    bosses_list[4]:5,
    bosses_list[5]:5,
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
        self.is_nt_character = False
        if self.identity in NT_characters_list:
            self.attack_type = characteres_attacks_stats.get(self.identity)[0]
            self.is_nt_character = True
        
        
        # Apply NT character restrictions
        if self.is_nt_character:
            self.animation_types = ['idle']  # Only idle animation
            self.health = 100  # Fixed health
        else:
              
      
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
                if file.lower().endswith(('.png' )) or file.lower().endswith(('.jpeg' )) :
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
        self.identity = identity
        self.is_nt_character = identity in NT_characters_list
        self.num_of_attacks = characters_attacks.get(identity)
        self.animation_types = ['idle','walk']
        self.action_index = 0
        self.frame_index = 0
        
        # Apply NT character restrictions
        if self.is_nt_character:
            self.animation_types = ['idle']  # Only idle animation
            self.health = 100  # Fixed health
        else:
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
                if file.lower().endswith('.png') or file.lower().endswith('.jpeg'):
                    image_path = os.path.join(path,file)
                    image = pygame.image.load(image_path).convert_alpha()
                    if file.lower().endswith('.png') :
                        
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
        # NT characters cannot attack
        if self.is_nt_character:
            return False
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
                    dmg = characters_damage.get(self.identity)[attack_no-1]
                            
                    for c in in_game_character_list:
                        if c.identity in characters_morale_strength:
                            
                            dmg += characters_morale_strength.get(c.identity)
                            print(f'morale: {characters_morale_strength.get(c.identity)}')
                            print(f'dmg:{dmg}')
                    
                    boss.health -= dmg
                        
                    
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
                
                
            if self.identity == 'stickman':
                projectile_dx = 5
                projectile_dy = 0
                repetition = 10
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
        try:
            
            self.image = self.animation_list[self.action][self.frame_index]
        except IndexError:
            self.action = 0
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
            killed_characters.append(self)
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
                            self.identity = current_characters_list[current_characters_list.index(self.identity) + 1]
                            character_dict.update({1:self.identity})
                            self.reload_identity(self.identity)
                            turns[0] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = current_characters_list[0]
                            character_dict.update({1:self.identity})
                            self.reload_identity(self.identity)
                            turns[0] = self.identity
                            print(turns)
                if event.key == pygame.K_2:
                    if self.number == 2:
                        try:
                            self.identity = current_characters_list[current_characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({2:self.identity})
                            turns[1] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = current_characters_list[0]
                            self.reload_identity(self.identity)
                            character_dict.update({2:self.identity})
                            turns[1] = self.identity
                            print(turns)
                if event.key == pygame.K_3:
                    if self.number == 3:
                        try:
                            self.identity = current_characters_list[current_characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({3:self.identity})
                            turns[2] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = current_characters_list[0]
                            self.reload_identity(self.identity)
                            character_dict.update({3:self.identity})
                            turns[2] = self.identity
                            print(turns)
                if event.key == pygame.K_4:
                    if self.number == 4:
                        try:
                            self.identity = current_characters_list[current_characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({4:self.identity})
                            turns[3] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = current_characters_list[0]
                            self.reload_identity(self.identity)
                            turns[3] = self.identity
                            character_dict.update({4:self.identity})
                            print(turns)
                if event.key == pygame.K_5:
                    if self.number == 5:
                        try:
                            self.identity = current_characters_list[current_characters_list.index(self.identity) + 1]
                            self.reload_identity(self.identity)
                            character_dict.update({5:self.identity})
                            turns[4] = self.identity
                            print(turns)
                        except IndexError:
                            self.identity = current_characters_list[0]
                            self.reload_identity(self.identity)
                            character_dict.update({5:self.identity})
                            turns[4] = self.identity
                            print(turns)
                elif event.key == pygame.K_r:
                    self.identity = random.choice(current_characters_list)
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
            self.drop_reward()
            self.kill()
    
    def drop_reward(self):
        try:
            
            c = Cage(self.rect.centerx,self.rect.centery,stage_rewards.get(STAGE)[0],stage_rewards.get(STAGE)[1])
            cages.add(c)
        except TypeError:
            reset_game()
            
        
class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,dx,dy,boss,attack_type):
        super().__init__()
        self.boss = bosses_list[boss-1]
        self.images = []
        self.attack_type = attack_type
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
        self.dx *= bosses_projectile_speed_multiplier.get(bosses_list[boss-1]).get(self.attack_type)
        self.dy *= bosses_projectile_speed_multiplier.get(bosses_list[boss-1]).get(self.attack_type)
       
        
        
        
        
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
        if character == 'nyanko':
            
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
            if self.character != 'nyanko':
                
                self.rect.topright = (self.parent.rect.topright[0] - 70, self.parent.rect.topright[1])
            else:
                self.rect.bottomright =  (self.parent.rect.bottomright[0] - 70, self.parent.rect.bottomright[1])
        else:
            if self.character != 'nyanko':
                self.rect.topleft = (self.parent.rect.topleft[0] + 70, self.parent.rect.topleft[1])
            else:
                self.rect.bottomleft =  (self.parent.rect.bottomleft[0] - 70, self.parent.rect.bottomleft[1])
        if not self.parent.attacking:
            self.kill()
            
class Cage(pygame.sprite.Sprite):
    def __init__(self,x,y,reward_type,reward):
        super().__init__()
        self.reward = reward
        self.image = pygame.image.load("images/cage.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*0.5,self.image.get_height()*0.5))
        self.frect = self.image.get_frect(center=(x,y))
        self.rect = self.frect
        self.reward_type = reward_type
    def draw(self):
        screen.blit(self.image,self.rect)
    def reward_player(self):
        global credits
        if self.reward_type == 'characters':
            for i in self.reward:
                current_characters_list.append(i)
                
        elif self.reward_type == 'credits':
            credits += self.reward
        
        
characters = pygame.sprite.Group()
bosses = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()
player_beams = pygame.sprite.Group()
boss_health_bars = []
characters_initial_pos = []
for i in range(5):
    
    c = Character(150+(i*170),SCREEN_HEIGHT//2,current_characters_list[i],i+1)
    characters.add(c)
    characters_initial_pos.append((c.rect.centerx,c.rect.centery))
    in_game_character_list.append(c)#
 
# create persistent health bars for the 5 slots (not attached to Character)
health_bars = []
for idx, c in enumerate(in_game_character_list):
    x = (idx + 1) * 170 - 60
    hb = HealthBar(x, 10, c.health, characters_health.get(c.identity),(random.uniform(0,255),random.uniform(0,255),random.uniform(0,255)))
    health_bars.append(hb)


cages = pygame.sprite.GroupSingle()
in_game_bosses_list = []
boss_health_bars = []

def reset_game():
    """Reset game to starting screen state"""
    global game_started
    # Clear all battle objects
    projectiles.empty()
    player_projectiles.empty()
    player_beams.empty()
    cages.empty()
    bosses.empty()
    in_game_bosses_list.clear()
    boss_health_bars.clear()
    
    # Reset character health
    for c in in_game_character_list:
        c.health = characters_health.get(c.identity)
        
        
        c.rect.centerx = characters_initial_pos[c.number-1][0]
        c.rect.centery = characters_initial_pos[c.number-1][1]
        if c in killed_characters:
            d = Character(characters_initial_pos[c.number-1][0],characters_initial_pos[c.number-1][1],c.identity,c.number)
            characters.add(d)
        
    game_started = False

            
    
   
   
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
                    # Spawn boss for the selected stage
                    new_boss = Boss(random.uniform(0, SCREEN_WIDTH), random.uniform(500, SCREEN_HEIGHT - 100), STAGE)
                    bosses.add(new_boss)
                    in_game_bosses_list.append(new_boss)
                    bhb = HealthBar(SCREEN_WIDTH//2, 200, bosses_health.get(new_boss.identity), bosses_health.get(new_boss.identity), (0, 0, 255))
                    boss_health_bars.append(bhb)
                    game_started = True
                  
                    turn = turns[0]
                    
                if event.key == pygame.K_DOWN:
                    try:
                        STAGE = stages_available[stages_available.index(STAGE)+ 1]
                    except (IndexError, ValueError):
                        STAGE = stages_available[0]
                        
                if event.key == pygame.K_UP:
                    try:
                        STAGE = stages_available[stages_available.index(STAGE)- 1]
                    except (IndexError, ValueError):
                        STAGE = stages_available[len(stages_available)-1]
                    
                    
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
            dmg = character_projectile_damage.get(pp.character)
            for b in pygame.sprite.groupcollide(bosses,player_projectiles,False,False):
                for c in in_game_character_list:
                    if c.identity in characters_morale_strength:
                        print(f'morale: {characters_morale_strength.get(c.identity)}')
                        dmg += characters_morale_strength.get(c.identity)
                    else:
                        pass
                        
                    b.health -= dmg
            pp.kill()
            
    if pygame.sprite.groupcollide(player_beams,bosses,False,False):
        for bm in pygame.sprite.groupcollide(player_beams,bosses,False,False):
            dmg = characters_beam_damage.get(bm.character)
            for b in pygame.sprite.groupcollide(bosses,player_beams,False,False):
             
                
                
                
                
               
                for c in in_game_character_list:
                    if c.identity in characters_morale_strength:
                        print(f'morale: {characters_morale_strength.get(c.identity)}')
                        dmg += characters_morale_strength.get(c.identity)
                    else:
                        pass
                        
                b.health -= dmg
            
    cage_collisions = pygame.sprite.groupcollide(cages,characters,True,False)
    if cage_collisions:
        for cage in cage_collisions:
            cage.reward_player()
            if STAGE + 1 <= 6 and STAGE + 1 not in stages_available:
                stages_available.append(STAGE + 1)
            reset_game()
    font = pygame.font.Font(None,36)
    small_font = pygame.font.Font(None,20)
    title = font.render('WELCOME TO BOSSFIGHTERS',False,pygame.Color('red'))
    instruction1 = font.render(f'CHOOSE YOUR CHARACTERS TO BUILD YOUR TEAM,\n  PRESS S TO PLAY STAGE {STAGE}\n (change stage using up and down keys)\n PRESS R FOR RANDOM TEAM',False,pygame.Color('blue'))
    turn_label = font.render(f'using:{turn}',False,pygame.Color('blue'))
    credits_label = font.render(f'credits: {credits}',False,pygame.Color('darkgreen'))
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
        screen.blit(credits_label,(0,100))
        
        for c in in_game_character_list:
            
            screen.blit(small_font.render(f'character :{c.identity} \n press {in_game_character_list.index(c)+1} to change',False,pygame.Color('red')),c.rect.bottomleft)
            
        
    else:
        screen.blit(turn_label,(SCREEN_WIDTH//2 + 300,100))
    if len(killed_characters) >= 5:
        reset_game()
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
        for c in cages:
            c.draw()
    clock.tick(FPS)
    
pygame.quit()