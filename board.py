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
    return np.array([ shift_row(row) for row in matrix ])

# Shifts a matrix in a given direction according to the 2048 semantics
def shift(matrix, dir):
    # Rotate the matrix so we shift left, and then rotate back 
    angle = dir.angle_to_left()
    return np.rot90(shift_left(np.rot90(matrix, angle)), -angle)


white = (255, 255, 255)
gray = (169, 169, 169)
light_gray = (211, 211, 211)
beige = (207, 185, 151)
light_orange = (255, 213, 128)
orange = (255, 165, 0)
light_red = (255, 204, 203)
red = (255, 0, 0)
light_yellow = (255, 255, 191)
# 2, 4, 8, 16, 32, 64, 128
tile_colors = [gray, light_gray, beige, light_orange,
               orange, light_red, red, light_yellow]

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
        return str(np.array([ [ 0 if i == 0 else 2 ** i for i in row ] for row in self.board ]))
        
    # Shift this 2048 board in place
    def shift(self, dir: Dir):
        self.board = shift(self.board, dir)

    def at(self, i, j):
        return self.board[i][j]

    def draw(self, screen, width, height):
        font_size = height // self.side // 5
        font = pygame.font.Font(None, font_size)
        tile_size = height // self.side
        for i in range(self.side):
            for j in range(self.side):
                tile_exponent = self.at(i, j)
                tileX = i / self.side * width
                tileY = j / self.side * height
                tile_color = tile_colors[tile_exponent]
                tile = pygame.draw.rect(screen, tile_color, (tileX - tile_size / 2,
                                                             tileX + tile_size / 2, tileY - tile_size / 2, tileY + tile_size / 2))

                tile_number = 2 ** tile_exponent
                # if no number, then text is ""
                tile_text = font.render(str(tile_number), True,
                                        white) if tile_number != 1 else ""
                tile_rect = tile_text.get_rect(centerx=tileX, y=tileY)
                screen.blit(tile_text, tile_rect)
        pygame.display.flip()
        

    def test_gui(self):
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j] = 1
