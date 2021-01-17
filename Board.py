import pygame
import numpy as np
import math as m

pygame.init()


def init_centerpoints():
    """
    :return: List of coordinate points at center of boxes
    """
    centerpoints = []
    for i in range(56, 307, 124):
        for j in range(56, 307, 124):
            centerpoints.append((j, i))
    return centerpoints


def draw_cross(coord):
    """
    :param coord: Coordinate points
    :return: Draws circle on surface at coordinates
    """
    x, y = coord

    for i in range(-25, 26):
        for j in range(-2, 5):
            board[x + i + j][y + i] = 0
            board[x - i + j][y + i] = 0


def draw_circle(coord):
    """
    :param coord: Coordinate points
    :return: Draws circle on surface at coordinates
    """
    x, y = coord
    first_radius = 25
    for radius in range(first_radius, first_radius + 4):
        for i in range(-radius, radius + 1):
            board[x + i][m.ceil(y + m.sqrt(radius ** 2 - i ** 2))] = 0
            board[x + i][m.ceil(y - m.sqrt(radius ** 2 - i ** 2))] = 0
            board[m.ceil(x + m.sqrt(radius ** 2 - i ** 2))][y + i] = 0
            board[m.ceil(x - m.sqrt(radius ** 2 - i ** 2))][y + i] = 0

            board[x + i][m.floor(y + m.sqrt(radius ** 2 - i ** 2))] = 0
            board[x + i][m.floor(y - m.sqrt(radius ** 2 - i ** 2))] = 0
            board[m.floor(x + m.sqrt(radius ** 2 - i ** 2))][y + i] = 0
            board[m.floor(x - m.sqrt(radius ** 2 - i ** 2))][y + i] = 0


def get_box():
    """
    :return: Box index
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    abs_diff = []
    # find way to check if mouse in window
    for i in range(0, 9):
        x, y = centerpoints[i]
        abs_diff.append(abs(m.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)))
    return abs_diff.index(min(abs_diff))


def light_box(pos):
    """
    :param pos: Box index
    :return: Lights up box at index
    """
    onoroff = []
    for i in range(0, 9):
        if i == get_box():
            onoroff.append(True)
        else:
            onoroff.append(False)
    first_radius = 56

    for r in range(first_radius - 15, first_radius):

        # Draw Box
        for i in range(0, 9):
            if onoroff[i] and get_box() not in filledBox:
                x, y = centerpoints[i]
                for j in range(-r, r + 1, 2 * r):
                    for k in range(-r, r + 1):
                        board[x + j][y + k][1] = (r - 35) * 12
                        board[x - k][y - j][1] = (r - 35) * 12
                        board[x + j][y + k][0] = (r - 35) * 12
                        board[x - k][y - j][0] = (r - 35) * 12

            # Clean up previous squares
            else:
                x, y = centerpoints[i]
                for j in range(-r, r + 1, 2 * r):
                    for k in range(-r, r + 1):
                        board[x + j][y + k] = 255
                        board[x - k][y - j] = 255


def check_win():
    for i in range(0, 8, 3):
        if states[i:i + 3].count("X") == 3 or states[i:i + 3].count("O") == 3:
            print("{} Wins".format(states[i]))
            return False

    for i in range(0, 3):
        if states[i::3].count("X") == 3 or states[i::3].count("O") == 3:
            print("{} Wins".format(states[i]))
            return False

    if states[::4].count("X") == 3 or states[::4].count("O") == 3:
        print("{} Wins".format(states[4]))
        return False

    elif states[2:7:2].count("X") == 3 or states[2:7:2].count("O") == 3:
        print("{} Wins".format(states[4]))
        return False

    return True


size = (360, 360)
arraySize = (360, 360, 3)
squareSize = (114, 114)
display = pygame.display.set_mode(size)


# Create Surface
board = np.ones(arraySize)
board *= 255

centerpoints = init_centerpoints()
filledBox = []
states = []
for i in range(0, 9):
    states.append("Empty")

# Draw lines
for i in range(114, 124):
    for j in range(0, size[0]):
        for k in range(0, 3):
            board[i][j][k] = 0
            board[i + 123][j][k] = 0
            board[j][i][k] = 0
            board[j][i + 123][k] = 0

surf = pygame.surfarray.make_surface(board)
display.blit(surf, (0, 0))
pygame.display.update()

turn = True
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Some times just likes to miss a click for no fucking reason
        # reeeeeeeeeeeeeeeeeeeeeee
        if event.type == pygame.MOUSEBUTTONUP and get_box() not in filledBox:
            box = get_box()
            if turn:
                draw_cross(centerpoints[box])
                filledBox.append(box)
                states[box] = "X"
                turn = False
            else:
                draw_circle(centerpoints[box])
                filledBox.append(box)
                states[box] = "O"
                turn = True
            running = check_win()

    light_box(get_box())
    surf = pygame.surfarray.make_surface(board)
    display.blit(surf, (0, 0))
    pygame.display.update()
pygame.quit()
