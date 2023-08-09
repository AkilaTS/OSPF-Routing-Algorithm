Main Code:
Use 'make clean' to remove existing output files before running the main program.

To run:
     make clean
     python3 ospf.py -f infile -o outfile -h hi -a lsai -s spfi
     
where the command line arguments are as specified in the problem statement. These time interval arguments can be skipped as default values have been provided in the code.

After the router processes are started, user can enter 'BREAK' or 'ADD' commands to introduce dynamic link changes. The format for the 'BREAK' and 'ADD' commans will be displayed in the terminal itself.

The main program and router processes can be terminated by entering the 'Bye' command. The output of the routing tables of router with id 'i' along with the timestamps will be
recorded in the 'output-i.txt' file. If there is no path possible to some destination node then the cost will be displayed as 10000000.

The input and output files for the two test cases have been put in separate folders. Test Case 1 has some dynamic link changes(as per Demo_1 video in Extra Credit folder). Test Case 2 does not have any dynamic link changes.

Extra Credit part:
The extra credit part of introducing dynamic link changes has been implemented in the main code in the main directory itself.
The code, report and video files for the extra credit part (implementing on different machines) is in the 'Extra Credit' folder. The report with details of changes made is in the 'Extra Credit' folder.

To run code:
     make clean
     python3 ospf.py -i id -f infile -o outfile -h hi -a lsai -s spfi -m machine_num -ip1 IP_addr1 -ip2 IP_addr2
     
 where machine_num is 0 or 1, and IP_aadr1 and IP_addr2 are the IP addresses of the corresponding machines. Half the routers will be run on the first machine and the other half on the other machine.

Input interface for dynamic link changes, output format and program termination procedure are same as above.


