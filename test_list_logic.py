import threading
import time
from socket import *

#vayu server
servername='vayu.iitd.ac.in'
serverport=9801
server_socket = socket(AF_INET, SOCK_STREAM)

#locks
lock = threading.Lock()

#Me acting as server
#   SWAP HERE
me_as_server_port= 7000
me_as_server_socket= socket(AF_INET, SOCK_STREAM)


#Me receiving from peers DISTINCT PEER NAMES
# "10.194.5.123", 
peernames=["10.194.44.115"]
#Here write the me_as_server_ports of your peers (ALL 9801)
peer_s_server_ports=[8000]
#first port is to receive from server, then others from peers
peer_sockets_recv = []
for i in range (len(peernames)):
    peer_sockets_recv.append(socket(AF_INET, SOCK_STREAM))


#Data Structures
most_recent = "Hello"
lst = [""]*1000
lines = 0


#Functions

#SERVER FUNCTIONS
def server_connect():
    server_socket.connect((servername, serverport))
    
def server_recv():
    global lines
    while (lines < 1000):
        sentence = "SENDLINE\n"
        server_socket.send(sentence.encode())
        st=server_socket.recv(4096).decode()

        i=0
        tmp = st.split("\n")
        while (i < len(tmp)):
            if (tmp[i].isnumeric()):
                s = tmp[i]+"\n"+tmp[i+1]+"\n"
                if (tmp[i+1]!=tmp[-1]):
                    global most_recent
                    most_recent = s
                    lock.acquire()
                    if (lst[int(tmp[i])] == ""):
                        lines+=1
                    lst[int(tmp[i])] = s
                    lock.release()
            i+=2

        print("SERVER: ", lines)
    print("SERVER: 1000 lines recieved")
    server_socket.close()
        
        
#ME AS SERVER FUNCTIONS
def make_me_server():
        me_as_server_socket.bind(('', me_as_server_port))
        me_as_server_socket.listen(10000)
        print("server deployed")
        
def handle_clients(conn,addr):
    print("New Connection Established from: ",addr)
    while(True):
        msg=conn.recv(4096).decode()
        # print(msg)
        if msg=="DISCONNECT\n":
            break
        elif (msg.isnumeric()):
            lock.acquire()
            conn.send(lst[int(msg)].encode())
            lock.release()
        else:
            lock.acquire()
            global most_recent
            conn.send(most_recent.encode())
            # print("Sent line to peer")
            lock.release()
        
    conn.close()
    print("connection closed")
              
def peer_send():
    for i in range (len(peernames)):
        connectionSocket,addr=me_as_server_socket.accept()
        thread_for_clients=threading.Thread(target=handle_clients,args=(connectionSocket,addr))
        thread_for_clients.start()
        thread_for_clients.join()
    me_as_server_socket.close()
    print("me server closed")


#RECEIVING FROM MY PEERS FUNCTIONS
def peers_connect_to_recv():
    print("Trying to connect ...")
    for i in range (len(peernames)):
       peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
       print("connection succesful")
       
def peer_recv(i):
    global lines
    while (lines < 1000):
        sentence = ""
        if (lines > 900):
            index = lst.index("")
            sentence = str(index)
        else:
            sentence = "SENDLINE\n"
            
        peer_sockets_recv[i].send(sentence.encode())
        st=peer_sockets_recv[i].recv(4096).decode()
        print("PEER: ",i , lines)
    else:
        sentence="DISCONNECT\n"
        peer_sockets_recv[i].send(sentence.encode())
        
    print("PEER: 1000 lines recieved")
    peer_sockets_recv[i].close()
        
        

def main():

    #Make Initial connections
    server_connect()
    # make_me_server()
    # time.sleep(5)
    # peers_connect_to_recv()
    
    ts=time.time()
    
    #Make threads
    server_thread= threading.Thread(target=server_recv)
    # peer_rec_thread = []
    # for i in range (len(peernames)):
    #     peer_rec_thread.append(threading.Thread(target=peer_recv,args=(i,)))   
    # send_thread = threading.Thread(target=peer_send)
    
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
    
    f = open("test.txt", 'w')
    te=time.time()
    arr=sorted(lst)
    for i in arr:
        f.write(i)
        print(i)
        
        
    print()
    print(len(arr))
    print(te-ts)
    f.close()
    
main()
