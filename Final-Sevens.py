#Final Sevens rewrite

import sys
import random

import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
WINDOWWIDTH = 280
WINDOWHEIGHT = 560
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Final Sevens')
screen = pygame.display.get_surface()

BLOCKSIZE = 40
MOVESPEED = BLOCKSIZE / 10
ROWS = 13
COLS = 7

mainFont = pygame.font.SysFont(None, 19) #Pause menu text
blockFont = pygame.font.SysFont(None, 40) #Block numbers and pause menu score

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
    normalColors = list(colors)

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
        tinyBlock = BLOCKSIZE * (3./8.)
        for i, color in enumerate(gd.colors):
            x = WINDOWWIDTH * (50./280.) + (i * tinyBlock * (4./3.))
            colorRect = pygame.Rect(x, y, tinyBlock, tinyBlock)
            pygame.draw.rect(window, color, colorRect)

    bgcolor = (220, 220, 220)
    pause = True
    reset = False
    pauseText = [ 'GAME PAUSED',
                  'A/left: Left',
                  'D/right: Right',
                  'S/down: Go faster',
                  'Toggle Reset: R',
                  'Normal Mode: J',
                  'Hard Mode: K',
                  'Random Mode: L',
                  'Quit: Q',
                  'Return with any other key' ]

    #The +1 after getting the length is for the bottom line of blocks
    rowsNum = len(pauseText) + 1
    left = WINDOWWIDTH * (35./280.)
    right = WINDOWWIDTH * (170./280.)
    top = WINDOWHEIGHT * (215./560.)
    bottom = rowsNum * BLOCKSIZE * (3./4.)
    pygame.draw.rect(window, bgcolor, (left, right, top, bottom))

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
    scoreTextRect.centerx,scoreTextRect.centery = screen.get_rect().centerx,90
    screen.blit(scoreText, scoreTextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('r'):
                    resetStr = "RESET IS ACTIVE!"
                    if reset:
                        reset = False
                        resetText = mainFont.render(resetStr, 1, bgcolor)
                    else:
                        reset = True
                        resetText = mainFont.render(resetStr, 1, (255, 0, 0))
                    screen.blit(resetText, (WINDOWWIDTH/3, incrementy - 15))
                elif event.key in [ord('j'), ord('J')]:
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
    return reset

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

def spawn_blocks(topBlocks, botBlocks):
    windowCenter = WINDOWWIDTH / 2
    curBlockCol = int(COLS/2)

    for i in [0, -1]: #0: top left, -1: top right
        block = topBlocks[i]
        if block[0] == 0:
            new_number = get_block_num()
            block[0] = new_number
            block[1] = pygame.Rect(i * -240, 0, BLOCKSIZE, BLOCKSIZE)
            text = blockFont.render(str(new_number), False,
                                    gd.colors[0], gd.colors[new_number])
            block[2] = text.get_rect()
            if i: block[3] = 'left'
            else: block[3] = 'right'

    if topBlocks[3][0] == 0 and (topBlocks[2][0] or topBlocks[4][0]):
        order = [2, 4]
        random.shuffle(order)
        for i in order:
            if topBlocks[i][0]:
                if topBlocks[i][1].centerx < windowCenter:
                    topBlocks[i][1].centerx += 4
                elif topBlocks[i][1].centerx > windowCenter:
                    topBlocks[i][1].centerx -= 4
                topBlocks[3] = topBlocks[i][:]
                topBlocks[i][0] = 0
                break

    if topBlocks[3][0] and not botBlocks[curBlockCol][0][0]:
        if topBlocks[3][1].centerx == windowCenter:
            topBlocks[3][3] = 'down'
            botBlocks[curBlockCol][0] = list(topBlocks[3])
            topBlocks[3][0] = 0
    
    return topBlocks, botBlocks

def print_block(block):
    if block[0] == 0: return
    pygame.draw.rect(window, gd.colors[block[0]], block[1])
    blockNum = blockFont.render(str(block[0]), False,
                                gd.colors[0], gd.colors[block[0]])
    block[2].centerx = block[1].centerx
    block[2].centery = block[1].centery
    screen.blit(blockNum, block[2])

def check_overlap(loc, blocks):
    for block in blocks:
        if block[0] != 0 and loc == [block[1].centerx, block[1].centery]:
            return True
    return False

def move_blocks(blocks, btype):
    windowCenter = WINDOWWIDTH / 2
    topStops = [windowCenter, windowCenter-BLOCKSIZE, windowCenter+BLOCKSIZE]
    directionMap = {'left': [-MOVESPEED,0], 'right': [MOVESPEED,0],
                             'up':[0,-MOVESPEED], 'down':[0,MOVESPEED]}

    for block in blocks:
        if block[0] == 0 or (btype == 'top' and block[1].centerx in topStops):
            continue

        #This assumes that the blocks are moving at 1/10 of the block's size
        targetx = block[1].centerx + directionMap[block[3]][0] * 10
        targety = block[1].centery + directionMap[block[3]][1] * 10

        bottom = block[1].bottom
        if check_overlap([targetx, targety], blocks) or bottom == WINDOWHEIGHT:
            if btype == 'bot':
                blocks[(block[1].top / BLOCKSIZE) - 1] = block[:]
                block[0] = 0
            continue

        block[1].centerx += directionMap[block[3]][0]
        block[1].centery += directionMap[block[3]][1]

        if btype == 'top' and not bool(block[1].left % BLOCKSIZE):
            blocks[block[1].left / BLOCKSIZE] = block[:]
            block[0] = 0

    return blocks

def setup_blocks(cols, rows):
    #Block format [number, rect, number rect, direction]
    blockf = [0, None, None, None]
    topBlocks = [ blockf[:] for i in range(cols) ]
    botBlocks = [ [ blockf[:] for i in range(cols) ] for j in range(rows) ]
    
    return topBlocks, botBlocks

def main():
    moveSide = 0
    score = 0
    gameSpeed = 40
    pause_screen(score)

    topBlocks, botBlocks = setup_blocks(ROWS, COLS)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in [K_LEFT, ord('a'), ord('A')]:
                    moveSide = 'left'
                elif event.key in [K_RIGHT, ord('d'), ord('D')]:
                    moveSide = 'right'
                elif event.key in [K_DOWN, ord('s'), ord('S')]:
                    gameSpeed = 120
                elif event.key in [ord('p'), ord('P')]:
                    if pause_screen(score):
                        topBlocks, botBlocks = setup_blocks(ROWS, COLS)
                        score = 0
            elif event.type == KEYUP:
                if event.key in [K_DOWN, ord('s'), ord('S')]:
                    gameSpeed = 40

        #This draws the background
        window.fill(gd.colors[0])
        for i in range(0, 280, 40):
            pygame.draw.line(window, gd.colors[8], (i,40), (i,WINDOWHEIGHT), 1)
        pygame.draw.line(window, gd.colors[8], (0, 40), (120, 40), 1)
        pygame.draw.line(window, gd.colors[8], (160, 40), (280, 40), 1)

        #Spawn new blocks
        topBlocks, botBlocks = spawn_blocks(topBlocks, botBlocks)

        topBlocks = move_blocks(topBlocks, 'top')
        for col in botBlocks:
            col = move_blocks(col, 'bot')

        #Add all the blocks to a single list which is passed to a print function
        allBlocks = topBlocks[:]
        allBlocks.extend(block for line in botBlocks for block in line)
        map(print_block, allBlocks)
        pygame.display.update()

        if botBlocks[3][0][0] != 0 and botBlocks[3][1][0]:
            break #Game over

        clock.tick(gameSpeed)

    print("Thanks for playing!")
    print("Your score: %s" %(score)) 

main()
