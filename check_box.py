#!/usr/local/bin/python3.11

import socket
import sys
import redis


# get the ip address of box
box_IP = str(sys.argv[1])
#box_name = str(sys.argv[2])

# array to send
a = []
a.append(240)
a.append(240)
a.append(0)
a.append(1)
for i in range(5,69):
    a.append(0)
a.append(240)
a.append(240)
a.append(63)

#recieve array
data = []

r = redis.Redis(host='localhost', port=6379, db=0)

try:
    socket_BF = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_BF.settimeout(3)
    socket_BF.connect((box_IP,50002))
    socket_BF.sendall(bytes(a))

    for i in range(0,14):
        datarecieve = socket_BF.recv(1)
        if i > 3 :
            data.append(datarecieve)

    # Put the data in redis
    if data:
        for i in range(0, 10):
            key = box_IP + "-" + str(i+1)
            in1 = int.from_bytes(data[i],"big")
            value = "0" if in1 == 0 else "1"
            r.set(key, value)

        print("box Up")
        sys.exit(0)

except socket.error as e:

    for i in range(0, 10):
        key = box_IP + "-" + str(i+1)
        value = "2"
        r.set(key, value)
    
    print("box Unreachable")
    sys.exit(2)

finally:
    socket_BF.close()
    r.close()
