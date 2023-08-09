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
import sys
from threading import Thread
from time import sleep
import time
import random

# to send 'HELLO' packets to neighbor nodes
def send_hellos(hello_time):    #are there arguments needed or glabal variables are shared
    sleep(1)
    msg = "HELLO "+str(node_id)
    while(True):
        for i in range(len(neighbors)):    # send to each neighbor
           bytesToSend = msg.encode()
           if(int(neighbors[i]) < (N//2)):
              UDPSocket.sendto(bytesToSend, (IP_1, 10000 + int(neighbors[i])))
           else:
              UDPSocket.sendto(bytesToSend, (IP_2, 10000 + int(neighbors[i])))
        sleep(hello_time)   # repeat after 'hello_time' seconds
     
# to send 'LSA' packets to neighbor nodes  
def send_LSA(lsa_time):
    LSA_seq_no = 0
    sleep(lsa_time)
    while(True):
        msg = "LSA "+str(node_id)+" "+str(LSA_seq_no)
        no_of_entries = 0
        temp_msg = ""
        for i in range(len(neighbors)):
            curr_node = neighbors[i]
            if(curr_node in costs):
                temp_msg += " "+curr_node+" "+ str(costs[curr_node])
                no_of_entries += 1
            
        msg += " "+str(no_of_entries)+temp_msg
        recv_IP = ""
        for i in range(len(neighbors)):
           bytesToSend = msg.encode()
           if(int(neighbors[i]) < (N//2)):
              UDPSocket.sendto(bytesToSend, (IP_1, 10000 + int(neighbors[i])))
           else:
              UDPSocket.sendto(bytesToSend, (IP_2, 10000 + int(neighbors[i])))
        LSA_seq_no += 1
        sleep(lsa_time)

# to recompute shortest path every 'spf_time' seconds
def compute_spf(spf_time, out_file):
    # reference time to calculate timestamp of output
    start_time = time.time()
     
    # compute shortest paths every 'spf_time' seconds
    sleep(spf_time)
    try:
        while(True):
            # run dijkstra's algorithm on the topology(as known by current node)
            min_dist = []
            visited = [0]*N
            shortest_paths = []
            for k in range(N):
                min_dist.append(1e7)
                shortest_paths.append([])
            min_dist[node_id] = 0
            shortest_paths[node_id].append(node_id)
                           
            for k in range(N):                    
                # find the 'unvisited' node with least distance from source node
                curr_min = 1e7
                curr_min_vertex = -1
                for p in range(N):
                    if(visited[p] == 0 and min_dist[p] < curr_min):
                        curr_min = min_dist[p]
                        curr_min_vertex = str(p)
                
                # mark node as visited       
                visited[int(curr_min_vertex)] = 1 
                neighbor_nodes = []
                if(curr_min_vertex in topology):         
                    neighbor_nodes = topology[curr_min_vertex].keys()
                # update distances for neighbor nodes of current min dist node
                for node in neighbor_nodes:
                    node_num = int(node)
                    min_v_num = int(curr_min_vertex)
                    if(visited[node_num] != 1 and min_dist[min_v_num] + topology[curr_min_vertex][node] < min_dist[node_num]):
                        # update distance
                        min_dist[node_num] = min_dist[min_v_num] + topology[curr_min_vertex][node]
                        shortest_paths[node_num] = []
                        # update the shortest path
                        for q in range(len(shortest_paths[min_v_num])):
                            shortest_paths[node_num].append(shortest_paths[min_v_num][q])
                        shortest_paths[node_num].append(node)
            
            # generate timestamp
            curr_time = time.time()-start_time
                           
            # record routing table in output file
            f = open(out_file+"-"+str(node_id)+".txt", "a")
            f.write("Routing Table for Node "+str(node_id)+" at time "+str(curr_time)+" s:\n")
            f.write("Destination\tPath\tCost\n")
            for k in range(N):
                if(k != node_id):
                   f.write(str(k)+"   "+str(shortest_paths[k])+"   "+str(min_dist[k]))
                   f.write("\n")
            f.write("\n")
            f.close()
            
            # wait for 'spf_time' seconds before recomputing shortest paths
            sleep(spf_time)
    except KeyboardInterrupt:
        f.close()
    finally:
        f.close()

debug_term = False

# default values, actual values will be given as command line parameters
node_id = 0
input_file = "input"
output_file = "output"

# default time intervals, specified in seconds
hello_interval = 1
lsa_interval = 5
spf_interval = 20

# read command line parameters
node_id = int(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]
hello_interval = int(sys.argv[4])
lsa_interval = int(sys.argv[5])
spf_interval = int(sys.argv[6])
IP_1 = sys.argv[7]
IP_2 = sys.argv[8]

# parameters to be read from input file
N = 0  # no of routers
L = 0  # no of links
min_Cij = {}  # min value of the link cost
max_Cij = {}  # max value of the link cost

costs = {}
neighbors = []
topology = {}

with open(input_file+".txt", 'r') as fp:
    # read N and L values, and link details
    x = fp.readlines()
    N = int(x[0].strip())
    L = int(x[1].strip())    
    for i in range(L):
        vals = x[i+2].split(" ")
        if(node_id == int(vals[0])):
            neighbors.append(vals[1])
            min_Cij[vals[1]] = int(vals[2])
            max_Cij[vals[1]] = int(vals[3])
        elif(node_id == int(vals[1])):
            neighbors.append(vals[0])
            min_Cij[vals[0]] = int(vals[2])
            max_Cij[vals[0]] = int(vals[3])

last_seq_no = [-1]*N
for i in range(N):
    topology[str(i)] = {}

# create a socket for this router
localIP = ""
if(node_id<(N//2)):
    localIP = IP_1
else:
    localIP = IP_2
localPort = 10000+node_id
bufferSize = 2048
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind((localIP, localPort))
sleep(2)

# start thread to send HELLO packets
thread = Thread(target = send_hellos, args = (hello_interval,))
thread.daemon = True
thread.start()
# start thread to send LSA packets
thread2 = Thread(target = send_LSA, args = (lsa_interval,))
thread2.daemon = True
thread2.start()
# start thread to compute the shortest path
thread3 = Thread(target = compute_spf, args = (spf_interval, output_file))
thread3.daemon = True
thread3.start()

print("Router ",str(node_id)," started on ",localIP, " port ",localPort)

try:
    while(True):
        # receive packets sent by neighbor nodes
        bytesAddressPair = UDPSocket.recvfrom(bufferSize)
        msg_recd = bytesAddressPair[0].decode()
        sender_address = bytesAddressPair[1]
        msg_parts = msg_recd.split(" ")
               
        # router process has to be terminated
        if(msg_parts[0]=="Bye"):
            break
        
        # indicates dynamic link change
        elif(msg_parts[0]=="INFO"):
            node_1 = msg_parts[2]
            node_2 = msg_parts[3]
            # link is down
            if(msg_parts[1]=="BREAK"):
                               
                if(node_id == int(node_1)):
                    neighbors.remove(node_2)
                elif (node_id == int(node_2)):
                    neighbors.remove(node_1)
                                    
                del_val = topology[node_1].pop(node_2, "No key found")
            
                if(del_val == "No key found"):
                    print("Requested link not present")
                del_val = topology[node_2].pop(node_1, "No key found")
                if(del_val == "No key found"):
                    print("Requested link not present")
                                
            # new link added  
            elif(msg_parts[1]=="ADD"):
                minVal = int(msg_parts[4])
                maxVal = int(msg_parts[5])
                
                if(node_id == int(node_1)):
                    neighbors.append(node_2)
                    min_Cij[node_2] = minVal
                    max_Cij[node_2] = maxVal
                elif(node_id == int(node_2)):
                    neighbors.append(node_1)
                    min_Cij[node_1] = minVal
                    max_Cij[node_1] = maxVal
        
        # received 'HELLO' packet  
        elif(msg_parts[0]=="HELLO"):
            node_num = msg_parts[1]
            link_cost = random.randrange(min_Cij[node_num], max_Cij[node_num]+1)
            msg_to_send = "HELLOREPLY "+str(node_id)+" "+node_num+" "+str(link_cost)
            bytesToSend = msg_to_send.encode()
            UDPSocket.sendto(bytesToSend, sender_address)
        
        # received 'HELLOREPLY" from some neighbor node
        elif(msg_parts[0]=="HELLOREPLY"):
            node_num_1 = msg_parts[2]   #check if cost_ij or cost_ji
            node_num_2 = msg_parts[1]
            link_cost = int(msg_parts[3])
            costs[node_num_2] = link_cost
            topology[node_num_1][node_num_2] = link_cost
        
        # received LSA packet 
        elif(msg_parts[0]=="LSA"):
            sender_node = msg_parts[1]
            sender_id = int(sender_node)
            seq_no = int(msg_parts[2])
            if(seq_no>last_seq_no[sender_id]):
                # extract topology information from the LSA packet
                last_seq_no[sender_id] = seq_no
                no_of_entries = int(msg_parts[3])
                topology[sender_node].clear()
                for j in range(no_of_entries):
                    node_num_1 = msg_parts[4+2*j] 
                    link_cost = int(msg_parts[5+2*j])
                    topology[sender_node][node_num_1] = link_cost
                    
                # forward LSA to neighbors, except the neighbor from which the LSA was received
                for j in range(len(neighbors)):
                    if(j != sender_id):
                        curr_recv_id = int(neighbors[j])
                        if(curr_recv_id < (N//2)):
                            UDPSocket.sendto(msg_recd.encode(), (IP_1, 10000+curr_recv_id))
                        else:
                            UDPSocket.sendto(msg_recd.encode(), (IP_2, 10000+curr_recv_id))
except KeyboardInterrupt:
	if(debug_term):
	    print("Keyboard Interrupt")
finally:
    UDPSocket.close()
    print("Router ",str(node_id)," terminated")
