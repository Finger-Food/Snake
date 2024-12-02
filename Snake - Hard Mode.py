import pygame
import random
import threading
import encrypt

# Initialisation
pygame.init()
clock = pygame.time.Clock()

# Colours
colourout = (100, 180, 0)
colourin = (0, 90, 200)
colourbor = (20, 20, 20)
colourscore = (0, 51, 102)
colourend = (70, 206, 233)

# Colour Thickness
sb = 40 #screen border
sbo = 4 #screen border outline
bb = 1  #body border
bo = 3  #body outer layer
h = 2   #head centre
db = 1  #dead head border

# Essentials
dispx, dispy = 960 + 2*sb, 540 + 2*sb
screen = pygame.display.set_mode((dispx, dispy))
done = False
pressed = None
start = False
font_small = pygame.font.SysFont("Tahoma", 20)
font_big = pygame.font.SysFont("Tahoma", 40)

# Food
lim = 0
curr = 0
growth = 3

# Coordinates
width, height = 20, 20
x, y = width*2 + sb, sb
comp = [(x, y), (x - width, y), (x - width*2, y), (x - width*3, y)]
press = ('x', width)
foodx, foody = sb + 300, sb + 300

# High Score
try:
    high_score = encrypt.read()
except:
    high_score = False
if not high_score:
    encrypt.write(0)
    high_score = encrypt.read()

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
        length = font_small.render("Length: " + str(len(comp)), 1, colourscore)
        screen.blit(length, (sb, 7))
        if len(comp) > high_score:
            high = font_small.render("High Score: " + str(len(comp)), 1, colourscore)
        else:
            high = font_small.render("High Score: " + str(high_score), 1, colourscore)
        screen.blit(high, (dispx - sb - high.get_rect().width, 7))
    def score_end(self):
        clock.tick(10)
        score_text = font_big.render("SCORE", 1, colourend)
        score = font_big.render(str(len(comp)), 1, colourend)
        screen.blit(score_text, ((dispx - score_text.get_rect().width)//2, (dispy - score.get_rect().height)//2 - score_text.get_rect().height + 5))
        screen.blit(score, ((dispx - score.get_rect().width)//2, (dispy - score.get_rect().height)//2))
        if len(comp) > high_score:
            new = font_big.render("NEW HIGH SCORE!!", 1, colourend)
            screen.blit(new, ((dispx - new.get_rect().width)//2, (dispy + score.get_rect().height)//2))
        pygame.display.flip()
                    
def rand():
    a = random.randint(0, ((dispx-2*sb)/width) - 1) * width + sb
    b = random.randint(0, ((dispy-2*sb)/height) - 1) * height + sb
    while (a, b) in comp:
        a = random.randint(0, ((dispx-2*sb)/width) - 1) * width + sb
        b = random.randint(0, ((dispy-2*sb)/height) - 1) * height + sb
    return a, b

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            pressed = event.key
        
    if pressed == pygame.K_UP and press != ('y', height):
        y -= height
        press = ('y', -(height))
    elif pressed == pygame.K_DOWN and press != ('y', -(height)):
        y += height
        press = ('y', height)
    elif pressed == pygame.K_LEFT and press != ('x', width):
        x -= width
        press = ('x', -(width))
    elif pressed == pygame.K_RIGHT and press != ('x', -(width)):
        x += width
        press = ('x', width)
    else:
        if press[0] == 'x':
            x += press[1]
        if press[0] == 'y':
            y += press[1]
    
    if (x, y) == (foodx, foody):
        lim += growth
        foodx, foody = rand()

    if curr < lim:
        comp.append((x, y))
        curr += 1

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
        break
    if (x + width) > (dispx - sb) or x < sb or (y + height) > (dispy - sb) or y < sb:
        break
    
    pygame.display.flip()
    clock.tick(40)

    while not pressed or pressed == pygame.K_LEFT and not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            if event.type == pygame.KEYDOWN:
                pressed = event.key
        if done == True:
             break
    start = True

if not done:
    Printing().dead(comp[0][0], comp[0][1])
    Printing().score_end()
    clock.tick(2)
if len(comp) > high_score:
    encrypt.write(len(comp))
