import config
import numpy as np
import algorithm.Triangulation as Triangulation

gateways = config.gateways
gateways = Triangulation._sort_dict_get_value(gateways)

beacon=np.array([5,0])
R = Triangulation._dist(gateways,beacon)
print(R)
RSSI = config.A - 10*config.n*np.log10(R)
print(RSSI)


import socket,time

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    '''
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        print("Received:", repr(data))
    print("Connection closed.")
    '''
    s.close()

while True:
    for i in range(len(gateways)):
        gateway =  sorted(config.gateways.keys())[i]
        print('{}:{}'.format(gateway,RSSI[i]))
        netcat(config.hostname, config.port, '{}:{}'.format(gateway,RSSI[i]))
    time.sleep(0.5)

