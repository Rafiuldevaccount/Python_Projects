
import socket
import threading

def client_handle(client_sock):
    with client_sock as sock:
        ans = sock.recv(4096)
        print(ans.decode());
        sock.send(b'ACK')
        sock.close()
        
        

host_ip = ''
host_port = 1024  # Use a port above 1024 to avoid permission issues

def main():
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host.bind((host_ip, host_port))
    host.listen(5)
    print(f"HOST IS LISTENING AT: {host_ip}, {host_port}")

    while True:
        client_sock, addr = host.accept()
        client_todo = threading.Thread(target=client_handle, args=(client_sock,))
        client_todo.start()
       

if __name__ == "__main__":
    main()
