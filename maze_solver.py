from PIL import Image
from timeit import default_timer as timer
import pygame
import pygame.gfxdraw

mazeImage = Image.open('mazeSmall.png')
pix = mazeImage.load()
size = mazeImage.size
width = size[0]
height = size[1]
maze = []
solution = []
wasHere = set()
scaleFactor = 4
offset = 2


def mazeCreator():
    """
    Create a 2D list from the maze image.
    - "B" for black (wall)
    - "W" for white (path)
    """
    for y in range(0, height):
        # Create a list for each row in the maze
        mazeX = []
        for x in range(0, width):
            # Check if the pixel is black or white
            if pix[x, y] == (0, 0, 0):
                mazeX.append("B")
            elif pix[x, y] == (255, 255, 255):
                mazeX.append("W")
        # Add the row to the maze
        maze.append(mazeX)


def findPoints():
    """
    Finds the entry and exit points of the maze.
    """
    indexA = 0
    pointA = 0
    indexB = 0
    pointB = 0

    try:
        # Check left and right sides of the maze
        pointA = [i for i, j in enumerate(maze[0]) if j == "W"][0]
        indexA = 0

        if not pointA:
            pointA = [i for i, j in enumerate(maze[height - 1]) if j == "W"][0]
            indexA = height - 1
        else:
            pointB = [i for i, j in enumerate(maze[height - 1]) if j == "W"][0]
            indexB = height - 1
    except:
        pass

    if not pointA:
        # Check top and bottom sides of the maze
        for x in range(0, len(maze)):
            if maze[x][0] == "W":
                indexA = x
                pointA = 0
    else:
        for x in range(0, len(maze)):
            if maze[x][0] == "W":
                indexB = x
                pointB = 0

    for x in range(0, len(maze)):
        if maze[x][width - 1] == "W":
            indexB = x
            pointB = width - 1

    return indexA, pointA, indexB, pointB


def recursiveSolve(y, x):
    """
    Solve the maze by recursively exploring all available paths.

    :param y: The current y-coordinate of the maze
    :param x: The current x-coordinate of the maze
    """
    while (y, x) != (exitY, exitX):
        pos = (y, x)
        # Keep track of all the positions that have been visited
        wasHere.add((y, x))
        # Keep track of all the positions that have been taken
        solution.append((y, x))
        # Visualise the solution
        visualiseSolver(x, y, (255, 0, 0))
        # Check if there is a path up, right, down, or left
        if maze[y - 1][x] == "W" and (y - 1, x) not in wasHere:
            # print("Up")
            possibleSteps = (y - 1, x)
        elif maze[y][x + 1] == "W" and (y, x + 1) not in wasHere:
            # print("Right")
            possibleSteps = (y, x + 1)
        elif maze[y + 1][x] == "W" and (y + 1, x) not in wasHere:
            # print("Down")
            possibleSteps = (y + 1, x)
        elif maze[y][x - 1] == "W" and (y, x - 1) not in wasHere:
            # print("Left")
            possibleSteps = (y, x - 1)
        else:
            # print("Stuck", pos)
            # If stuck, backtrack to the previous position
            solution.pop()
            possibleSteps = (solution[-1][0], solution[-1][1])
            solution.pop()
            # Visualise the backtrack
            visualiseSolver(x, y, (255, 255, 255))

        y = possibleSteps[0]
        x = possibleSteps[1]
    # Once the exit is reached, add the exit to the solution
    solution.append((exitY, exitX))
    visualiseSolver(exitX, exitY, (255, 0, 0))
    print("Solution:", solution)


def printImage():
    """
    Saves the maze solution as an image.

    :return: None
    """
    # Loop through the solution and change the color of the pixels to red
    for x in solution:
        pix[x[1], x[0]] = (255, 0, 0)
    # Save the image with the solution
    mazeImage.save("mazeSol.png")


def visualise():
    pygame.init()
    windowSize = 1920, 1080
    screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.DOUBLEBUF)
    screen.set_alpha(None)
    pygame.display.set_caption('Maze Solver')
    screen.fill((255, 255, 255))

    return screen


def visualiseMaze():
    """
    Visualises the maze on the pygame window.
    """
    # Loop through the maze and draw the walls (black) and the path (white)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "B":
                # Create a rectangle for each pixel in the maze
                rect = pygame.Rect((x * scaleFactor) + offset, (y * scaleFactor) + offset, scaleFactor, scaleFactor)
                # Draw the rectangle on the screen
                pygame.draw.rect(screen, (0, 0, 0), rect)
                # Update the display for each pixel
                pygame.event.pump()
    # Update the display one last time
    pygame.display.flip()


def visualiseSolver(x, y, color):
    """
    Visualises the solution of the maze on the pygame window.

    :param x: x-coordinate of the solution
    :param y: y-coordinate of the solution
    :param color: color of the solution
    :return: None
    """
    # Create a rectangle for each pixel in the solution
    rect = pygame.Rect((x * scaleFactor) + offset, (y * scaleFactor) + offset, scaleFactor, scaleFactor)
    # Draw the rectangle on the screen
    pygame.draw.rect(screen, color, rect)
    # Update the display for each pixel
    pygame.display.update(rect)
    # Process any events (e.g. closing the window)
    pygame.event.pump()


mazeCreator()
(entryY, entryX, exitY, exitX) = findPoints()
print("Entry:", entryY, entryX)
print("Exit:", exitY, exitX)
screen = visualise()
visualiseMaze()
visualiseSolver(entryX, entryY, (0, 255, 0))
visualiseSolver(exitX, exitY, (0, 255, 0))
start = timer()
recursiveSolve(entryY, entryX)
printImage()

timeTaken = timer() - start
print("Time Taken: ", timeTaken)

running = True

while running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False