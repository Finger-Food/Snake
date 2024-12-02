## tasks: 1: Threading pressed, 2: Stationary start, 3: Score appearing
import pygame
import random
import threading

# Initialisation
pygame.init()
clock = pygame.time.Clock()

# Essentials
dispx, dispy = 1000, 600
screen = pygame.display.set_mode((dispx, dispy))
done = False
pressed = None
font = pygame.font.SysFont("Times New Roman", 18)

# Food
eat = False
lim = 0
curr = 0
growth = 3

# Coordinates
width, height = 40, 40
x, y = width*4, height
comp = [(x, y), (x - width, y), (x - width*2, y), (x - width*3, y)]
press = ['x', 40]
foodx, foody = 400, 400

# Colours
colourout = (100, 180, 0)
colourin = (0, 90, 200)
colourbor = (20, 20, 20)

# Colour Thickness
sb = 40  #screen border
sbo = 4  #screen border outline
bb = 1  #body border
bo = 4  #body outer layer
h = 5   #head centre
db = 1  #dead head border

##class Movement(threading.Thread):
##    def run(self):
##        while not done:
##            for event in pygame.event.get():
##                global pressed
##                if event.type == pygame.KEYDOWN:
##                    pressed = event.key
##                    print('jaskd')
##
##thread = Movement()
##thread.start()

class Printing():
    def border(self):
        screen.fill((150, 150, 150))
        pygame.draw.rect(screen, (57, 255, 10), pygame.Rect(sbo, sbo, dispx - 2*sbo, dispy - 2*sbo))
        pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(sb - sbo, sb - sbo, dispx - 2*(sb - sbo), dispy - 2*(sb - sbo)))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sb, sb, dispx - 2*sb, dispy - 2*sb))
    def body(self, a, b):
        pygame.draw.rect(screen, colourbor, pygame.Rect(a, b, width, height))
        pygame.draw.rect(screen, colourout, pygame.Rect(a + bb, b + bb, width - 2*bb, height - 2*bb))
        pygame.draw.rect(screen, colourbor, pygame.Rect(a + bb + bo, b + bb + bo, width - 2*(bb + bo), height - 2*(bb + bo)))
        pygame.draw.rect(screen, colourin, pygame.Rect(a + 2*bb + bo, b + 2*bb + bo, width - 2*(2*bb + bo), height - 2*(2*bb + bo)))
    def head(self, a, b):
        pygame.draw.rect(screen, colourbor, pygame.Rect(a + width/2 - h - bb, b + height/2 - h - bb, 2*(h + bb), 2*(h + bb)))
        pygame.draw.rect(screen, (252, 252, 252), pygame.Rect(a + width/2 - h, b + height/2 - h, h*2, h*2))
    def food(self, foodx, foody):
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(foodx + 3, foody + 3, width - 6, height - 6))
    def dead(self, a, b):
        pygame.draw.rect(screen, colourbor, pygame.Rect(a, b, width, height))
        pygame.draw.rect(screen, (252, 0, 0), pygame.Rect(a + db, b + db, width - 2*db, height - 2*db))
        pygame.draw.rect(screen, colourbor, pygame.Rect(a + width/2 - h - bb, b + height/2 - h - bb, 2*(h + bb), 2*(h + bb)))
        pygame.draw.rect(screen, (252, 252, 252), pygame.Rect(a + width/2 - h, b + height/2 - h, h*2, h*2))
        pygame.display.flip()
    def score(self):
        score = font.render("Length: " + str(len(comp)), 1, (0, 0, 0))
        screen.blit(score, (40, 11))     

def rand():
    a = random.randint(0, ((dispx-2*sb)/width) - 1) * width + sb
    b = random.randint(0, (dispy-2*sb/height) - 1) * height + sb
    while (a, b) in comp:
        a = random.randint(1, (dispx/width) - 2) * width
        b = random.randint(1, (dispy/height) - 2) * height
    return a, b
         
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            pressed = event.key
        
    if eat == True:
        if press[0] == 'x':
            x += press[1]
        if press[0] == 'y':
            y += press[1]
    elif pressed == pygame.K_UP and press != ('y', 40):
        y -= 40
        press = ('y', -40)
    elif pressed == pygame.K_DOWN and press != ('y', -40):
        y += 40
        press = ('y', 40)
    elif pressed == pygame.K_LEFT and press != ('x', 40):
        x -= 40
        press = ('x', -40)
    elif pressed == pygame.K_RIGHT and press != ('x', -40):
        x += 40
        press = ('x', 40)
    else:
        if press[0] == 'x':
            x += press[1]
        if press[0] == 'y':
            y += press[1]
    
    if (x, y) == (foodx, foody):
        eat = True
        lim += growth
        foodx, foody = rand()

    if curr < lim:
        comp.append((x, y))
        curr += 1
    else:
        eat = False

    for i in range(len(comp) - 1, 0, -1):
        comp[i] = comp[i - 1]
    comp[0] = (x, y)

    Printing().border()
    for (a, b) in comp:
        Printing().body(a, b)
        if (a, b) == comp[0]:
            Printing().head(a, b)
    Printing().food(foodx, foody)
    Printing().head(foodx, foody)
    Printing().score()
    
    if comp[0] in comp[1:]:
        done = True
        break
    if (x + width) > (dispx - width) or x < width or (y + height) > (dispy - height) or y < height:
        done = True
        break
    
    pygame.display.flip()
    clock.tick(4)

Printing().dead(comp[0][0], comp[0][1])
