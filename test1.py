import threading
import time
from socket import *

servername='vayu.iitd.ac.in'
serverport=9801
my_server_port=2048
my_client_ports=[2049]
# most_recent = ("0","")

clientnames=["10.184.60.82"]
arr=set([])
Socket_server = socket(AF_INET, SOCK_STREAM)
client_sockets = []
for i in range (len(clientnames)):
    client_sockets.append(socket(AF_INET, SOCK_STREAM))


def server_connect(servername,serverport):
    Socket_server.connect((servername, serverport))

def server_recv(myserverport):
    while (len(arr) < 1000):
        sentence = "SENDLINE\n"
        Socket_server.send(sentence.encode())
        str=Socket_server.recv(myserverport).decode()
        for i in range(len(str)):
            if(str[i]=="\n"):
                index=i
                break
        l=[str[0:index],str[index+1:]]   
        # most_recent=(l[0]+"\n",l[1]+"\n")
        print(l)
        arr.add((l[0]+"\n",l[1]))
        

def client_connect(client_sockets,clientnames,clientports):
   for i in range (len(client_sockets)):
       client_sockets[i].connect((clientnames[i], clientports[i]))

def client_recv(i):
    while (len(arr) < 1000):
        sentence = str('SENDLINE\n')
        client_sockets[i].send(sentence.encode())
        line=client_sockets[i].recv(my_client_ports[i])
    
def client_send(i):
    while (True):    
        client_sockets[i].bind(('', my_client_ports[i]))
        client_sockets[i].listen(1)
        connectionSocket,addr=client_sockets[i].accept()
        sentence = connectionSocket.recv(client_sockets[i]).decode()
        if (sentence == "SENDLINE\n"): 
            connectionSocket.send(most_recent[0].encode())
            connectionSocket.send(most_recent[1].encode())

def main():
    ts=time.time()
    server_connect(servername,serverport)
#     client_connect(client_sockets,clientnames,my_client_ports)
#     t1 = threading.Thread(server_recv,my_server_port)
#     recv_t = [t1]
#     send_t = []
#     for i in range (len(my_client_ports)):
#         recv_t.append(threading.Thread(client_recv,i))
        
#     for i in range (len(my_client_ports)):
#         send_t.append(threading.Thread(client_connect_send,i)) 

    t1 = threading.Thread(target=server_recv, args=(my_server_port,))
#     send_thread = []
#     recv_thread = []
#     for i in range (len(client_sockets)):
#         send_thread.append(threading.Thread(target=client_send,args=(i,)))
#     for i in range (len(client_sockets)):
#         recv_thread.append(threading.Thread(target=client_recv,args=(i,)))
        
    t1.start()
    t1.join()
#     for i in range (len(client_sockets)):
#         send_thread[i].start()
#     for i in range (len(client_sockets)):
#         recv_thread[i].start()


    Socket_server.close()
#     for i in range (len(client_sockets)):
#         client_sockets[i].close()
    te=time.time()
#     print(arr)
    print(len(arr))
    print(te-ts)
    
main()