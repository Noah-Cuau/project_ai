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
    def __init__(self, x, y, angle, ):
        self.x = x
        self.y = y
        self.angle =angle
        self.pilot = False
        self.radius = 10
        self.health = 3
        self.energy = 600
        self.dead = False
        self.immortal = False

    def set_eyes(self,eyes_list):
        self.eyes = eyes_list

    def move(self):
        if self.pilot !=False:
            x,y,rot = self.pilot.get_move()
            self.input_movement(x,y,rot)
       
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_pilot(self, pilot):
        self.pilot = pilot
    
    def get_angle(self):
        return self.angle
    
    def get_radius(self):
        return self.radius
    def get_energy(self):
        return self.energy
    def eat(self):
        self.energy += 300
    
    def get_eyes(self):
        return self.eyes
    def collide_spike(self, spike):
        return collide_circle((self.x,self.y), self.radius, (spike.x,spike.y), spike.radius)
    def collide_food(self, food):
        return collide_circle((self.x, self.y), self.radius, (food.x,food.y),food.radius)
    def kill(self):
        self.dead = True

    def is_dead(self):
        return self.dead
    
    def input_movement(self, x_channel, y_channel, rot_channel):
        self.x += x_channel
        self.y +=y_channel
        self.angle +=rot_channel

    def make_immortal(self):
        self.immortal = True

    def starve(self):
        if not self.immortal:
            self.energy -=1
    
    

class Eye:
    def __init__(self, lenght, angle,parent_boule):
        self.lenght =lenght
        self.angle = angle
        self.boule = parent_boule
        self.saw_spike = False
    def get_vect(self):
        return pygame.math.Vector2.from_polar((self.lenght,self.angle+self.boule.angle))
    def get_end_sight(self):
        vect = self.get_vect()
        return (self.boule.x+vect[0], self.boule.y+vect[1])
    
   
    
    def see_for_spike(self, spike):
        vect = self.get_vect()
        point = [self.boule.x, self.boule.y]
        for i in range(self.lenght):
            if point_in_circle(point, spike.radius, (spike.x, spike.y)):
                return i/self.lenght
            point[0]+=vect.x
            point[1]+=vect.y
        return 1


class Spike:
    def __init__(self, x, y, pilot):
        self.x = x
        self.y = y
        self.pilot = pilot
        self.radius =10

    def move(self):
        if self.pilot != False:
            self.pilot.move(self)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_radius(self):
        return self.radius
    
    def set_pilot(self,pilot):
        self.pilot = pilot

class Food:
    def __init__(self, x, y):
         self.x = x
         self.y = y
         self.radius = 10
         self.eaten = False
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_eaten(self):
        return self.eaten
    def get_radius(self):
        return self.radius
    def die(self):
        self.eaten = True

class Default_spike_pilot:
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

class Default_boule_pilot:
    def __init__(self,boule, board_w,board_h):
        self.boule =boule
        self.board_w = board_w
        self.board_h = board_h
        self.up = random.choice([-1, 1])
        self.right = random.choice([-1, 1])

    
    def get_move(self):
        if (self.up == 1):
            if self.boule.y + self.boule.radius +1 > self.board_h:
                self.up = -1
        elif self.boule.y-1 <0:
                self.up =1

        if (self.right == 1):
            if self.boule.x+ self.boule.radius+1 > self.board_w:
                self.right = -1
        elif self.boule.x-1 <0:
                self.right =1
        
        return self.right, self.up,0


         

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
    
                    for food in self.foods:
                        if food.get_eaten()==False:
                            if boule.collide_food(food):
                                food.die()
                                boule.eat()
                            if boule.energy == 0:
                                boule.kill()
                            if boule.collide_spike(spike):
                                    boule.kill()
                    for eye in boule.get_eyes():
                        print(eye.see_for_spike(spike))
                        if eye.see_for_spike(spike)==1:
                            eye.saw_spike = False
                        else:
                            eye.saw_spike = True
        
        for boule in self.boules:
            boule.starve()
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

    def get_boules(self):
        return self.boules
    
    def get_spikes(self):
        return self.spikes

def even_spaced_eyes(nb_eyes,lenght,boule):
    new_list = []
    for i in range(nb_eyes):
        new_list.append(Eye(lenght,i*(360/nb_eyes),boule))
    return new_list


def create_sim_test(width, height, nombre_spikes, nombre_foods, nombre_boule):
    new_b = Board(width,height)
    for i in range(nombre_spikes):
        new_pilot = Default_spike_pilot(width,height)
        new_spike = Spike(random.randint(15,width-15), random.randint(15,height-15), new_pilot)
        new_spike.pilot.up = random.choice([-1,1])
        new_spike.pilot.right = random.choice([-1,1])
        new_b.add_spike(new_spike)
    for i in range(nombre_foods):
        new_food = Food(random.randint(0,width),random.randint(0,height))
        new_b.add_food(new_food)
    
    for i in range(nombre_boule):
        new_boule = Boule(random.randint(0, width), random.randint(0,height), 0)
        new_boule.set_pilot(Default_boule_pilot(new_boule, width, height))
        new_b.add_boule(new_boule)

        new_eyes = even_spaced_eyes(1, 35,new_b.boules[i])
        new_boule.set_eyes(new_eyes)



        

    return new_b

if __name__ == "__main__":
    b = create_sim_test(1000,1000)
    for i in range(1000):
        b.run()
        for s in b.spikes:
            if (s.x >1000) or (s.y >1000) or s.y<0 or s.x <0:
                print("error at frame "+str(i))
        
    
    
     
    
        


        



