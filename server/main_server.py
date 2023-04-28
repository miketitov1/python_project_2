import socket
import threading
import pickle

from server.server_game import ServerGame, Message



class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5050
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.address = (self.server_ip, self.port)
        self.message_size = 2048
        self.disconnect_message = "!DISCONNECT"
        self.format = "utf-8"

        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.bind_server()

        print("[STARTING]: Server is starting...")
        self.server.listen()
        print(f"[LISTENING]: Sever is listening on {self.server_ip}")

        self.games_dict = {}

    def bind_server(self):
        try:
            self.server.bind(self.address)
        except socket.error as error:
            print(str(error))

    def receive_data(self, client):
        data = client.recv(self.message_size)
        if data:
            data = pickle.loads(data)
            return data
        else:
            return None

    def send_data(self, client, data):
        try:
            data = pickle.dumps(data)
            client.send(data)
        except socket.error as error:
            print(str(error))

    def delete_game(self, game_id):
        self.games_dict.pop(game_id, None)

    def create_new_game(self, host):
        new_game_id = -1
        for key in range(0, 10000):
            if key not in self.games_dict.keys():
                new_game_id = key
                break
        self.games_dict[new_game_id] = ServerGame(new_game_id, host)
        return new_game_id

    def handle_data(self, client, addr, data):
        if data.status == "update_game":
            content = data.content
            print(f"[RECEIVED] From player {addr} received data {content}")
            game_id = content[0]
            game_data = content[1]
            status, server_players_dict, server_bullets_dict = self.games_dict[game_id].update_game(game_data)
            reply = Message(status, (server_players_dict, server_bullets_dict))
            self.send_data(client, reply)
            print(f"[SENT] Sent reply {reply.content} to player {addr}")

        elif data.status == "create_new_game":
            new_game_id = self.create_new_game(client)
            print(f"[NEW GAME]: Player {addr} created new game {new_game_id}.")
            reply = Message(None, new_game_id)
            self.send_data(client, reply)

        elif data.status == "leaving_game":
            game_id, player_id = data.content
            game = self.games_dict[game_id]
            game.remove_player(player_id)
            print(f"[PLAYER LEFT GAME]: Player {addr} left the game {game.game_id}.")
            if self.games_dict[game_id].players_number() == 0:
                print(f"[GAME DELETED]: Game {game_id} was deleted due to no players left in the lobby.")
                self.delete_game(game_id)

        elif data.status == "update_host_menu":
            game_id = data.content
            game = self.games_dict[game_id]
            status, server_players_dict = game.update_host_menu()
            reply = Message(status, server_players_dict)
            self.send_data(client, reply)

        elif data.status == "join_game":
            game_id = data.content
            if game_id not in self.games_dict.keys():
                reply = Message("wrong_game_id", None)
                self.send_data(client, reply)
            elif self.games_dict[game_id].is_full:
                reply = Message("game_is_full", None)
                self.send_data(client, reply)
            elif self.games_dict[game_id].has_started():
                reply = Message("game_already_started", None)
                self.send_data(client, reply)
            else:
                player_id = self.games_dict[game_id].add_new_player(client)
                reply = Message(None, player_id)
                self.send_data(client, reply)

        elif data.status == "start_game":
            game_id = data.content
            self.games_dict[game_id].start_game()
            print(f"[GAME STARTED]: Game {game_id} was started by player {addr}.")

    def handle_client(self, client, addr):
        print(f"[NEW CONNECTION]: {addr} connected.")
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")

        while True:
            try:
                message = self.receive_data(client)
                if message:
                    if message == self.disconnect_message:
                        break
                    else:
                        self.handle_data(client, addr, message)
            except socket.error as error:
                print(f"[ERROR]: {error} {addr} connection lost.")
                break

        print(f"[PLAYER DISCONNECTED]: {addr} disconnected.")
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 2}")
        client.close()

    def run(self):
        while True:
            new_socket, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(new_socket, addr))
            thread.start()


server = Server()
server.run()
