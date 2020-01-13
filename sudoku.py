import pygame
import time
import copy
from tkinter import *
from tkinter import messagebox

pygame.init()
Tk().wm_withdraw()


def gridline():
    height_grid = Height
    widht_grid = 2
    for i in range(0, Height+1, Height//9):
        pygame.draw.rect(win, (150, 150, 150), (i, 0, widht_grid, height_grid))
        pygame.draw.rect(win, (150, 150, 150), (0, i, height_grid, widht_grid))

    for i in range(Height//3, Height, Height//3):
        pygame.draw.rect(win, (0, 0, 0), (i, 0, 2, height_grid))
        pygame.draw.rect(win, (0, 0, 0), (0, i, height_grid, 2))
 # function for initiate cells


def initiate_cells():
    data = {}
    full_cell = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for x in range(0, 9):
        for y in range(0, 9):
            data[x, y] = list(full_cell)

    return data


def place_num(data, dataToBeLocked, pencilmarks=False):
    x_place = 0
    y_place = 0
    for item in data:
        celldata = data[item]

        # if celldata.count(' ') == 9:
        #     return
        # elif item == [xSelectedCell, ySelectedCell]:
        #     continue
        for number in celldata:
            if number != ' ':
                x_place = (number-1) % 3

                if number <= 3:
                    y_place = 0
                elif number <= 6:
                    y_place = 1
                else:
                    y_place = 2

                if celldata.count(' ') < 8:
                    if pencilmarks or not space:
                        print_num(number, (item[0]*Height//9 + x_place*Height//27),
                                  (item[1]*Height//9 + y_place*Height//27), "small", "None")
                    else:
                        pass
                else:
                    if not pencilmarks:
                        print_num(number, (item[0]*Height//9),
                                  (item[1]*Height//9), "large", "None")
                    else:
                        print_num(number, (item[0]*Height//9 + x_place*Height//27),
                                  (item[1]*Height//9 + y_place*Height//27), "small", "None")

    if dataToBeLocked:
        for itemDash in dataToBeLocked:
            questionData = dataToBeLocked[itemDash]
            if questionData.count(' ') == 8:
                            #     if item == itemDash:
                for questionNumber in questionData:
                    if questionNumber != ' ':
                        print_num(questionNumber, (itemDash[0]*Height//9),
                                  (itemDash[1]*Height//9), "large", "lock")


def print_num(celldata, x, y, size, color):

    if size == "small":
        win_text = small_font.render('%s' % (celldata), True, (200, 200, 200))
        text_rect = win_text.get_rect()
        text_rect.center = (x+14, y+14)
    else:

        if color == "lock":
            pygame.draw.rect(win, (255, 255, 0), (x+2, y+2, 58, 58))
        elif showStatus:
            pass
        elif solve:
            pygame.draw.rect(win, (255, 218, 185), (x+2, y+2, 58, 58))

        else:
            pygame.draw.rect(win, (255, 255, 153), (x+2, y+2, 58, 58))

        win_text = large_font.render('%s' % (celldata), True, (200, 100, 100))
        text_rect = win_text.get_rect()
        text_rect.center = (x+30, y+30)

    win.blit(win_text, text_rect)


def drawbox(mousex, mousey):
    boxx = ((mousex*27) // (Widht)) * Widht//27
    boxy = ((mousey*27) // (Height)) * Height//27
    pygame.draw.rect(win, (0, 0, 255), (boxx, boxy, Widht//27, Height//27), 1)


def refreshgrid(data):
    full_Cell = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # for x in range(0, 9):
    #     for y in range(0, 9):
    for item in data:
        celldata = data[item]
        if celldata.count(' ') < 8:
            data[item] = list(full_Cell)
    return data


def selectedNumUpdate(data, mousex, mousey, dataToBeLocked):
    refresh = False
    xunit = ((mousex*27) // (Widht))
    yunit = ((mousey*27) // (Height))
    if xunit % 3 == 0:
        num_temp = [1, 4, 7]
    if xunit % 3 == 1:
        num_temp = [2, 5, 8]
    if xunit % 3 == 2:
        num_temp = [3, 6, 9]

    numToBeDisplayed = num_temp[yunit % 3]
    print(numToBeDisplayed)
    xcell = xunit//3
    ycell = yunit//3
    if dataToBeLocked and dataToBeLocked[xcell, ycell].count(' ') == 8:
        return data
    current_state = data[xcell, ycell]
    if current_state.count(' ') == 8:
        if current_state.count(numToBeDisplayed) == 1:
            data[xcell, ycell] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            refresh = True
    if not refresh:
        for i in range(9):
            if i+1 != numToBeDisplayed:
                current_state[i] = ' '
            else:
                current_state[i] = numToBeDisplayed
            data[xcell, ycell] = current_state
    data = refreshgrid(data)
    return data


def solve_sudoku(data, both=True):
    temp_data = copy.deepcopy(data)
    if if_solved(data):
        return data
    for item in data:

        celldata = data[item]
        if celldata.count(' ') == 8:
            for number in celldata:
                if number != ' ':
                    updateNumber = number
            data = removeX(data, item, updateNumber)
            data = removeY(data, item, updateNumber)
            data = removeGrid(data, item, updateNumber)
    if both:
        data = onlyinx(data)
        data = onlyiny(data)
        data = onlyingrid(data)

    # if if_error(data):
    #     return False
    if both:
        if (temp_data != data):
            solve_sudoku(data, both)

    return data


def removeY(data, unit, updateNumber):
    for item in data:
        if item[0] == unit[0] and item[1] != unit[1]:
            celldata = data[item]
            for number in celldata:
                if number == updateNumber:
                    celldata[number-1] = ' '

            data[item] = celldata
    return data


def removeX(data, unit, updateNumber):
    for item in data:
        if item[1] == unit[1] and item[0] != unit[0]:
            celldata = data[item]
            for number in celldata:
                if number == updateNumber:
                    celldata[number-1] = ' '

            data[item] = celldata
    return data


def removeGrid(data, unit, updateNumber):
    for item in data:
        if item[0] in range(unit[0]//3*3, unit[0]//3*3+3):
            if item[1] in range(unit[1]//3*3, unit[1]//3*3+3):
                if item[1] != unit[1] and item[0] != unit[0]:
                    celldata = data[item]
                    for number in celldata:
                        if number == updateNumber:
                            celldata[number-1] = ' '

                    data[item] = celldata
    return data


def onlyinx(data):
    for x in range(9):
        allNumbersIncol = []
        for item in data:
            if item[0] == x:
                celldata = data[item]
                allNumbersIncol = allNumbersIncol + celldata
        for i in range(1, 10):
            k = allNumbersIncol.count(i)
            if k == 1:
                req_index = allNumbersIncol.index(i)
                req_y = req_index//9
                celldata = data[x, req_y]
                for j in range(1, 10):
                    if j != i:
                        celldata[j-1] = ' '

                data[x, req_y] = celldata
    return data


def onlyiny(data):
    for y in range(9):
        allNumbersIncol = []
        for item in data:
            if item[1] == y:
                celldata = data[item]
                allNumbersIncol = allNumbersIncol + celldata
        for i in range(1, 10):
            k = allNumbersIncol.count(i)
            if k == 1:
                req_index = allNumbersIncol.index(i)
                req_x = req_index//9
                celldata = data[req_x, y]
                for j in range(1, 10):
                    if j != i:
                        celldata[j-1] = ' '
                    data[req_x, y] = celldata
    return data


def onlyingrid(data):
    for kx in range(3):
        for ky in range(3):
            allNumbersInGrid = []
            for item in data:
                if item[0] in range(kx*3, kx*3+3):
                    if item[1] in range(ky*3, ky*3+3):
                        celldata = data[item]
                        allNumbersInGrid = allNumbersInGrid + celldata
            for i in range(1, 10):
                k = allNumbersInGrid.count(i)
                if k == 1:
                    req_index = allNumbersInGrid.index(i)
                    l = req_index//9
                    [req_x, req_y] = [kx*3 + l//3, ky*3 + l % 3]
                    celldata = data[req_x, req_y]
                    for j in range(1, 10):
                        if j != i:
                            celldata[j-1] = ' '
                        data[req_x, req_y] = celldata
    return data


def if_error(data):
    for item in data:
        celldata = data[item]
        if celldata.count(' ') == 9:
            return True
    return False


def if_solved(data):
    if data is False:
        return False
    countForSearch = 0
    for item in data:
        celldata = data[item]
        if celldata.count(' ') == 8:
            countForSearch += 1

    if countForSearch == 81:
        return True
    return False


def search(data):
    celldata_temp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    count_list = []
    count_for_solved = 0
    temp_data = copy.deepcopy(data)

    for item in data:
        celldata = data[item]
        if celldata.count(' ') == 9:
            return data
        elif celldata.count(' ') == 8:
            count_for_solved += 1

    if count_for_solved == 81:
        return data

    for item in data:
        celldata = data[item]
        if celldata.count(' ') != 8:
            count_list.append(celldata.count(' '))
    minCellCount = max(count_list)

    temp_data = copy.deepcopy(data)

    for item in data:
        celldata = temp_data[item]
        if celldata.count(' ') == minCellCount:
            req_item = item
            break

    celldata = temp_data[req_item]

    for i in range(9):
        if celldata[i] != ' ':
            for j in range(9):
                if j != i:
                    celldata_temp[j] = ' '
                else:
                    celldata_temp[j] = i+1
            temp_data[req_item] = celldata_temp
            if not if_error(solve_sudoku(copy.deepcopy(temp_data))):
                temp1_data = copy.deepcopy(temp_data)
                temp1_data = search(solve_sudoku(temp1_data))
                if temp1_data:
                    temp_data = temp1_data

            if if_solved(temp_data):
                return temp_data

    return False


def if_extreme(data):
    if data is False:
        return False
    countForSearch = 0
    for item in data:
        celldata = data[item]
        if celldata.count(' ') == 8:
            countForSearch += 1

    if countForSearch <= 50:
        return True
    return False


bg = pygame.image.load("sudoku.jpg")
refresh = pygame.image.load("refresh.jpg")
solveImage = pygame.image.load("solve.jpg")
hintImage = pygame.image.load("hint.jpg")
backImage = pygame.image.load("back.jpg")
enterImage = pygame.image.load("enter.jpg")
checkImage = pygame.image.load("check.jpg")
pencilMarksImage = pygame.image.load("pencilMarks.jpeg")
small_font = pygame.font.SysFont("comicsansms", 25)
large_font = pygame.font.SysFont("comicsansms", 50)
clock = pygame.time.Clock()
Height = 540
Widht = 540
mousex = 0
mousey = 0
hintCount = 0
allowedHints = 3
Flag = 0
win = pygame.display.set_mode((Height, Widht+50))
pygame.display.set_caption('Sudoku Solver')
clickUpdate = False
keyUpdate = False
solve = False
firstScreen = True
secondScreen = True
searchEnd = False
space = False
tyme = True
searchMethod = False
enter = False
enterDash = False
enterlock = False
check = False
dataToBeSolved = False
checkDash = False
showStatus = False
pencilMarks = False

while firstScreen:
    win.blit(bg, (0, 0))
    win_text = large_font.render("Hello Sudoku Here", True, (50, 205, 50))
    text_rect = win_text.get_rect()
    text_rect.center = (Widht//2, Height//2)
    win.blit(win_text, text_rect)

    pygame.display.update()
    time.sleep(2)
    firstScreen = False
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_RETURN]:
    #     firstScreen = False


# while secondScreen:
#     win.fill((255, 255, 255))
#     mouse = pygame.mouse.get_pos()
#     colorForText1 = (0, 0, 0)
#     colorForText2 = (0, 0, 0)
#     colorForText3 = (0, 0, 0)
#     if (Widht//2-25) < mouse[0] < (Widht//2 + 25):
#         if (Height//4-25) < mouse[1] < (Height//4+25):
#             colorForText1 = (120, 5, 5)
#         if (Height//2-25) < mouse[1] < (Height//2+25):
#             colorForText2 = (120, 5, 5)
#         if (3*Height//4-25) < mouse[1] < (3*Height//4+25):
#             colorForText3 = (120, 5, 5)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         elif event.type == pygame.MOUSEBUTTONUP:
#             mousex, mousey = event.pos
#             if (Widht//2-25) < mousex and mousex < Widht//2 + 25 and (Height//4-25) < mousey and mousey < (Height//4+25):
#                 secondScreen = False

#     win_text1 = large_font.render("Play", False, colorForText1)
#     text_rect1 = win_text1.get_rect()
#     text_rect1.center = (Widht//2, Height//4)
#     win.blit(win_text1, text_rect1)

#     win_text2 = large_font.render("Help", False, colorForText2)
#     text_rect2 = win_text2.get_rect()
#     text_rect2.center = (Widht//2, Height//2)
#     win.blit(win_text2, text_rect2)

#     win_text3 = large_font.render("Know About Sudoku", False, colorForText3)
#     text_rect3 = win_text3.get_rect()
#     text_rect3.center = (Widht//2, 3*Height//4)
#     win.blit(win_text3, text_rect3)
#     pygame.display.update()


win.fill((255, 255, 255))
pygame.draw.rect(win, (32, 178, 170), (0, 540, 540, 50))
run = True


data = initiate_cells()
dataToBeLocked = False
xSelectedCell = 0
ySelectedCell = 0


while run:
    count = 0
    countForSearch = 0
    clock.tick(5)
    mouseclick = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:

            mousex, mousey = event.pos
            mouseclick = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        if enterDash:
            pass
        else:
            enter = True
            enterlock = True
    if enterDash:
        if pencilMarks:
            if keys[pygame.K_SPACE]:
                if space:
                    space = False
                    refreshgrid(data)
                else:
                    space = True

        if keys[pygame.K_TAB]:
            searchMethod = True
            solve = True
            
        if keys[pygame.K_RETURN]:
            if enterDash:
                pass
            else:
                enter = True
                enterlock = True
        if keys[pygame.K_h]:
            if dataToBeSolved:
                leftHint = allowedHints - hintCount
                if leftHint != 1:
                    messageForHint = "You have " + \
                        str(leftHint) + \
                        " hints left. Are you sure you want answer to pop out in selected cell."
                elif leftHint:
                    messageForHint = "This is your last hint. Are you sure you want answer to pop out in selected cell"
                if leftHint:
                    askingHint = messagebox.askyesno(None, messageForHint)
                if askingHint == YES and leftHint:
                    data[xSelectedCell,
                         ySelectedCell] = dataToBeSolved[xSelectedCell, ySelectedCell]
                    hintCount += 1
                else:
                    pass
                if not leftHint:
                    messagebox.showinfo(
                        None, "There are no more Hints available.")

        if keys[pygame.K_c]:
            if enterDash:
                if checkDash:
                    checkDash = False
                    showStatus = False
                else:
                    check = True


    if keys[pygame.K_DOWN]:
        if ySelectedCell < 8:
            ySelectedCell += 1
    if keys[pygame.K_UP]:
        if ySelectedCell > 0:
            ySelectedCell -= 1
    if keys[pygame.K_RIGHT]:
        if xSelectedCell < 8:
            xSelectedCell += 1
    if keys[pygame.K_LEFT]:
        if xSelectedCell > 0:
            xSelectedCell -= 1
    if keys[pygame.K_1]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+10, ySelectedCell*Height//9+10, dataToBeLocked)
    if keys[pygame.K_2]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+30, ySelectedCell*Height//9+10, dataToBeLocked)
    if keys[pygame.K_3]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+50, ySelectedCell*Height//9+10, dataToBeLocked)
    if keys[pygame.K_4]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+10, ySelectedCell*Height//9+30, dataToBeLocked)
    if keys[pygame.K_5]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+30, ySelectedCell*Height//9+30, dataToBeLocked)
    if keys[pygame.K_6]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+50, ySelectedCell*Height//9+30, dataToBeLocked)
    if keys[pygame.K_7]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+10, ySelectedCell*Height//9+50, dataToBeLocked)
    if keys[pygame.K_8]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+30, ySelectedCell*Height//9+50, dataToBeLocked)
    if keys[pygame.K_9]:
        clickUpdate = False
        keyUpdate = True
        data = selectedNumUpdate(
            data, xSelectedCell*Widht//9+50, ySelectedCell*Height//9+50, dataToBeLocked)
    if keys[pygame.K_BACKSPACE]:
        data[xSelectedCell, ySelectedCell] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    if mouseclick == True:

        if mousey > 541:
            if 345 < mousex < 400 and 550 < mousey < 580:
                if pencilMarks and enterDash:
                    if space:
                        space = False
                        refreshgrid(data)
                    else:
                        space = True
            if not checkDash:
                if 25 < mousex < 50 and 552 < mousey < 577:
                    answerForRefresh = messagebox.askyesno(
                        None, "Are you sure want to refresh the grid.")
                    if answerForRefresh == YES:
                        data = initiate_cells()
                        dataToBeLocked = initiate_cells()
                        dataToBeSolved = initiate_cells()
                        enter = False
                        solve = False
                        space = False
                        pencilMarks = False
                        enterDash = False
                        searchMethod = False
                elif 75 < mousex < 125 and 552 < mousey < 577:
                    if enterDash:
                        answerForSolve = messagebox.askyesno(
                            None, "Are you sure want to solve it without giving try.")
                        if answerForSolve == YES:
                            searchMethod = True
                            solve = True
                    else:
                        if enterDash:
                            pass
                        else:
                            enter = True
                            enterlock = True

                elif 150 < mousex < 175 and 552 < mousey < 577:
                    if dataToBeSolved:
                        leftHint = allowedHints - hintCount
                        if leftHint != 1:
                            messageForHint = "You have " + \
                                str(leftHint) + \
                                " hints left. Are you sure you want answer to pop out in selected cell."
                        elif leftHint:
                            messageForHint = "This is your last hint. Are you sure you want answer to pop out in selected cell"
                        if leftHint:
                            askingHint = messagebox.askyesno(
                                None, messageForHint)
                        if askingHint == YES and leftHint:
                            data[xSelectedCell,
                                 ySelectedCell] = dataToBeSolved[xSelectedCell, ySelectedCell]
                            hintCount += 1
                        else:
                            pass
                        if not leftHint:
                            messagebox.showinfo(
                                None, "There are no more Hints available.")
                elif 200 < mousex < 340 and 550 < mousey < 580:
                    if enterDash:
                        if checkDash:
                            checkDash = False
                            showStatus = False
                        else:
                            check = True

            else:
                if 25 < mousex < 100 and 552 < mousey < 577:
                    checkDash = False
                    showStatus = False
        else:
            if not if_solved(data):
                drawbox(mousex, mousey)
                data = selectedNumUpdate(data, mousex, mousey, dataToBeLocked)

                clickUpdate = True
                keyUpdate = False

    if solve:
        data = dataToBeSolved

    if enter:

        dataToBeLocked = copy.deepcopy(data)

        dataToBeSolved = copy.deepcopy(data)
        tempDataToBeSolved = copy.deepcopy(dataToBeSolved)
        tempDataToBeSolved = solve_sudoku(tempDataToBeSolved)
        dataToBeSolved = copy.deepcopy(tempDataToBeSolved)
        dataToBeSolved = search(dataToBeSolved)
        enterDash = True
        enter = False
        if if_error(dataToBeSolved):
            Flag = 1
            messagebox.showerror(None, "No solution possible.")
            dataToBeLocked = initiate_cells()
            dataToBeSolved = initiate_cells()
            enter = False
            enterDash = False
            solve = False
            space = False
            searchMethod = False
        else:
            Flag = 0
        if not if_solved(tempDataToBeSolved):
            if Flag != 1:
                pencilMarks = True
                pencilMarksbox = messagebox.askyesno(
                    "PencilMarks", "Turning on the pencilMarks are recommended. This is a relatively tough sudoku so pencilMarks would be helpful.You can always turn it on and off anytime you want by pressing space.Do you want to turn it on.")
                if pencilMarksbox == YES:
                    space = True

    if check and not solve:

        for item in data:
            celldata = data[item]
            if celldata.count(' ') == 8:
                if celldata != dataToBeSolved[item]:
                    count += 1
        if count == 0:
            messagebox.showinfo(None, 'All boxes are correct.')
        else:
            FullMessage = 'You have ' + str(count) + ' wrong boxes'
            messagebox.showinfo(None, FullMessage)

        msgBox = messagebox.askyesno(
            None, 'If you want to see your status of Right and Wrong.')
        if msgBox == YES:
            showStatus = True
            checkDash = True
        else:
            pass

        check = False

    if showStatus and not solve:
        for item in data:
            celldata = data[item]
            if celldata.count(' ') == 8:
                if celldata != dataToBeSolved[item]:
                    [x, y] = item
                    pygame.draw.rect(win, (255, 100, 100),
                                     (x*60+2, y*60+2, 58, 58))
                else:
                    [x, y] = item
                    pygame.draw.rect(win, (100, 255, 100),
                                     (x*60 + 2, y*60+2, 58, 58))

    if space:
        temperory_data = copy.deepcopy(data)
        temperory_data = solve_sudoku(temperory_data, False)
        place_num(temperory_data, dataToBeLocked, True)

    gridline()
    place_num(data, dataToBeLocked)
    if not solve:
        pygame.draw.rect(win, (200, 255, 254), (xSelectedCell *
                                                Widht//9+2, ySelectedCell*Height//9+2, 58, 58))

    if if_solved(data) and data == dataToBeSolved and not solve:
        solve = True
        messagebox.showinfo(None, "Well Done.")

    pygame.display.update()
    win.fill((255, 255, 255))

    if checkDash:
        win.blit(backImage, (25, 552))
    if not checkDash:
        if enterDash:
            win.blit(solveImage, (70, 552))
            win.blit(checkImage, (185, 550))
        else:
            win.blit(enterImage, (75, 547))
        win.blit(refresh, (25, 552))
    if enterDash and not checkDash:
        win.blit(hintImage, (140, 552))
    if pencilMarks:
        win.blit(pencilMarksImage, (340, 546))


pygame.quit
