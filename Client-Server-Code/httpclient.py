# Hsin Tai
# Ht235
# Section 2

import sys
import socket
import time
import os.path

# Break down command line arg
url = sys.argv[1]
host, filename = url.split('/')
port = int(host.split(':')[1])
host = host.split(':')[0]

# Create TCP client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create TCP connection to server
clientSocket.connect((host, port))

#Check for cache file
cacheName = 'cache.txt'
conditional = False
try:
    cache = open(cacheName, 'r') 
    # Conditional GET request
    for line in cache:
        if 'Last-Modified' in line:
            lastM = line.split(': ')[1]
    conditional = True
    cache.close()
    request = 'GET /' + filename + '  HTTP/1.1\r\nHost: ' + host + ':' + str(port) + '\r\n' + 'If-Modified-Since: ' + lastM + '\r\n\r\n'
    print('Sending the following conditional GET request:\n' + request)
except IOError:
    # HTTP GET request
    request = 'GET /' + filename + '  HTTP/1.1\r\nHost: ' + host + ':' + str(port) + '\r\n\r\n'
    print('Sending the following GET request:\n' + request)
    
# Send encoded data through TCP connection
clientSocket.send(request.encode())
# Receive the server response
response = clientSocket.recv(8192)
decodedR= response.decode()
print('Received the following response: \n' + decodedR.split('\r\n\r\n')[0] + '\r\n\r\n')

if 'Not Found' in decodedR:
    clientSocket.close()
elif 'Not Modified' in decodedR:
    clientSocket.close()
else:
    if conditional == False:
        cache = open(cacheName, 'w') 
        body = decodedR.split('\r\n')[-1]
        print('Content of file: \n' + body)

        for line in decodedR.split('\r\n'):
            if 'Last-Modified' in line:
                cache.write(line + '\n')

        cache.write(body)
        cache.close()
    else:
        cache = open(cacheName, 'w') 
        body = decodedR.split('\r\n')[-1]
        print('New content of file: \n' + body)

        for line in decodedR.split('\r\n'):
            if 'Last-Modified' in line:
                cache.write(line + '\n')

        cache.write(body)
        cache.close()

# Close the client socket
clientSocket.close()
