import random
import select
import threading
import time
from socket import *

# Vayu server
servername='vayu.iitd.ac.in'
serverport=9801
server_socket = socket(AF_INET, SOCK_STREAM)

# Locks
lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()
lock4 = threading.Lock()
lock5 = threading.Lock()

# Me acting as server
me_as_server_port=9998
me_as_server_socket = socket(AF_INET, SOCK_STREAM)


# Me receiving from peers DISTINCT PEER NAMES
my_addr = "10.184.36.163"
ip1 = "10.184.9.10"
ip2 = "10.184.23.207"
ip3 = "10.194.9.19"
peernames=[ip1, ip2, ip3]
mapping = {my_addr: 0,  ip3: 1}
breaking = [0, 0]

# Here write the me_as_server_ports of your peers
peer_s_server_ports=[9998, 9998, 9998]

# Time array
duration = []

# First port is to receive from server, then others from peers
peer_sockets_recv = []
for i in range (len(peernames)):
    peer_sockets_recv.append(socket(AF_INET, SOCK_STREAM))


# Data Structures
most_recent = "Hello"
lst = [""]*1000
unique = [i  for i in range(1000)]
lines = 0


# Functions

# Submiting answer to server
def SUBMIT():
    lock5.acquire()
    server_socket.send("SUBMIT\n".encode())
    print("Wrote submit")
    server_socket.send(("cs1210793@blue_dictators\n").encode())
    server_socket.send((str(len(lst))+"\n").encode())
    print("Submitted no. of lines")
    i=0
    st=""
    while(i<len(lst)):
        server_socket.send(lst[i].encode())
        i+=1

    print("SUBMITTED LINE", i)
    print("loop ends")
    st=server_socket.recv(4096).decode()
    tmp = st.split("\n")
    print(tmp[-2]+"\n")
    server_socket.send("SEND INCORRECT LINES\n".encode())
    st=server_socket.recv(9000).decode()
    print(st)
    lock5.release()

#SERVER FUNCTIONS
def server_connect():
    while(True):
        try:
            server_socket.connect((servername, serverport))
            break
        except Exception:
            continue
    
def server_recv():
    global lines,lst,unique,most_recent,duration,breaking,mapping,my_addr
    while (lines < 1000):
        sentence = "SENDLINE\n"
        lock1.acquire()
        
        try:
            server_socket.send(sentence.encode())
        except Exception:
            server_connect()
            server_socket.send(sentence.encode())
        
        st = ""
        try:
            st=server_socket.recv(4096).decode()
        except Exception:
            server_connect()
            server_socket.send(sentence.encode())
            st=server_socket.recv(4096).decode()

        tmp = st.split("\n")
        i=0
        if(len(tmp)%2==1 and len(tmp) > 2):
            while (i<len(tmp)):
                if (tmp[i].isnumeric() and lst[int(tmp[i])]==""):
                    s = tmp[i]+"\n"+tmp[i+1]+"\n"
                    unique.remove(int(tmp[i]))
                    lst[int(tmp[i])] = s
                    lines+=1
                    duration.append(time.time())
                    most_recent = s
                i+=2

        # print("SERVER: ", lines)
        lock1.release()

    # breaking[mapping[my_addr]] = 1
    start = duration[0]
    for i in range(len(duration)):
        duration[i] -= start
    
    SUBMIT()
    print(duration)
    server_socket.close()
    print("Server Sokcet Closed")

        
#ME AS SERVER FUNCTIONS
def deploy_server():
    me_as_server_socket.bind(('', me_as_server_port))
    me_as_server_socket.listen(10000)
    print("Server Deployed")
        
def handle_peers(conn,addr):
    global most_recent,lst,breaking,mapping
    print("New connection established from: ",addr)
    while(True):
        lock2.acquire()
        try:
            msg=conn.recv(100).decode()
        except Exception:
            break
        if (msg=="DISCONNECT\n"):
            # breaking[mapping[addr[0]]] = 1
            ack = "DONE\n"
            try:
                conn.send(ack.encode())
            except Exception:
                break
            # print(breaking)
            break
        elif (msg.isnumeric() and int(msg)<1000):
            line=lst[int(msg)]
            try:
                conn.send(line.encode())
            except Exception:
                break
        elif (msg == "SENDLINE\n"):
            try:
                conn.send(most_recent.encode())
            except Exception:
                break
        else:
            line = random.choice(lst)
            try:
                conn.send(line.encode())
            except Exception:
                break

        lock2.release()
        
    # conn.close()
    # print("Connection closed from: ", addr)
              
def peer_send():
    thread_for_clients = []
    sockets = []
    for i in range (len(peernames)):
        connectionSocket,addr=me_as_server_socket.accept()
        sockets.append(connectionSocket)
        thread_for_clients.append(threading.Thread(target=handle_peers,args=(connectionSocket,addr)))
    
    for t in thread_for_clients:
        t.start()

    # for t in thread_for_clients:
    #     t.join()
    
    while (True):
        connectionSocket,addr=me_as_server_socket.accept()
        t = threading.Thread(target=handle_peers,args=(connectionSocket,addr))
        t.start()
        t.join()

    # me_as_server_socket.close()
    # for i in range (len(peernames)):
    #     sockets[i].close()
    # print("Done sending peers, Ready to terminate ...")


#RECEIVING FROM MY PEERS FUNCTIONS
def connect_peer_i(i):
    while (True):
        try:
            peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
            print("connection succesful from: ", peernames[i])
            break
        except Exception:
            continue


def connect_peers():
    print("Trying to connect ...")
    for i in range (len(peernames)):
        while (True):
            try:
                peer_sockets_recv[i].connect((peernames[i], peer_s_server_ports[i]))
                print("connection succesful from: ", peernames[i])
                break
            except Exception:
                continue

def peer_recv(i):
    global lines,lst,duration,mapping,breaking,my_addr
    while (lines < 1000):
        sentence = "SENDLINE\n"
        if(lines>800 and len(unique)>0):
            sentence=str(random.choice(unique))

        lock3.acquire()
        try:
            peer_sockets_recv[i].send(sentence.encode())
        except Exception:
            connect_peer_i(i)
            peer_sockets_recv[i].send(sentence.encode())
            
        
        st = ""
        peer_sockets_recv[i].setblocking(0)
        ready = select.select([peer_sockets_recv[i]], [], [], 0.03)
        if ready[0]:
            try:
                string = peer_sockets_recv[i].recv(4096)
                st = string.decode()
            except Exception:
                connect_peer_i(i)
                peer_sockets_recv[i].send(sentence.encode())
                string = peer_sockets_recv[i].recv(4096)
                st = string.decode()

        j = 0
        if (st != "Hello" and st!=""):
            tmp = st.split("\n")
            if(len(tmp)%2==1 and len(tmp) > 2):
                while (j<2):
                    if (tmp[j].isnumeric() and lst[int(tmp[j])]==""):
                        s = tmp[j]+"\n"+tmp[j+1]+"\n"
                        unique.remove(int(tmp[j]))
                        lst[int(tmp[j])] = s
                        lines+=1
                        # print("total lines so far: ", lines)
                        duration.append(time.time())
                    j+=2
        
                # print("PEER:",i, lines)
        lock3.release()
        
    # SUBMIT()    
    lock4.acquire()
    # breaking[mapping[my_addr]] = 1   
    while(True):
        sentence="DISCONNECT\n"
        peer_sockets_recv[i].send(sentence.encode())

        st = ""
        peer_sockets_recv[i].setblocking(0)
        ready = select.select([peer_sockets_recv[i]], [], [], 0.08)
        if ready[0]:
            string = peer_sockets_recv[i].recv(4096)
            st = string.decode()
        if (st != "DONE\n"): 
            break
    lock4.release()
        
    # peer_sockets_recv[i].close()
    # print("Done receiving and closed peer socket: ", peernames[i])

def main():

    
    # Make Initial connections
    server_connect()
    deploy_server()
    connect_peers()
    
    ts=time.time()
    
    # Make threads
    server_thread= threading.Thread(target=server_recv)
    peer_recv_thread = []
    for i in range (len(peernames)):
        peer_recv_thread.append(threading.Thread(target=peer_recv,args=(i,)))   
    peer_send_thread = threading.Thread(target=peer_send)
    
    # Start all threads    
    server_thread.start()
    for i in range (len(peernames)):
        peer_recv_thread[i].start()
    peer_send_thread.start()

    # Join all threads
    server_thread.join()
    for i in range (len(peernames)):
        peer_recv_thread[i].join()
    peer_send_thread.join()
    

    print("done threads")
        
    global breaking
    # while (True):
    #     if (breaking[0]==1 and breaking[1]==1 and breaking[2]==1):
    #         # Close all connections
    #         for i in range (len(peernames)):
    #             peer_sockets_recv[i].close()
    #         me_as_server_socket.close()
    #         break
    
    
    # print("closed all connections and server")
    
    f = open("test.txt", 'w')
    te=time.time()
    for i in lst:
        f.write(i)
        # print(i)
        
    print()
    print(len(lst))
    print(te-ts)
    f.close()
    
    # global breaking
    # while (True):
    #     if (breaking[0]==1 and breaking[1]==1 and breaking[2]==1):
    #         # Close all connections
    #         for i in range (len(peernames)):
    #             peer_sockets_recv[i].close()
    #         me_as_server_socket.close()
    #         break

    
    print(duration)
    
main()
