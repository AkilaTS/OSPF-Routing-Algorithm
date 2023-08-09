This is an implementation of a simplified version of the Open Shortest Path First (OSPF) routing protocol.

Given a set of N routers,each router: 
(a) exchanges HELLO packets with neighbours,
(b) creates Link State Advertisement (LSA) packets based on neighboring nodes’ info
(c) broadcasts the LSA packets to all other routers in the network
(d) constructs the network topology based on the LSA packets received from other routers
(e) determine the routing table entries based on this topology by using Dijkstra’ algorithm. If multiple equal-cost paths exist, any one of them will be reported.

The HELLO packets are exchanged every x seconds. The LSA updates are sent every y seconds. The routing table computation is done every z seconds.

To run code:
     python3 ospf.py -f infile -o outfile -h hi -a lsai -s spfi

where the command line arguments are as specified in the problem statement. These time interval arguments can be skipped as default values have been provided in the code.

After the router processes are started, user can enter 'BREAK' or 'ADD' commands to introduce dynamic link changes. The format for the 'BREAK' and 'ADD' commands will be displayed in the terminal itself.

The main program and router processes can be terminated by entering the 'Bye' command. The output of the routing tables of router with id 'i' along with the timestamps will be recorded in the 'output-i.txt' file. If there is no path possible to some destination node then the cost will be displayed as 10000000.

Code to run the routers on two different machines can be found in the 'Different Machines' directory.
