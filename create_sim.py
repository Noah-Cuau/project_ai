from simulation import *

from ai_boule import *


def create_sim_test(width, height, nombre_spikes, nombre_foods, nombre_boule):
    new_b = Board(width,height)
    for i in range(nombre_spikes):
        #new_pilot = Default_spike_pilot(width,height)
        new_pilot = False
        new_spike = Spike(random.randint(15,width-15), random.randint(15,height-15), new_pilot)
        #new_spike.pilot.up = random.choice([-1,1])
        #new_spike.pilot.right = random.choice([-1,1])
        new_b.add_spike(new_spike)
    for i in range(nombre_foods):
        new_food = Food(random.randint(0,width),random.randint(0,height))
        new_b.add_food(new_food)
    
    for i in range(nombre_boule):
        new_boule = Boule(random.randint(0, width), random.randint(0,height), 0, new_b)
        new_boule.set_pilot(Default_boule_pilot(new_boule, width, height))
        new_b.add_boule(new_boule)

        new_eyes = even_spaced_eyes(4,0, 35,new_b.boules[i])
        new_boule.set_eyes(new_eyes,"food")

        new_eyes = even_spaced_eyes(4,45, 35,new_b.boules[i])
        new_boule.set_eyes(new_eyes,"spike")



        

    return new_b


def create_sim_test_nn(width, height, nombre_spikes, nombre_foods, nombre_boule):
    new_b = create_sim_test(1000, 1000, nombre_spikes, nombre_foods, 0)
    for i in range(nombre_boule):
        new_boule = Boule(random.randint(0, width), random.randint(0,height), 0, new_b)
        new_boule.set_pilot(Default_boule_pilot(new_boule, width, height))
        new_b.add_boule(new_boule)

        new_eyes = even_spaced_eyes(4,0, 35,new_b.boules[i])
        new_boule.set_eyes(new_eyes,"food")

        new_eyes = even_spaced_eyes(4,45, 35,new_b.boules[i])
        new_boule.set_eyes(new_eyes,"spike")
        new_boule.set_pilot(Boule_NN_Pilot(new_boule,Boule_NN(new_boule, new_b), new_b))
        new_boule.make_immortal()
    
   
    return new_b
        

        