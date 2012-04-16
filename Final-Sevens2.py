#Final Sevens rewrite
#April 13th, 2012

import sys
import random
import time
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
windowWidth = 280
windowHeight = 560
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Final Sevens')
screen = pygame.display.get_surface()

class gd: #Global data
    #The colors list used by the program in determining what color to draw things
    colors = [ (0, 0, 0),        #Black
               (255, 255, 255), #White
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

#For normal writing (like menus)
mainFont = pygame.font.SysFont(None, 19)
#For writing on the blocks
blockFont = pygame.font.SysFont(None, 40)

def pause_screen(score):

    def print_pause_blocks(y):
        for i, color in enumerate(gd.colors):
            x = 50 + (i * 20)
            colorRect = pygame.Rect( x, y, 15, 15)
            pygame.draw.rect(window, color, colorRect)

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

    #The +1 after getting the length of pause is for the bottom line of blocks
    rect_bottom = 35 + (len(pauseText) + 1) * 27
    pygame.draw.rect(window, (240, 240, 240), (35, 170, 215, rect_bottom))

    incrementx = 50
    incrementy = 180

    for line in pauseText:
        text = mainFont.render(line, False, gd.colors[0], (240, 240, 240))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = incrementy
        screen.blit(text, textRect)
        incrementy += 30

    print_pause_blocks(incrementy)

    scoreString = 'Score: ' + str(score)
    scoreText = blockFont.render(scoreString, False, gd.colors[0], (240, 240, 240))
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
                elif event.key not in [K_LSHIFT, K_RSHIFT]:
                    pause = False
        pygame.display.update()

def get_block_num():
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

def spawn_blocks(blockList):
    blockSize = 40
    #0: top left, -1: top right
    for i in range(0, -2, -1):
        if blockList[i][0] == 0:
            new_number = get_block_num()
            blockList[i][0] = new_number
            blockList[i][1] = pygame.Rect(i * -240, 0, blockSize, blockSize)
            text = blockFont.render(str(new_number), False,
                                    gd.colors[0], gd.colors[new_number])
            blockList[i][2] = text.get_rect()
    return blockList

def update_topBlock(block):
    if block[0] == 0: return block

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
    pause_screen(score)

    topBlocks = [ [0, None, None] for i in range(7) ]
    
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
                    pass
                if event.key in [ord('p'), ord('P')]:
                    pause_screen(score)
            if event.type == KEYUP:
                if event.key == K_DOWN or event.key in [ord('s'), ord('S')]:
                    pass

        window.fill(gd.colors[0])
        for i in range(0, 280, 40):
            pygame.draw.line(window, gd.colors[8], (i, 40), (i, windowHeight), 1)
        pygame.draw.line(window, gd.colors[8], (0, 40), (120, 40), 1)
        pygame.draw.line(window, gd.colors[8], (160, 40), (280, 40), 1)

        topBlocks = spawn_blocks(topBlocks)

        for block in topBlocks:
            block = update_topBlock(block)

        allBlocks = topBlocks #+ [curBlock] + fallenBlocks
        print_blocks(allBlocks)

        clock.tick(40)

main()
