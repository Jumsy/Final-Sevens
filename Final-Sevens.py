# Final Sevens rewrite

import sys
import random

import pygame
from pygame.locals import *

from Classes import Colors, Shape

MOVESPEED = 2
BLOCKSIZE = 20

BLOCK_AREA_WIDTH = 280
BLOCK_AREA_HEIGHT = 560

MenuSize = 0
WINDOWWIDTH = BLOCK_AREA_WIDTH + MenuSize
WINDOWHEIGHT = BLOCK_AREA_HEIGHT

ROWS = BLOCK_AREA_HEIGHT / BLOCKSIZE
COLS = BLOCK_AREA_WIDTH / BLOCKSIZE

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Final Sevens')
screen = pygame.display.get_surface()

# Pause menu text
mainFont = pygame.font.SysFont(None, BLOCKSIZE)
# Block number/pause menu score
blockFont = pygame.font.SysFont(None, int(BLOCKSIZE*1.4))

colors = Colors()

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
        tinyBlock = BLOCKSIZE * (3./4.)
        xOffset = int(WINDOWWIDTH / 15)
        for i in range(1, len(colors.colors) + 1):
            x = xOffset + (i * (3./4.) * (WINDOWWIDTH / len(colors.colors)))
            colorRect = pygame.Rect(x, y, tinyBlock, tinyBlock)
            pygame.draw.rect(window, colors.colors[i-1], colorRect)

    pause = True
    reset = False
    pauseText = [ 'GAME PAUSED',
                  'A-D/left-right: Move',
                  'S/down: Go faster',
                  'W/up: Rotate',
                  'Toggle Reset: R',
                  'Normal Mode: J',
                  'Hard Mode: K',
                  'Random Mode: L',
                  'Quit: Q',
                  'Return with any other key' ]

    # These numbers are just to get good screen ratios for the menu block
    x = int(WINDOWWIDTH / 10)
    y = int(WINDOWHEIGHT / 5)
    horizontal = WINDOWWIDTH - (2 * x)
    vertical = WINDOWHEIGHT - (1.2 * y)

    pygame.draw.rect(window, colors.silver, (x, y, horizontal, vertical))

    incrementy = y + int(WINDOWHEIGHT / 30)

    for line in pauseText:
        text = mainFont.render(line, False, colors.black, colors.silver)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = incrementy
        screen.blit(text, textRect)
        incrementy += int(WINDOWHEIGHT / 15)

    print_pause_blocks(incrementy)

    y = int(WINDOWHEIGHT / 10)
    scoreString = 'Score: ' + str(score)
    scoreText = blockFont.render(scoreString, False,
                                 colors.black, colors.silver)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.centerx,scoreTextRect.centery = screen.get_rect().centerx, y
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
                        resetText = mainFont.render(resetStr, 1, colors.silver)
                    else:
                        reset = True
                        resetText = mainFont.render(resetStr, 1, (255, 0, 0))
                    screen.blit(resetText, (WINDOWWIDTH/3, incrementy - 15))
                elif event.key in [ord('j'), ord('J')]:
                    colors.reset()
                    print_pause_blocks(incrementy)
                elif event.key in [ord('k'), ord('K')]:
                    colors.make_uniform()
                    print_pause_blocks(incrementy)
                elif event.key in [ord('l'), ord('L')]:
                    colors.randomize()
                    print_pause_blocks(incrementy)
                elif event.key in [ord('q'), ord('Q')]:
                    pygame.quit()
                    sys.exit("Your score: " + str(score))
                # To avoid unpausing if the user presses either shift key
                elif event.key not in [K_LSHIFT, K_RSHIFT]:
                    pause = False
        pygame.display.update()
    return reset

def get_block_num():
    '''
    This function is called for each block when it is created.
    Lower block numbers seem to be more useful, so spawn more often.
    7's should be rare enough that they're problematic.
    '''
    randNum = random.randrange(1, 101)
    if randNum < 25:
        return 1
    elif randNum < 50:
        return 2
    elif randNum < 80:
        return 3
    elif randNum < 90:
        return 4
    elif randNum < 98:
        return 5
    else:
        return 7

def spawn_blocks(curBlock):
    """Creates a new curBlock if one doesn't already exist.
    """
    if curBlock.exists:
        return curBlock

    one = BLOCKSIZE
    two = 2*BLOCKSIZE
    three = 3*BLOCKSIZE

    offsets = [ 
                [ [0, 0] ],                                    # Single block
                [ [0, 0], [one, 0] ],                          # Horizontal pair
                [ [0, 0], [0, one] ],                          # Vertical pair
                [ [0, 0], [one, 0], [one, one] ],              # 3-J
                [ [0, 0], [0, one], [one, one] ],              # 3-L
                [ [0, 0], [0, one], [0, two] ],                # 3 line
                ##### ^ Small pieces ## V Tetris-sized pieces #####
                #[ [0, 0], [one, 0], [two, 0], [two, one] ],    # 4-L
                #[ [0, one], [one, one], [two, one], [two, 0] ],# 4-L
                #[ [0, 0], [0, one], [0, two], [one, one] ],    # T
                #[ [0, 0], [0, one], [0, two], [0, three] ],    # 4 line
                #[ [0, 0], [one, 0], [one, one], [two, one] ],  # Z
                #[ [0, one], [one, one], [one, 0], [two, 0] ],  # S
              ]

    blockOffset = random.choice(offsets)
    blocks = []

    midCol = int(COLS/2)
    x_start = midCol * BLOCKSIZE
    y_start = 0

    for offset in blockOffset:
        block = [get_block_num()]
        text = blockFont.render(str(block[0]), False,
                                colors.black, colors.colors[block[0] - 1])
        block.append(pygame.Rect(x_start + offset[0], y_start + offset[1],
                                 BLOCKSIZE, BLOCKSIZE))
        block.append(text.get_rect())
        blocks.append(block)

    curBlock.set_new(blocks)

    return curBlock 

def print_block(block):
    """Prints the given block to the screen
    """
    if block[0] == 0: return
    pygame.draw.rect(window, colors.colors[block[0] - 1], block[1])
    blockNum = blockFont.render(str(block[0]), False,
                                colors.black, colors.colors[block[0] - 1])
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

def move_blocks(blocks):
    """This function takes a list of blocks and moves them all downwards.
    botBlocks is given to this function one column at a time and every
    block in the column is moved until they hit the bottom of the screen
    or another block.
    Each location in the given list represents a location on the board. When
    a block has moved past the board location that the block's location in
    the list references, then the block must be moved within its list.
    If a block in botBlocks hits the bottom of the screen, then a block is
    returned so that the score function can see if the block needs to be
    taken away.
    """

    scoreBlock = False
    windowCenter = BLOCK_AREA_WIDTH / 2
    direction = [0, MOVESPEED]

    for block in blocks:
        if not block[0] or block[1].bottom >= BLOCK_AREA_HEIGHT:
            continue

        # This assumes that the blocks are moving at 1/10 of the block's size
        targetx = block[1].centerx + direction[0] * 10
        targety = block[1].centery + direction[1] * 10

        if check_overlap([targetx, targety], blocks):
            continue

        block[1].centerx += direction[0]
        block[1].centery += direction[1]

        if not bool(block[1].top % BLOCKSIZE):
            scoreBlock = block[:]
            row = (block[1].top / BLOCKSIZE) - 1
            blocks[row] = block[:]
            block[0] = 0

    return blocks, scoreBlock

def move_curBlock(curBlock, botBlocks, moveSide, rotate):
    """This function moves the player-controlled curBlock downwards until
    it hits the bottom of the screen or another block. If the player wishes
    to move right or left, the argument 'moveSide' will reflect the direction.
    If the curBlock stops, then its component blocks are returned as
    scoreBlocks so that they can get checked by score function to determine
    whether they need to be destroyed.
    This function first does horizontal movement, then vertical.
    """

    scoreBlocks = False
    if not curBlock.exists:
        return curBlock, botBlocks, scoreBlocks

    blocks = curBlock.get_printable_blocks()

    if rotate:
        toRotate = True
        newPositions = curBlock.rotate()
        if newPositions:
            for block in newPositions:
                tarCol = botBlocks[int(block[0] / BLOCKSIZE)]
                if check_overlap(block, tarCol, BLOCKSIZE/2):
                    toRotate = False
                    break
            if toRotate:
                curBlock.sync(newPositions)

    if moveSide:
        toMove = True
        for block in blocks:
            target = block[1].centerx + moveSide
            if target < 0 or target > BLOCK_AREA_WIDTH:
                toMove = False
                break
            tarCol = botBlocks[int(target / BLOCKSIZE)]
            # The distance to check for an overlap in check_overlap()
            dist = BLOCKSIZE - MOVESPEED
            if check_overlap([target, block[1].centery], tarCol, dist):
                toMove = False
                break
        if toMove:
            curBlock.move('x', moveSide)

    toStop = False
    for block in blocks:
        row = int(block[1].top / BLOCKSIZE) - 1
        col = int(block[1].left / BLOCKSIZE)
        if block[1].bottom == BLOCK_AREA_HEIGHT or botBlocks[col][row + 1][0]:
            toStop = True
            break

    if toStop:
        for block in blocks:
            row = int(block[1].top / BLOCKSIZE) - 1
            col = int(block[1].left / BLOCKSIZE)
            botBlocks[col][row] = block
        scoreBlocks = curBlock.get_printable_blocks()
        curBlock.delete()
    else:
        curBlock.move('y', MOVESPEED)

    return curBlock, botBlocks, scoreBlocks

def score_check(botBlocks, score, newBlock):
    """This function takes a recently fallen block as newBlock
    and searches botBlocks for all available triples that could
    be made from this block. If the triple is valid and the 
    blocks composing it add to 7 or 21, score is updated and the
    blocks are removed.
    """

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
            scoreSum += block[0]

        if len(blockList) == 3 and (scoreSum == 7 or scoreSum == 21):
            if scoreSum == 7:
                score += 1
            elif scoreSum == 21:
                score += 50
            for block in blockList:
                block[0] = 0

    return botBlocks, score

def setup_blocks(cols, rows):
    """Returns the two lists of blocks with their starting values
    In the beginning of the game this is just for initializing the
    blocks, but later it is used to reset the game without quitting.
    """

    # Block format [number, rect, number rect]
    blockf = [0, None, None]
    curBlock = Shape()
    botBlocks = [ [ blockf[:] for i in range(cols) ] for j in range(rows) ]
    
    return curBlock, botBlocks

def main():
    score = 0
    slow = 40
    fast = 320
    gameSpeed = slow
    pause_screen(score)

    curBlock, botBlocks = setup_blocks(ROWS, COLS)

    while True:
        rotate = False
        moveSide = 0
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
                    gameSpeed = fast
                elif event.key in [K_UP, ord('w'), ord('W')]:
                    rotate = True
                elif event.key in [ord('p'), ord('P')]:
                    if pause_screen(score):
                        score = 0
                        curBlock, botBlocks = setup_blocks(ROWS, COLS,)
            elif event.type == KEYUP:
                if event.key in [K_DOWN, ord('s'), ord('S')]:
                    gameSpeed = slow

        # Draw the background
        window.fill(colors.black)
        menu_dimensions = ( BLOCK_AREA_WIDTH,
                            0,
                            WINDOWWIDTH - BLOCK_AREA_WIDTH,
                            WINDOWHEIGHT, )
                            
        pygame.draw.rect(window, colors.silver, menu_dimensions)
        for i in range(0, BLOCK_AREA_WIDTH, BLOCKSIZE):
            pygame.draw.line(window, colors.off_black, (i, 0),
                             (i,BLOCK_AREA_HEIGHT), 1)

        # Spawn new falling blocks
        curBlock = spawn_blocks(curBlock) 

        # Move fallen blocks
        scoreBlocks = []
        for col in botBlocks:
            col, tmp = move_blocks(col)
            if tmp: scoreBlocks.append(tmp)

        # Move player controlled block
        curBlock, botBlocks, tmp = move_curBlock(curBlock, botBlocks, moveSide, rotate)
        if tmp: scoreBlocks.extend(block for block in tmp)

        # Update score and get rid of any groups totaling 7 or 21
        for block in scoreBlocks:
            botBlocks, score = score_check(botBlocks, score, block)

        # Add all the blocks to one list which is passed to a print function
        allBlocks = curBlock.get_printable_blocks()
        allBlocks.extend(block for line in botBlocks for block in line)
        map(print_block, allBlocks)
        pygame.display.update()

        if botBlocks[int(COLS/2)][0][0]:
            break # Game over. A block was in the spawning area

        clock.tick(gameSpeed)

    print("Thanks for playing!")
    print("Your score: %s" %(score)) 

main()
