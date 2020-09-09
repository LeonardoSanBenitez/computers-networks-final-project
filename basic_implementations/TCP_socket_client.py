import socket

# Samir's server: 54.211.210.101:10100
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
HEADERSIZE = 10
payload = "{'data1':666, 'data2':667}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    msg = f"{len(payload):<{HEADERSIZE}}"+payload
    print (msg)

    s.sendall(bytes(msg, "utf-8"))
    full_msg = s.recv(64)
    s.close()

print('Received back:', full_msg)
