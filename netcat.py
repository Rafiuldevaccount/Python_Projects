import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
     cmd = cmd.strip()
     if not cmd:
          return
     output = subprocess.check_output(shlex.split(cmd), stderr= subprocess.STDOUT)
     return output.decode()

#the class NetCat which does the work

class NetCat():
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response = data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('>') + '\n'
                    self.socket.send(buffer.encode())  # Fixed the encode call
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))  # Fixed bind
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket):
        try:
            if self.args.execute:
                output = execute(self.args.execute)
                client_socket.send(output.encode())
            elif self.args.upload:
                file_buffer = b''
                while True:
                    data = client_socket.recv(4096)
                    if data:
                        file_buffer += data
                    else:
                        break
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                client_socket.send(message.encode())
            elif self.args.command:
                cmd_buffer = b''
                while True:
                    client_socket.send(b'RH: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
        except Exception as e:
            print(f"Server killed: {e}")
            self.socket.close()
            sys.exit()






'''
This is where the code starts in main():
'''
if __name__ == '__main__':
     
     # the program starts with calling the ArgumentParser object in the 'argparse' module which initalizez the parsing module giving it a description called 'BHP Net Tool', It points towards a class or 'formatter_class' which is a method as well in the argparse module called RawDescriptionHelpFormatter that works with the layout of the text and at last the epilog is for adding extra text
     
     parser = argparse.ArgumentParser(description = 'BHP Net Tool', formatter_class = argparse.RawDescriptionHelpFormatter, epilog = textwrap.dedent(('''---''')))
     
     ''' -------------------------
     Adding arguments to the parser object Created above'''
     
     parser.add_argument('-c', '--command', action='store_true', help='--listen')
     
     parser.add_argument('-e', '--execute', help='execute specified command')
     
     parser.add_argument('-l', '--listen', help = 'listen', action='store_true' )
     
     parser.add_argument('-p', '--port', help = 'specified port',type = int, default= 5555 )
      
     parser.add_argument('-t', '--target', help = 'specified IP', default='127.0.0.1' )
       
     parser.add_argument('-u', '--upload', help = 'upload file')
     
     '''------------------
     parsing the arguments given above into the parser by calling in parse_args() to the parser variable holding the parser and then pushes it into the variable called args'''
     
     args = parser.parse_args()
     
     
     #listens to the input by the user
     
     if args.listen:
          buffer = ''
     else:
          #takes user input
          buffer = sys.stdin.read()
     

     #takes the input inside the 'buffer variable and also 'args' variable which consist of parsed arguments into the class Netcat
     
     nc = NetCat(args, buffer.encode())    
     
     nc.run()
     