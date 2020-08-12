# Simplified-HTTP-Client-Server
A simplified version of a HTTP client and server using TCP sockets

### The HTTP client will perform the following functions:
1. Take in a single command line argument that specifies a web url containing the hostname and port
where the server is running, as well as the name of the file to be fetched, in the appropriate format.
Example: localhost:12000/filename.html
2. If the file is not yet cached, use a HTTP GET operation to fetch the file named in the URL
   - Print out the contents of the file
   - Cache the file
3. If the file is cached, use a Conditional GET operation for the file named in the URL
   - If the server indicates the file has not been modified since last downloaded, print output
saying so (no need to print file contents in this case)
   - Otherwise, indicate that the file has been modified, and print and cache new contents

### The HTTP server will perform the following functions:
1. Read a command-line argument specifying IP address and port server is to listen on e.g. 127.0.0.1
12000
2. Open a TCP socket and listen for incoming HTTP Get and Conditional GET requests from one or more
HTTP Clients at above address and port
3. In the case of a HTTP Get request:
   - Read the named file and return a HTTP GET Response, including the Last-Modified header
field
4. In the case of a HTTP Conditional Get Request:
   - If the file has not been modified since that indicated by If-Modified-Since, return the
appropriate Not Modified response (return code 304)
   - If the file has been modified, return the file contents as in step 2
5. In the case that the named file does not exist, return the appropriate “Not Found” error (return
code 404)
6. The server must ignore all header fields in HTTP Requests it does not understand

### Simplifying Assumptions:
- Only GET and Conditional GET requests need be supported in client and server
- Only a subset of header fields need to be supported in HTTP Requests and Responses (see Message
Format section)
- However, the client and server must ignore all header fields it does not understand. For example, a
“real’ web browser will send many more header fields in GET requests than those expected to be 
implemented by the server. The server MUST ignore these fields and continue processing as if these
fields were not part of the GET request. The server MUST NOT report an error in these cases.
