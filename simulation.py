from pygame import math
import random

class Circle:
    def __init__(self, x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def get_center_x(self):
        return self.x
    
    def get_center_y(self):
        return self.y
     
    def get_radius(self):
        return self.radius

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

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_angle(self):
        return self.angle
    
    def get_radius(self):
        return self.radius
    
    

class Eye:
    def __init__(self, lenght, angle):
        self.lenght =lenght
        self.angle = angle
    


class Spike:
    def __init__(self, x, y, pilot):
        self.x = x
        self.y = y
        self.pilot = pilot
        self.radius =10

    def move(self):
        self.pilot.move(self)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_radius(self):
        return self.radius



class Spike_Pilot:
    def __init__(self, board_w, board_h):
            self.board_w = board_w
            self.board_h = board_h
            self.up = 1
            self.right = 1
    
    def move(self, spike):
        if (self.up == 1):
            if spike.y + spike.radius +1 > self.board_h:
                self.up = -1
        elif spike.y-1 <0:
                self.up =1

        if (self.right == 1):
            if spike.x+ spike.radius+1 > self.board_w:
                self.right = -1
        elif spike.x-1 <0:
                self.right =1

        spike.x += self.right
        spike.y += self.up

class Board:
    def __init__(self, width, height):
        self.boules = []
        self.spikes = []
        self.width = width
        self.height = height

    def run(self):
        for spike in self.spikes:
             spike.move()

    def add_spike(self, spike):
        self.spikes.append(spike)

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height



def create_sim_test(width, height, nombre):
    new_b = Board(width,height)
<<<<<<< HEAD
    for i in range(10000):
=======
    if nombre < 1:
        nombre = 1
    for i in range(nombre):
>>>>>>> 6e727921703df71659160480cff6ede56fa47b50
        new_pilot = Spike_Pilot(width,height)
        new_spike = Spike(random.randint(0,width), random.randint(0,height), new_pilot)
        new_spike.pilot.up = random.choice([-1,1])
        new_spike.pilot.right = random.choice([-1,1])
        new_b.add_spike(new_spike)
    return new_b

if __name__ == "__main__":
    b = create_sim_test(1000,1000)
    for i in range(1000):
        b.run()
        for s in b.spikes:
            if (s.x >1000) or (s.y >1000) or s.y<0 or s.x <0:
                print("error at frame "+str(i))
        
    
    
     
    
        


        



