from game.shared.bomber_constants import *
import game.shared.bombermap as bombermap
import game.scripting.explosion as explosion

class Bomb:
    def __init__(self, power, position, player):
        self.power = power
        self.position = position
        self.timeleft = 2000
        self.player = player

    def update(self, timelapsed):
        self.timeleft -= timelapsed
        if self.timeleft < 0:
            self.explode()

    def explode(self):
        self.remove()
        explosions.add(explosion.Explosion(self.power, self.position))
        self.player.recharge_bomb()

    def remove(self):
        bombs.discard(self)
        if(bombermap.get_object(self.position) == self):
            bombermap.set_object(self.position, None)
