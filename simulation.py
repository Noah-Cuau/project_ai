import pygame
from math import sqrt
import random

def point_in_circle(point, radius_circle, center_circle):
    return euclidien_dist(point, center_circle)< radius_circle

def euclidien_dist(p1,p2):
    x_dist = p2[0] - p1[0]
    y_dist = p2[1] -p1[1]
    return sqrt(x_dist**2+y_dist**2)

def collide_circle(c1_center, c1_radius, c2_center, c2_radius):
    return euclidien_dist(c1_center,c2_center) <c1_radius+c2_radius
    

class Boule:
    def __init__(self, x, y, angle, pilot):
        self.x = x
        self.y = y
        self.angle =angle
        
        self.pilot = pilot
        self.radius = 10
        self.health = 3
        self.dead = False

    def set_eyes(self,eyes_list):
        self.eyes = eyes_list

    def move(self):
        if self.pilot == False:
            pass
        else:
            self.pilot.move(self)
       
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_angle(self):
        return self.angle
    
    def get_radius(self):
        return self.radius
    
    def get_eyes(self):
        return self.eyes
    def collide_spike(self, spike):
        return collide_circle((self.x,self.y), self.radius, (spike.x,spike.y), spike.radius)
    
    def kill(self):
        self.dead = True

    def is_dead(self):
        return self.dead
    
    

class Eye:
    def __init__(self, lenght, angle,parent_boule):
        self.lenght =lenght
        self.angle = angle
        self.boule = parent_boule
    def get_vect(self):
        return pygame.math.Vector2.from_polar((self.lenght,self.angle+self.boule.angle))
    def get_end_sight(self):
        vect = self.get_vect()
        return (self.boule.x+vect[0], self.boule.y+vect[1])
    
   
    
    def see_for_spike(self, spike):
        vect = self.get_vect
        point = [self.boule.x, self.boule.y]
        for i in range(self.lenght):
            if point_in_circle(point, spike.radius, (spike.x, spike.y)):
                return i/self.lenght
        return 1


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

class Food:
    def __init__(self, x, y , eaten):
         self.x = x
         self.y = y
         self.eaten = eaten
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_eaten(self):
        return self.eaten
    def die(self):
        self.eaten = True

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
        self.foods = []
        self.width = width
        self.height = height

    def run(self):
        for spike in self.spikes:
            spike.move()
            for boule in self.boules:
                if boule.is_dead()==False:
                    if boule.collide_spike(spike):
                        boule.kill()
        
        for boule in self.boules:
            if boule.is_dead()==False:
                boule.move()
            

    def add_spike(self, spike):
        self.spikes.append(spike)

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    def add_food(self, food):
        self.foods.append(food)

    def add_boule(self, boule):
        self.boules.append(boule)

def even_spaced_eyes(nb_eyes,lenght,boule):
    new_list = []
    for i in range(nb_eyes):
        new_list.append(Eye(lenght,i*(360/nb_eyes),boule))
    return new_list


def create_sim_test(width, height, nombre_spikes, nombre_foods, nombre_boule):
    new_b = Board(width,height)
    for i in range(nombre_spikes):
        new_pilot = Spike_Pilot(width,height)
        new_spike = Spike(random.randint(15,width-15), random.randint(15,height-15), new_pilot)
        new_spike.pilot.up = random.choice([-1,1])
        new_spike.pilot.right = random.choice([-1,1])
        new_b.add_spike(new_spike)
    for i in range(nombre_foods):
        new_food = Food(random.randint(0,width),random.randint(0,height),False)
        new_b.add_food(new_food)
    
    for i in range(nombre_boule):
        new_boule = Boule(random.randint(0, width), random.randint(0,height), 0, Spike_Pilot(width,height))
        new_b.add_boule(new_boule)

        new_eyes = even_spaced_eyes(6, 35,new_b.boules[i])
        new_boule.set_eyes(new_eyes)



        

    return new_b

if __name__ == "__main__":
    b = create_sim_test(1000,1000)
    for i in range(1000):
        b.run()
        for s in b.spikes:
            if (s.x >1000) or (s.y >1000) or s.y<0 or s.x <0:
                print("error at frame "+str(i))
        
    
    
     
    
        


        



