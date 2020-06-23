#This file contains all the globals as well as all the fucntions the
#snake game and AI uses

import pygame, random, sys
from pygame.locals import *

#Intialize Globals

ORANGE = (255, 128, 0)
MAGENTA = (255,0,255)
PURPLE = (145,44,238)
CYAN = (0, 238, 238)
NAVY_BLUE = (0, 0, 128)
DARK_RED = (220, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)

WINHEIGHT = 512
WINWIDTH = 512

SIDE_LENGTH = 32

BLOCK_HEIGHT = BLOCK_WIDTH = (WINHEIGHT / SIDE_LENGTH)

OFFSET = 2


#A class for a node on the drid, it contains the number of the nodes around it
#as well as its own numbers, whether or not it is an end, and its coordinates
#on the grid
class Node:
    def __init__(self, left, right, down, up, isEnd, coordinates, number):
        self.left = left
        self.right = right
        self.down = down
        self.up = up
        self.end = isEnd
        self.coordinates = coordinates
        self.num = number

    def __str__(self):
        print (self.up, self.right, self.down, self.left)
        return ''

#A class for each block of the snake that knows its own height, width, color, and block
class Snake:
    def __init__(self, spawnX, spawnY):
        self.height = BLOCK_HEIGHT - OFFSET
        self.width = BLOCK_WIDTH - OFFSET
        self.color = GREEN
        self.block = pygame.Rect(spawnX, spawnY, self.height, self.width)


    #Checks if the snakes body is there
    def IsThere(self, coord):
        snakeCoord = (self.block.left - OFFSET, self.block.top - OFFSET)
        if(snakeCoord == coord):
            return True
        else:
            return False

#A class for the apple that knows its own height, width, color, and block
class Apple:
    def __init__(self, spawnX, spawnY):
        self.height = BLOCK_HEIGHT - 2
        self.width = BLOCK_WIDTH - 2
        self.color = RED
        self.block = pygame.Rect(spawnX, spawnY, self.height, self.width)


    #This function makes sure when the apple spawns it does not spawn
    #on the snake or on the wall
    def IsLegal(self, snake):
        if (len(snake) == (SIDE_LENGTH * SIDE_LENGTH)):
            return True
        for i in snake:
            if (i.block.top == self.block.top and i.block.left == self.block.left):
                return False
        return True

    #This function gets the number of the node the apple is on
    def GetNum(self, grid):
        for i in grid:
            for j in i:
                if ((self.block.left - OFFSET == j.coordinates[0]) and (self.block.top - OFFSET == j.coordinates[1])):
                    return j.num


#This function builds a snake of the length pased to it
def BuildSnake(startNum, path):
    snake = []
    for i in range((startNum - 1), -1, -1):
        if (i == 0):
            snake.append(Snake(path[0].coordinates[0] + OFFSET, path[0].coordinates[1] + OFFSET))
        else:
            snake.append(Snake(path[len(path) - i].coordinates[0] + OFFSET, path[len(path) - i].coordinates[1] + OFFSET))


    return snake

#This function moves the snakes head in the direction passed to it
def MoveSnake(movement, snake):
    head = snake[len(snake) - 1]

    if (movement[0]):
         snake.append(Snake((head.block.left + BLOCK_HEIGHT), head.block.top))
    if (movement[1]):
        snake.append(Snake((head.block.left - BLOCK_HEIGHT), head.block.top))
    if (movement[2]):
        snake.append(Snake(head.block.left, (head.block.top + BLOCK_HEIGHT)))
    if (movement[3]):
        snake.append(Snake(head.block.left, (head.block.top - BLOCK_HEIGHT)))

#This checks whether or not the snake has died
def TestDeath(snake):
    head = snake[len(snake) - 1]
    for i in range(len(snake) - 2):
        if (head.block.top == snake[i].block.top and head.block.left == snake[i].block.left):
            return True
        if (head.block.top <= 0 or head.block.bottom > WINHEIGHT or head.block.left <= 0 or head.block.right > WINWIDTH):
            return True

    return False

#This makes a 2D list containg the grid the nodes wil be placed in
#and adds the nodes to it
def MakeGraph(grid):
    for i in range(SIDE_LENGTH):
        tempList = []
        for j in range(SIDE_LENGTH):
            num = 0
            isEnd = False
            up = down = 1
            right = left = 0
            if (i % 2 == 0):
                num = (i * SIDE_LENGTH) + j
                if (i == 0):
                    left = 2
                if (j == 0):
                    if (i == 0):
                        isEnd = True
                        up = 2
                    else:
                        up = 2
                        left = 1
                if (i == SIDE_LENGTH - 1):
                    right = 2
                if (j == SIDE_LENGTH - 1):
                    if (i == SIDE_LENGTH - 1):
                        isEnd = True
                        down = 2
                        right = 2
                    else:
                        down = 2
                        right = 1
            else:
                num = ((SIDE_LENGTH * (i + 1)) - 1 - j)
                if (j == 0):
                    if (i == SIDE_LENGTH - 1):
                        isEnd = True
                    up = 2
                    right = 1
                if (i == SIDE_LENGTH - 1):
                    right = 2
                if (j == SIDE_LENGTH - 1):
                    down = 2
                    left = 1

            tempList.append(Node(left, right, down, up, isEnd, (i *16, j *16), (num)))

        grid.append(tempList)

#A helper function for Himil thay finds the end
#indexes of the hamiltonian path
def FindEndIndexes(grid, findSecond = False):
    if (not findSecond):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (grid[i][j].end):
                    return (i, j)
    else:
        indexes = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (grid[i][j].end):
                    indexes = (i, j)
        return indexes

#This monstrosity is what randomizes the hamiltonian path.
def Himil(grid, i):
    indexes = FindEndIndexes(grid)
    indexes2 = FindEndIndexes(grid, True)

    if (random.randint(0, 1)):
        indexes = indexes2

    endNode = grid[indexes[0]][indexes[1]]

    num = random.randint(0, 3)

    if (num == 0):
        if(endNode.right == 0):
            grid[indexes[0]][indexes[1]].right = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] + 1][indexes[1]]
            changeNode.left = 1
            newDirection = "right"
            newIndexes = (indexes[0] + 1, indexes[1])
        elif(endNode.left == 0):
            grid[indexes[0]][indexes[1]].left = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] - 1][indexes[1]]
            changeNode.right = 1
            newDirection = "left"
            newIndexes = (indexes[0] - 1, indexes[1])
        elif(endNode.up == 0):
            grid[indexes[0]][indexes[1]].up = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] - 1]
            changeNode.down = 1
            newDirection = "up"
            newIndexes = (indexes[0], indexes[1] - 1)
        elif(endNode.down == 0):
            grid[indexes[0]][indexes[1]].down = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] + 1]
            changeNode.up = 1
            newDirection = "down"
            newIndexes = (indexes[0], indexes[1] + 1)


    if (num == 1):
        if(endNode.left == 0):
            grid[indexes[0]][indexes[1]].left = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] - 1][indexes[1]]
            changeNode.right = 1
            newDirection = "left"
            newIndexes = (indexes[0] - 1, indexes[1])
        elif(endNode.right == 0):
            grid[indexes[0]][indexes[1]].right = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] + 1][indexes[1]]
            changeNode.left = 1
            newDirection = "right"
            newIndexes = (indexes[0] + 1, indexes[1])
        elif(endNode.down == 0):
            grid[indexes[0]][indexes[1]].down = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] + 1]
            changeNode.up = 1
            newDirection = "down"
            newIndexes = (indexes[0], indexes[1] + 1)
        elif(endNode.up == 0):
            grid[indexes[0]][indexes[1]].up = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] - 1]
            changeNode.down = 1
            newDirection = "up"
            newIndexes = (indexes[0], indexes[1] - 1)

    if (num == 2):
        if(endNode.up == 0):
            grid[indexes[0]][indexes[1]].up = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] - 1]
            changeNode.down = 1
            newDirection = "up"
            newIndexes = (indexes[0], indexes[1] - 1)
        elif(endNode.down == 0):
            grid[indexes[0]][indexes[1]].down = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] + 1]
            changeNode.up = 1
            newDirection = "down"
            newIndexes = (indexes[0], indexes[1] + 1)
        elif(endNode.right == 0):
            grid[indexes[0]][indexes[1]].right = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] + 1][indexes[1]]
            changeNode.left = 1
            newDirection = "right"
            newIndexes = (indexes[0] + 1, indexes[1])
        elif(endNode.left == 0):
            grid[indexes[0]][indexes[1]].left = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] - 1][indexes[1]]
            changeNode.right = 1
            newDirection = "left"
            newIndexes = (indexes[0] - 1, indexes[1])

    if (num == 3):
        if(endNode.down == 0):
            grid[indexes[0]][indexes[1]].down = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] + 1]
            changeNode.up = 1
            newDirection = "down"
            newIndexes = (indexes[0], indexes[1] + 1)
        elif(endNode.up == 0):
            grid[indexes[0]][indexes[1]].up = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0]][indexes[1] - 1]
            changeNode.down = 1
            newDirection = "up"
            newIndexes = (indexes[0], indexes[1] - 1)
        elif(endNode.left == 0):
            grid[indexes[0]][indexes[1]].left = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] - 1][indexes[1]]
            changeNode.right = 1
            newDirection = "left"
            newIndexes = (indexes[0] - 1, indexes[1])
        elif(endNode.right == 0):
            grid[indexes[0]][indexes[1]].right = 1
            grid[indexes[0]][indexes[1]].end = False
            changeNode = grid[indexes[0] + 1][indexes[1]]
            changeNode.left = 1
            newDirection = "right"
            newIndexes = (indexes[0] + 1, indexes[1])

    endNode = grid[indexes[0]][indexes[1]]

    if (changeNode.right == 1 and newDirection != "left"):
        currIndexes = (newIndexes[0] + 1, newIndexes[1])
        currentNode = grid[currIndexes[0]][currIndexes[1]]
        if(not Trace(grid, currentNode, endNode, currIndexes, "right")):
            grid[newIndexes[0]][newIndexes[1]].right = 0
            grid[newIndexes[0] + 1][newIndexes[1]].left = 0
            grid[newIndexes[0] + 1][newIndexes[1]].end = True

    if (changeNode.left == 1 and newDirection != "right"):
        currIndexes = (newIndexes[0] - 1, newIndexes[1])
        currentNode = grid[currIndexes[0]][currIndexes[1]]
        if(not Trace(grid, currentNode, endNode, currIndexes, "left")):
            grid[newIndexes[0]][newIndexes[1]].left = 0
            grid[newIndexes[0] - 1][newIndexes[1]].right = 0
            grid[newIndexes[0] - 1][newIndexes[1]].end = True

    if (changeNode.up == 1 and newDirection != "down"):
        currIndexes = (newIndexes[0], newIndexes[1] - 1)
        currentNode = grid[currIndexes[0]][currIndexes[1]]
        if(not Trace(grid, currentNode, endNode, currIndexes, "up")):
            grid[newIndexes[0]][newIndexes[1]].up = 0
            grid[newIndexes[0]][newIndexes[1] - 1].down = 0
            grid[newIndexes[0]][newIndexes[1] - 1].end = True

    if (changeNode.down == 1 and newDirection != "up"):
        currIndexes = (newIndexes[0], newIndexes[1] + 1)
        currentNode = grid[currIndexes[0]][currIndexes[1]]
        if(not Trace(grid, currentNode, endNode, currIndexes, "down")):
            grid[newIndexes[0]][newIndexes[1]].down = 0
            grid[newIndexes[0]][newIndexes[1] + 1].up = 0
            grid[newIndexes[0]][newIndexes[1] + 1].end = True


#This is used to find which node should become the new end of the path,
#if it reaches the current end then it should not, but if it reaches a
#a different end then it should
def Trace(grid, currentNode, endNode, currIndexes, direction):

    if (currentNode == endNode):
        return False
    elif (currentNode.end):
        return True

    if(currentNode.right == 1 and direction != "left"):
        newIndexes = (currIndexes[0] + 1, currIndexes[1])
        currentNode = grid[newIndexes[0]][newIndexes[1]]
        return Trace(grid, currentNode, endNode, newIndexes, "right")

    if(currentNode.left == 1 and direction != "right"):
        newIndexes = (currIndexes[0] - 1, currIndexes[1])
        currentNode = grid[newIndexes[0]][newIndexes[1]]
        return Trace(grid, currentNode, endNode, newIndexes, "left")

    if(currentNode.up == 1 and direction != "down"):
        newIndexes = (currIndexes[0], currIndexes[1] - 1)
        currentNode = grid[newIndexes[0]][newIndexes[1]]
        return Trace(grid, currentNode, endNode, newIndexes, "up")

    if(currentNode.down == 1 and direction != "up"):
        newIndexes = (currIndexes[0], currIndexes[1] + 1)
        currentNode = grid[newIndexes[0]][newIndexes[1]]
        return Trace(grid, currentNode, endNode, newIndexes, "down")

#This is a helper function for Himil that checks whether or not the
#current path is a hamiltonion path (the two ends are next to each other)
def CheckIfCycle(grid):
    firstIndexes = FindEndIndexes(grid)
    secondIndexes = FindEndIndexes(grid, True)

    subtractedIndexes = (firstIndexes[0] - secondIndexes[0], firstIndexes[1] - secondIndexes[1])


    if (subtractedIndexes == (1, 0)):
        grid[firstIndexes[0]][firstIndexes[1]].left = 1
        grid[secondIndexes[0]][secondIndexes[1]].right = 1
        return True

    elif (subtractedIndexes == (-1, 0)):
        grid[firstIndexes[0]][firstIndexes[1]].right = 1
        grid[secondIndexes[0]][secondIndexes[1]].left = 1
        return True

    elif (subtractedIndexes == (0, 1)):
        grid[firstIndexes[0]][firstIndexes[1]].down = 1
        grid[secondIndexes[0]][secondIndexes[1]].up = 1
        return True

    elif (subtractedIndexes == (0, -1)):
        grid[firstIndexes[0]][firstIndexes[1]].up = 1
        grid[secondIndexes[0]][secondIndexes[1]].down = 1
        return True

    else:
        return False

#This is a helper function for Himil that re numbers the nodes that
#are being restructured for the random path
def ReNumber(grid):
    p = FindEndIndexes(grid)
    q = FindEndIndexes(grid, True)
    endNode = grid[q[0]][q[1]]
    grid[q[0]][q[1]].num = ((SIDE_LENGTH * SIDE_LENGTH) - 1)
    currentNode = grid[p[0]][p[1]]

    currIndexes = p

    direction = 'left'

    count = 0
    while(currentNode != endNode):

        print(currIndexes)

        grid[currIndexes[0]][currIndexes[1]].num = count


        if(currentNode.right == 1 and direction != "left"):
            currIndexes = (currIndexes[0] + 1, currIndexes[1])
            currentNode = grid[currIndexes[0]][currIndexes[1]]
            direction = "right"

        elif(currentNode.left == 1 and direction != "right"):
            currIndexes = (currIndexes[0] - 1, currIndexes[1])
            currentNode = grid[currIndexes[0]][currIndexes[1]]
            direction = "left"

        elif(currentNode.up == 1 and direction != "down"):
            currIndexes = (currIndexes[0], currIndexes[1] - 1)
            currentNode = grid[currIndexes[0]][currIndexes[1]]
            direction = "up"

        elif(currentNode.down == 1 and direction != "up"):
            currIndexes = (currIndexes[0], currIndexes[1] + 1)
            currentNode = grid[currIndexes[0]][currIndexes[1]]
            direction = "down"

        count += 1

#Makes a list that contains the numbers of the hamiltonian path
def MakePath(grid):
    path = []
    for i in range (SIDE_LENGTH * SIDE_LENGTH):
        path.append(0)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            path[grid[i][j].num] = grid[i][j]

    return path


#Replace the AI with this if a person wants to play
def PlayerMove():
    for i in pygame.event.get():
        if (i.type == QUIT):
            playing = False
            pygame.quit()
            sys.exit()
        elif (i.type == KEYDOWN):
            if (i.key == K_k):
                playing = False
                pygame.quit()
                sys.exit()
            elif (i.key == K_RIGHT):
                movement[0] = 1
                movement[1] = 0
                movement[2] = 0
                movement[3] = 0

            elif (i.key == K_LEFT):
                movement[0] = 0
                movement[1] = 1
                movement[2] = 0
                movement[3] = 0

            elif (i.key == K_DOWN):
                movement[0] = 0
                movement[1] = 0
                movement[2] = 1
                movement[3] = 0

            elif (i.key == K_UP):
                movement[0] = 0
                movement[1] = 0
                movement[2] = 0
                movement[3] = 1


#First AI for nostalgia
def FirstAI():

        first = True
        distance = 0
        onlyMove = []
        headLocation = 0


        if(headLocation == len(path)):
            headLocation = 0

        moveOptions = [path[headLocation].right, path[headLocation].left, path[headLocation].down, path[headLocation].up]
        if (first):
            testCoord = (snake[len(snake) - 1].block.left - OFFSET, snake[len(snake) - 1].block.top - OFFSET)

            #Up
            if(moveOptions[2] == 1):
                tempCoord = (testCoord[0], testCoord[1] - 16)
                if(tempCoord == path[headLocation + 1].coordinates):
                    onlyMove = [0, 0, 0, 1]

            #Right
            if(moveOptions[0] == 1):
                tempCoord = (testCoord[0] + 16, testCoord[1])
                if(tempCoord == path[headLocation + 1].coordinates):
                    onlyMove = [1, 0, 0, 0]

            #Down
            if(moveOptions[3] == 1):
                tempCoord = (testCoord[0], testCoord[1] + 16)
                if(tempCoord == path[headLocation + 1].coordinates):
                    onlyMove = [0, 0, 1, 0]

            #Left
            if(moveOptions[1] == 1):
                tempCoord = (testCoord[0] - 16, testCoord[1])
                if(tempCoord == path[headLocation + 1].coordinates):
                    onlyMove = [0, 1, 0, 0]

            first = False

        else:
            if (onlyMove[0] == 1):
                onlyMove[0] = 0
                onlyMove[1] = 1

            elif (onlyMove[1] == 1):
                onlyMove[0] = 1
                onlyMove[1] = 0

            elif (onlyMove[2] == 1):
                onlyMove[2] = 0
                onlyMove[3] = 1

            elif (onlyMove[3] == 1):
                onlyMove[2] = 1
                onlyMove[3] = 0

            tempList = []
            for i in range(len(onlyMove)):
                if(moveOptions[i] == 2):
                    moveOptions[i] = 0

                #I Multiply by -1 because the direction becomes -1, not 1. So i must
                #change it to 1. Also 0 * -1 is still 0, so i dont need to correct
                #anything
                tempList.append(-1* (onlyMove[i] - moveOptions[i]))

            onlyMove = tempList



            headLocation += 1


#Better AI that is currently being used
def Jeremy():
    if (len(snake) < 50):
        skipLength = 500
    elif (len(snake) < 100):
        skipLength = 100
    elif (len(snake) < 140):
        skipLength = 35
    elif (len(snake) < 400):
        skipLength = 30
    elif (len(snake) < 800):
        skipLength = 10
    else:
        skipLength = 2

    currentNum = grid[gridIndexes[0]][gridIndexes[1]].num
    appleNum = apple.GetNum(grid)
    maxNum = -1
    maxIndexes = gridIndexes
    if(currentNum <= appleNum):
        if (gridIndexes[0] > 0):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0] - 1][gridIndexes[1]].coordinates)):
                    isThere = True
            if(not isThere):
                if(maxNum < grid[gridIndexes[0] - 1][gridIndexes[1]].num and grid[gridIndexes[0] - 1][gridIndexes[1]].num <= appleNum and (grid[gridIndexes[0] - 1][gridIndexes[1]].num <  (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0] - 1][gridIndexes[1]].num
                    maxIndexes = (gridIndexes[0] - 1, gridIndexes[1])
                    movement = (0, 1, 0, 0)

        if(gridIndexes[0] < (len(grid) - 1)):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0] + 1][gridIndexes[1]].coordinates)):
                    isThere = True
            if(not isThere):
                if(maxNum < grid[gridIndexes[0] + 1][gridIndexes[1]].num and grid[gridIndexes[0] + 1][gridIndexes[1]].num <= appleNum and (grid[gridIndexes[0] + 1][gridIndexes[1]].num < (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0] + 1][gridIndexes[1]].num
                    maxIndexes = (gridIndexes[0] + 1, gridIndexes[1])
                    movement = (1, 0, 0, 0)

        if (gridIndexes[1] > 0):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] - 1].coordinates)):
                    isThere = True
            if(not isThere):
                if(maxNum < grid[gridIndexes[0]][gridIndexes[1] - 1].num and grid[gridIndexes[0]][gridIndexes[1] - 1].num <= appleNum and (grid[gridIndexes[0]][gridIndexes[1] - 1].num < (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0]][gridIndexes[1] - 1].num
                    maxIndexes = (gridIndexes[0], gridIndexes[1] - 1)
                    movement = (0, 0, 0, 1)

        if(gridIndexes[1] < (len(grid) - 1)):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] + 1].coordinates)):
                    isThere = True
            if(not isThere):
                if(maxNum < grid[gridIndexes[0]][gridIndexes[1] + 1].num and grid[gridIndexes[0]][gridIndexes[1] + 1].num <= appleNum and (grid[gridIndexes[0]][gridIndexes[1] + 1].num < (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0]][gridIndexes[1] + 1].num
                    maxIndexes = (gridIndexes[0], gridIndexes[1] + 1)
                    movement = (0, 0, 1, 0)

    else:
        if (gridIndexes[0] > 0):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0] - 1][gridIndexes[1]].coordinates)):
                    isThere = True
            if(not isThere):
                if ((maxNum < grid[gridIndexes[0] - 1][gridIndexes[1]].num or grid[gridIndexes[0] - 1][gridIndexes[1]].num == 0) and (grid[gridIndexes[0] - 1][gridIndexes[1]].num <  (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0] - 1][gridIndexes[1]].num
                    maxIndexes = (gridIndexes[0] - 1, gridIndexes[1])
                    movement = (0, 1, 0, 0)

        if(gridIndexes[0] < (len(grid) - 1)):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0] + 1][gridIndexes[1]].coordinates)):
                    isThere = True
            if(not isThere):
                if ((maxNum < grid[gridIndexes[0] + 1][gridIndexes[1]].num or grid[gridIndexes[0] + 1][gridIndexes[1]].num == 0) and (grid[gridIndexes[0] + 1][gridIndexes[1]].num <  (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0] + 1][gridIndexes[1]].num
                    maxIndexes = (gridIndexes[0] + 1, gridIndexes[1])
                    movement = (1, 0, 0, 0)

        if (gridIndexes[1] > 0):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] - 1].coordinates)):
                    isThere = True
            if(not isThere):
                if ((maxNum < grid[gridIndexes[0]][gridIndexes[1] - 1].num or grid[gridIndexes[0]][gridIndexes[1] - 1].num == 0) and (grid[gridIndexes[0]][gridIndexes[1] - 1].num <  (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0]][gridIndexes[1] - 1].num
                    maxIndexes = (gridIndexes[0], gridIndexes[1] - 1)
                    movement = (0, 0, 0, 1)

        if(gridIndexes[1] < (len(grid) - 1)):
            isThere = False
            for i in snake:
                if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] + 1].coordinates)):
                    isThere = True
            if(not isThere):
                if ((maxNum < grid[gridIndexes[0]][gridIndexes[1] + 1].num or grid[gridIndexes[0]][gridIndexes[1] + 1].num == 0) and (grid[gridIndexes[0]][gridIndexes[1] + 1].num <  (skipLength + currentNum))):
                    maxNum = grid[gridIndexes[0]][gridIndexes[1] + 1].num
                    maxIndexes = (gridIndexes[0], gridIndexes[1] + 1)
                    movement = (0, 0, 1, 0)



    gridIndexes = maxIndexes
