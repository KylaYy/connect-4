import pygame

class Position:
    def __init__(self, coord, radius):
        """
        We initialize the variables for this object

        coord: a tuple (x, y) which is the center of this position, coord[0], coord[1]
        radius: the radius of this Position
        """

        self.coord = coord
        self.radius = radius
        self.drawn = False

        self.colour = None

    def draw(self, screen, colour):
        """
        This will display the circle on the screen.

        screen: a pygame display that you can place shapes and other objects for display
        """

        # TODO we need to set the colour of the position
        self.colour = colour

        pygame.draw.circle(screen, self.colour, self.coord, self.radius)
        self.drawn = True

    def is_hovering(self, coord):
        """
        This function will check if the user clicks on this Positions.

        coord: a tuple (x, y). This is the position that the user has clicked
        Return True if this Position is being clicked, else return False
        """
        if (self.coord[0]-self.radius < coord[0] < self.coord[0] + self.radius and 
            self.coord[1]-self.radius < coord[1] < self.coord[1] + self.radius):
            print("CLICKED A SQUARE " + str(self.coord[0]), str(self.coord[1]))
            return True

        return False

    def is_drawn(self):
        return self.drawn
