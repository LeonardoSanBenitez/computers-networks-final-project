import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
HEADERSIZE = 10


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    print("-----------------------------")
    print('Connected by', addr)

    ## Decode header
    headerReceived = 0
    headerData = []
    while headerReceived < HEADERSIZE:
        data = conn.recv(min(HEADERSIZE-headerReceived, 4))
        headerData.append(data)
        headerReceived+=len(data)
        #print('Received in header', len(data), "bytes")
    print("Full header received")
    
    ## Decode payload
    payloadSize = int(b''.join(headerData))
    payloadReceived = 0
    payloadData = []
    while payloadReceived < payloadSize:
        data = conn.recv(min(payloadSize-payloadReceived, 4))
        payloadData.append(data)
        payloadReceived += len(data)
    print("Full payload received: ", b''.join(payloadData))

    ## Process payload, hower you want
    # ...

    ## Give response
    conn.sendall(b'fuk ya')
