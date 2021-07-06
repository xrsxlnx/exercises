"""
The script is written by Ruslan Miriniuc 2021_07_06.
It scans ports for a given host or range and updates csv file with appiared open ports.
Also the script can be written with CLI arguments and with whole scope of existing ports,
but for the exercise I prefeared to use input prompt and range for ports to make it run faster for testing
CSV file can be in a different place in your environment, lines 25, 66 and 80 should be updated with your path
"""

import nmap
import os
import csv

hosts = str(input('Enter a host to scan or a range:\n '
              'Examples:\n'
              'If one host: 127.0.0.1\n'
              'If range: 127.0.0.1 - 127.0.0.5  with a space on both sides of the dash\n'
              'Pingsweep a network: 192.168.1.0/24\n'))

ports = input('Enter a port or range to scan\n'
                  'Examples:\n'
                  'If one port: 22\n'
                  'If range: 22-44 without spaces\n')


csvfile = "C:/Users/DragoN/pythonProject/data.csv"
headers = 'IP, Ports, State, Type\n'


try:                               #check for a csv file existance
    csvfile = open(csvfile)
    csvfile.close()
except FileNotFoundError:
    csvfile = open(csvfile, 'w')
    csvfile.write(str(headers))
    csvfile.close()

list1 = []
list2 = []
try:
    nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)

nm.scan(hosts=hosts, arguments='-n -sP -PE -PA21,23,80,3389')
hosts_list = list([(x) for x in nm.all_hosts()])
#print(hosts_list)

#Scans given ports for requested hosts, checks ports status and type(in this case tcp),
#sends an output to a list2
for h in hosts_list:
    nm.scan(h, str(ports))
    if ('tcp' in nm[h]):
        ports = list(nm[h].all_tcp())
    #print(ports)
    #print('Target - %s' %(h))
    for i in ports:
        if nm[h]['tcp'][i]['state'] == 'open':
            data = h, str(i), nm[h]['tcp'][i]['state'], 'tcp'
            list2.append(data)
#print(list2)

with open ("C:/Users/DragoN/pythonProject/data.csv", "r") as f: #reads the csv file and send the output to a list1
    list1 = list(csv.reader(f, delimiter=','))
#print(list1)
f.close()

list1 = [tuple(l) for l in list1]  #convert a list of lists to a list of tuples
#print(list1)

#compares list2 which contains fresh scan results with reading data from csv in list1,
#appdate the csv with new appeared results
adate_list=set(list2) - set(list1)


if len(adate_list)>0:
    with open ("C:/Users/DragoN/pythonProject/data.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\r")
        writer.writerows(adate_list)
    f.close()
    print('Update CSV...')
    print('Target - %s: Full scan results:\n' %(hosts))
    for i in adate_list:
        print('Host: %s  Port: %s/%s/%s/' %(i[0],i[1],i[2],i[3]))
    print('CSV updated')

else:
    print('Target - %s: No new records found in the last scan.' %(hosts))










