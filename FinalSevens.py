#Final Sevens
#June 5th, 2011

import pygame, sys, random, time
from pygame.locals import *

pygame.init()
gameClock = pygame.time.Clock()

#Set-up the screen
windowwidth = 280
windowheight = 560
window = pygame.display.set_mode((windowwidth, windowheight))
pygame.display.set_caption('Final Sevens')
screen = pygame.display.get_surface()

#Colors
Colors = []
Colors.append((0, 0, 0)) #Black
Colors.append((255, 255, 255)) #White
Colors.append((255, 0, 0)) #Red
Colors.append((0, 128, 0)) #Green
Colors.append((0, 0, 255)) #Blue
Colors.append((255, 0, 255)) #Fuchsia
Colors.append((255, 255, 0)) #Yellow
Colors.append((0, 255, 0)) #Lime
Colors.append((192, 192, 192)) #Silver

ColorsNorm = []
for i in range(len(Colors)):
    ColorsNorm.append(Colors[i])
    
ColorsRand = []
for i in range(len(Colors)):
    ColorsRand.append((random.randrange(1, 256), random.randrange(1, 256), random.randrange(1, 256)))

#Pause screen info
pauseScreenText = {}
pauseScreenText['main'] = {}
pauseScreenText['main'][0] = 'GAME PAUSED'
pauseScreenText['main'][1] = 'A/left: Left'
pauseScreenText['main'][2] = 'D/right: Right'
pauseScreenText['main'][3] = 'S/down: Go faster'
pauseScreenText['main'][4] = 'Normal Mode: J'
pauseScreenText['main'][5] = 'Hard Mode: K'
pauseScreenText['main'][6] = 'Random Mode: L'
pauseScreenText['main'][7] = 'Return with any other key'

#Font used for writing on the screen, blockFont used for the numbers in the blocks
Font = pygame.font.SysFont(None, 19)
blockFont = pygame.font.SysFont(None, 40)

topBlocks = {}
for i in range(7):
    topBlocks[i] = {}
    topBlocks[i][0] = 0
    topBlocks[i][1] = pygame.Rect(500, 500, 40, 40) #Junk data to avoid error in print_blocks()
    topBlocks[i][2] = pygame.Rect(500, 500, 40, 40)
topBlocks[7] = False
curBlock = {}
curBlock[0] = {} #Redundant zero needed to pass data into main() function. I don't know why...
curBlock[0][0] = 0
curBlock[0][1] = pygame.Rect(500, 500, 40, 40)
curBlock[0][2] = pygame.Rect(500, 500, 40, 40)
curTiles = {}
for i in range(7):
    curTiles[i] = {}
    for j in range(14):
        curTiles[i][j] = {}
        curTiles[i][j][0] = 0
        curTiles[i][j][1] = pygame.Rect(500, 500, 40, 40)
        curTiles[i][j][2] = pygame.Rect(500, 500, 40, 40)
curTiles[7] = True

def pause_text(menu):
    '''
    Increments through pauseScreenText to print relevant menu.
    '''
    pygame.draw.rect(window, (240, 240, 240), (35, 160, 215, 300))
    incrementy = 180
    incrementx = 50
    for key in pauseScreenText[menu]:
        Text = Font.render(pauseScreenText[menu][key], False, Colors[0], (240, 240, 240))
        TextRect = Text.get_rect()
        TextRect.centerx, TextRect.centery = screen.get_rect().centerx, incrementy
        screen.blit(Text, TextRect)
        incrementy += 30

    for i in range(len(Colors)):
        pygame.draw.rect(window, Colors[i], pygame.Rect(incrementx, incrementy, 15, 15))
        incrementx += 20
    return

def pause_screen(playerScore):
    """
    Prints the players score and waits for input before continuing
    """
    Unpause = 0
    pause_text('main')
    scoreText = blockFont.render('Score: '+str(playerScore), False, Colors[0], (240, 240, 240))
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.centerx, scoreTextRect.centery = screen.get_rect().centerx, 90
    screen.blit(scoreText, scoreTextRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('j'):
                    for i in range(len(Colors)):
                        Colors[i] = ColorsNorm[i]
                    pause_text('main')
                    pygame.display.update()
                elif event.key == ord('k'):
                    for i in range(len(Colors)):
                        if i == 0:
                            Colors[i] = ColorsNorm[0]
                        else: Colors[i] = ColorsNorm[1]
                    pause_text('main')
                    pygame.display.update()
                elif event.key == ord('l'):
                    for i in range(len(Colors)):
                        if i == 0:
                            Colors[i] = ColorsNorm[0]
                        else: Colors[i] = (random.randrange(1, 256), random.randrange(1, 256), random.randrange(1, 256))
                        pause_text('main')
                        pygame.display.update()
                else:
                    Unpause = 1
        if Unpause == 1:
            break

def create_background():
    """
    Fills the screen with black and draws the grey lines
    """
    window.fill(Colors[0])
    for i in range(0, 280, 40):
        pygame.draw.line(window, (192, 192, 192), (i, 40), (i, windowheight), 1)
    pygame.draw.line(window, (192, 192, 192), (0, 40), (120, 40), 1)
    pygame.draw.line(window, (192, 192, 192), (160, 40), (280, 40), 1)

def new_block_num():
    randNum = random.randrange(1,101)
    if randNum < 33:
        randNum = 1
    elif randNum < 60:
        randNum = 2
    elif randNum < 75:
        randNum = 3
    elif randNum < 85:
        randNum = 4
    elif randNum < 95:
        randNum = 5
    else:
        randNum = 7
    return randNum

def check_overlap(xl, xr, yt, yb, target):
    '''
    Returns True if the centers of any blocks in target overlap tarx, tary
    '''
    if xr == False: xr = xl
    if yb == False: yb = yt
    check = False
    if not target[7]: #Check topBlocks
        for i in range(7):
            if target[i][1].centerx >= xl and target[i][1].centerx <= xr:
                if target[i][1].centery >= yt and target[i][1].centery <= yb:
                    check = True
                    break
    elif target[7]: #Check curTiles
        for i in range(7):
            for j in range(14):
                if target[i][j][0] != 0:
                    if target[i][j][1].centerx >= xl and target[i][j][1].centerx <= xr:
                        if target[i][j][1].centery >= yt and target[i][j][1].centery <= yb:
                            check = True
                            break
    else:
        print("Error in check_overlap")
    return check

def move_dict(var1):
    var2 = {}
    for i in range(len(var1)):
        var2[i] = var1[i]
    return var2

def spawn_block():
    '''
    Spawns a block in either the top left(0), or top right(6)
    '''
    #Top left
    if topBlocks[0][0] == 0:
        topBlocks[0][0] = new_block_num()
        topBlocks[0][1] = pygame.Rect(0, 0, 40, 40)
        topBlocks[0][2] = blockFont.render(str(topBlocks[0][0]), False, Colors[0], Colors[topBlocks[0][0]]).get_rect()
    #Top right
    if topBlocks[6][0] == 0:
        topBlocks[6][0] = new_block_num()
        topBlocks[6][1] = pygame.Rect(240, 0, 40, 40)
        topBlocks[6][2] = blockFont.render(str(topBlocks[6][0]), False, Colors[0], Colors[topBlocks[6][0]]).get_rect()

def top_blocks(block):
    """
    Takes input of topBlock[x] and returns an updated topBlock[x] 
    """
    if block[0] == 0: return block #Block doesn't exist in current space
    if block[1].centerx < 140 and not check_overlap(block[1].centerx+40, False, 20, False, topBlocks) and block[1].centerx != 100:
        block[1].centerx += 4
        if block[1].left%40 == 0:
            topBlocks[int(block[1].left/40)] = move_dict(block)
            block[0] = 0
    elif block[1].centerx > 140 and not check_overlap(block[1].centerx-40, False, 20, False, topBlocks) and block[1].centerx != 180:
        block[1].centerx -= 4
        if block[1].left%40 == 0:
            topBlocks[int(block[1].left/40)] = move_dict(block)
            block[0] = 0
    elif block[1].centerx == 100 or block[1].centerx == 180:
        randNum = random.randrange(2)
        if randNum == 1 and not check_overlap(101, 179, 20, 20, topBlocks):
            block[1].centerx -= ((block[1].centerx-140)/10)
    return block

def cur_block(block, side, speed):
    """
    Takes input of curBlock returns an updated curBlock
    """
    score = 0
    if block[0] == 0:
        if topBlocks[3][0] != 0:
            block = move_dict(topBlocks[3])
            topBlocks[3][0] = 0
    else:
        #Move left/right if possible
        if side != 0 and not check_overlap(block[1].centerx+side, False, block[1].centery, block[1].centery+40, curTiles) and block[1].centerx+side >= 0 and block[1].centerx+side <= 280:
            block[1].centerx += side
            side = 0
        #Move down if possible, else move block to curTiles
        endValue = 540
        for i in range(14):
            if curTiles[int((block[1].centerx-20)/40)][i][0] != 0:
                endValue = curTiles[int((block[1].centerx-20)/40)][i][1].centery-40
                break
        if block[1].centery+speed > endValue:
            block[1].centery = endValue
            score, loseblock = score_calc()
            if not loseblock: curTiles[int((block[1].centerx-20)/40)][int((block[1].centery-20)/40)] = move_dict(block)
            block[0] = 0
        else:
            block[1].centery += speed
    return block, side, score

def cur_tiles(block):
    """
    Takes input of curTiles[x] and returns an updated curTiles[x]
    """
    if not check_overlap(block[1].centerx, False, block[1].centery+40, False, curTiles) and block[1].centery != 540:
        block[1].centery += 4
        if (block[1].centerx-20)%40 == 0 and (block[1].centery-20)%40 == 0:
            curTiles[int((block[1].centerx-20)/40)][int((block[1].centery-20)/40)] = move_dict(block)
            block[0] = 0
    return block

def score_calc():
    '''
    Searches for triples of 7's or of numbers adding to 7. If Successful, deletes the blocks in the triple and update the score.
    Searches horizontally where the curBlock is the center. Then searches left, right and down.
    '''
    loseBlock = False
    tripList = {}
    if curBlock[0][1].centerx >= 60 and curBlock[0][1].centerx <= 220:
        tripList[0] = [int((curBlock[0][1].centerx-20)/40-1), int((curBlock[0][1].centery-20)/40), int((curBlock[0][1].centerx-20)/40+1), int((curBlock[0][1].centery-20)/40)]
    if curBlock[0][1].centerx >= 100:
        tripList[1] = [int((curBlock[0][1].centerx-20)/40-2), int((curBlock[0][1].centery-20)/40), int((curBlock[0][1].centerx-20)/40-1), int((curBlock[0][1].centery-20)/40)]
    if curBlock[0][1].centerx <= 180:
        tripList[2] = [int((curBlock[0][1].centerx-20)/40+1), int((curBlock[0][1].centery-20)/40), int((curBlock[0][1].centerx-20)/40+2), int((curBlock[0][1].centery-20)/40)]
    if curBlock[0][1].centery <= 460:
        tripList[3] = [int((curBlock[0][1].centerx-20)/40), int((curBlock[0][1].centery-20)/40+1), int((curBlock[0][1].centerx-20)/40), int((curBlock[0][1].centery-20)/40+2)]
    
    score = 0
    for key in tripList:
        if curTiles[tripList[key][0]][tripList[key][1]][0] != 0 and curTiles[tripList[key][2]][tripList[key][3]][0] != 0:
            if curTiles[tripList[key][0]][tripList[key][1]][0]+curTiles[tripList[key][2]][tripList[key][3]][0]+curBlock[0][0] == 21:
                score += 42
                curTiles[tripList[key][0]][tripList[key][1]][0] = 0
                curTiles[tripList[key][2]][tripList[key][3]][0] = 0
                loseBlock = True
            if curTiles[tripList[key][0]][tripList[key][1]][0]+curTiles[tripList[key][2]][tripList[key][3]][0]+curBlock[0][0] == 7:
                score += 7
                curTiles[tripList[key][0]][tripList[key][1]][0] = 0
                curTiles[tripList[key][2]][tripList[key][3]][0] = 0
                loseBlock = True
    return score, loseBlock

def print_blocks():
    """
    Iterate through curTiles, topBlocks, curBlock and print everything
    """
    for i in range(7):
        if topBlocks[i][0] != 0:
            pygame.draw.rect(window, Colors[topBlocks[i][0]], topBlocks[i][1])
            blockNum = blockFont.render(str(topBlocks[i][0]), False, Colors[0], Colors[topBlocks[i][0]])
            topBlocks[i][2].centerx, topBlocks[i][2].centery = topBlocks[i][1].centerx, topBlocks[i][1].centery
            screen.blit(blockNum, topBlocks[i][2])
    pygame.draw.rect(window, Colors[curBlock[0][0]], curBlock[0][1])
    blockNum = blockFont.render(str(curBlock[0][0]), False, Colors[0], Colors[curBlock[0][0]])
    curBlock[0][2].centerx, curBlock[0][2].centery = curBlock[0][1].centerx, curBlock[0][1].centery
    screen.blit(blockNum, curBlock[0][2])
    for i in range(7):
        for j in range(14):
            if curTiles[i][j][0] != 0:
                pygame.draw.rect(window, Colors[curTiles[i][j][0]], curTiles[i][j][1])
                blockNum = blockFont.render(str(curTiles[i][j][0]), False, Colors[0], Colors[curTiles[i][j][0]])
                curTiles[i][j][2].centerx, curTiles[i][j][2].centery = curTiles[i][j][1].centerx, curTiles[i][j][1].centery
                screen.blit(blockNum, curTiles[i][j][2])
            
def main():
    moveSpeed = 4
    moveSide = 0
    playerScore = 0
    pause_screen(playerScore)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveSide = -40
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveSide = 40
                if event.key == K_DOWN or event.key == ord('s'):
                    moveSpeed = 16
                if event.key == ord('p'):
                    pause_screen(playerScore)
            if event.type == KEYUP:
                if event.key == K_DOWN or event.key == ord('s'):
                    moveSpeed = 4

        create_background()
        spawn_block()
        for i in range(7):
            topBlocks[i] = top_blocks(topBlocks[i])
        curBlock[0], moveSide, tempScore = cur_block(curBlock[0], moveSide, moveSpeed)
        playerScore += tempScore
        for i in range(7):
            for j in range(14):
                if curTiles[i][j][0] != 0:
                    curTiles[i][j] = cur_tiles(curTiles[i][j])
        print_blocks()

        pygame.display.update()
        gameClock.tick(40)

main()
