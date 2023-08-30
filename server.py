import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1234))
s.listen(10000)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    while True:
        msg = clientsocket.recv(2048).decode()
        if msg == "SEND":
            print("yes")
            str = "Hello!"
            clientsocket.send(str.encode())