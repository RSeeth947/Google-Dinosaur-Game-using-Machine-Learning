

import sys, os, pygame, random, neat



pygame.init()
clock = pygame.time.Clock()
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)

RUN = [pygame.image.load(os.path.join("dinos", "DinoRun1.png")),
            pygame.image.load(os.path.join("dinos", "DinoRun2.png"))]

JUMP = pygame.image.load(os.path.join("dinos", "DinoJump.png")) 

CACTI = [pygame.image.load(os.path.join("dinos", "LargeCactus1.png")),
        pygame.image.load(os.path.join("dinos", "LargeCactus2.png")),
        pygame.image.load(os.path.join("dinos", "LargeCactus3.png")),
        pygame.image.load(os.path.join("dinos", "SmallCactus1.png")),
        pygame.image.load(os.path.join("dinos", "SmallCactus2.png")),
        pygame.image.load(os.path.join("dinos", "SmallCactus3.png"))]






class Dinos:
    ANIMATION_TIME = 5



    def __init__(self, x, y):
        self.xpos = x
        self.ypos = y
        self.tick_count = 0
        self.vel = 0
        self.img = RUN[0]
        self.step_index = 0
        self.dino_rect = pygame.Rect(self.xpos, self.ypos , self.img.get_width(), self.img.get_height())
        self.get_jump = True


    def update(self):
        if self.step_index >= 10:
            self.step_index = 0

    
    def run(self):
        if self.step_index < 5:
            self.img = RUN[0]
        else:
             self.img = RUN[1]

        self.step_index += 2

    

    def jump(self):
        self.tick_count = 0
        self.dino_rect.y -= 250
        
       

        

    def move(self):
        self.tick_count += 2
        floor = 500
        
        dis = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2 

        if dis >= 16:
            dis = (dis/abs(dis)) * 16
        if dis < 0:
            dis -= 2

        if self.dino_rect.y < floor + 1:
            self.dino_rect.y = self.dino_rect.y + dis
        
        if self.dino_rect.y > floor:
            self.can_jump = True
        
        else:
            self.can_jump = False

        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self, screen):
        screen.blit(self.img, (self.dino_rect.x, self.dino_rect.y))
        

class Cactus:
    IMGS = CACTI

    def __init__(self, x):
        i = random.randrange(6)
        self.xpos = x
        self.ypos = 500
        self.img = CACTI[i]
        self.cactus_rect = pygame.Rect(self.xpos, self.ypos , self.img.get_width(), self.img.get_height())



    def move(self):
        self.cactus_rect.x -= 35

    def collide(self, dino):
        cactus_mask = pygame.mask.from_surface(self.img)
        dino_mask = dino.get_mask()

        offset = (int(self.cactus_rect.x - dino.dino_rect.x), int(self.cactus_rect.y - dino.dino_rect.y))
        collision = dino_mask.overlap(cactus_mask, offset)
        return collision


    

    def draw(self, screen):
        screen.blit(self.img, (self.cactus_rect.x, self.cactus_rect.y))
        




dino = [Dinos(200, 500 - RUN[0].get_height())]
cactus = Cactus(width)

font = pygame.font.Font("freesansbold.ttf", 32)











    
clock = pygame.time.Clock()
score = 0


def eval_genomes(genomes, config):
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

        screen.fill((255,255,255))
        clock.tick(30)
        
        user_input = pygame.key.get_pressed()
        text = font.render("Score: " + str(score), True, (0, 255, 0), (0, 0, 128))
        text_rect = text.get_rect()
        score += 1
        





        
        screen.blit(text, text_rect)
        pygame.display.update()



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 49)
    print('\nBest genome:\n{!s}'.format(winner))
