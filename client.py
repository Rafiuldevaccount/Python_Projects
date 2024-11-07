import socket

target_ip = '127.0.0.1'
target_port = 1024;

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

client.connect((target_ip, target_port));
client.send(b'12');

client.settimeout(10);

resp = client.recv(4096)

print(resp.decode())
client.close();

