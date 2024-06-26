import sys
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from tile import Tile
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w, info_w, game_speed):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.info_width = info_w
        self.game_speed = game_speed
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid and the next tetromino to be moved
        self.current_tetromino = None
        self.next_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(84, 73, 78)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(50, 50, 50)
        self.boundary_color = Color(0, 0, 0)
        # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.005
        self.box_thickness = 1.5 * self.line_thickness
        # set the score to 0 at the beginning of the game
        self.score = 0
        self.max_score = None

    # Method used for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color

        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid

        self.draw_boundaries()
        self.draw_info_panel()

        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(self.game_speed)

    # Method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.54, self.grid_width - 0.54
        start_y, end_y = -0.47, self.grid_height - 0.47
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        # set pen radius for info box boundaries
        stddraw.rectangle(self.grid_width - 0.5, pos_y, self.info_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the information panel on the right side of the game grid (score, next tetromino, instructions, user interface key mapping,etc.)
    def draw_info_panel(self):
        stddraw.setPenColor(Color(84, 73, 78))
        stddraw.filledRectangle(self.grid_width - 0.5, -0.5, self.info_width, self.grid_height + 0.5)
        info_center_x_scale = self.grid_width + self.info_width / 2 - 0.5
        info_score_y_scale = self.grid_height - 1
        next_tetromino_y_scale = self.grid_height - 4

        # Draw the score
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.boldText(info_center_x_scale, info_score_y_scale, "Your Score: " + str(self.score))
        stddraw.boldText(info_center_x_scale, next_tetromino_y_scale, "Next Tetromino: ")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 1.5, "Best Score: " + str(self.max_score))


        block_size = 1
        block_spacing = 0.07

        tetromino_base_x = info_center_x_scale - 0.5
        tetromino_base_y = self.grid_height - 6
        stddraw.setPenColor(Color(238, 228, 218))

        if self.next_tetromino.type == 'I':
            for i in range(4):
                stddraw.filledRectangle(tetromino_base_x, tetromino_base_y - i * (block_size + block_spacing),
                                        block_size, block_size)
        elif self.next_tetromino.type == 'O':
            offsets = [(0, 0), (0, -1), (1, 0), (1, -1)]
            for dx, dy in offsets:
                stddraw.filledRectangle(tetromino_base_x + dx * (block_size + block_spacing),
                                        tetromino_base_y + dy * (block_size + block_spacing), block_size, block_size)
        elif self.next_tetromino.type == 'S':
            offsets = [(0, 0), (1, 0), (-1, -1), (0, -1)]
            for dx, dy in offsets:
                stddraw.filledRectangle(tetromino_base_x + dx * (block_size + block_spacing),
                                        tetromino_base_y + dy * (block_size + block_spacing), block_size, block_size)
        elif self.next_tetromino.type == 'Z':
            offsets = [(0, 0), (-1, 0), (0, -1), (1, -1)]
            for dx, dy in offsets:
                stddraw.filledRectangle(tetromino_base_x + dx * (block_size + block_spacing),
                                        tetromino_base_y + dy * (block_size + block_spacing), block_size, block_size)
        elif self.next_tetromino.type == 'L':
            for i in range(3):
                stddraw.filledRectangle(tetromino_base_x, tetromino_base_y - i * (block_size + block_spacing),
                                        block_size, block_size)
            stddraw.filledRectangle(tetromino_base_x + block_size + block_spacing,
                                    tetromino_base_y - 2 * (block_size + block_spacing), block_size, block_size)
        elif self.next_tetromino.type == 'J':
            for i in range(3):
                stddraw.filledRectangle(tetromino_base_x, tetromino_base_y - i * (block_size + block_spacing),
                                        block_size, block_size)
            stddraw.filledRectangle(tetromino_base_x - (block_size + block_spacing),
                                    tetromino_base_y - 2 * (block_size + block_spacing), block_size, block_size)
        elif self.next_tetromino.type == 'T':
            for dx in [-1, 0, 1]:
                stddraw.filledRectangle(tetromino_base_x + dx * (block_size + block_spacing),
                                        tetromino_base_y - (block_size + block_spacing), block_size, block_size)
            stddraw.filledRectangle(tetromino_base_x, tetromino_base_y, block_size, block_size)

        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 11.5, "A-D = Rotate")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 12.5, "Left-Right = Move")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 13.5, "Space = Hard Drop")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 14.5, "Down = Soft Drop")
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 9, "R = Main Menu")
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 10, "ESC = Stop Menu")
        # Exit game button positioning
        button_height = 1
        button_width = self.info_width - 2
        button_top = 0.5  # Distance from bottom of the info panel
        button_center_y = button_top + button_height / 2

        stddraw.setPenColor(Color(90, 90, 90))
        stddraw.filledRectangle(self.grid_width + 0.5, button_top, button_width, button_height)
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.boldText(info_center_x_scale, button_center_y, "Exit Game")

        # Handle button click
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if (self.grid_width + 0.5 <= mouse_x <= self.grid_width + button_width + 0.5 and
                    button_top <= mouse_y <= button_top + button_height):
                sys.exit()  # Exit the program if the button is clicked

        # Method used for checking whether the grid cell with given row and column
        # indexes is occupied by a tile or empty

    # Method used for checking whether the grid cell with given row and column indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    # The method also removes the full rows and shifts the tiles down.
    # The method also merges the tiles with the same number and updates the score.
    # The method also removes the flying tiles that are not connected to the ground.
    # The method also checks if the score is greater than or equal to 2048 to end the game.
    # Method will first merge, then remove flying tiles, then remove full rows and shift
    # This order is given by the instructor
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None

        # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos_x = blc_position.x + col
                    pos_y = blc_position.y + (n_rows - 1) - row
                    # check if the position is inside the game grid
                    if self.is_inside(pos_y, pos_x):
                        self.tile_matrix[pos_y][pos_x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid

                    else:
                        self.game_over = True
                        return self.game_over
        previous_score = -1
        while previous_score != self.score:
            previous_score = self.score
            self.score = Tile.merge_tiles(self.tile_matrix, self.score)
        self.display()
        self.remove_flying_tiles()
        self.remove_full_rows_and_shift()

        # After locking the tiles, remove the full rows and update the grid
        # The game is over if the score is greater than or equal to 2048
        if self.score >= 2048:
            self.game_over = True
        return self.game_over

    # Method used for removing the full rows and shifting the tiles down
    # The method also updates the score by adding the numbers on the removed tiles
    def remove_full_rows_and_shift(self):
        for row in range(self.grid_height):
            if None not in self.tile_matrix[row]:
                self.score += sum(tile.number for tile in self.tile_matrix[row] if tile is not None)
                for shift_row in range(row, self.grid_height - 1):
                    self.tile_matrix[shift_row] = self.tile_matrix[shift_row + 1]
                self.tile_matrix[self.grid_height - 1] = [None] * self.grid_width
                self.display()

    # Method used for removing the flying tiles that are not connected to the ground
    # The method also updates the score by adding the numbers on the removed tiles
    # The method uses Depth First Search (DFS) algorithm to find the connected tiles
    # Method first checks the top row, then iterates over the rest of the rows
    # Method will first mark every tile as a false
    def remove_flying_tiles(self):
        visited = [[False] * self.grid_width for _ in range(self.grid_height)]

        for col in range(self.grid_width):
            if self.tile_matrix[0][col] is not None and not visited[0][col]:
                self.dfs(0, col, visited)

        for row in range(1, self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None and not visited[row][col]:
                    self.score += self.tile_matrix[row][col].number
                    self.tile_matrix[row][col] = None
                    self.display()

    # Method used for Depth First Search (DFS) algorithm to find the connected tiles
    # The method marks the visited tiles as True and recursively calls the DFS method
    # for the neighboring tiles
    # The method uses the visited matrix to keep track of the visited tiles
    def dfs(self, row, col, visited):
        if row < 0 or row >= self.grid_height or col < 0 or col >= self.grid_width:
            return

        if visited[row][col] or self.tile_matrix[row][col] is None:
            return

        visited[row][col] = True

        self.dfs(row - 1, col, visited)
        self.dfs(row + 1, col, visited)
        self.dfs(row, col - 1, visited)
        self.dfs(row, col + 1, visited)
