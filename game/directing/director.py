import sys
import os

if len(sys.argv)>=1 and sys.argv[0] and os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

import pygame
import random #for AI

from game.shared.bomber_constants import *
from game.casting.player import *
from game.shared.bombermap import *
from game.shared.drawstuff import *
from game.shared.menu import *

pygame.init()

class Director:

    def __init__(self):
        self.data = []
    
    def init_normal_game(self, params):

        num_humans = params.get('num_humans', 1)
        num_computers = params.get('num_computers', 1)

        start_positions = [[1,1], [13,11], [13,1], [1,11]]

        all_humans.clear()
        all_computers.clear()
        for i, pos in enumerate(start_positions):
            if num_humans > 0:
                all_humans.add(Player(pos, num=i))
                num_humans -= 1
            elif num_computers > 0:
                all_computers.add(Player(pos, num=i * -1, isComputer=True))
                num_computers -=1

    def reset_game(self):
        global bombs, explosions, powerups, humans

        humans.clear()
        for p in all_humans:
            p.reset()
            humans.add(p)

        computers.clear()
        for p in all_computers:
            p.reset()
            computers.add(p)

        bombs.clear()
        explosions.clear()
        powerups.clear()

        for x in range(mapW):
            for y in range(mapH):
                map[x][y] = Block(startmap[x][y].btype)
                map_objects[x][y] = None


    def handle_input(self, key, keydown=False):
        if key == None:
            return

        if key == pygame.constants.K_SPACE:
            self.reset_game()

        for h in humans.copy():
            if not h.alive:
                continue

            x = keys[h.num].get(key, None)
            if x == "bomb":
                h.drop_bomb()
            elif x != None:
                if keydown:
                    h.player_move_delay = 0
                    h.move(x)
                    h.player_move_delay = repeat_key_wait
                else:
                    h.move(x)


    def do_AI(self,p):
        if p.repeat_move_delay > 0:
            return

        possible = []
        max_effect = -10000

        for (axis, inc) in ([0, -1], [0, 1], [1, -1], [1, 1]):
            pos = list(p.position)
            pos[axis] += inc
            if not is_valid_position(pos):
                continue

            b = get_block(pos)
            if b.is_destroyable() and not isinstance(get_object(p.position), Bomb):
                p.drop_bomb()
            if b.is_walkable() and \
                not isinstance(get_object(pos), explosion.Explosion) and \
                not isinstance(get_object(pos), Bomb):
                effect = bomb_effects[pos[0]][pos[1]]
                if(possible == [] or effect > max_effect):
                    max_effect = effect
                    possible = [pos]
                elif effect == max_effect:
                    possible.append(pos)

        #check effect at current position
        effect = bomb_effects[p.position[0]][p.position[1]]
        if effect > max_effect:
            return  # DON'T MOVE!
        elif effect == max_effect:
            possible.append(p.position)

        if possible != []:
            p.change_position(random.choice(possible))


    def update_computers(self, t):
        for p in computers.copy():
            p.update(t)
            self.do_AI(p)

    def update_bomb_effects(self, bomb):
        for (axis, increment) in [[0, -1], [0, 1], [1, -1], [1, 1]]:
            p = list(bomb.position)
            for i in range(bomb.power, 0, -1):
                p[axis] += increment
                if not is_valid_position(p):
                    break
                elif can_explosion_pass(p):
                    bomb_effects[p[0]][p[1]] -= i
                else:
                    break
        bomb_effects[bomb.position[0]][bomb.position[1]] -= bomb.power+1


    def update_bombs(self, t):
        for i in range(len(bomb_effects)):
            for j in  range(len(bomb_effects[0])):
                bomb_effects[i][j] = 0

        for bomb in bombs.copy():
            bomb.update(t)
            self.update_bomb_effects(bomb)


    def update_explosions(self, t):
        for e in explosions.copy():
            e.update(t)

    def update_humans(self, t):
        for p in humans.copy():
            p.update(t)

    def update_stuff(self, t):
        self.update_bombs(t)
        self.update_explosions(t)
        self.update_humans(t)
        self.update_computers(t)

    def is_game_over(self):
        return len(computers)+len(humans)<=1

    def main_loop(self):
        draw_stuff()
        while True:
            tickFPS = Clock.tick(fps)
            pressed = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    pressed.append(event.key)

            for key in pressed:
                if key==pygame.K_ESCAPE:
                    return #to menu
                else:
                    self.handle_input(key, keydown=True)

            all_pressed = pygame.key.get_pressed()
            for key in direction_keys:
                if all_pressed[key] and pressed != key:
                    self.handle_input(key)

            self.update_stuff(tickFPS)
            draw_stuff(game_over=self.is_game_over())


    def start_game(self):
        while True:
            game_params = game_menu()
            if 'quit' in game_params:
                break

            self.init_normal_game(game_params)
            self.reset_game()
            self.main_loop()
            self.reset_game()

        sys.exit(0)
