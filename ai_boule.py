import torch
from torch import nn
from simulation import Boule, Eye, Board

class Boule_NN(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(12, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 3)
        )

    def forward(self, x):
        return self.model(x)




class Boule_NN_Pilot:
    def __init__(self,boule,NN,board):
        self.boule : Boule =boule
        self.NN = NN
        self.b_width = board.get_width()
        self.b_height = board.get_height()
        self.nb_eyes_spike = len(boule.get_spike_eyes())
        self.nb_eyes_food =  len(boule.get_food_eyes())


    def get_context(self):
        tensor_context = torch.zeros(3+self.nb_eyes_spike+self.nb_eyes_food)
        tensor_context[0] = (self.boule.get_x()/self.b_width -0.5)
        tensor_context[1] = (self.boule.get_y()/self.b_height -0.5)
        tensor_context[2] = ((self.boule.get_angle()/360)%360)-0.5
        
        for i in range(self.nb_eyes_spike):
            tensor_context[3+i] = self.boule.saw_by_spike_eyes[i]
            
        for i in range(self.nb_eyes_food):
            tensor_context[3+self.nb_eyes_spike+i] = self.boule.saw_by_food_eyes[i]
            

        return tensor_context
    
    def get_move(self):
        tensor = self.NN.forward(self.boule.get_nn_input())
        print(tensor)
        return round(float(tensor[0])), round(float(tensor[1])), round(float(tensor[2]))

