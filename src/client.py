import socket
import pickle

class Client:
    def __init__(self):
        # get local machine name
        host = socket.gethostname()

        # set port number
        port = 9999

        # create a socket object
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connection to hostname on the port
        self.clientsocket.connect((host, port))

        # prompt the user for their name
        name = input("Enter your name: ")
        self.clientsocket.send(name.encode())
        
        client_id = self.clientsocket.recv(1028)
        self.client_id = int(client_id.decode())
    
    def send(self, coords):
        """
        This function will send a coordinate tuple to the server
        
        coords: the coordinates tuple that we will send to ther server
        """
        serialized_coords = pickle.dumps(coords)
        self.clientsocket.sendall(serialized_coords)

    def recieve(self):
        """
        This is a function that receives a response from the server and returns a coordinate tuple.

        Return None if our socket does not receive anything within 1 second.
        """
        self.clientsocket.settimeout(1)  # Set a timeout value (in seconds)

        try:
            serialized_coords = self.clientsocket.recv(1028)
            if serialized_coords:
                return pickle.loads(serialized_coords)
        except socket.timeout:
            pass

        return None  # Return None if no data is received within the timeout period