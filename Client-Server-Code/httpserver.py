# Hsin Tai
# Ht235
# Section 2

import sys
import socket
import os.path
import time

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a TCP "welcoming" socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port:  ' + str(serverPort) + '\n')

while True:
    # Accept incoming connection requests; allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()

    # Receive and breakdown request from client
    request = connectionSocket.recv(8192).decode()
    headers= request.split('\r\n')
    head0 = headers[0]
    if 'GET' not in head0:
        print('???')
        serverSocket.close()
        break
    filename = head0.split(' ')[1]
    filename = filename[1:]
    if 'If-Modified-Since' in request:
        rType = 'cGET'
    else:
        rType = 'GET'

    try:
        # Read file
        file = open(filename, 'r')
    # Error -> File Not Found
    except:
        # Status Line
        status = 'HTTP/1.1 404 Not Found\r\n'
        # Date header
        currentT = time.gmtime()
        t = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", currentT)
        date = 'Date: ' + t
        # Content Length
        conL = 'Content-Length: 0\r\n'
        blank = '\r\n'
        response = status + date + conL + blank
        connectionSocket.send(response.encode())
        serverSocket.close()
        break

    if rType == 'GET':
        body = file.read()
        # GET response
        # Status Line
        status = 'HTTP/1.1 200 OK\r\n'
        # Date header
        currentT = time.gmtime()
        t = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", currentT)
        date = 'Date: ' + t
        # Last Modified
        secs = os.path.getmtime(filename)
        modT = time.gmtime(secs)
        lastMod = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", modT)
        lastModified = 'Last-Modified: ' + lastMod
        # Content Length and Type
        conL = 'Content-Length: ' + str(len(body.encode('utf-8'))) + '\r\n'
        conT = 'Content-Type:  text/html; charset=UTF-8\r\n' 
        blank = '\r\n'
        response = status + date + lastModified + conL + conT + blank + body
        
    elif rType == 'cGET':
        # Get If-Modified-Since
        for header in headers:
            if 'If-Modified-Since' in header:
                ifM = header.split(': ')[1]
                t = time.strptime(ifM, "%a, %d %b %Y %H:%M:%S %Z\r\n")
                ifSecs = time.mktime(t)
        # If not modified, return not modified reponse
        lastMod = os.path.getmtime(filename)
        lastModT = time.gmtime(lastMod)
        lastModTime = time.mktime(lastModT)
        if  lastModTime <= ifSecs:
            # returnCode = 304
            # Status Line
            status = 'HTTP/1.1 304 Not Modified\r\n'
            # Date header
            currentT = time.gmtime()
            t = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", currentT)
            date = 'Date: ' + t
            blank = '\r\n'
            response = status + date + blank
        else:
            body = file.read()
            # GET response
            # Status Line
            status = 'HTTP/1.1 200 OK\r\n'
            # Date header
            currentT = time.gmtime()
            t = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", currentT)
            date = 'Date: ' + t
            # Last Modified
            secs = os.path.getmtime(filename)
            modT = time.gmtime(secs)
            lastMod = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", modT)
            lastModified = 'Last-Modified: ' + lastMod
            # Content Length and Type
            conL = 'Content-Length: ' + str(len(body.encode('utf-8'))) + '\r\n'
            conT = 'Content-Type:  text/html; charset=UTF-8\r\n' 
            blank = '\r\n'
            response = status + date + lastModified + conL + conT + blank + body
    else:
        print("Something's Wrong.")
        response = '???'

    connectionSocket.send(response.encode())
    file.close()
    serverSocket.close()
    break



