# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
 
import pygame
import random
import time
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)

pygame.init()
  
# Set the height and width of the screen
x_width = 1000
y_width = 780
size=[x_width,y_width]
screen=pygame.display.set_mode(size)

level = 2
block_size = 40
margin = 2


def initboard(level):
    grids =[]
    for i in range(level):
        grids.append([])
        for j in range(level):
            grids[i].append(0)
    result=[]
    s=range(level*level)
    # random memory
    for i in range(level):
        while True:
            n = random.choice(s)
            if n not in result:
                result.append(n)
                break
    return (grids,result)

def draw_block(screen,start_pos,color):
    rect = start_pos+[block_size,block_size]
    pygame.draw.rect(screen,color,rect)
    

def drawgrids(screen,start_pos,grids):
    row = len(grids)
    x_start = start_pos[0]
    y_start = start_pos[1]
    screen.fill(black)
    for r in range(row):
        for c in range(row):
            color=white
            if grids[r][c] == 1:
                color = blue
            elif grids[r][c] == 2:
                color = red
            draw_block(screen,[x_start+c*(block_size+margin)+margin,y_start+r*(block_size+margin)+margin],color)
                

def clickgrid(grids,result,clicked,start_x,start_y,x,y):
    level = len(grids)
    gridswidth = block_size*level
    x -= start_x
    y -= start_y
    if x <0 or x>gridswidth or y<0 or y> gridswidth:
        pass
    else:
        col = int(x/(block_size+margin))
        row = int(y/(block_size+margin))
        g=row*level+col
        if g in result:
            grids[row][col]=1
            clicked.append(g)
        else:
            grids[row][col]=2
            return False
    return True

def show_score(color=red,font_size=25):
    font = pygame.font.Font(None,font_size)
    text = font.render("LEVEL %d    SCORE:%d" % (level,score),True,color)
    screen.blit(text,[600,40])
    
def showresult(screen,start_pos,level,result,delay):
    grids,_ = initboard(level)
    for i in range(len(result)):
        row = result[i]/level
        col = result[i]%level
        grids[row][col] = 1
    drawgrids(screen,start_pos,grids)
    show_score()
    pygame.display.flip()
    time.sleep(delay)

def show_menu(color=white,font_size=30):
    font = pygame.font.Font(None,font_size)
    texts = ['GAME OVER!','Try again','Exit']
    for i in range(len(texts)):
        text = font.render(texts[i],True,color)
        screen.blit(text,[380,300+60*i])           
    pygame.display.flip()
    
def gameover(level,score):
    print("you have completed level %d\n.your score:%d" % (level,score))
    screen.fill(black)
    show_score()
    show_menu()
    rt = {pygame.K_t:True,pygame.K_ESCAPE:False,pygame.K_e:False}
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                return rt.get(event.key,True)
    return True
  
pygame.display.set_caption("memory challenge!")

score = 0
grids,result = initboard(level)
clicked=[]
start_pos=[x_width/2 - block_size*level/2,y_width/2-block_size*level/2]
showresult(screen,start_pos,level,result,5)
#Loop until the user clicks the close button.
done=False
 
# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_pos,y_pos = pygame.mouse.get_pos()
            if clickgrid(grids,result,clicked,start_pos[0],start_pos[1],x_pos,y_pos) is False:
                # click a wrong grid, game over
                go_on = gameover(level-1,score) # game over
                if go_on:
                    score = 0
                    level = 2
                    clicked = []
                    grids,result = initboard(level)
                    start_pos=[x_width/2 - block_size*level/2,y_width/2-block_size*level/2]
                    showresult(screen,start_pos,level,result,5)
                else:
                    done = True
            else:# check whether all grid had been showed has been clicked
                clicked.sort()
                result.sort()
                if clicked == result:
                    # yes, turn to next level
                    score += level*500
                    level += 1
                    print('level %d start' % (level,))
                    grids,result = initboard(level)
                    start_pos=[x_width/2 - block_size*level/2,y_width/2-block_size*level/2]
                    clicked = []
                    showresult(screen,start_pos,level,result,5)
                
    # Set the screen background
    drawgrids(screen,start_pos,grids)
    show_score()
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
     
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    # Limit to 20 frames per second
    clock.tick(40)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
