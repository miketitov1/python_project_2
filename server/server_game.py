class Message:
    def __init__(self, status, content):
        self.status = status
        self.content = content


class ServerGame:
    def __init__(self, game_id, host):
        self.is_full = False
        self.is_empty = False
        self.status = "host_lobby"
        self.game_id = game_id
        self.players_ip = {}
        self.players_dict = {}
        self.bullets_dict = {}

        self.add_new_player(host)

    def players_number(self):
        return len(self.players_ip)

    def has_started(self):
        return self.status == "started"

    def start_game(self):
        self.status = "started"

    def add_new_player(self, client):
        for player_id in range(0, 4):
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

    def update_host_menu(self):
        return self.status, self.players_dict

    def update_game(self, data):
        player, bullets = data
        player_id = player.player_id
        self.players_dict[player_id] = player
        self.bullets_dict[player_id] = bullets
        print(self.players_dict, '\n', self.bullets_dict)
        return self.status, self.players_dict, self.bullets_dict


class ServerPlayer:
    def __init__(self, player_id, pos, facing_angle):
        self.player_id = player_id
        self.pos = pos
        self.facing_angle = facing_angle


class ServerBullet:
    def __init__(self, player_id, pos, direction):
        self.player_id = player_id
        self.pos = pos
        self.direction = direction
