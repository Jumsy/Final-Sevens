#Final Sevens rewrite
#April 27th, 2012

import sys
import random

import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
windowWidth = 280
windowHeight = 560
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Final Sevens')
screen = pygame.display.get_surface()

blockSize = 40

#For text in the pause menu
mainFont = pygame.font.SysFont(None, 19)
#For writing on the blocks and the score value in the menu
blockFont = pygame.font.SysFont(None, 40)

class gd: #Global data
    #The colors list used by the program in determining what color to draw stuff
    colors = [ (0, 0, 0),        #Black
               (255, 255, 255),  #White
               (255, 0, 0),      #Red
               (0, 128, 0),      #Green
               (0, 0, 255),      #Blue
               (255, 0, 255),    #Fuchsia
               (255, 255, 0),    #Yellow
               (0, 255, 0),      #Lime
               (192, 192, 192),  #Silver
             ]

    #A copy of the colors list for resetting it back to normal when changed
    normalColors = list(colors) # normalColors = colors[:] would also work

def pause_screen(score):
    '''
    Prints a rectangle for the background of the menu and then
    prints some text containing game commands and the current
    colors in effect. Also allows for editting the current colors.
    '''
    def print_pause_blocks(y):
        '''
        Prints a small block for each active color in a line
        at the given y value
        '''
        for i, color in enumerate(gd.colors):
            x = 50 + (i * 20)
            colorRect = pygame.Rect( x, y, 15, 15)
            pygame.draw.rect(window, color, colorRect)

    bgcolor = (220, 220, 220)
    pause = True
    pauseText = [ 'GAME PAUSED',
                  'A/left: Left',
                  'D/right: Right',
                  'S/down: Go faster',
                  'Normal Mode: J',
                  'Hard Mode: K',
                  'Random Mode: L',
                  'Quit: Q',
                  'Return with any other key' ]

    #The +1 after getting the length is for the bottom line of blocks
    rect_bottom = 35 + (len(pauseText) + 1) * 27
    pygame.draw.rect(window, bgcolor, (35, 170, 215, rect_bottom))

    incrementx = 50
    incrementy = 180

    for line in pauseText:
        text = mainFont.render(line, False, gd.colors[0], bgcolor)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = incrementy
        screen.blit(text, textRect)
        incrementy += 30

    print_pause_blocks(incrementy)

    scoreString = 'Score: ' + str(score)
    scoreText = blockFont.render(scoreString, False, gd.colors[0], bgcolor)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.centerx, scoreTextRect.centery = screen.get_rect().centerx, 90
    screen.blit(scoreText, scoreTextRect)
    
    pygame.display.update()

    while pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key in [ord('j'), ord('J')]:
                    gd.colors = list(gd.normalColors)
                    print_pause_blocks(incrementy)
                elif event.key in [ord('k'), ord('K')]:
                    for i in range(2, len(gd.colors)):
                        gd.colors[i] = gd.colors[1]
                    print_pause_blocks(incrementy)
                elif event.key in [ord('l'), ord('L')]:
                    for i in range(2, len(gd.colors)):
                        gd.colors[i] = (random.randrange(1, 255),
                                        random.randrange(1, 255),
                                        random.randrange(1, 255))
                    print_pause_blocks(incrementy)
                elif event.key in [ord('q'), ord('Q')]:
                    pygame.quit()
                    sys.exit()
                #To avoid unpausing if the user presses either shift key
                elif event.key not in [K_LSHIFT, K_RSHIFT]:
                    pause = False
        pygame.display.update()

def get_block_num():
    '''
    This function is called for each block when it is created.
    It attempts to keep a reasonable distribution of block numbers.
    '''
    randNum = random.randrange(1, 101)
    if randNum < 33:
        return 1
    elif randNum < 60:
        return 2
    elif randNum < 75:
        return 3
    elif randNum < 85:
        return 4
    elif randNum < 97:
        return 5
    else:
        return 7

def spawn_blocks(blockList, curBlock):
    '''
    Take topBlocks as an argument and spawns a block in the
    top left and/or top right of the screen if necessary.
    Also gives a block a nudge towards the center if necessary.
    '''
    windowCenter = windowWidth / 2

    #0: top left, -1: top right
    for i in [-1, 0]:
        if blockList[i][0] == 0:
            new_number = get_block_num()
            blockList[i][0] = new_number
            blockList[i][1] = pygame.Rect(i * -240, 0, blockSize, blockSize)
            text = blockFont.render(str(new_number), False,
                                    gd.colors[0], gd.colors[new_number])
            blockList[i][2] = text.get_rect()

    if blockList[3][0] == 0 and (blockList[2][0] or blockList[4][0]):
        if random.randrange(2):
            order = [2, 4]
        else: order = [4, 2] 
        for i in order:
            if blockList[i][0]:
                if blockList[i][1].centerx < windowCenter:
                    blockList[i][1].centerx += 4
                elif blockList[i][1].centerx > windowCenter:
                    blockList[i][1].centerx -= 4
                blockList[3] = list(blockList[i])
                blockList[i][0] = 0
                break

    if blockList[3][0] and not curBlock[0]:
        if blockList[3][1].centerx == windowCenter:
            curBlock = list(blockList[3])
            blockList[3][0] = 0
    
    return blockList, curBlock

def check_overlap(block, direction, blockList, range=0):
    '''
    Checks the given blockList for a collision with the given block
    if it moves in the given direction.
    '''
    directionOffset = {'left':[-blockSize, 0], 'right':[blockSize, 0],
                       'up':[0, -blockSize], 'down':[0, blockSize]}
    offset = directionOffset[direction]
    checkLocX = block.centerx + offset[0]
    checkLocY = block.centery + offset[1]
   
    for target in blockList:
        if target[0] == 0: continue
        if target[1].centerx == checkLocX and target[1].centery == checkLocY:
            return True
    return False

def update_topBlock(block, topBlocks):
    '''
    Keeps all the topBlocks moving towards the center.
    '''
    if block[0] == 0: return block

    windowCenter = windowWidth / 2
    leftBound = windowCenter - blockSize
    rightBound = windowCenter + blockSize
    if block[1].centerx < windowCenter and block[1].centerx != leftBound:
        if not check_overlap(block[1], 'right', topBlocks):
            block[1].centerx += 4
    elif block[1].centerx > windowCenter and block[1].centerx != rightBound:
        if not check_overlap(block[1], 'left', topBlocks):
            block[1].centerx -= 4

    if block[1].left%40 == 0:
        topBlocks[int(block[1].left / 40)] = list(block)
        block[0] = 0

    return block

def move_curBlock(block):
    if block[0] == 0: return block
    windowBottom = windowHeight
    
    if block[1].bottom == windowHeight:
        block[0] = 0
    else: block[1].centery += 4

    return block

def print_blocks(blocks):
    for block in blocks:
        if block[0] != 0:
            pygame.draw.rect(window, gd.colors[block[0]], block[1])
            blockNum = blockFont.render(str(block[0]), False,
                                        gd.colors[0], gd.colors[block[0]])
            block[2].centerx = block[1].centerx
            block[2].centery = block[1].centery
            screen.blit(blockNum, block[2])
    pygame.display.update()

def main():
    moveSpeed = 4
    moveSide = 0
    score = 0
    sleepTime = 40 #Amount of time to pause between game loops
    pause_screen(score)

    #7 is the number of columns, 13 is the number of rows
    topBlocks = [ [0, None, None] for i in range(7) ]
    curBlock = [0, None, None]
    fallenBlocks = [ [0, None, None] for i in range(7) for j in range(13) ]
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key in [ord('a'), ord('A')]:
                    pass
                if event.key == K_RIGHT or event.key in [ord('d'), ord('D')]:
                    pass
                if event.key == K_DOWN or event.key in [ord('s'), ord('S')]:
                    sleepTime = 100
                if event.key in [ord('p'), ord('P')]:
                    pause_screen(score)
            if event.type == KEYUP:
                if event.key == K_DOWN or event.key in [ord('s'), ord('S')]:
                    sleepTime = 40

        window.fill(gd.colors[0])
        for i in range(0, 280, 40):
            pygame.draw.line(window, gd.colors[8], (i,40), (i,windowHeight), 1)
        pygame.draw.line(window, gd.colors[8], (0, 40), (120, 40), 1)
        pygame.draw.line(window, gd.colors[8], (160, 40), (280, 40), 1)

        #Spawn new blocks
        topBlocks, curBlock = spawn_blocks(topBlocks, curBlock)

        for block in topBlocks:
            block = update_topBlock(block, topBlocks)

        curBlock = move_curBlock(curBlock)

        allBlocks = topBlocks + [curBlock] #+ fallenBlocks
        print_blocks(allBlocks)

        clock.tick(sleepTime)

main()
