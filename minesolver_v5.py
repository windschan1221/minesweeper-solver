import win32gui
import win32api
import win32con
import keyboard
import time
import sys

tileSize = 16
marginTop = 100
marginLeft = 15
buttonTop = 72
colors = (0xEEEEEE, 0x2196F3, 0x4CAF50, 0xF44336, 0x3F51B5, 0xD50000, 0x009688, 0x9C27B0, 0x212121, 0xED1C24, 0xE0E0E0)

# Get window info
msxWin = win32gui.FindWindow(None, "Minesweeper X")
winRect = win32gui.GetWindowRect(msxWin)
cliRect = win32gui.GetClientRect(msxWin)
rect = (winRect[0], winRect[1], cliRect[2], cliRect[3])

# Calculate board size
width = int((winRect[2] - winRect[0] - 30) / tileSize - 1)
height = int((winRect[3] - winRect[1] - 116) / tileSize - 1)

around = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
startSet = ((1/2, 1/2), (1/4, 1/2), (3/4, 1/2), (1/2, 1/4), (1/2, 3/4), (1/4, 1/4), (1/4, 3/4), (3/4, 1/4), (3/4, 3/4))
tilecache = {}  # Save the scanned tiles
margin = []  # The set of tiles opened but not solved
solved = []  # The set of tiles solved

# Mouse functions
def lclick(x, y):  # Left click
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.01)


def rclick(x, y):  # Right click
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    time.sleep(0.01)


def getPixel(i_x, i_y):  # Detect color
    i_desktop_window_id = win32gui.FindWindow(None, "Minesweeper X")
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x - winRect[0], i_y - winRect[1])
    i_colour = int(long_colour)
    return ((i_colour & 0xff) << 16) + (i_colour & 0xff00) + ((i_colour & 0xff0000) >> 16)


# Game functions
def gameRestart():
    global tilecache, margin, solved
    tilecache = {}
    margin = []
    solved = []
    lclick(int(rect[0] + (rect[2] / 2)), int(rect[1] + buttonTop))


def gameStatus():
    color = getPixel(int(rect[0] + (rect[2] / 2)), int(rect[1] + buttonTop))
    if color == 0x00FF00:
        return 0  # Normal
    elif color == 0xFF0000:
        return 2  # Lose
    else:
        return 1  # Win


def tileCoord(x, y):  # Return tile coordinate
    return int(rect[0] + marginLeft + tileSize * x + tileSize / 2), int(rect[1] + marginTop + tileSize * y + tileSize /2)


def tileStatus(x, y):  # Return tile number, 0-8 = opened tile, 9 = flag, 10 = new
    global tilecache
    try:
        return tilecache[x, y]
    except:
        rx, ry = tileCoord(x, y)
        color = getPixel(rx, ry)
        for i in range(len(colors)):
            if colors[i] == color:
                if i < 10:
                    tilecache[x, y] = i
                return i
        return 99


def tileAround(x, y, val):  # Return the number of tiles around with tileStatus val
    n = 0
    for offset in around:
        if tileStatus(x + offset[0], y + offset[1]) == val: n += 1
    return n


def coneighbor(tileA, tileB):  # Return the common neighbours of two tiles
    xdiff = tileA[0] - tileB[0]
    ydiff = tileA[1] - tileB[1]
    nb = []
    if abs(xdiff) == 2:
        if abs(ydiff) == 2:
            nb.append((int(tileA[0] - xdiff / 2), int(tileA[1] - ydiff / 2)))
        if abs(ydiff) == 1:
            nb.append((int(tileA[0] - xdiff / 2), tileA[1]))
            nb.append((int(tileA[0] - xdiff / 2), tileB[1]))
        if abs(ydiff) == 0:
            nb.append((int(tileA[0] - xdiff / 2), tileA[1]))
            nb.append((int(tileA[0] - xdiff / 2), tileA[1] - 1))
            nb.append((int(tileA[0] - xdiff / 2), tileA[1] + 1))
    if abs(xdiff) == 1:
        if abs(ydiff) == 2:
            nb.append((tileA[0], int(tileA[1] - ydiff / 2)))
            nb.append((tileB[0], int(tileA[1] - ydiff / 2)))
        if abs(ydiff) == 1:
            nb.append((tileA[0], tileB[1]))
            nb.append((tileB[0], tileA[1]))
        if abs(ydiff) == 0:
            nb.append((tileA[0], tileA[1] - 1))
            nb.append((tileA[0], tileA[1] + 1))
            nb.append((tileB[0], tileB[1] - 1))
            nb.append((tileB[0], tileB[1] + 1))
    if abs(xdiff) == 0:
        if abs(ydiff) == 2:
            nb.append((tileA[0], int(tileA[1] - ydiff / 2)))
            nb.append((tileA[0] - 1, int(tileA[1] - ydiff / 2)))
            nb.append((tileA[0] + 1, int(tileA[1] - ydiff / 2)))
        if abs(ydiff) == 1:
            nb.append((tileA[0] - 1, tileA[1]))
            nb.append((tileA[0] + 1, tileA[1]))
            nb.append((tileA[0] - 1, tileB[1]))
            nb.append((tileA[0] + 1, tileB[1]))
    return nb
    

def tileOpen(x, y):
    rx, ry = tileCoord(x, y)
    lclick(rx, ry)
    getMargin(x, y)


def tileFlag(x, y):
    rx, ry = tileCoord(x, y)
    rclick(rx, ry)


def gameStart():  # Start a game with opening tiles in start set
    for ratio in startSet:
        x = int(ratio[0] * width)
        y = int(ratio[1] * height)
        tileOpen(x, y)
        if tileStatus(x, y) == 0: return
        if gameStatus() == 2:
            gameRestart()
            game()


def analyzeTile(x, y):  # Analyze whether a tile solvable
    global tilecache,margin, solved
    if keyboard.is_pressed('s'):
        del tilecache
        del margin
        del solved
        sys.exit(1)
    s = tileStatus(x, y)
    if gameStatus() == 2 or s == 0 or s == 9 or s == 10:
        return 0
    else:
        taflag = tileAround(x, y, 9)  # Return the number of mines marked
        tanew = tileAround(x, y, 10)  # Return the number of new tiles
        if tanew == 0:  # If no new tile is around, then the tile is solved
            margin.remove((x, y))
            solved.append((x, y))
            return 0
        elif taflag == s:  # If all mines are found, then the remaining new tiles can be opened
            margin.remove((x, y))
            solved.append((x, y))
            for offset in around:
                if tileStatus(x + offset[0], y + offset[1]) == 10:
                    tileOpen(x + offset[0], y + offset[1])
            return 1
        elif (taflag + tanew) == s:  # If all remaining tiles are mines, mark the mines
            margin.remove((x, y))
            for offset in around:
                if tileStatus(x + offset[0], y + offset[1]) == 10:
                    tileFlag(x + offset[0], y + offset[1])
                else:
                    getMargin(x + offset[0], y + offset[1])
            return 1
        elif tanew == 2 and taflag + 1 == s:  # If there are 2 new tiles left and one of them is mine, try double tile analysis
            tileA = (x, y)
            for offset in around:
                if tileStatus(x + offset[0], y + offset[1]) == 10:
                    if tileA == (x, y):
                        tileA = (x + offset[0], y + offset[1])
                    else:
                        tileB = (x + offset[0], y + offset[1])
            return analyzeDoubleTile(tileA, tileB)
        return 0


def analyzeDoubleTile(tileA, tileB):  # Double tile analysis (2 tiles with 1 to be mine)
    coneighbors = coneighbor(tileA, tileB)
    for tile in coneighbors:
        if tile[0] >= 0 and tile[0] <= width and tile[1] >= 0 and tile[1] <= height:
            s = tileStatus(tile[0], tile[1])
            if s != 0 and s!= 9 and s!= 10:
                taflag = tileAround(tile[0], tile[1], 9)
                tanew = tileAround(tile[0], tile[1], 10)
                if tanew > 2:
                    if taflag + 1 == s:  # If a coneighbor has one mine to be marked, then other new tiles are safe
                        for offset in around:
                            if tileStatus(tile[0] + offset[0], tile[1] + offset[1]) == 10 and (tile[0] + offset[0], tile[1] + offset[1]) != tileA and (tile[0] + offset[0], tile[1] + offset[1]) != tileB:
                                tileOpen(tile[0] + offset[0], tile[1] + offset[1])
                        return 1
                    elif taflag + tanew - 1 == s:  # If a coneighbor has one mine to be safe, then other new tiles are mines
                        for offset in around:
                            if tileStatus(tile[0] + offset[0], tile[1] + offset[1]) == 10 and (tile[0] + offset[0], tile[1] + offset[1]) != tileA and (tile[0] + offset[0], tile[1] + offset[1]) != tileB:
                                tileFlag(tile[0] + offset[0], tile[1] + offset[1])
                        return 1
    return 0
        
    

def analyzeMargin():  # Start analysis
    global tilecache, margin, solved
    if keyboard.is_pressed('s'):
        del tilecache
        del margin
        del solved
        sys.exit(1)
    guess = 0
    for tile in reversed(margin):  # Analyze in LIFO order because the newly opened tiles have more clues to solve
        guess += analyzeTile(tile[0], tile[1])
    if guess == 0:  # If no tile is solvable, then guess one
        guessingTile = margin[len(margin) - 1]
        guessAroundTile(guessingTile[0], guessingTile[1])


def getMargin(x, y):  # Add the opened tiles into the margin set
    global tilecache, margin, solved
    if keyboard.is_pressed('s'):
        del tilecache
        del margin
        del solved
        sys.exit(1)
    if (x, y) in solved:
        return
    elif (x, y) in margin:
        margin.remove((x, y))
        margin.append((x, y))
    elif tileStatus(x, y) == 0:
        solved.append((x, y))
        for offset in around:
            getMargin(x + offset[0], y + offset[1])
    elif tileStatus(x, y) < 9:
        margin.append((x, y))
        
        
def guessAroundTile(x, y):  # Guess around a certain tile
    global tilecache, margin, solved
    guesslog = str(tileStatus(x, y))
    taflag = tileAround(x, y, 9)
    tanew = tileAround(x, y, 10)
    for offset in around:
        if tileStatus(x + offset[0], y + offset[1]) == 10:
            guesslog += "-"
        elif tileStatus(x + offset[0], y + offset[1]) == 99:
            guesslog += "x"
        else:
            guesslog += str(tileStatus(x + offset[0], y + offset[1]))
    with open("guess.txt", 'r+') as logfile:  # Find the best one to open in the log file
        safe = (0, 0, 0, 0, 0, 0, 0, 0)
        danger = (0, 0, 0, 0, 0, 0, 0, 0)
        while 1:
            record = logfile.readline()
            if record == '':
                break
            elif record[:-2] == guesslog:
                if record[10] == '0':
                    danger[int(record[9])] += 1
                else:
                    safe[int(record[9])] += 1
        bestIdx = 0
        bestProb = -1
        for idx in range(8):
            if guesslog[idx + 1] == '-':
                if safe[idx] + danger[idx] == 0:
                    prob = (tileStatus(x, y) - taflag) / tanew
                else:
                    prob = safe[idx] / (safe[idx] + danger[idx])
                if prob > bestProb:
                    bestProb = prob
                    bestIdx = idx
        guesslog += str(bestIdx)
        offset = around[bestIdx]
        tileOpen(x + offset[0], y + offset[1])
        if gameStatus() == 2:
            guesslog = guesslog + "0\n"
            logfile.write(guesslog)
            logfile.close()
            del tilecache
            del margin
            del solved
            sys.exit(1)
        else:
            guesslog = guesslog + "1\n"
            logfile.write(guesslog)
            logfile.close()
            return


def game():
    gameRestart()
    print("Start Game")
    global tilecache, margin, solved
    tilecache = {}
    margin = []
    solved = []

    gameStart()
    x = 0
    y = 0	
    guess = 0

    while 1:
        if gameStatus() > 0: return
        if keyboard.is_pressed('s'): sys.exit(1)
        analyzeMargin()
        

# Initialize
if __name__ == "__main__":
    game()
