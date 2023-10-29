class Map:
    def __init__(self, level_data, facing_angle_dict):
        self.level_data = level_data
        self.facing_angle_dict = facing_angle_dict
        self.tile_size = 48


def setup_maps():
    level_data_1 = [
        'X X X X X X X X X X X X X',
        'X           X           X',
        'X           X           X',
        'X     3             2   X',
        'X                       X',
        'X           X           X',
        'X X X     X X X     X X X',
        'X           X           X',
        'X                       X',
        'X                       X',
        'X     1     X       4   X',
        'X           X           X',
        'X X X X X X X X X X X X X']
    facing_angle_dict_1 = {1: 0, 2: 180, 3: 0, 4: 180}
    map_1 = Map(level_data_1, facing_angle_dict_1)

    level_data_2 = [
        'X X X X X X X X X X X X X',
        'X           X           X',
        'X         X X X         X',
        'X     3   X         2   X',
        'X                       X',
        'X   X             X X   X',
        'X X X       X       X X X',
        'X   X X             X   X',
        'X                       X',
        'X             X         X',
        'X     1   X X X     4   X',
        'X           X           X',
        'X X X X X X X X X X X X X']
    facing_angle_dict_2 = {1: 0, 2: 180, 3: 0, 4: 180}
    map_2 = Map(level_data_2, facing_angle_dict_2)

    level_data_3 = [
        'X X X X X X X X X X X X X',
        'X                       X',
        'X   X X           X X   X',
        'X   X       X       X   X',
        'X       3   X     2     X',
        'X                       X',
        'X     X X   X   X X     X',
        'X                       X',
        'X           X           X',
        'X   X   1   X     4 X   X',
        'X   X X           X X   X',
        'X                       X',
        'X X X X X X X X X X X X X']
    facing_angle_dict_3 = {1: 0, 2: 180, 3: 0, 4: 180}
    map_3 = Map(level_data_3, facing_angle_dict_3)

    level_data_4 = [
        'X X X X X X X X X X X X X',
        'X                       X',
        'X       X       X   2   X',
        'X     X X       X X     X',
        'X                       X',
        'X   3       X     X X X X',
        'X     X     X     X     X',
        'X     X                 X',
        'X X X X             4   X',
        'X     X     X     X     X',
        'X   1       X X X X     X',
        'X                       X',
        'X X X X X X X X X X X X X']
    facing_angle_dict_4 = {1: 0, 2: 180, 3: 0, 4: 180}
    map_4 = Map(level_data_4, facing_angle_dict_4)

    level_data_5 = [
        'X X X X X X X X X X X X X',
        'X                       X',
        'X   3 X X X     X X   2 X',
        'X     X           X   X X',
        'X X   X           X     X',
        'X           X           X',
        'X           X           X',
        'X     X X X X     X     X',
        'X   X X           X     X',
        'X     X           X X   X',
        'X   1 X     X X X X     X',
        'X     X               4 X',
        'X X X X X X X X X X X X X']
    facing_angle_dict_5 = {1: 0, 2: 180, 3: 0, 4: 180}
    map_5 = Map(level_data_5, facing_angle_dict_5)

    map_dict = {1: map_1, 2: map_2, 3: map_3, 4: map_4, 5: map_5}
    return map_dict


map_dict = setup_maps()
