import socket
import threading
import pickle

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set port number
port = 9999

# bind the socket to a public host, and a port
serversocket.bind((host, port))

# become a server socket
serversocket.listen(2)

# list to hold client sockets
clients = []
client_names = []

def send(socket, coords):
    """
    socket: the connection to the client we want to send data to
    coords: a tuple for a position on the board. We will send this to the other client
    """
    serialized_coords = pickle.dumps(coords)
    socket.sendall(serialized_coords)

def receive(socket):
    """
    socket: the connection to the client we will receive data from
    returns the tuple of coordinates
    """
    serialized_coords = socket.recv(4096)
    return pickle.loads(serialized_coords)

def handle_client(clientsocket, client_name, client_id):
    # Send the client id to the client
    clientsocket.send(str(client_id).encode())

    while True:
        try:
            coords = receive(clientsocket)

            # find the index of the current client
            current_index = clients.index(clientsocket)

            if len(clients) > 1:
                # find the index of the other client
                other_index = (current_index + 1) % 2

                # send the message to the other client
                socket = clients[other_index]
                send(socket, coords)
            else:
                clientsocket.send("Waiting for client 2.".encode())

        except:
            # if there's an error, remove the client from the list
            clients.remove(clientsocket)
            client_names.remove(client_name)
            break

    # close the client socket
    clientsocket.close()

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    # Client will send name after connecting
    client_name = clientsocket.recv(1024).decode()

    print("Got a connection from %s" % str(addr))
    print(client_name + " has joined the game.")

    # add the client to the list
    clients.append(clientsocket)
    client_names.append(client_name)
    client_id = clients.index(clientsocket)

    # create a new thread to handle the connection
    client_thread = threading.Thread(target=handle_client, args=(clientsocket, client_name, client_id))
    client_thread.start()