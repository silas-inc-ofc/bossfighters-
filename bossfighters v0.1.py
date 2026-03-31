import pygame
import os
import random
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Bossfighters v0.1")
FPS = 40
clock = pygame.Clock()
characters_list = ['knight','archer','axe','druid','potion_zaku','emerald_zaku_young','emerald_zaku_old','combustighoul','velocighoul',
                   'diamond_zaku','chars','gouf','bobbins']
in_game_character_list = []
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
    characters_list[0]:1,
    characters_list[1]:3,
    characters_list[2]:2,
    characters_list[3]:0.7,
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
running = True
game_started = False
mouse_pos_x = 0
mouse_pos_y = 0


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
            if dy < 0:
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
        print('updating')
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
        
        
            
            
        
               
        
characters = pygame.sprite.Group()
for i in range(5):
    
    c = Character(150+(i*170),SCREEN_HEIGHT//2,characters_list[i],i+1)
    characters.add(c)
    in_game_character_list.append(c)#
    

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
    font = pygame.font.Font(None,36)
    small_font = pygame.font.Font(None,20)
    title = font.render('WELCOME TO BOSSFIGHTERS',False,pygame.Color('red'))
    instruction1 = font.render('CHOOSE YOUR CHARACTERS TO BUILD YOUR TEAM,\n  PRESS S TO START \n PRESS R FOR RANDOM TEAM',False,pygame.Color('blue'))
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos_x = mouse_pos[0]
    mouse_pos_y = mouse_pos[1]
    for c in characters:
        c.draw()
    
    if game_started == False:
        
        screen.blit(title,(SCREEN_WIDTH//2 - 200,100))
        screen.blit(instruction1,(SCREEN_WIDTH//2 - 200,200))   
        for c in in_game_character_list:
            
            screen.blit(small_font.render(f'character :{c.identity} \n press {in_game_character_list.index(c)+1} to change',False,pygame.Color('red')),c.rect.bottomleft)
            
        
    else:
        pass
    if game_started == True:
        characters.update()
        for c in characters:
            c.move()
    clock.tick(FPS)
    
pygame.quit()