"""Flippy (a reversi clone)

(Requires pygame)Play against a computer and try to flip their tiles"""

__version__ = 1
#Based on "reversi.py' code that originally appeared in "Invent
# your Own Computer Games with Python", chapter 15:
#  http://inventwithpython.com/chapter15.html

import random, sys, copy, time, pygame
from pygame.locals import *

FPS = 10 #Frames per second to update the screen
WINDOWWIDTH = 640 #width of the programs window in pixels
WINDOWHEIGHT = 480 #height in pixels
SPACESIZE = 50 #Width and Height of each space on the board, in pixels
BOARDWIDTH = 8 #How many columns of spaces on the game board
BOARDHEIGHT = 8 #How many rows of spaces on on the game board
WHITE_TILE = 'whitetile' #An arbitrary but unique value
BLACK_TILE = 'blacktile' #An arbitrary value
EMPTY_SPACE = 'emptyspace' #An arbitrary value
HINT_VALUE = 'hinttile' #An arbitrary value
ANIMATION_SPEED = 25

#Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH*SPACESIZE))/2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT*SPACESIZE))/2)

#                  R   G   B
WHITE =         (255,255,255)
BLACK =         (  0,  0,  0)
GREEN =         (  0,155,  0)
BRIGHTBLUE =    (  0, 50,255)
BROWN =         (174, 94,  0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf',16)
    BIGFONT = pygame.font.Font('freesansbold.ttf',32)

    # Set up the background image
    boardImage = pygame.image.load('flippyboard.png')
    #Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage,(BOARDWIDTH*SPACESIZE, BOARDHEIGHT*SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN,YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    #Use smoothscale to stretch the image to fit the window
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE,(WINDOWWIDTH,WINDOWWIDTH))
    BGIMAGE.blit(boardImage,boardImageRect)

    #Run the main game
    while True:
        if runGame() == False:
            break

def runGame():
    #Plays a single game of reversi each time this function is called

    #Reset the board and game
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    showHints = False
    turn = random.choice(['computer', 'player'])

    #Draw the starting board and ask the player what color they want
    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()

    #make the surface and rect objects for the 'New Game' and 'Hints' buttons
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8,10)
    hintsSurf = FONT.render('Hint', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH - 8,40)
    while True: #Main game loop
        #Keep looping for computer and player turns.
        if turn == 'player':
            #Players Turn
            if getValidMoves(mainBoard,playerTile) == []:
                #It is players turn but they cant move
                # end the game
                break
            movexy = None
            while movexy == None:
                #Keep looping until the player clicks on a valid space
                #Determine which data structure to use for display
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get(): #Event handling loop
                    if event.type == MOUSEBUTTONUP:
                        #Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex,mousey)):
                            #Start a new game
                            return True
                        elif hintsRect.collidepoint((mousex,mousey)):
                            #Toggle hints mode
                            showHints = not showHints
                        #movexy is set to a two-item tuple XY coordinate, or Nonevalue
                        movexy = getSpaceClicked(mousex,mousey)
                        if movexy != None and not isValidMove(mainBoard,playerTile,movexy[0],movexy[1]):
                            movexy = None
                        
                #Draw the game board
                drawBoard(boardToDraw)
                drawInfo(boardToDraw, playerTile, computerTile, turn)

                #Draw the "New Game" and "Hints" buttons
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()
            
            #make the move and end the turn
            makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)
            if getValidMoves(mainBoard, computerTile) == []:
                #Only set for a computer's turn if it can get a valid move
                turn = 'computer'
        else:
            #Computers turn
            if getValidMoves(mainBoard, computerTile) == []:
                #If it was set to be the computers turn but
                #they cant move, then end the game
                break

            #Draw the board
            drawBoard(mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)

            #Draw the "New Game" and "Hints" buttons
            DISPLAYSURF.blit(newGameSurf, newGameRect)
            DISPLAYSURF.blit(hintsSurf, hintsRect)
            
            #make it look like the computer is thinking by pausing a bit
            pauseUntil = time.time() + random.randint(5,15)*0.1
            while time.time() < pauseUntil:
                pygame.display.update()
            
            #Make the move and end the turn
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y, True)
            if getValidMoves(mainBoard, playerTile) != []:
                #Only set for players turn if they can make a move
                turn = 'player'

    #Display the final score
    drawBoard(mainBoard)
    score = getScoreOfBoard(mainBoard)

    #Determine the text message to display
    if score[playerTile] > score[computerTile]:
        text = f'You beat the computer by {score[playerTile]-score[computerTile]}\
    points'
    elif score[playerTile] < score[computerTile]:
        text = f'You lost. The computer beat you by {score[computerTile]-score[playerTile]}\
        points'
    else:
        text = 'The game was a tie'
    
    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    #Display the "Play Again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play Again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    #Make "Yes" Button
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    #Make "No" button
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2)+90)

    while True:
        #Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): #event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def translateBoardTobePixelCoord(x,y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional title that was just laid down. (Otherwise we'd 
    # have to completely redraw the board & the board info.)
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardTobePixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2)-4)
    pygame.display.update()

    for rgbValues in range (0, 255, int(ANIMATION_SPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0
        
        if tileColor == WHITE_TILE:
            color = tuple([rgbValues]*3) #rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255-rgbValues]*3) #rgbValues goes from 255 to 0

        for x,y in tilesToFlip:
            centerx, centery = translateBoardTobePixelCoord(x,y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2)-4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


def drawBoard(board):
    #Draw background of bard.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw horizontal lines of the board.
        startx = (x*SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x*SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT*SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    for y in range(BOARDHEIGHT +1):
        #draw the verical lines
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH*SPACESIZE)
        endy = (y*SPACESIZE)+YMARGIN
        pygame.draw.line(DISPLAYSURF,GRIDLINECOLOR, (startx,starty), (endx, endy))
    
    #Draw the black & white tiles or hint spots
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardTobePixelCoord(x,y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE/2)-4)
            if board[x][y] == HINT_VALUE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8,8))

def getSpaceClicked(mousex, mousey):
    #Return a tuple of two integers of the board space cordinates where
    #the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
                mousex < (x+1)*SPACESIZE + XMARGIN and \
                mousey > y * SPACESIZE + YMARGIN and \
                mousey < (y+1)*SPACESIZE + YMARGIN:
                return (x,y)
    return None


def drawInfo(board, playerTile, computerTile, turn):
    #Draws scores and whose turn it is at the bottom of the screen.
    score = getScoreOfBoard(board)
    scoreSurf = FONT.render(f"Player Score: {score[playerTile]}   Computer Score: {score[computerTile]}   {turn.title()}",True,TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT-5)
    DISPLAYSURF.blit(scoreSurf, scoreRect) 

def resetBoard(board):
    #Blanks out the board it is passed, and sets up starting tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

    # Add starting pieces to the center
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[3][4] = WHITE_TILE


def getNewBoard():
    #Creates a brand new, empty board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE]*BOARDHEIGHT)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of sapces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False
    
    board[xstart][ystart] = tile #temporarily set the tile on the board.

    if tile == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE
    
    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y = xstart, ystart
        x += xdirection
        y+= ydirection
        if isOnBoard(x,y) and board[x][y] == otherTile:
            # The piece belongs to the other next to our piece
            x += xdirection
            y += ydirection
            if not isOnBoard(x,y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x,y):
                    break #break out of while loop, continue in for loop
            if not isOnBoard(x,y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse
                # direction until we reach the original space, noting all
                # the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x,y])
    board[xstart][ystart] = EMPTY_SPACE #make space empty
    if len(tilesToFlip) == 0: #If no tiles flipped, this move is invalid
        return False
    return tilesToFlip

       
def isOnBoard(x,y):
    # Returns True if the coordinates are located on the board.
    return x>= 0 and x < BOARDWIDTH and y>=0 and y < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    #Returns a new board with hint markings
    dupeBoard = copy.deepcopy(board)

    for x,y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_VALUE
    return dupeBoard


    
def getValidMoves(board, tile):
    #Returns a list of (x,y) tuples of all valid moves
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append((x,y))
    return validMoves


def getScoreOfBoard(board):
    #Determine the score by counting the tiles
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                xscore += 1
            if board[x][y] == BLACK_TILE:
                oscore += 1
    return{WHITE_TILE:xscore, BLACK_TILE:oscore}


def enterPlayerTile():
    #Draws the text and handles the mouse click events for letting 
    #the player choose which color they want to be. Returns
    #[WHITE_TILE, BLACK_TILE] if the player chooses to be white, 
    # [BLACK_TILE, WHITE_TILE] if Black

    #Create text
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): #event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [BLACK_TILE, WHITE_TILE]
        
        # Draw the screen
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False
    
    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for  x, y in tilesToFlip:
        board[x][y] = tile
    return True


def isOnCorner(x,y):
    #Returns True if the position is one of the four corners.
    return (x==0 and y== 0) or \
            (x== BOARDWIDTH and y==0) or \
            (x == 0 and y == BOARDHEIGHT) or \
            (x==BOARDWIDTH and y==BOARDHEIGHT)



def getComputerMove(board, computerTile):
    #Given a board and the computers tile, determine where to
    # move and return that move as a [x,y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # rendomize the order of possible moves
    random.shuffle(possibleMoves)

    #always go for a corner if available.
    for x,y in possibleMoves:
        if isOnCorner(x,y):
            return [x,y]
    

    #Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x,y]
            bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.display.quit(); pygame.quit() # Display quit is a workaround for a Raspberry Pi bug.
            sys.exit()


if __name__ == '__main__':
    main()
