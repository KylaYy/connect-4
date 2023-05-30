import pygame
from Components.Board import Board
import time
from client import Client
import threading

class App:
    def __init__(self):

        pygame.init()

        self.background_img = pygame.image.load('../img/Connect4Board.png') # importing an image
        self.screen_width = self.background_img.get_width()
        self.screen_height = self.background_img.get_height()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.board = Board((self.screen_width, self.screen_height)) 

        self.finished = False   # A flag that is used to check when the game is complete
        self.our_turn = True    # A flag to indicate if it is our turn or not

        pygame.display.set_caption("Connect 4 Window")

        print(self.screen_width, self.screen_height)


    def run(self):
        client = Client()

        def recieve():
            """
            This function is called when we want to receive data from the client.

            We will start a thread that will continuously check for data.
            """
            receiving_thread = threading.Thread(target=receiving_coords)
            receiving_thread.start()

            self.our_turn = False

        def update_display(coords, client=None):
            self.screen.blit(self.background_img, (0, 0)) # set the image to be the background

            for pos in self.board.positions:
                if not pos.drawn and coords and pos.is_hovering(coords) and self.board.is_clickable(pos):
                    self.board.draw_position(self.screen, pos)

                    if self.board.four_in_a_row(pos):
                        print(f"{pos.colour} wins!")
                        self.finished = True
                    
                    if client != None:
                        client.send(coords)

                        recieve() # It is no longer our turn, we will want to receive data from the client

            pygame.display.update()

        def receiving_coords():
            received_coords = client.recieve()

            while received_coords == None:
                received_coords = client.recieve()
            
            update_display(received_coords)
            self.our_turn = True

        # If we are client_id 1 then we must wait first
        if client.client_id == 1:
            recieve() # It's not our turn. We will want to receive data from our client

        running = True
        while running:
            coords = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.our_turn:
                    coords = pygame.mouse.get_pos()

                    update_display(coords, client)
            
            update_display(coords)
            
            if self.finished:
                time.sleep(2)
                self.reset()

    def exit(self):
        pygame.quit()

    def reset(self):
        self.finished = False
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.board = Board((self.screen_width, self.screen_height)) 
        self.screen.blit(self.background_img, (0, 0)) # set the image to be the background
        pygame.display.update()
    