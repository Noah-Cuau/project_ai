

class Boule:
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
    

class Spike:
    def __init__(self, x, y, pilot):
        self.x = x
        self.y = y
        self.pilot = pilot

    def move(self):
        self.pilot.move(self)



class Spike_Pilot:
    def __init__(self, board_w, board_h):
            self.board_w = board_w
            self.board_h = board_h
            self.up = 1
            self.right = 1
    
    def move(self, spike):
        if (self.up == 1):
            if spike.y+1 > self.board_h:
                self.up = -1
        elif spike.y-1 <0:
                self.up =1

        if (self.right == 1):
            if spike.x+1 > self.board_w:
                self.right = -1
        elif spike.x-1 <0:
                self.right =1

        spike.x += self.right
        spike.y += self.up

      
        



