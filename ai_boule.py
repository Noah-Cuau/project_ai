import torch
from torch import nn
from simulation import Boule, Eye, Board
import random



class Genome_v1:
    def __init__(self, wieght_l1 : torch.tensor, bias_l1 : torch.tensor, 
                 wieght_l2 : torch.tensor, bias_l2 : torch.tensor, 
                 wieght_l3 : torch.tensor, bias_l3 : torch.tensor):
        self.weight_l1 = wieght_l1
        self.bias_l1 = bias_l1
        self.weight_l2 = wieght_l2
        self.bias_l2 = bias_l2
        self.weight_l3 = wieght_l3
        self.bias_l3 = bias_l3

    def __str__(self):
        return "layers 1 : \n   weight : " +str(self.weight_l1) +"\n   bias : " +str(self.bias_l1) +  "\nlayers 2 : \n   weight : " +str(self.weight_l2) +"\n   bias : " +str(self.bias_l2) +  "\nlayers 3 : \n   weight : " +str(self.weight_l3) +"\n   bias : " +str(self.bias_l3) 


def random_genome_v1()->Genome_v1:
    weight_l1 = (torch.rand(3,12)-0.5)*2
    bias_l1 = (torch.rand(3)-0.5)*2
    weight_l2 = (torch.rand(3,3)-0.5)*2
    bias_l2 = (torch.rand(3)-0.5)*2
    weight_l3 = (torch.rand(3,3)-0.5)*2
    bias_l3 = (torch.rand(3)-0.5)*2



   


    return Genome_v1(weight_l1, bias_l1, weight_l2, bias_l2, weight_l3, bias_l3)



def pick_mutation(chance, magnitude):
    #chance in percentage value between 0 and 100
    value = random.randint(0,100)
    if (value<=chance):
        return magnitude *random.choice([-1,1])
    else:
        return 0


def crossover_genome_v1(g1 :Genome_v1, g2 : Genome_v1):
    choice = [g1,g2]
    weight_l1 = torch.zeros(3,12)
    bias_l1 = torch.zeros(3)
    weight_l2 = torch.zeros(3,3)
    bias_l2 = torch.zeros(3) 
    weight_l3 = torch.zeros(3,3)
    bias_l3 = torch.zeros(3)


    layers_w = [weight_l1, weight_l2, weight_l3]
    layers_w_name = ["weight_l1","weight_l2","weight_l3"]

    for i_layer,l in enumerate(layers_w):
        for i,t in enumerate(l):
            for j,_ in enumerate(t): 
                l[i][j] = getattr(choice[random.randint(0,1)], layers_w_name[i_layer])[i][j] + pick_mutation(10, 0.2)

    layers_b = [bias_l1, bias_l2, bias_l3]
    layers_b_name = ["bias_l1","bias_l2","bias_l3"]

    for i_layer,l in enumerate(layers_b):
        for i,_ in enumerate(l):
                l[i] = getattr(choice[random.randint(0,1)], layers_b_name[i_layer])[i] + pick_mutation(10, 0.2)

    return Genome_v1(weight_l1, bias_l1, weight_l2, bias_l2, weight_l3, bias_l3)

    
    








class Boule_NN_v1(nn.Module):
    def __init__(self,genome :Genome_v1):
        super().__init__()

        layer1 = nn.Linear(12,3)
        layer1.weight = nn.parameter.Parameter(genome.weight_l1)
        layer1.bias = nn.parameter.Parameter(genome.bias_l1)

        layer2 = nn.Linear(3,3)
        layer2.weight = nn.parameter.Parameter(genome.weight_l2)
        layer2.bias = nn.parameter.Parameter(genome.bias_l2)

        layer3 = nn.Linear(3,3)
        layer3.weight = nn.parameter.Parameter(genome.weight_l3)
        layer3.bias = nn.parameter.Parameter(genome.bias_l3)

        self.model = nn.Sequential(
            layer1,
            layer2,
            layer3,
                        nn.Sigmoid()

        )
        self.genome = genome

    def forward(self, x):
        return (self.model(x))


def activation_v1(a):
    if 0<=a<0.33:
        return -1
    elif 0.33<=a <0.66:
        return 0
    elif 0.66 <= a <=1:
        return 1


class Boule_NN_Pilot:
    def __init__(self,boule,NN,board):
        self.boule : Boule =boule
        self.NN = NN
        self.b_width = board.get_width()
        self.b_height = board.get_height()
        self.nb_eyes_food =  len(boule.get_food_eyes())


    def get_context(self):
        tensor_context = torch.zeros(4+self.nb_eyes_food)
        tensor_context[0] = (self.boule.get_x()/self.b_width )
        tensor_context[1] = (self.boule.get_y()/self.b_height )
        tensor_context[2] = ((self.boule.get_angle()/360)%360)-0.5
        tensor_context[3] = self.boule.energy

        
      
            
        for i in range(self.nb_eyes_food):
            tensor_context[4+i] = self.boule.saw_by_food_eyes[i]
            

        return tensor_context
    
    def get_move(self):
        #print(self.get_context().shape)
        tensor = self.NN.forward(self.get_context())
        #print(f"\r{tensor[0]}", end = "", flush=True)
        return activation_v1(tensor[0]), activation_v1(tensor[1]), activation_v1(tensor[2])


def random_nn_v1() -> Boule_NN_v1:
    return Boule_NN_v1(random_genome_v1())
