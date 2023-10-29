import socket
import pickle

from network_settings import *


class Message:
    def __init__(self, status, content):
        self.status = status
        self.content = content

class ServerPlayer:
    def __init__(self, player_id, pos, facing_angle, status):
        self.player_id = player_id
        self.pos = pos
        self.facing_angle = facing_angle
        self.status = status


class ServerBullet:
    def __init__(self, player_id, pos, direction):
        self.player_id = player_id
        self.pos = pos
        self.direction = direction



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = PORT
        self.server_ip = SERVER_IP
        self.address = (self.server_ip, self.port)
        self.message_size = MESSAGE_SIZE
        self.disconnect_message = DISCONNECT_MESSAGE

        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.connected = False

    def connect(self):
        if not self.connected:
            self.client.connect(self.address)
            self.connected = True

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
        if self.connected:
            try:
                self.send_data(self.disconnect_message)
            except socket.error as error:
                print(str(error))


network = Network()
