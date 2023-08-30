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
me_as_server_port=9801
me_as_server_socket= socket(AF_INET, SOCK_STREAM)


#Me receiving from peers DISTINCT PEER NAMES
peernames=["172.30.144.1"]
#Here write the me_as_server_ports of your peers (ALL 9801)
peer_s_server_ports=[4000]
#first port is to receive from server, then others from peers
peer_sockets_recv = []
for i in range (len(peernames)):
    peer_sockets_recv.append(socket(AF_INET, SOCK_STREAM))


#Data Structures
most_recent = "Heloo"
arr=set([])


#Functions

#SERVER FUNCTIONS
def server_connect():
    server_socket.connect((servername, serverport))
    
def server_recv():
    byte_length=0
    while (len(arr) < 1001):
        sentence = "SENDLINE\n"
        server_socket.send(sentence.encode())

        st=server_socket.recv(3000).decode()
    
        for j in range(len(st)):
            if(not st[j].isdigit()):
                index=j
                break
        
        if (index!=0):

        # global most_recent
            most_recent=st
            # most_recent=(st[0:index],st[index:])
            # # print("Received from server",most_recent[0])
            # # print("size of array tilll now: ", len(arr))
            lock.acquire()
            arr.add(most_recent)
            lock.release()

        
        
#ME AS SERVER FUNCTIONS
def make_me_server():
        me_as_server_socket.bind(('', me_as_server_port))
        me_as_server_socket.listen(1000)
        
def peer_send():
    while (True):
        connectionSocket,addr=me_as_server_socket.accept()
        while True:
 
            sentence = connectionSocket.recv(1024).decode()
            # lock.acquire()
            if (sentence == "SENDLINE\n"): 
                connectionSocket.send(most_recent.encode())
                # connectionSocket.close()    
            # lock.release()
        
        

#RECEIVING FROM MY PEERS FUNCTIONS
def peers_connect_to_recv():
   for i in range (len(peernames)):
       peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
       print("connection succesful")
       
def peer_recv(i):
    while (len(arr) < 1001):
        sentence = "SENDLINE\n"
        peer_sockets_recv[i].send(sentence.encode())

        st=peer_sockets_recv[i].recv(1024).decode()
        # for j in range(len(st)):
        #     if(not st[j].isdigit()):
        #         index=j
        #         break
        
        # if (st[0]!="-"):
        global most_recent
        most_recent=st
            # most_recent=(st[0:index],st[index:])
        print("Received from peer")
            # # print("size of array tilll now: ", len(arr))
        # lock.acquire()
        arr.add(most_recent)
        # lock.acquire()


def main():
    ts=time.time()

    #Make Initial connections
    server_connect()
    # make_me_server()
    # print("HERE")
    # time.sleep(5)
    # peers_connect_to_recv()
    # print("HERE")
    
    #Make threads
    server_thread= threading.Thread(target=server_recv)
    # peer_rec_thread = []
    # for i in range (len(peernames)):
    #     peer_rec_thread.append(threading.Thread(target=peer_recv,args=(i,)))   


    send_thread = threading.Thread(target=peer_send)
    
    # server_recv()
    # Start all threads    
    server_thread.start()
    # send_thread.start()
    # for i in range (len(peernames)):
    #     peer_rec_thread[i].start()

    # #Join all threads
    server_thread.join()
    # send_thread.join()
    # for i in range (len(peernames)):
    #     peer_rec_thread[i].join()

        
    #Close all connections
    server_socket.close()
    # for i in range (len(peernames)):
    #     peer_sockets_recv[i].close()
    # me_as_server_socket.close()
    
    
    te=time.time()
    # print(len(arr))
    arrs=sorted(arr)
    # arrs.remove({"Heloo"})
    print(len(arrs))
    max_size=0;
    for i in arrs:
        print("....................................................................................")
        if(len(i.encode())>max_size):
            max_size=len(i.encode())
            break
        print(i)
    print()
    print(max_size)
    print(te-ts)
    
main()