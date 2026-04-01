import pygame
from math import sqrt
import random
import torch
import numpy as np

TOLERANCE_MASK = 5
COLLISION_GRID_MARGIN = 80
def create_circle_mask(radius, tolerance):
    mask = []
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            r = (i ** 2) + (j ** 2)
            if radius**2-tolerance <r<radius**2+tolerance:
                mask.append((i,j))
    return mask
     
def widden_mask(mask):
    new_mask = []
    for vect in mask:
        new_mask.append(vect)
    for vect in mask:
        x = vect[0]
        y = vect[1]
        new_x = False
        new_y = False
        if x>0:
            new_x = x-1
        if x<0:
            new_x = x+1
        if y>0:
            new_y = y-1
        if y<0:
            new_y = y+1
        if new_x!=False and new_y!=False:
            new_mask.append((new_x, new_y))
        

def point_in_circle(point, radius_circle, center_circle):
    return euclidien_dist(point, center_circle)< radius_circle

def euclidien_dist(p1,p2):
    x_dist = p2[0] - p1[0]
    y_dist = p2[1] -p1[1]
    return sqrt(x_dist**2+y_dist**2)

def collide_circle(c1_center, c1_radius, c2_center, c2_radius):
    return euclidien_dist(c1_center,c2_center) <c1_radius+c2_radius
    
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
        vect = self.get_vect().normalize()
        point = [self.boule.x, self.boule.y]
        for i in range(self.lenght):
            if point_in_circle(point, spike.radius, (spike.x, spike.y)):
                return i/self.lenght
            point[0]+=vect.x
            point[1]+=vect.y
        return 1
    
    def see_for_food(self, food):
        vect = self.get_vect().normalize()
        point = [self.boule.x +COLLISION_GRID_MARGIN/2, self.boule.y+COLLISION_GRID_MARGIN/2]
        for i in range(self.lenght):
            if point_in_circle(point, food.radius, (food.x, food.y)):
                return i/self.lenght
            point[0]+=vect.x
            point[1]+=vect.y
        return 1
    
    def see_for_food2(self, collision_ref):
        vect = self.get_vect().normalize()
        intern_point = [
                self.boule.x +int(COLLISION_GRID_MARGIN/2), 
                self.boule.y+int(COLLISION_GRID_MARGIN/2)
        ]
        x = int(intern_point[0])
        y = int(intern_point[1])
        for i in range(self.lenght):
            if collision_ref[x][y]!=0:
                return i/self.lenght
            intern_point[0]+=vect.x
            intern_point[1]+=vect.y
            x = int(intern_point[0])
            y = int(intern_point[1])

        return 1

class Boule:
    def __init__(self, x, y, angle,board ):
        self.x = x
        self.y = y
        self.angle =angle
        self.pilot = False
        self.radius = 10
        self.health = 3
        self.energy = 600
        self.dead = False
        self.immortal = False
        self.food_eyes = []
        self.spike_eyes = []
        self.nb_food_eye = 0
        self.nb_spike_eye = 0
        self.saw_by_food_eyes = []
        self.saw_by_spike_eyes = []
        self.board : Board = board
        self.mask = create_circle_mask(self.radius,TOLERANCE_MASK)
        self.score = 0
        

    def set_eyes(self,eyes_list,eye_type):
        if eye_type == "spike":
            self.spike_eyes = eyes_list
            self.nb_spike_eye = len(self.spike_eyes)
            self.saw_by_spike_eyes = [1]*self.nb_spike_eye
            
        
        if eye_type == "food":
            self.food_eyes = eyes_list
            self.nb_food_eye = len(self.food_eyes)
            self.saw_by_food_eyes = [1]* self.nb_food_eye 

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
    
    def get_spike_eyes(self) ->list[Eye]:
        return self.spike_eyes
    
    def get_food_eyes(self) ->list[Eye]:
        return self.food_eyes
    
    

    def collide_spike(self, spike):
        return collide_circle((self.x,self.y), self.radius, (spike.x,spike.y), spike.radius)
    def collide_food(self, food):
        return collide_circle((self.x, self.y), self.radius, (food.x,food.y),food.radius)
    def kill(self):
        self.dead = True

    def is_dead(self):
        return self.dead
    
    def input_movement(self, x_channel, y_channel, rot_channel):
        if((x_channel + self.x) - self.radius <0):
                x_channel = 0
        elif (x_channel+self.x +self.radius>self.board.width):
                x_channel = 0
        if ((y_channel+self.y)-self.radius<0):
                y_channel= 0
        elif (y_channel +self.y+self.radius >self.board.height):
                y_channel = 0
        self.x += x_channel
        self.y +=y_channel
        self.angle +=rot_channel

    def make_immortal(self):
        self.immortal = True

    def starve(self):
        if not self.immortal:
            self.energy -=1
        if self.energy <=0:
            self.dead =True

    def see_eyes(self,eye_type,object):
        if eye_type == "spike":
            for i in range(self.nb_spike_eye):
                vision = self.spike_eyes[i].see_for_spike(object)
                if vision !=1:
                    self.saw_by_spike_eyes[i] = vision
        if eye_type == "food":
            for i in range(self.nb_food_eye):
                vision = self.food_eyes[i].see_for_food(object)
                if vision !=1:
                    self.saw_by_food_eyes[i] = vision

    def see_eyes2(self, eye_type,collision_ref):
        if eye_type == "f":
            for i in range(self.nb_food_eye):
                vision = self.food_eyes[i].see_for_food2(collision_ref)
                if vision !=1:
                    self.saw_by_food_eyes[i] = vision


    def reset_sight(self):
        for i in range(self.nb_food_eye):
            self.saw_by_food_eyes[i] = 1
        for i in range(self.nb_spike_eye):
            self.saw_by_spike_eyes[i] = 1

    
        


    def get_context(self):
        tensor_context = torch.tensor(size = (3+self.nb_eyes_spike+self.nb_eyes_food))
        tensor_context[0] = Boule.get_x()/self.b_width
        tensor_context[1] = Boule.get_y()/self.b_height
        tensor_context[2] = Boule.get_angle()/360
        for i in range(self.nb_eyes_spike):
            tensor_context[3+i] = 0

        return tensor_context
    def get_nn_input(self):
        inputs = []

        inputs.append(self.x / self.board.width)
        inputs.append(self.y / self.board.height)

        inputs.append(self.angle / 360)

        inputs.append(self.energy / 1000)

        inputs.extend(self.saw_by_spike_eyes)

        inputs.extend(self.saw_by_food_eyes)

        return torch.tensor(inputs, dtype=torch.float32)
    
    def upgrade_score(self):
        self.score+=1

    
   
class Spike:
    def __init__(self, x, y, pilot):
        self.x = x
        self.y = y
        self.pilot = pilot
        self.radius =10
        self.mask = widden_mask(create_circle_mask(self.radius,5))


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
         self.mask = create_circle_mask(self.radius, TOLERANCE_MASK)
         self.id = False

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
    def set_id(self,id):
        self.id =id

        

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
        self.collision_grid_margin = COLLISION_GRID_MARGIN
        self.width = width
        self.height = height
        self.food_collision = np.zeros((width+self.collision_grid_margin,height+self.collision_grid_margin))
        self.spike_collision =  np.zeros((width+self.collision_grid_margin,height+self.collision_grid_margin))
        self.last_used_id_food = 0
        self.dead_boule = list()
        self.nb_alive_boule = 0
        

    def run(self):
        
        for boule in self.boules:
            boule.reset_sight()
            self.collide_food_boule(boule)
            boule.see_eyes2("f", self.food_collision)
            boule.move()
            boule.starve()
            boule.upgrade_score()
            if boule.is_dead():
                self.boules.remove(boule)
                self.dead_boule.append(boule)
                self.nb_alive_boule -=1
                
                if (self.nb_alive_boule<=0):
                    return True
        
        return False
    
    def get_sorted_generation(self):
        return sorted(self.dead_boule, key= lambda b : b.score)
            


        # for boule in self.boules:
        #     boule.starve()
            
        #     if boule.is_dead() == False:
        #         boule.move()
        #         if boule.energy == 0:
        #             boule.kill()
        #             continue
        #         boule.reset_sight()

        #         for food in self.foods:
        #             if food.get_eaten() == False:
        #                     if boule.collide_food(food):
        #                         food.die()
        #                         boule.eat()
        #                     boule.see_eyes("food", food)
        # for spike in self.spikes:
        #             spike.move()
        #             for boule in self.boules:
        #                 if boule.is_dead() == False:
        #                     if boule.collide_spike(spike):
        #                         boule.kill()
        #                     boule.see_eyes("spike", spike)


    def set_collision_food(self, food):
        if (food.id !=False):
            for vec in food.mask:
                x = vec[0] +food.x +int(self.collision_grid_margin/2)
                y = vec[1] +food.y +int(self.collision_grid_margin/2)
                if (0<x<self.width) and (0<y<self.height):
                    
                        self.food_collision[x][y] = food.id
        else:
            print("Waring : food without ID\n")

    def add_spike(self, spike):
        self.spikes.append(spike)

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    def add_food(self, food : Food):
        self.foods.append(food)
        new_id = self.last_used_id_food +1
        food.set_id(new_id)
        self.last_used_id_food = new_id
        self.set_collision_food(food)
        


    def add_boule(self, boule):
        self.boules.append(boule)
        self.nb_alive_boule+=1
        

    def get_boules(self):
        return self.boules
    
    def get_spikes(self):
        return self.spikes
    
    def remove_food(self,food):
        for p in food.mask:
            x = p[0]+food.get_x() +int(self.collision_grid_margin/2)
            y = p[1]+food.get_y() +int(self.collision_grid_margin/2)
            self.food_collision[x][y] = 0
        self.foods.remove(food)
    
    def get_food_by_id(self, id):
        for food in self.foods:
            if food.id == id:
                return food


    def collide_food_boule(self,boule :Boule):
        for p in boule.mask:
            x = p[0]+boule.get_x() +int(self.collision_grid_margin/2)
            y = p[1]+boule.get_y() +int(self.collision_grid_margin/2)
            square_value = self.food_collision[x][y]
            if square_value !=0:
                self.remove_food(self.get_food_by_id(square_value))
                boule.eat()

    

def even_spaced_eyes(nb_eyes,offset,lenght,boule):
    new_list = []
    for i in range(nb_eyes):
        new_list.append(Eye(lenght,i*(360/nb_eyes)+offset,boule))
    return new_list





                       


        
    
    
     
    
        


        



