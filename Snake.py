import Snakefunctions
import pygame, random, sys
from pygame.locals import *
from Snakefunctions import *

pygame.init()

clock = pygame.time.Clock()

window  = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)

def main():
    #Create the grid
    grid = []
    MakeGraph(grid)

    i = 1
    while(not CheckIfCycle(grid)):
        Himil(grid, i)
        i += 1

    ReNumber(grid)

    path = MakePath(grid)

    #Bool for if its first iteration
    playing = True

    #Spawn in apple and make the snake, start its movement at nothing
    apple = Apple(WINWIDTH - (random.randint(0, 32) * 16) + 2, WINHEIGHT - (random.randint(0, 32) * 16) + 2)
    snake = BuildSnake(4, path)
    gridIndexes = (0, 0)
    movement = (0, 0, 0, 0)
    
    speed = 10
    first = True
    distance = 0
    onlyMove = []
    headLocation = 0
    for i in range(len(grid)):
        for j in range(i):
            if (grid[i][j].num == 0):
                gridIndexes = (i, j)
                
    while (playing):

        #checks if you close the application or hit a key
        for i in pygame.event.get():
            if (i.type == QUIT):
                playing = False
                pygame.quit()
                sys.exit()
            #This allows you to change speed of the snake as it can sometimes be slow
            if (i.type == KEYDOWN):
                if (i.key == K_LEFT):
                    speed -= 10
                if (i.key == K_RIGHT):
                    speed += 10

        window.fill(BLACK)
        for i in snake:
            pygame.draw.rect(window, i.color, i.block)
        pygame.draw.rect(window, apple.color, apple.block)


        #changes how much of the path the snake can omit based on its length
        if (len(snake) < 50):
            skipLength = 500
        elif (len(snake) < 100):
            skipLength = 100
        elif (len(snake) < 140):
            skipLength = 25
        elif (len(snake) < 300):
            skipLength = 2
        else:
            skipLength = 2

        #Changes the movement of the snake based on its current sqaure, the squares around it,
        #the sqaure of the apple, and its allowed skip length
        currentNum = grid[gridIndexes[0]][gridIndexes[1]].num
        appleNum = apple.GetNum(grid)
        #Max num is to make sure that the snake moves the highest possible value allowed to it
        maxNum = -1
        maxIndexes = gridIndexes

        #If the snakes sqaure number is less than the apples
        if(currentNum <= appleNum):
            #If the left isnt a wall
            if (gridIndexes[0] > 0):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0] - 1][gridIndexes[1]].coordinates)):
                        isThere = True
                #If the sqaure is a higher number than where it is currently going to move and less than or equal to the
                #number of the apples square go to
                if(not isThere):
                    if(maxNum < grid[gridIndexes[0] - 1][gridIndexes[1]].num and grid[gridIndexes[0] - 1][gridIndexes[1]].num <= appleNum and (grid[gridIndexes[0] - 1][gridIndexes[1]].num <  (skipLength + currentNum))):
                        maxNum = grid[gridIndexes[0] - 1][gridIndexes[1]].num
                        maxIndexes = (gridIndexes[0] - 1, gridIndexes[1])
                        movement = (0, 1, 0, 0)

            #If the right isnt a wall
            if(gridIndexes[0] < (len(grid) - 1)):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0] + 1][gridIndexes[1]].coordinates)):
                        isThere = True
                #If the sqaure is a higher number than where it is currently going to move and less than or equal to the
                #number of the apples square go to
                if(not isThere):
                    if(maxNum < grid[gridIndexes[0] + 1][gridIndexes[1]].num and grid[gridIndexes[0] + 1][gridIndexes[1]].num <= appleNum and (grid[gridIndexes[0] + 1][gridIndexes[1]].num < (skipLength + currentNum))):
                        maxNum = grid[gridIndexes[0] + 1][gridIndexes[1]].num
                        maxIndexes = (gridIndexes[0] + 1, gridIndexes[1])
                        movement = (1, 0, 0, 0)

            #If up isnt a wall
            if (gridIndexes[1] > 0):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] - 1].coordinates)):
                        isThere = True
                #If the sqaure is a higher number than where it is currently going to move and less than or equal to the
                #number of the apples square go to
                if(not isThere):
                    if(maxNum < grid[gridIndexes[0]][gridIndexes[1] - 1].num and grid[gridIndexes[0]][gridIndexes[1] - 1].num <= appleNum and (grid[gridIndexes[0]][gridIndexes[1] - 1].num < (skipLength + currentNum))):
                        maxNum = grid[gridIndexes[0]][gridIndexes[1] - 1].num
                        maxIndexes = (gridIndexes[0], gridIndexes[1] - 1)
                        movement = (0, 0, 0, 1)

            #If down isnt a wall
            if(gridIndexes[1] < (len(grid) - 1)):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] + 1].coordinates)):
                        isThere = True
                #If the sqaure is a higher number than where it is currently going to move and less than or equal to the
                #number of the apples square go to
                if(not isThere):
                    if(maxNum < grid[gridIndexes[0]][gridIndexes[1] + 1].num and grid[gridIndexes[0]][gridIndexes[1] + 1].num <= appleNum and (grid[gridIndexes[0]][gridIndexes[1] + 1].num < (skipLength + currentNum))):
                        maxNum = grid[gridIndexes[0]][gridIndexes[1] + 1].num
                        maxIndexes = (gridIndexes[0], gridIndexes[1] + 1)
                        movement = (0, 0, 1, 0)

        else:
             #If the left isnt a wall
            if (gridIndexes[0] > 0):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0] - 1][gridIndexes[1]].coordinates)):
                        isThere = True
                #If the square is a higher number than where it is currently going to move or if the square is equal to zero
                if(not isThere):
                    if ((maxNum < grid[gridIndexes[0] - 1][gridIndexes[1]].num or grid[gridIndexes[0] - 1][gridIndexes[1]].num == 0) and (grid[gridIndexes[0] - 1][gridIndexes[1]].num <  (skipLength + currentNum)) and maxNum != 0):
                        maxNum = grid[gridIndexes[0] - 1][gridIndexes[1]].num
                        maxIndexes = (gridIndexes[0] - 1, gridIndexes[1])
                        movement = (0, 1, 0, 0)

            #If the right isnt a wall
            if(gridIndexes[0] < (len(grid) - 1)):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0] + 1][gridIndexes[1]].coordinates)):
                        isThere = True
                #If the square is a higher number than where it is currently going to move or if the square is equal to zero
                if(not isThere):
                    if ((maxNum < grid[gridIndexes[0] + 1][gridIndexes[1]].num or grid[gridIndexes[0] + 1][gridIndexes[1]].num == 0) and (grid[gridIndexes[0] + 1][gridIndexes[1]].num <  (skipLength + currentNum)) and maxNum != 0):
                        maxNum = grid[gridIndexes[0] + 1][gridIndexes[1]].num
                        maxIndexes = (gridIndexes[0] + 1, gridIndexes[1])
                        movement = (1, 0, 0, 0)

            #If up isnt a wall
            if (gridIndexes[1] > 0):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] - 1].coordinates)):
                        isThere = True
                #If the square is a higher number than where it is currently going to move or if the square is equal to zero
                if(not isThere):
                    if ((maxNum < grid[gridIndexes[0]][gridIndexes[1] - 1].num or grid[gridIndexes[0]][gridIndexes[1] - 1].num == 0) and (grid[gridIndexes[0]][gridIndexes[1] - 1].num <  (skipLength + currentNum)) and maxNum != 0):
                        maxNum = grid[gridIndexes[0]][gridIndexes[1] - 1].num
                        maxIndexes = (gridIndexes[0], gridIndexes[1] - 1)
                        movement = (0, 0, 0, 1)

            #If down isnt a wall
            if(gridIndexes[1] < (len(grid) - 1)):
                isThere = False
                #If the snakes body is not there
                for i in snake:
                    if(i.IsThere(grid[gridIndexes[0]][gridIndexes[1] + 1].coordinates)):
                        isThere = True
                #If the square is a higher number than where it is currently going to move or if the square is equal to zero
                if(not isThere):
                    if ((maxNum < grid[gridIndexes[0]][gridIndexes[1] + 1].num or grid[gridIndexes[0]][gridIndexes[1] + 1].num == 0) and (grid[gridIndexes[0]][gridIndexes[1] + 1].num <  (skipLength + currentNum)) and maxNum != 0):
                        maxNum = grid[gridIndexes[0]][gridIndexes[1] + 1].num
                        maxIndexes = (gridIndexes[0], gridIndexes[1] + 1)
                        movement = (0, 0, 1, 0)



        gridIndexes = maxIndexes
        MoveSnake(movement, snake)

        #check if the snake died
        if (TestDeath(snake)):
            playing = False
            print("You Lose!")
            print("Score: ", len(snake))

        #If the apple was eaten respawn the apple and dont delete the snakes tail
        if (snake[len(snake) - 1].block.top == apple.block.top and snake[len(snake) - 1].block.left == apple.block.left):
            apple = Apple(WINWIDTH - BLOCK_WIDTH - (random.randint(0, (SIDE_LENGTH - 1)) * BLOCK_HEIGHT) + OFFSET, WINHEIGHT - BLOCK_HEIGHT -(random.randint(0, (SIDE_LENGTH - 1)) * BLOCK_HEIGHT) + OFFSET)
            while(not apple.IsLegal(snake)):
                apple = Apple(WINWIDTH - BLOCK_WIDTH - (random.randint(0, (SIDE_LENGTH - 1)) * BLOCK_HEIGHT) + OFFSET, WINHEIGHT - BLOCK_HEIGHT -(random.randint(0, (SIDE_LENGTH - 1)) * BLOCK_HEIGHT) + OFFSET)

        #Otherwise delete the tail
        else:
            snake.pop(0)

        #If the snake has became the screen you win
        if (len(snake) == (SIDE_LENGTH * SIDE_LENGTH)):
            playing = False
            print("You Win!")
            print("Score:", len(snake))
            pygame.quit()
            sys.exit()




        pygame.display.update()
        clock.tick(speed)






main()
