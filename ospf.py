# NAME: Akila Tharini Sivakumar
# Roll Number: CS20B006
# Course: CS3205 Jan. 2023 semester
# Lab number: 5
# Date of submission: 27.04.2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): https://pythontic.com/modules/socket/udp-client-server-example

import socket
import os
import sys
from threading import Thread
from time import sleep

# default time intervals, specified in seconds
hello_interval = 1
lsa_interval = 5
spf_interval = 20

input_file = "input"
output_file = "output"

# read command line arguments
n_args = len(sys.argv)
arg_no = 1
while arg_no<n_args:
    if(sys.argv[arg_no]=="-f"):
       input_file = sys.argv[arg_no+1]
       arg_no = arg_no+2
    elif(sys.argv[arg_no]=="-o"):
       output_file = sys.argv[arg_no+1]
       arg_no = arg_no+2
    elif(sys.argv[arg_no]=="-h"):
       hello_interval = int(sys.argv[arg_no+1])
       arg_no = arg_no+2
    elif(sys.argv[arg_no]=="-a"):
       lsa_interval = int(sys.argv[arg_no+1])
       arg_no = arg_no+2
    elif(sys.argv[arg_no]=="-s"):
       spf_interval = int(sys.argv[arg_no+1])
       arg_no = arg_no+2

# parameters to be read from input file
N = 0  # no of routers
L = 0  # no of links

with open(input_file+".txt", 'r') as fp:
    # read no of routers and no of link values from input file
    x = fp.readlines()
    N = int(x[0].strip())
    L = int(x[1].strip())

localIP = "127.0.0.1"
localPort = 10000+N
bufferSize = 2048
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind((localIP, localPort))

# create the router processes (N router processes)
for i in range(N):
    pid = os.fork()
    if pid == -1:
        os.exit(1)

    if pid == 0:    # child process to execute router.py
        command = ["python3", "router.py",str(i),input_file,output_file,str(hello_interval),str(lsa_interval),str(spf_interval)]
        os.execvp(command[0], command)
        
sleep(2)
# display command for dynamic link changes
print("Enter BREAK node1 node2 to bring link between node_1 and node_2 down")
print("Enter ADD node1 node2 minVal maxVal to add link between node_1 and node_2")

try:
    while (True):
        print("Enter command:")
        op = input(" -> ")
        if(op == "Bye"):  # terminate the program and all router processes
            for i in range(N):
                term_msg = "Bye"
                UDPSocket.sendto(term_msg.encode(), ("127.0.0.1", 10000+i))
            break
        
        temp = op.split(" ")
        node_1 = int(temp[1])
        node_2 = int(temp[2])
        op = "INFO " + op
        
        # Send info regarding dynamic link status change to corresponding routers
        UDPSocket.sendto(op.encode(), ("127.0.0.1", 10000+node_1))
        UDPSocket.sendto(op.encode(), ("127.0.0.1", 10000+node_2))
except KeyboardInterrupt:
    # terminate router process on Keyboard Interrupt
    for i in range(N):
        term_msg = "Bye"
        UDPSocket.sendto(term_msg.encode(), ("127.0.0.1", 10000+i))
    UDPSocket.close()
finally:
    UDPSocket.close()
