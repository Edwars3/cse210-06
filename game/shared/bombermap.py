from game.shared.bomber_constants import *
from game.scripting.powerup import *
import game.scripting.explosion as explosion
import copy

class Direction:
    up, down, left, right = range(4)

class BlockType:
    blank, wall, brick = range(3)

class PowerupType:
    extraBomb, speed, bombPower = range(3)

class Block:
    def __init__(self, btype=BlockType.blank, powerup=None, bomb = False):
        self.btype = btype
    def is_walkable(self):
        return self.btype != BlockType.wall and self.btype != BlockType.brick
    def is_destroyable(self):
        return self.btype == BlockType.brick
    def is_bomb_passable(self):
        return self.btype == BlockType.blank

    def destroy(self):
        if self.is_destroyable():
            self.btype = BlockType.blank
            return True
        else:
            return False


read_map_from_file = True

if read_map_from_file:
    textfile = open("game/shared/map.txt", "rt")
    map = [[None for x in range(mapH)] for y in range(mapW)]
    startmap = [[None for x in range(mapH)] for y in range(mapW)]
    for i in range(mapH):
        line = textfile.readline()
        for j in range(mapW):
            map[j][i] = Block(map_key.get(line[j], BlockType.blank))
            startmap[j][i] = Block(map_key.get(line[j], BlockType.blank))

    textfile.close()

else:
    map = [[Block() for x in range(mapH)] for y in range(mapW)]
    startmap =    [[Block() for x in range(mapH)] for y in range(mapW)]
    map[2][2].btype = BlockType.wall

map_objects = [[None for x in range(mapH)] for y in range(mapW)]

bomb_effects = [[0 for x in range(mapH)] for y in range(mapW)]

def set_object(pos, obj):
    map_objects[pos[0]][pos[1]] = obj

def get_object(pos):
    return map_objects[pos[0]][pos[1]]

def get_block(pos):
    return map[pos[0]][pos[1]]

def get_player(position):
    players = humans.union(computers)
    for player in players:
        if player.position == position:
            return player
    return False

def can_move(p):
    if not get_block(p).is_walkable():
        return False
    obj = get_object(p)
    return not obj or isinstance(obj, Powerup) or isinstance(obj, explosion.Explosion)

def can_explosion_pass(p):
    return get_block(p).is_bomb_passable() and get_object(p) == None

def is_valid_position(p):
    return p[0] >= 0 and p[1] >= 0 and p[0] < mapW and p[1] < mapH

def adjacent_positions(pos):
    p = list(pos)
    for x in ([0,1], [0, -1], [1, 0], [-1, 0]):
        x[0] += p[0]
        x[1] += p[1]
        if(is_valid_position(x)):
            yield x
