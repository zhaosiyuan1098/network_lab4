import json
import socket
from User import User

class CommunicateServer:
    def __init__(self, sock=socket.socket(socket.AF_INET6)):
        self.socket = sock

    def serve(self):
        while True:
            data = self.socket.recvfrom(1024)
            print(data)
            message = json.loads(data[0].decode())
            ip = data[1][0]
            port = data[1][1]

            if message["operate"] == "login":
                print("login was called")
                state = User().login_check(message["username"], message["password"], ip, port)
                if state:
                    self.socket.sendto(json.dumps({"operate": "login", "state": "success"}).encode(), (ip, port))
                else:
                    self.socket.sendto(json.dumps({"operate": "login", "state": "fail"}).encode(), (ip, port))

            elif message["operate"] == "register":
                print("register was called")
                state = User().register(message["username"], message["password"], ip, port)
                if state:
                    self.socket.sendto(json.dumps({"operate": "register", "state": "success"}).encode(), (ip, port))

            elif message["operate"] == "p2p":
                print("p2p was called")
                user = User().search_username(message["dest_username"])
                dest_ip = user[3]
                dest_port = user[4]
                if user[2] == 1:
                    self.socket.sendto(json.dumps(message).encode(), (dest_ip, dest_port))
                    print("send success")
                else:
                    self.socket.sendto("user is not online or exits".encode(), (ip, port))
                    print("error, send success")

            elif message["operate"] == "p2g":
                print("p2g was called")
                for row in User().select_all():
                    if row[0] != message["my_username"] and row[2]:
                        self.socket.sendto(json.dumps(message).encode(), (row[3], row[4]))
                        

def main():
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind(("localhost", 20000))
    communicate_server=CommunicateServer(sock)
    print("sock setup success")
    communicate_server.serve()


if __name__ == '__main__':
    user = User()
    main()