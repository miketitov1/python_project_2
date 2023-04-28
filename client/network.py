import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5050
        self.server_ip = "172.22.240.1"
        self.address = (self.server_ip, self.port)
        self.message_size = 2048
        self.disconnect_message = "!DISCONNECT"
        self.format = "utf-8"

        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.is_connected = False

    def connect(self):
        self.client.connect(self.address)
        self.is_connected = True


    def receive_data(self):
        data = self.client.recv(self.message_size)
        if data:
            data = pickle.loads(data)
            return data
        else:
            return None

    def send_data(self, data):
        try:
            data = pickle.dumps(data)
            self.client.send(data)
        except socket.error as error:
            print(str(error))

    def __del__(self):
        try:
            self.send_data(self.disconnect_message)
        except socket.error as error:
            print(str(error))


network = Network()
