from random import randint

GAME_LOBBY_STATUS = "host lobby"
GAME_IN_PROGRESS_STATUS = "in progress"

PLAYER_ALIVE_STATUS = "alive"

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


class ServerGame:
    def __init__(self, game_id, host):
        self.game_id = game_id
        self.invite_code = randint(100000, 1000000)
        self.map_id = 1
        self.rounds_number = 1
        self.current_round = 1

        self.is_full = False
        self.is_empty = False
        self.finished = False
        self.status = GAME_LOBBY_STATUS

        self.players_ip = {}
        self.players_dict = {}
        self.bullets_dict = {}

        self.add_player(host)

    def players_number(self):
        return len(self.players_ip)

    def has_started(self):
        return self.status != GAME_LOBBY_STATUS

    def start_game(self):
        self.status = GAME_IN_PROGRESS_STATUS

    def get_player_id(self, client):
        for player_id in self.players_ip.keys():
            if self.players_ip[player_id] == client:
                return player_id
        return None

    def add_player(self, client):
        for player_id in range(1, 5):
            if player_id not in self.players_ip.keys():
                self.players_ip[player_id] = client
                self.players_dict[player_id] = None
                self.bullets_dict[player_id] = None
                if len(self.players_ip) == 4:
                    self.is_full = True
                return player_id

    def remove_player(self, player_id):
        self.players_ip.pop(player_id, None)
        self.players_dict.pop(player_id, None)
        self.bullets_dict.pop(player_id, None)
        if len(self.players_ip) == 0:
            self.is_empty = True
        else:
            self.is_full = False

    def update_host_menu(self, map_id, rounds_number):
        if map_id and rounds_number:
            self.map_id = map_id
            self.rounds_number = rounds_number
        return self.status, self.players_dict, self.map_id, self.rounds_number

    def reset(self):
        self.status = GAME_LOBBY_STATUS
        for player_id in self.players_ip.keys():
            self.players_dict[player_id] = None
            self.bullets_dict[player_id] = None

    def update_game(self, data):
        player, bullets = data
        player_id = player.player_id

        if player.status == PLAYER_ALIVE_STATUS:
            self.players_dict[player_id] = player
            self.bullets_dict[player_id] = bullets
        else:
            self.players_dict.pop(player_id, None)
            self.bullets_dict.pop(player_id, None)

        other_players_dict = {other_player_id: other_player for other_player_id, other_player in self.players_dict.items() if other_player_id != player_id}
        other_bullets_dict = {other_player_id: other_bullets for other_player_id, other_bullets in self.bullets_dict.items() if other_player_id != player_id}

        if len(self.players_dict) == 1 and not self.finished:
            if self.current_round == self.rounds_number:
                self.reset()
            else:
                self.current_round += 1
                self.finished = True
        if len(self.players_dict) > 1:
            self.finished = False
        return self.status, other_players_dict, other_bullets_dict

    def __del__(self):
        pass
