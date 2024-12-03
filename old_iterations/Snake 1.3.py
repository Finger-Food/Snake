## tasks: 1: threading pressed, 2: Stationary start,
##        3: Fancy colours (border), 4: Score appearing
import pygame
import random
import threading

pygame.init()
clock = pygame.time.Clock()

# Initialisation
dispx, dispy = 1000, 600
screen = pygame.display.set_mode((dispx, dispy))
done = False
pressed = None

# Food
eat = False
lim = 0
curr = 0
growth = 4

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
#sb = 4

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

##class Printing(object):
##    def border():
##        sa
##    def body(a, b):
##        sa
##    def head(a, b):
##        as
     
def rand():
    a = random.randint(1, (dispx/width) - 2) * width
    b = random.randint(1, (dispy/height) - 2) * height
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
            print('fgfg')
        
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

    screen.fill((150, 150, 150))
    pygame.draw.rect(screen, (57, 255, 10), pygame.Rect(2, 2, dispx - 4, dispy - 4))
    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(width - 2, height - 2, dispx - 2*width + 4, dispy - 2*height + 4))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(width, height, dispx - 2*width, dispy - 2*height))

    for (a, b) in comp:
        pygame.draw.rect(screen, colourbor, pygame.Rect(a, b, width, height))
        pygame.draw.rect(screen, colourout, pygame.Rect(a + 1, b + 1, width - 2, height - 2))
        pygame.draw.rect(screen, colourbor, pygame.Rect(a + 5, b + 5, width - 10, height - 10))
        pygame.draw.rect(screen, colourin, pygame.Rect(a + 6, b + 6, width - 12, height - 12))
        if (a, b) == comp[0]:
            pygame.draw.rect(screen, colourbor, pygame.Rect(a + width/2 - 5, b + height/2 - 5, 10, 10))
            pygame.draw.rect(screen, (252, 252, 252), pygame.Rect(a + width/2 - 4, b + height/2 - 4, 8, 8))
    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(foodx + 3, foody + 3, width - 6, height - 6))

    if comp[0] in comp[1:]:
        done = True
        break
    if (x + width) > (dispx - width) or x < width or (y + height) > (dispy - height) or y < height:
        done = True
        break
    
    pygame.display.flip()
    clock.tick(4)

a, b = comp[0]
pygame.draw.rect(screen, colourbor, pygame.Rect(a, b, width, height))
pygame.draw.rect(screen, (252, 0, 0), pygame.Rect(a + 1, b + 1, width - 2, height - 2))
pygame.draw.rect(screen, colourbor, pygame.Rect(a + width/2 - 5, b + height/2 - 5, 10, 10))
pygame.draw.rect(screen, (252, 252, 252), pygame.Rect(a + width/2 - 4, b + height/2 - 4, 8, 8))
pygame.display.flip()
