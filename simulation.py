

class Boule:
    def __init__(self, x, y, angle, eyes_list, pilot):
        self.x = x
        self.y = y
        self.angle =angle
        self.eye_list = eyes_list
        self.pilot = pilot
        self.radius = 10
        self.health = 3

    def move(self, x_move, y_move, angle):
        self.x += x_move
        self.y += y_move
        self.angle += angle
    

    

class Spike:
    def __init__(self, x, y, pilot):
        self.x = x
        self.y = y
        self.pilot = pilot
        self.radius =10

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

class Board:
    def __init__(self, width, height):
        self.boules = []
        self.spikes = []

    def run(self):
        for spike in self.spikes:
             spike.move()

    def add_spike(self, spike):
        self.spikes.append(spike)



def create_sim_test(width, height):
    new_b = Board(width,height)
    for i in range(10):
        new_pilot = Spike_Pilot(width,height)
        new_spike = Spike(10*i, 10*i,new_pilot)
        new_b.add_spike(new_spike)
    return new_b

if __name__ == "__main__":
    b = create_sim_test(1000,1000)
    for i in range(1000):
        b.run()
        for s in b.spikes:
            if (s.x >1000) or (s.y >1000) or s.y<0 or s.x <0:
                print("error at frame "+str(i))
        
    
    
     
    
        


        



