map_1 = [
    'X X X X X X X X X X X X X',
    'X           X           X',
    'X   2       X       1   X',
    'X                       X',
    'X                       X',
    'X           X           X',
    'X X X     X X X     X X X',
    'X           X           X',
    'X                       X',
    'X                       X',
    'X   0       X       3   X',
    'X           X           X',
    'X X X X X X X X X X X X X']

TILE_SIZE = 48
SCREEN_WIDTH = len(map_1) * TILE_SIZE
SCREEN_HEIGHT = len(map_1) * TILE_SIZE

FACING_ANGLE_DICT = {0: 0, 1: 180, 2: 0, 3: 180}

#print(len(map_1), map_1[0].count("X"))
