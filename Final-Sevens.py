#Final Sevens rewrite

import sys
import random
from pprint import pprint

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
    """
    Prints a rectangle for the background of the menu and then
    prints some text containing game commands and the current
    colors in effect. Also allows for editing the current colors
    and resetting all the blocks.
    """
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

def spawn_blocks(topBlocks, curBlock):
    windowCenter = WINDOWWIDTH / 2
    midCol = int(COLS/2)

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

    if topBlocks[3][0] and not curBlock[0]:
        if topBlocks[3][1].centerx == windowCenter:
            topBlocks[3][3] = 'down'
            curBlock = list(topBlocks[3])
            topBlocks[3][0] = 0
    
    return topBlocks, curBlock 

def print_block(block):
    if block[0] == 0: return
    pygame.draw.rect(window, gd.colors[block[0]], block[1])
    blockNum = blockFont.render(str(block[0]), False,
                                gd.colors[0], gd.colors[block[0]])
    block[2].centerx = block[1].centerx
    block[2].centery = block[1].centery
    screen.blit(blockNum, block[2])

def check_overlap(loc, blocks, yrange=0):
    """
    loc is the location that is checked given in [x, y] format.
    blocks is a list of blocks where the overlap is possible.
    yrange is for checking for a block within a certain range.
    """
    for block in blocks:
        if block[0] != 0:
            ydistance = abs(block[1].centery - loc[1])
            if ydistance <= yrange and block[1].centerx == loc[0]:
                return True
    return False

def move_blocks(blocks, btype):
    scoreBlock = False
    windowCenter = WINDOWWIDTH / 2
    topStops = [windowCenter, windowCenter-BLOCKSIZE, windowCenter+BLOCKSIZE]
    directionMap = {'left': [-MOVESPEED,0], 'right': [MOVESPEED,0],
                    'down':[0,MOVESPEED]}

    for block in blocks:
        if not block[0] or ((btype == 'top' and block[1].centerx in topStops)
                       or (btype == 'bot' and block[1].bottom >= WINDOWHEIGHT)):
            continue

        #This assumes that the blocks are moving at 1/10 of the block's size
        targetx = block[1].centerx + directionMap[block[3]][0] * 10
        targety = block[1].centery + directionMap[block[3]][1] * 10

        if check_overlap([targetx, targety], blocks):
            continue

        block[1].centerx += directionMap[block[3]][0]
        block[1].centery += directionMap[block[3]][1]

        if btype == 'top' and not bool(block[1].left % BLOCKSIZE):
            blocks[block[1].left / BLOCKSIZE] = block[:]
            block[0] = 0

        if btype == 'bot' and not bool(block[1].top % BLOCKSIZE):
            scoreBlock = block[:]
            row = (block[1].top / BLOCKSIZE) - 1
            blocks[row] = block[:]
            block[0] = 0

    return blocks, scoreBlock

def move_curBlock(curBlock, botBlocks, moveSide):
    scoreBlock = False
    if not curBlock[0]:
        return curBlock, botBlocks, scoreBlock

    if moveSide:
        target = curBlock[1].centerx + moveSide
        if target > 0 and target < WINDOWWIDTH:
            tarCol = botBlocks[int(target / BLOCKSIZE)]
            if not check_overlap([target, curBlock[1].centery], tarCol, 36):
                curBlock[1].centerx = target

    row = int(curBlock[1].top / BLOCKSIZE) - 1
    col = int(curBlock[1].left / BLOCKSIZE)

    newLoc = [curBlock[1].centerx, curBlock[1].centery + BLOCKSIZE]
    botCol = botBlocks[col]

    if curBlock[1].bottom == WINDOWHEIGHT or botBlocks[col][row + 1][0]:
        botBlocks[col][row] = curBlock[:]
        scoreBlock = curBlock[:]
        curBlock[0] = 0
        return curBlock, botBlocks, scoreBlock

    curBlock[1].centery += MOVESPEED

    return curBlock, botBlocks, scoreBlock

def score_check(botBlocks, score, newBlock):
    col = newBlock[1].left / BLOCKSIZE
    row = (newBlock[1].top / BLOCKSIZE) - 1
    
    triples = [ [[col - 2, row], [col - 1, row], [col, row]],
                [[col - 1, row], [col, row], [col + 1, row]],
                [[col, row], [col + 1, row], [col + 2, row]],
                [[col, row - 2], [col, row - 1], [col, row]],
                [[col, row - 1], [col, row], [col, row + 1]],
                [[col, row], [col, row + 1], [col, row + 2]], ]

    validRows = list(range(ROWS))
    validCols = list(range(COLS))

    validTriples = []

    for triple in triples:
        isValid = True
        for loc in triple:
            if loc[0] not in validCols or loc[1] not in validRows:
                isValid = False
                break
        if isValid:
            validTriples.append(triple)

    for triple in validTriples:
        blockList = []
        scoreSum = 0
        for loc in triple:
            block = botBlocks[loc[0]][loc[1]]
            if not block[0]: break
            blockList.append(block)
            if isinstance(block[0], list): print "block: ", block
            scoreSum += block[0]

        if len(blockList) == 3 and (scoreSum == 7 or scoreSum == 21):
            score += scoreSum
            for block in blockList:
                block[0] = 0

    return botBlocks, score

def setup_blocks(cols, rows):
    #Block format [number, rect, number rect, direction]
    blockf = [0, None, None, None]
    topBlocks = [ blockf[:] for i in range(cols) ]
    curBlock = blockf[:]
    botBlocks = [ [ blockf[:] for i in range(cols) ] for j in range(rows) ]
    
    return topBlocks, curBlock, botBlocks

def main():
    moveSide = 0
    score = 0
    gameSpeed = 40
    pause_screen(score)

    topBlocks, curBlock, botBlocks = setup_blocks(ROWS, COLS)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key in [K_LEFT, ord('a'), ord('A')]:
                    moveSide = -BLOCKSIZE
                elif event.key in [K_RIGHT, ord('d'), ord('D')]:
                    moveSide = BLOCKSIZE
                elif event.key in [K_DOWN, ord('s'), ord('S')]:
                    gameSpeed = 120
                elif event.key in [ord('p'), ord('P')]:
                    if pause_screen(score):
                        score = 0
                        topBlocks, curBlock, botBlocks = setup_blocks(ROWS,
                                                                      COLS,)
            elif event.type == KEYUP:
                if event.key in [K_DOWN, ord('s'), ord('S')]:
                    gameSpeed = 40

        #Draw the background
        window.fill(gd.colors[0])
        for i in range(0, 280, 40):
            pygame.draw.line(window, gd.colors[8], (i,40), (i,WINDOWHEIGHT), 1)
        pygame.draw.line(window, gd.colors[8], (0, 40), (120, 40), 1)
        pygame.draw.line(window, gd.colors[8], (160, 40), (280, 40), 1)

        #Spawn new blocks
        topBlocks, curBlock = spawn_blocks(topBlocks, curBlock) 

        #Move blocks
        topBlocks, _ = move_blocks(topBlocks, 'top')
        scoreBlocks = []
        for col in botBlocks:
            col, tmp = move_blocks(col, 'bot')
            if tmp: scoreBlocks.append(tmp[:])

        #Move player controlled block
        curBlock, botBlocks, tmp = move_curBlock(curBlock, botBlocks, moveSide)
        if tmp: scoreBlocks.append(tmp[:])

        moveSide = 0
        for block in scoreBlocks:
            botBlocks, score = score_check(botBlocks, score, block)

        #Add all the blocks to a single list which is passed to a print function
        allBlocks = topBlocks[:] + [curBlock]
        allBlocks.extend(block for line in botBlocks for block in line)
        map(print_block, allBlocks)
        pygame.display.update()

        if botBlocks[3][0][0] != 0:
            break #Game over

        clock.tick(gameSpeed)

    print("Thanks for playing!")
    print("Your score: %s" %(score)) 

main()
