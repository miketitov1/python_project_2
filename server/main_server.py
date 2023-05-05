import socket
import threading
import pickle
import sys

from server_game import ServerGame, Message
from server_settings import *

sys.path.append('../client')


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = PORT
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.address = (self.server_ip, self.port)
        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.bind_server()

        print("[STARTING]: Server is starting...")
        self.server.listen()
        print(f"[LISTENING]: Sever is listening on {self.server_ip}")

        self.games_dict = {}
        self.debug_mode = False

    def bind_server(self):
        try:
            self.server.bind(self.address)
        except socket.error as error:
            print(str(error))

    @staticmethod
    def receive_data(client):
        data = client.recv(MESSAGE_SIZE)
        if data:
            data = pickle.loads(data)
            return data
        else:
            return None

    @staticmethod
    def send_data(client, data):
        try:
            data = pickle.dumps(data)
            client.send(data)
        except socket.error as error:
            print(str(error))

    def delete_game(self, game_id):
        self.games_dict.pop(game_id, None)
        print(f"[GAME DELETED]: Game {game_id} was deleted due to no players left in the lobby.")
        print(f"[ACTIVE GAMES]: {len(self.games_dict)}")

    def create_new_game(self, host):
        for key in range(1, 101):
            if key not in self.games_dict.keys():
                new_game_id = key
                self.games_dict[new_game_id] = ServerGame(new_game_id, host)
                invite_code = self.games_dict[new_game_id].invite_code
                return new_game_id, invite_code

    def handle_data(self, client, addr, data):
        if data.status == CREATE_GAME_MESSAGE:
            new_game_id, invite_code = self.create_new_game(client)
            print(f"[NEW GAME]: Player {addr} created new game {new_game_id} with invite code {invite_code}.")
            reply = Message(None, (new_game_id, invite_code))
            self.send_data(client, reply)

        elif data.status == UPDATE_HOST_MENU_MESSAGE:
            game_id, map_id, rounds_number = data.content
            game = self.games_dict[game_id]
            status, server_players_dict, new_map_id, new_rounds_number = game.update_host_menu(map_id, rounds_number)
            reply = Message(status, (server_players_dict, new_map_id, new_rounds_number))
            self.send_data(client, reply)

        elif data.status == JOIN_GAME_MESSAGE:
            game_id, invite_code = data.content
            print(f"[DEBUG]: Got game id {game_id}, invite code {invite_code}")
            if game_id not in self.games_dict.keys():
                reply = Message("wrong_game_id", None)
                self.send_data(client, reply)
            elif self.games_dict[game_id].has_started():
                reply = Message("game_already_started", None)
                self.send_data(client, reply)
            elif self.games_dict[game_id].is_full:
                reply = Message("game_is_full", None)
                self.send_data(client, reply)
            else:
                if invite_code != self.games_dict[game_id].invite_code:
                    reply = Message("wrong_game_id", None)
                    self.send_data(client, reply)
                else:
                    player_id = self.games_dict[game_id].add_player(client)
                    reply = Message(None, player_id)
                    self.send_data(client, reply)
                    print(f"[PLAYER JOINED]: Player {addr} joined game {game_id}.")

        elif data.status == START_GAME_MESSAGE:
            game_id = data.content
            self.games_dict[game_id].start(addr)

        elif data.status == UPDATE_GAME_MESSAGE:
            content = data.content
            if self.debug_mode:
                print(f"[RECEIVED] From player {addr} received data {content}")
            game_id = content[0]
            game_data = content[1]
            status, server_players_dict, server_bullets_dict = self.games_dict[game_id].update_game(game_data)
            reply = Message(status, (server_players_dict, server_bullets_dict))
            self.send_data(client, reply)
            if self.debug_mode:
                print(f"[SENT] Sent reply {reply.content} to player {addr}")

        elif data.status == FINISH_GAME_MESSAGE:
            content = data.content
            game_id = content[0]
            game_data = content[1]
            status, server_players_dict, server_bullets_dict = self.games_dict[game_id].update_game(game_data)
            reply = Message(status, (server_players_dict, server_bullets_dict))
            self.send_data(client, reply)
            self.games_dict[game_id].finish()

        elif data.status == LEAVE_MESSAGE:
            game_id, player_id = data.content
            game = self.games_dict[game_id]
            game.remove_player(player_id)
            print(f"[PLAYER LEFT]: Player {addr} left the game {game.game_id}.")
            if self.games_dict[game_id].is_empty:
                self.delete_game(game_id)

    def safe_disconnect(self, client, addr):
        for game_id, game in self.games_dict.items():
            player_id = game.get_player_id(client)
            if player_id:
                game.remove_player(player_id)
                print(f"[PLAYER LEFT]: Player {addr} left the game {game_id}.")
                if game.is_empty:
                    self.delete_game(game_id)
                break

    def handle_client(self, client, addr):
        print(f"[NEW CONNECTION]: Player {addr} connected.")
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")

        while True:
            try:
                message = self.receive_data(client)
                if message:
                    if message == DISCONNECT_MESSAGE:
                        break
                    else:
                        self.handle_data(client, addr, message)
            except socket.error as error:
                print(f"[ERROR]: {error} {addr} connection lost.")
                break

        self.safe_disconnect(client, addr)

        client.close()
        print(f"[PLAYER DISCONNECTED]: Player {addr} disconnected.")
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 2}")

    def run(self):
        while True:
            new_socket, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(new_socket, addr))
            thread.start()

    def __del__(self):
        print("[STOPPING]: Server is stopping.")
        print(f"[PLAYERS DISCONNECTED]: Players were disconnected.")
        print(f"[GAMES FINISHED]: Games were finished.")
        print("[STOPPED]: Server was stopped.")


server = Server()
server.run()
