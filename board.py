import pygame
import numpy as np
from enum import Enum
import enum


# Represents a cardinal direction
class Dir(Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    # Calculates the angle to 180 degrees, in units of 90 degrees
    def angle_to_left(self):
        if self == Dir.UP:
            return 1
        if self == Dir.DOWN:
            return -1
        if self == Dir.LEFT:
            return 0
        if self == Dir.RIGHT:
            return 2


def create_board(side):
    return np.zeros((side, side), int)

# Filter out the zero elements of a given array, leaving only the nonzero elements


def filter_nonzeros(arr):
    nonzeros = []
    for i in arr:
        if i != 0:
            nonzeros.append(i)
    return nonzeros


# Shifts a row left according to 2048 semantics and returns the resulting row
# Empty tiles are represented with zeros
def shift_row(row):
    nonzeros = filter_nonzeros(row)
    shifted_tiles = []
    i = 1
    while i < len(nonzeros):
        right_tile = nonzeros[i]
        left_tile = nonzeros[i - 1]
        # Try to combine the tiles at index i - 1 and i
        if left_tile == right_tile:
            # If we can merge the tiles, add a doubled tile to the result
            # and bump the index by 2 to consider the next unmerged tile
            shifted_tiles.append(left_tile + 1)
            i += 2
        else:
            # Otherwise, we cannot merge the tile at index i,
            # so we append it to the result unchanged. We bump the counter by
            # 1 to try to merge the tiles at indices i and i + 1
            shifted_tiles.append(left_tile)
            i += 1
    # If we did not merge the second to last and last tile, we have to add the
    # last tile unchanged to the result
    if i == len(nonzeros):
        shifted_tiles.append(nonzeros[-1])
    # We pad the "empty space" created by merging and shifting tiles with empty tiles
    pad_length = len(row) - len(shifted_tiles)
    return np.pad(shifted_tiles, (0, pad_length), 'constant')

# Shifts a matrix left according to the 2048 semantics


def shift_left(matrix):
    return np.array([shift_row(row) for row in matrix])

# Shifts a matrix in a given direction according to the 2048 semantics


def shift(matrix, dir):
    # Rotate the matrix so we shift left, and then rotate back
    angle = dir.angle_to_left()
    return np.rot90(shift_left(np.rot90(matrix, angle)), -angle)


white = (255, 255, 255)
black = (0, 0, 0)
gray = (169, 169, 169)
tile_empty = (204, 192, 179)
tile_2 = (238, 228, 218)
tile_4 = (237, 224, 200)
tile_8 = (242, 177, 121)
tile_16 = (245, 149, 99)
tile_32 = (246, 124, 95)
tile_64 = (246, 94, 59)
tile_128 = (237, 207, 114)
tile_256 = (237, 204, 97)
tile_512 = (237, 200, 80)
tile_1024 = (237, 197, 63)
tile_2048 = (237, 194, 46)


tile_colors = [tile_empty, tile_2, tile_4, tile_8, tile_16, tile_32,
               tile_64, tile_128, tile_256, tile_512, tile_1024, tile_2048]


# Represents a 2048 board
class Board:
    def __init__(self, arg=4):
        if isinstance(arg, int):
            # initalize with side length
            self.side = arg
            self.board = create_board(self.side)
        else:
            # initialize with matrix
            self.side = len(arg)
            self.board = np.array(arg)

    def __str__(self):
        return str(np.array([[0 if i == 0 else 2 ** i for i in row] for row in self.board]))

    # Shift this 2048 board in place
    def shift(self, dir: Dir):
        self.board = shift(self.board, dir)

    def at(self, i, j):
        return self.board[i][j]

    def draw(self, screen, width, height, clock):
        count = 0
        font_size = height // self.side // 2
        font = pygame.font.Font(None, font_size)
        tile_height = height // self.side
        tile_width = width // self.side
        for i in range(self.side):
            for j in range(self.side):
                tile_exponent = self.at(i, j)
                to_shift = tile_width / 2
                tileX = j * tile_width + to_shift
                tileY = i * tile_height + to_shift / 2

                tile_color = tile_colors[tile_exponent + count]
                if count < len(tile_colors) - 2:
                    count = count + 0
                else:
                    count = 0

                text_color = white
                if tile_color == tile_2 or tile_color == tile_4:
                    text_color = gray

                tile = pygame.draw.rect(screen, tile_color, (tileX - to_shift,
                                                             tileY - to_shift / 2, tile_width, tile_height))

                tile_number = 2 ** tile_exponent
                # if no number, then text is ""]
                tile_text = font.render(str(tile_number), True,
                                        text_color) if tile_number != 1 else font.render("", True,
                                                                                         text_color)
                tile_rect = tile_text.get_rect(centerx=tileX, y=tileY)
                screen.blit(tile_text, tile_rect)

        # draw vertical and horizontal separating lines
        for i in range(2):
            for j in range(self.side + 3):
                if i == 0:  # horizontal
                    pygame.draw.line(
                        screen, white, (0, j * tile_height), (width, j * tile_height))
                else:  # vertical
                    pygame.draw.line(
                        screen, white, (j * tile_width, 0), (j * tile_width, height))

        pygame.display.flip()
        clock.tick(60)

    def test_gui(self):
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j] = 0
