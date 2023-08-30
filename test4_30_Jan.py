import threading
import time
from socket import *

#vayu server
servername='vayu.iitd.ac.in'
serverport=9801
server_socket = socket(AF_INET, SOCK_STREAM)

#locks
lock=threading.Lock()

#Me acting as server
#   SWAP HERE
me_as_server_port=5000
me_as_server_socket= socket(AF_INET, SOCK_STREAM)


#Me receiving from peers DISTINCT PEER NAMES
peernames=["10.194."]
#Here write the me_as_server_ports of your peers (ALL 9801)
peer_s_server_ports=[5000]
#first port is to receive from server, then others from peers
peer_sockets_recv = []
for i in range (len(peernames)):
    peer_sockets_recv.append(socket(AF_INET, SOCK_STREAM))


#Data Structures
most_recent = ("Heloo")
arr=set([])


#Functions

#SERVER FUNCTIONS
def server_connect():
    server_socket.connect((servername, serverport))
    
def server_recv():
    while (len(arr) < 1001):
        lock.acquire()

        sentence = "SENDLINE\n"
        server_socket.send(sentence.encode())
        st=server_socket.recv(3000).decode()
        index=0
        for j in range(len(st)):
            if(not st[j].isdigit()):
                index=j
                break
        
        if (index!=0):

            global most_recent
            most_recent=st
            # most_recent=(st[0:index],st[index:])
            # # print("Received from server",most_recent[0])
            # # print("size of array tilll now: ", len(arr))
            arr.add(most_recent)
        lock.release()
        
        
#ME AS SERVER FUNCTIONS
def make_me_server():
        me_as_server_socket.bind(('', me_as_server_port))
        me_as_server_socket.listen(10000)
        print("SERVER DEPLOYED")
  
        
def handle_clients(conn,addr):
    print("New Connection Established from: ",addr)
    connected=True
    while(connected):
        msg=conn.recv(3000).decode()
        if msg=="DISCONNECT\n":
            connected=False 
        conn.send(most_recent.encode())
    conn.close()
              
def peer_send():
    while (True):
        connectionSocket,addr=me_as_server_socket.accept()
        thread_for_clients=threading.Thread(target=handle_clients,args=(connectionSocket,addr))
        thread_for_clients.start()
        thread_for_clients.join()

# def peer_send():
#     while (True):
#         connectionSocket,addr=me_as_server_socket.accept()
#         while True:
#             lock.acquire()
#             sentence = connectionSocket.recv(3000).decode()
#             if (sentence == "SENDLINE\n"): 
#                 connectionSocket.send(most_recent.encode())
#                 # connectionSocket.close()    
        
        
        

#RECEIVING FROM MY PEERS FUNCTIONS
def peers_connect_to_recv():
   for i in range (len(peernames)):
       peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
       print("connection succesful")
       
def peer_recv(i):
    while (len(arr) < 1002):
        sentence = "SENDLINE\n"
        peer_sockets_recv[i].send(sentence.encode())
        st=peer_sockets_recv[i].recv(3000).decode()

        index=0
        for j in range(len(st)):
            if(not st[j].isdigit()):
                index=j
                break
        
        if (index!=0):

            global most_recent
            most_recent=st
            # most_recent=(st[0:index],st[index:])
            print("Received from peer")
            # # print("size of array tilll now: ", len(arr))
            arr.add(most_recent)
    else:
        sentence="DISCONNECT/n"
        peer_sockets_recv[i].send(sentence.encode())
        
        

def main():
    ts=time.time()

    #Make Initial connections
    server_connect()
    make_me_server()
    print("SERVER DEPLOYED")
    time.sleep(5)
    peers_connect_to_recv()
    
    #Make threads
    server_thread= threading.Thread(target=server_recv)
    peer_rec_thread = []
    for i in range (len(peernames)):
        peer_rec_thread.append(threading.Thread(target=peer_recv,args=(i,)))   
    send_thread = threading.Thread(target=peer_send)
    
    # Start all threads    
    server_thread.start()
    send_thread.start()
    for i in range (len(peernames)):
        peer_rec_thread[i].start()

    # #Join all threads
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
    arrs=sorted(arr)
    # arrs.remove({"Heloo"})
    print(len(arrs))
    max_size=0;
    for i in arrs:
        print("....................................................................................")
        print(i)
    print()
    print(max_size)
    print(te-ts)
    
main()
