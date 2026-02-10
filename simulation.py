

class Boules:
    def __init__(self, x, y, angle, eyes_list, pilot):
        self.x = x
        self.y = y
        self.angle =angle
        self.eye_list = eyes_list
        self.pilot = pilot
        self.radius = 10
        self.healt = 3

    def move(self, x_move, y_move, angle):
        self.x += x_move
        self.y += y_move
        self.angle += angle
    
class board:
    def __init__(self):
        self.boules = []
        self.spikes = []
        self.wall = []