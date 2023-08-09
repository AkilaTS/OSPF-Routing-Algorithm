This directory contains an implementation of the OSPF routing algorithm for routers running on two different machines.

To run code:
     python3 ospf.py -i id -f infile -o outfile -h hi -a lsai -s spfi -m machine_num -ip1 IP_addr1 -ip2 IP_addr2

 where machine_num is 0 or 1, and IP_aadr1 and IP_addr2 are the IP addresses of the corresponding machines. Half the routers will be run on the first machine and the other half on the other machine.

Input format for dynamic link changes, output format and program termination procedure are same as mentioned in the README of the main directory.
