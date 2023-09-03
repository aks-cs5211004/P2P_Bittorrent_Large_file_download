import random
import select
import threading
import time
from socket import *

# Vayu server
servername='10.17.51.115'
serverport=9801
server_socket = socket(AF_INET, SOCK_STREAM)

# Locks
lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()
# Me acting as server
# SWAP HERE
me_as_server_port=9011
me_as_server_socket= socket(AF_INET, SOCK_STREAM)


# Me receiving from peers DISTINCT PEER NAMES

peernames=["10.184.60.82"]
# Here write the me_as_server_ports of your peers (ALL 9801)
peer_s_server_ports=[9011,9011]
# First port is to receive from server, then others from peers
peer_sockets_recv = []
for i in range (len(peernames)):
    peer_sockets_recv.append(socket(AF_INET, SOCK_STREAM))


#Data Structures
most_recent = "Hello"
lst = [""]*1000
unique = [i  for i in range(1000)]
lines = 0


#Functions

#SERVER FUNCTIONS
def server_connect():
    while(True):
        try:
            server_socket.connect((servername, serverport))
            break
        except Exception:
            continue
    
def server_recv():
    global lines,lst,unique
    while (lines < 1000):
        sentence = "SENDLINE\n"
        server_socket.send(sentence.encode())
        
        lock1.acquire()
        st=server_socket.recv(4096).decode()
        tmp = st.split("\n")
        if (len(tmp) > 2):
            if (tmp[0].isnumeric() and lst[int(tmp[0])]==""):
                s = tmp[0]+"\n"+tmp[1]+"\n"
                unique.remove(int(tmp[0]))
                lst[int(tmp[0])] = s
                lines+=1
                global most_recent
                most_recent = s

        print("SERVER: ", lines)
        lock1.release()

    server_socket.close()
    print("Server Sokcet Closed")

        
#ME AS SERVER FUNCTIONS
def deploy_server():
    me_as_server_socket.bind(('', me_as_server_port))
    me_as_server_socket.listen(10000)
    print("Server Deployed")
        
def handle_peers(conn,addr):
    global most_recent,lst
    print("New connection established from: ",addr)
    while(True):
        lock2.acquire()
        msg=conn.recv(4096).decode()
        if (msg=="DISCONNECT\n"):
            break
        elif (msg.isnumeric() and int(msg)<1000):
            # print("Peer asked me this line................................." + msg )  
            sent=lst[int(msg)]
            conn.send(sent.encode())
            # print("I responded to peer this line................................." + msg )  
        else:
            conn.send(most_recent.encode())
        lock2.release()
        
    conn.close()
    print("Connection closed from: ", addr)
              
def peer_send():
    thread_for_clients = []
    # should we make more than one me_as_server_sokcets ?
    for i in range (len(peernames)):
        connectionSocket,addr=me_as_server_socket.accept()
        thread_for_clients.append(threading.Thread(target=handle_peers,args=(connectionSocket,addr)))
    
    for t in thread_for_clients:
        t.start()
        t.join()

    me_as_server_socket.close()
    print("my server socket closed")


#RECEIVING FROM MY PEERS FUNCTIONS
def connect_peers():
    print("Trying to connect ...")
    for i in range (len(peernames)):
       peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
       print("connection succesful from: ", peernames[i])

def peer_recv(i):
    global lines,lst,unique
    while (lines < 1000):
        lock3.acquire()
        sentence = "SENDLINE\n"
        if(lines>800):
            sentence=str(random.choice(unique))

        # print("Request........................... sent to peer........."+ sentence)
        peer_sockets_recv[i].send(sentence.encode())
        
        st = ""
        peer_sockets_recv[i].setblocking(0)
        ready = select.select([peer_sockets_recv[i]], [], [], 0.5)
        if ready[0]:
            string = peer_sockets_recv[i].recv(4096)
            st = string.decode()
        

        # print("Received from...........................  peer........."+ sentence)
        if (st != "Hello" and st!=""):
            tmp = st.split("\n")
            if (len(tmp) > 2 and tmp[0].isnumeric() and lst[int(tmp[0])]==""):
                s = tmp[0]+"\n"+tmp[1]+"\n"
                lst[int(tmp[0])] = s
                unique.remove(int(tmp[0]))
                lines+=1
        
        print("PEER:",lines)
        lock3.release()
        

    sentence="DISCONNECT\n"
    peer_sockets_recv[i].send(sentence.encode())
    peer_sockets_recv[i].close()
    print("Done receiving and closed peer socket: ", peernames[i])
        
# Submiting answer to server
def SUBMIT():
    submit_socket= socket(AF_INET, SOCK_STREAM)
    submit_socket.connect((servername, serverport))
    submit_socket.send("SUBMIT\n".encode())
    print("Wrote submit")
    submit_socket.send(("cs1210793@blue_dictators\n").encode())
    submit_socket.send((str(len(lst))+"\n").encode())
    print("Submitted no. of lines")
    i=0
    st=""
    while(i<len(lst)):
        st+=lst[i]
        i+=1
    submit_socket.send(st.encode())
    print("SUBMITTED LINE", i)
    print("loop ends")
    st=submit_socket.recv(4096).decode()
    print(st)
    submit_socket.close()    

def main():

    #Make Initial connections
    server_connect()
    deploy_server()
    time.sleep(5)
    connect_peers()
    
    ts=time.time()
    
    #Make threads
    server_thread= threading.Thread(target=server_recv)
    peer_recv_thread = []
    for i in range (len(peernames)):
        peer_recv_thread.append(threading.Thread(target=peer_recv,args=(i,)))   
    peer_send_thread = threading.Thread(target=peer_send)
    
    # Start all threads    
    server_thread.start()
    peer_send_thread.start()
    for i in range (len(peernames)):
        peer_recv_thread[i].start()

    # #Join all threads
    server_thread.join()
    peer_send_thread.join()
    for i in range (len(peernames)):
        peer_recv_thread[i].join()

        
    #Close all connections
    server_socket.close()
    for i in range (len(peernames)):
        peer_sockets_recv[i].close()
    me_as_server_socket.close()
    
    f = open("test.txt", 'w')
    te=time.time()
    for i in lst:
        f.write(i)
        # print(i)
        
    print()
    print(len(lst))
    print(te-ts)
    f.close()
    SUBMIT() 
    
main()
