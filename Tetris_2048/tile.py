import random
import numpy as np
from tile_color import tile_colors
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it


# Class used for modeling numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.003
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # Constructor that creates a random tile with a number 2 or 4
    # ---------------------------------------------------------------------------
    def __init__(self):
        self.foreground_color = None
        self.background_color = None
        random_numbers = [2, 4]
        # set the number on the tile
        self.number = random_numbers[random.randint(0, len(random_numbers) - 1)]
        # set the boundary color of the tile
        self.box_color = Color(132, 122, 113)  # box (boundary) color
        self.update_color()

    # Method for updating the color of the tile based on the number on it
    # Using the tile_colors dictionary from tile_color.py
    def update_color(self):
        self.background_color = tile_colors[self.number]['background_color']
        self.foreground_color = tile_colors[self.number]['foreground_color']

    # Method for updating the number and calling update_color function to update color of the tile
    def update_color_and_score(self, tile):
        self.number *= 2
        tile.number = None
        self.update_color()
        return self.number

    # Method for handling chain merge of tiles in a matrix
    # Method find upper tile and if it is the same as current tile, call the update_color_and_score method
    # and update the score. After that, set the upper tile to None and move all tiles above it one row down
    @staticmethod
    def merge_tiles(tile_matrix, score):
        for row, col in np.ndindex(tile_matrix.shape):
            current_tile = tile_matrix[row, col]
            if current_tile is not None:
                if row < tile_matrix.shape[0] - 1 and tile_matrix[row + 1, col] is not None:
                    adjacent_tile = tile_matrix[row + 1, col]
                    if current_tile.number == adjacent_tile.number:
                        score += current_tile.update_color_and_score(adjacent_tile)
                        tile_matrix[row + 1, col] = None
                        for r in range(row + 1, tile_matrix.shape[0]):
                            if tile_matrix[r, col] is not None:
                                tile_matrix[r - 1, col] = tile_matrix[r, col]
                                tile_matrix[r, col] = None
        return score

    # Method for drawing the tile
    def draw(self, position, length=1):
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        # draw the bounding box around the tile as a square
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))
