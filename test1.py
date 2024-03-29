import threading
import time
from socket import *

servername='vayu.iitd.ac.in'
serverport=9801
my_server_port=2047
my_client_ports_recv=[3050]
my_client_ports_send=[2050]
most_recent = ("0","")

clientnames=["10.184.63.175"]
arr=set([])
Socket_server = socket(AF_INET, SOCK_STREAM)
client_sockets_recv = []
client_sockets_send = []
for i in range (len(clientnames)):
    client_sockets_recv.append(socket(AF_INET, SOCK_STREAM))
for i in range (len(clientnames)):
    client_sockets_send.append(socket(AF_INET, SOCK_STREAM))


def server_connect(servername,serverport):
    Socket_server.connect((servername, serverport))

def server_recv(my_server_port):
    while (len(arr) < 1000):
        sentence = "SENDLINE\n"
        Socket_server.send(sentence.encode())
        str=Socket_server.recv(my_server_port).decode()
        for i in range(len(str)):
            if(str[i]=="\n"):
                index=i
                break
        l=[str[0:index],str[index+1:]]   
        most_recent=(l[0]+"\n",l[1])
        print(len(arr))
        arr.add((l[0]+"\n",l[1]))
        

def client_connect_recv(client_sockets_recv,clientnames,clientports):
   for i in range (len(client_sockets_recv)):
       client_sockets_recv[i].connect((clientnames[i], clientports[i]))
       

def cleint_bind_send(client_sockets_send, my_client_ports_send):
    for i in range (len(client_sockets_send)):
        client_sockets_send[i].bind(('', my_client_ports_send[i]))
        client_sockets_send[i].listen(5)
       

def client_recv(i):
    while (len(arr) < 1000):
        sentence = str('SENDLINE\n')
        client_sockets_recv[i].send(sentence.encode())
        str=client_sockets_recv[i].recv(my_client_ports_recv[i]).decode()
        for i in range(len(str)):
            if(str[i]=="\n"):
                    index=i
                    break
        l=[str[0:index],str[index+1:]]   
        most_recent=(l[0]+"\n",l[1])
        print(len(arr))
        arr.add((l[0]+"\n",l[1]))
        
        
def client_send(i):
    while (True):    
        connectionSocket,addr=client_sockets_send[i].accept()
        sentence = connectionSocket.recv(client_sockets_send[i]).decode()
        if (sentence == "SENDLINE\n"): 
            str=most_recent[0]+"\n"+most_recent[1]
            connectionSocket.send(str.encode())

def main():
    ts=time.time()
    server_connect(servername,serverport)
    cleint_bind_send(client_sockets_send, my_client_ports_send)
    time.sleep(5)
    client_connect_recv(client_sockets_recv,clientnames,my_client_ports_recv)
    t1 = threading.Thread(target=server_recv,args=(my_server_port,))
    recv_t = []
    send_t = []
    for i in range (len(my_client_ports_recv)):
        recv_t.append(threading.Thread(target=client_recv,args=(i,)))
        
    for i in range (len(my_client_ports_send)):
        send_t.append(threading.Thread(target=client_send,args=(i,)))
        
    t1.start()
    for i in range (len(client_sockets_send)):
        send_t[i].start()
    for i in range (len(client_sockets_recv)):
        recv_t[i].start()
        
    t1.join()
    for i in range (len(client_sockets_send)):
        send_t[i].join()
    for i in range (len(client_sockets_recv)):
        recv_t[i].join()

        

    Socket_server.close()
    for i in range (len(client_sockets_recv)):
        client_sockets_recv[i].close()
    te=time.time()
#     print(arr)
    print(len(arr))
    print(te-ts)
    
main()
