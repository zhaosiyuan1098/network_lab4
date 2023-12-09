import json
import socket
import threading
import sys

class CommunicateClient:
    def __init__(self, my_host, my_port, sock=socket.socket(socket.AF_INET6, socket.SOCK_DGRAM),server_ip="localhost", server_port=20000):
        self.my_host = my_host
        self.my_port = my_port
        self.socket = sock
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = None
        self.destination_name = None
        
    def login(self):
        username=str(input("please input the username:\n"))
        
        password=str(input("please input the password:\n"))
        message_send_str = {"operate": "login", "username": username, "password": password}
        message_send_json = json.dumps(message_send_str)
        self.socket.sendto(message_send_json.encode(), (self.server_ip, self.server_port))
        message_recv_str = self.socket.recvfrom(1024)
        message_recv_json = json.loads(message_recv_str[0].decode())
        if message_recv_json["state"] == "success":
            self.username = username
            print("login success")
            return username
        else:
            return None
    
    def register(self):

        username=str(input("please input the username:\n"))
        password=str(input("please input the password:\n"))
        
        message_send_str = {"operate": "register", "username": username, "password": password}
        message_send_json = json.dumps(message_send_str)
        self.socket.sendto(message_send_json.encode(), (self.server_ip, self.server_port))
        message_recv_str = self.socket.recvfrom(1024)
        message_recv_json = json.loads(message_recv_str[0].decode())
        if message_recv_json["state"] == "success":
            self.username = username
            print("register success")
            return username
        else:
            return None


    def get_destinasion_name(self):
        destination_name = input("please input the destination username:\n")
        self.destination_name = destination_name
        
    def send(self):
        if self.username is None:
            print("please login or register first")
            return None
        if self.destination_name is None:
            print("please input the destination username first")
            return None
        message=input("send to "+self.destination_name+":")
        if message != "END" and message != None:
            message_send_str = {"operate": "p2p", "my_username": self.username,
                                "dest_username": self.destination_name, "content": message}
            message_send_json = json.dumps(message_send_str)
            self.socket.sendto(message_send_json.encode(), (self.server_ip, self.server_port))
        elif message == "END":
            self.destination_name = None
            return self.get_destinasion_name()

    
    def receive(self):
        while True:
            message_recv_str = self.socket.recvfrom(1024)
            message_recv_json = json.loads(message_recv_str[0].decode())
            operate = str(message_recv_json["operate"])
            message=str(message_recv_json["content"])
            print("get from:"+str(message_recv_json["my_username"])+":"+message) 
    def close(self):
        self.socket.close()
        
def main():
    client = CommunicateClient("localhost", 20001)
    client.login()
    client.get_destinasion_name()
    
    #使用thread生成两个线程，一个用来收消息，一个用来发消息test
    t2 = threading.Thread(target=client.receive)

    t2.start()
    
    while True:
        client.send()


if __name__ == "__main__":
    main()
    


