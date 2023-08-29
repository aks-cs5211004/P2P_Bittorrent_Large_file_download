import threading
import time
from socket import *

#vayu server
servername='vayu.iitd.ac.in'
serverport=9801
server_line_recv_port=2500
server_socket = socket(AF_INET, SOCK_STREAM)


#Me acting as server
#   SWAP HERE
me_as_server_port=9801
sendline_recv_send_line_port=9800
me_as_server_socket= socket(AF_INET, SOCK_STREAM)


#Me receiving from peers DISTINCT PEER NAMES
peernames=["10.184.16.183"]
#Here write the me_as_server_ports of your peers (ALL 9801)
peer_s_server_ports=[9801]
#first port is to receive from server, then others from peers
line_recv_port=[2501]
peer_sockets_recv = []
for i in range (len(peernames)):
    peer_sockets_recv.append(socket(AF_INET, SOCK_STREAM))


#Data Structures
most_recent = ("0","")
arr=set([])


#Functions

#SERVER FUNCTIONS
def server_connect():
    server_socket.connect((servername, serverport))
def server_recv():
    while (len(arr) < 1000):
        sentence = "SENDLINE\n"
        server_socket.send(sentence.encode())
        st=server_socket.recv(server_line_recv_port).decode()
        index=0
        for j in range(len(st)):
            if(str[j]=="\n"):
                index=j
                break
        most_recent=(int(str[0:index]),str[index:])
        print("Received from server= ", most_recent[0])
        arr.add(most_recent)
        
        
#ME AS SERVER FUNCTIONS
def make_me_server():
        me_as_server_socket.bind(('', me_as_server_port))
        me_as_server_socket.listen(10000)
def peer_send():
    while (True):    
        connectionSocket,addr=me_as_server_socket.accept()
        sentence = connectionSocket.recv(sendline_recv_send_line_port).decode()
        if (sentence == "SENDLINE\n"): 
            st=str(most_recent[0])+most_recent[1]
            connectionSocket.send(st.encode())
        connectionSocket.close()
        
        

#RECEIVING FROM MY PEERS FUNCTIONS
def peers_connect_to_recv():
   for i in range (len(peernames)):
       peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
       print("connection succesful")   
def peer_recv(i):
    while (len(arr) < 1000):
        sentence = "SENDLINE\n"
        peer_sockets_recv[i].send(sentence.encode())
        st=peer_sockets_recv[i].recv(line_recv_port[i]).decode()
        index=0
        for j in range(len(st)):
            if(str[j]=="\n"):
                index=j
                break
        most_recent=(int(str[0:index]),str[index:])
        print("Received from server= ", most_recent[0])
        arr.add(most_recent)
        

def main():
    ts=time.time()
    
    #Make Initial connections????????
    server_connect()
    make_me_server()
    time.sleep(5)
    peers_connect_to_recv()
    print("HERE")
    
    #Make threads
    server_thread= threading.Thread(target=server_recv)
    peer_rec_thread = []
    for i in range (len(peernames)):
        peer_rec_thread.append(threading.Thread(target=peer_recv,args=(i,)))   


    send_thread = threading.Thread(target=peer_send)
    
    #Start all threads    
    server_thread.start()
    send_thread.start()
    for i in range (len(peernames)):
        peer_rec_thread[i].start()

    #Join all threads
    server_thread.join()
    send_thread.join()
    for i in range (len(peernames)):
        peer_rec_thread[i].join()

        
    #Close all connections
    server_socket.close()
    for i in range (len(peernames)):
        peer_sockets_recv[i].close()
    me_as_server_socket.close()
    
    
    te=time.time()
    print(len(arr))
    print(te-ts)
    
main()
