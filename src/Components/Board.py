import pygame
from Components.Position import Position

# TODO: Define constants for PLAYER_1 id's and PLAYER_2 id's
# TODO: Define colours that we will use for our pieces in the game

PLAYER_1 = 1
PLAYER_2 = 2

class Board:
    def __init__(self, dims):
        """
        Initialize the Board object. The Board object will hold all positions on the board
        
        dims: a tuple (width, height) which is the dimensions of the board.
        """

        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)
        RADIUS = 35

        self.turn = PLAYER_1
        self.player_colour = {PLAYER_1: RED, PLAYER_2: YELLOW}
        
        self.dims = dims
        self.positions = []
        self.coords = {}

        self.x = 90 
        self.y = dims[1] // 6

        # TODO: Create a map of coordinates to position. We need this for is_clickable

        for w in range(0, self.dims[0], self.x):
            for h in range(0, self.dims[1], self.y):
                coord = (w + 50, h + self.y/2)
                pos = Position(coord, RADIUS)
                self.positions.append(pos)
                self.coords[coord] = pos

    def change_turn(self):
        if self.turn == PLAYER_1:
            self.turn = PLAYER_2
        else:
            self.turn = PLAYER_1

    def draw_position(self, screen, position):
        position.draw(screen, self.player_colour[self.turn])
        self.change_turn()

    def is_clickable(self, position):
        """
        Determine if a given position on the board is clickable.
        """
        if position.is_drawn():
            return False

        def get_coord_below(coord):
            next_coord = (coord[0], coord[1] + self.y)
            return next_coord

        next_coord = get_coord_below(position.coord)
        
        return next_coord not in self.coords or self.coords[next_coord].is_drawn()
    
    def four_in_a_row(self, position):
        """
        Given a position, determine if this poition is part of a connect 4 
        in any direction.
        """

        def get_vertical_position(pos, below=False):
            next_pos = (pos[0], pos[1] + (self.y if below else -self.y))
            return next_pos
    
        def get_horizontal_position(pos, right=False):
            next_pos = (pos[0] + (self.x if right else -self.x), pos[1])
            return next_pos

        def get_diagonal_position(pos, below=False, right=False):
            next_pos = (pos[0] + (self.x if right else -self.x), pos[1] + (self.y if below else -self.y))
            return next_pos

        vertical_count = horizontal_count = 1
        diag1_count = diag2_count = 1
        
        # Check upwards
        next_pos = get_vertical_position(position.coord, below=False)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            vertical_count += 1
            next_pos = get_vertical_position(next_pos, below=False)
        
        # Check below
        next_pos = get_vertical_position(position.coord, below=True)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            vertical_count += 1
            next_pos = get_vertical_position(next_pos, below=True)

        # Check right
        next_pos = get_horizontal_position(position.coord, right=True)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            horizontal_count += 1
            next_pos = get_horizontal_position(next_pos, right=True)
        
        # Check left
        next_pos = get_horizontal_position(position.coord, right=False)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            horizontal_count += 1
            next_pos = get_horizontal_position(next_pos, right=False)

        # Check up-right
        next_pos = get_diagonal_position(position.coord, below=False, right=True)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            diag1_count += 1
            next_pos = get_diagonal_position(next_pos, below=False, right=True)
        
        # Check bot-left
        next_pos = get_diagonal_position(position.coord, below=True, right=False)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            diag1_count += 1
            next_pos = get_diagonal_position(next_pos, below=True, right=False)

        # Check up-left
        next_pos = get_diagonal_position(position.coord, below=False, right=False)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            diag2_count += 1
            next_pos = get_diagonal_position(next_pos, below=False, right=False)
        
        # Check bot-right
        next_pos = get_diagonal_position(position.coord, below=True, right=True)
        while next_pos in self.coords and self.coords[next_pos].colour == position.colour:
            diag2_count += 1
            next_pos = get_diagonal_position(next_pos, below=True, right=True)
        
        print(horizontal_count)
        print(vertical_count)
        print(diag1_count)
        print(diag2_count)
        return horizontal_count >= 4 or vertical_count >= 4 or diag1_count >= 4 or diag2_count >= 4