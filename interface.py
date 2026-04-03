import pygame
from create_sim import *
from create_sim import create_constant_sim
import time
class Game:
    def __init__(self, win_w, win_h,board
                ):
        pygame.init()

        self.win_w = win_w
        self.win_h = win_h
        self.h = 1000
        self.l = 1000
        self.grid_cols = win_h
        self.grid_rows = win_w
        self.board : Board =board 
        self.show_eyes = True

        #self.radius = self.board.boules[0].get_radius()

        #self.intern_surf = pygame.surface.Surface()
    

        self.screen = pygame.surface.Surface((board.width,board.height))
        self.output_screen = pygame.display.set_mode((win_h, win_w), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.manual_control = False

        self.border = 5

    def compute_cell_size(self):
        W, H = self.screen.get_size()
        cell_w = W / self.grid_cols
        cell_h = H / self.grid_rows
        return cell_w, cell_h

    def grid_to_pixel(self, gx, gy):
        cell_w, cell_h = self.compute_cell_size()
        px = gx * cell_w
        py = gy * cell_h
        return px, py

    def quadrillage(self):
        W, H = self.screen.get_size()
        cell_w, cell_h = self.compute_cell_size()

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x = col * cell_w
                y = row * cell_h
                rect = pygame.Rect(int(x), int(y), int(cell_w + 1), int(cell_h + 1))
                color = "lightgrey" if (row + col) % 2 == 0 else "darkgrey"
                pygame.draw.rect(self.screen, color, rect)


    def printf_spikes(self):
        for spike in self.board.spikes:
            rect = pygame.Rect(spike.get_x()-(spike.get_radius()*0.70), spike.get_y()-(spike.get_radius()*0.70), spike.get_radius()*1.41, spike.get_radius()*1.41)
            pygame.draw.circle(self.screen, "black", (spike.get_x(), spike.get_y()), spike.get_radius())
            pygame.draw.rect(self.screen, "red", rect)
            

    def printf_food(self):
        for food in self.board.foods:
            if food.get_eaten() == False:
                pygame.draw.circle(self.screen, "green",(food.get_x(),food.get_y()),food.get_radius())

    def printf_boules(self):
        for boule in self.board.boules:
            if boule.is_dead() == False:
                pygame.draw.circle(self.screen, "blue", (boule.get_x(), boule.get_y()),boule.get_radius())
                for i,eye in enumerate(boule.get_food_eyes()):
                    if boule.saw_by_food_eyes[i] !=1:
                        pygame.draw.line(self.screen, "orange", (boule.x,boule.y), eye.get_end_sight())
                    else:
                         pygame.draw.line(self.screen, "green", (boule.x,boule.y), eye.get_end_sight())
                
                for i,eye in enumerate(boule.get_spike_eyes()):
                    if boule.saw_by_spike_eyes[i] !=1:
                        pygame.draw.line(self.screen, "purple", (boule.x,boule.y), eye.get_end_sight())
                    else:
                         pygame.draw.line(self.screen, "yellow", (boule.x,boule.y), eye.get_end_sight())

                    

    def set_show_eyes(self, show_eye):
        self.show_eyes = show_eye

    def render(self):
        t0 = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.manual_control:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.up_pressed = True
                    if event.key == pygame.K_DOWN:
                        self.down_pressed = True
                    if event.key == pygame.K_LEFT:
                        self.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        self.right_pressed = True
                    if event.key == pygame.K_a:
                        self.a_pressed = True
                    if event.key == pygame.K_z:
                        self.z_pressed = True
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.up_pressed = False
                    if event.key == pygame.K_DOWN:
                        self.down_pressed = False
                    if event.key == pygame.K_LEFT:
                        self.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        self.right_pressed = False
                    if event.key == pygame.K_a:
                        self.a_pressed = False
                    if event.key == pygame.K_z:
                        self.z_pressed = False
                
                
                    
        if self.manual_control:
            x=y=rot = 0

            if self.right_pressed:
                x = 1
            elif self.left_pressed:
                x = -1

            if self.up_pressed:
                y = -1
            elif self.down_pressed:
                y = 1
            if self.a_pressed:
                rot = -1
            elif self.z_pressed:
                rot = 1
            self.manual_control.input_movement(x,y,rot)


        self.screen.fill("white")

        #self.quadrillage()
        self.printf_food()
        self.printf_spikes()
        self.printf_boules()
        self.output_screen.blit(pygame.transform.scale(self.screen, (self.win_w,self.win_h)), (0,0))

        pygame.display.flip()
        self.clock.tick(120)
        t = round(time.time() - t0,4)
        #print(f"\rTime to compute frame: {t}", end="", flush=True)
    
    def run(self):
        self.render()
        sim_ended = self.board.run()
        return sim_ended


        

    def set_manual_control(self, boule, immortal):
        self.manual_control = boule
        if immortal:
            boule.make_immortal()
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.a_pressed = False
        self.z_pressed = False
        boule.set_pilot(False)





def create_new_gen(b : Board,gen : list[Boule]):
    new_gen = []
    size_gen = len(gen)
    best_boule = gen[-1]
    second_boule = gen[-2]
    for i in range(int(size_gen/2)):
        
        new_gen.append(add_boule_from_genome(b, crossover_genome_v1(gen[i].get_genome(),best_boule.get_genome())))
    
    for i in range(int(size_gen/2)):
        new_gen.append(add_boule_from_genome(b, crossover_genome_v1(gen[i].get_genome(),second_boule.get_genome())))

        

def add_boule_from_genome(b : Board, g : Genome_v1):
    new_boule = Boule(random.randint(0, b.width), random.randint(0,b.height), 0, b)
    b.add_boule(new_boule)

    new_eyes = even_spaced_eyes(8,0, 300,new_boule)
    new_boule.set_eyes(new_eyes,"food")

       
    new_boule.set_pilot(Boule_NN_Pilot(new_boule,Boule_NN_v1(g), b))





def first_training_loop(nb_iteration, filename_best_genome):
    largeur =  5000
    hauteur = 5000
    res_width = 1000
    res_height = 1000
    nombre_spikes = 0
    nombre_food = 150
    nombre_boule = 64
    board = create_sim_test_nn(largeur,hauteur,nombre_spikes,nombre_food,nombre_boule)
    board.boules[0].get_genome()
    for i in range(nb_iteration):
        print("generation : "+str(i))
        while not board.run():
            pass
        result= board.get_sorted_generation()
        for r in result:
            print(r.score, end = ", ")
        print("best score : "+ str(result[-1].score))
        save_genome_v1(result[-1].get_genome(),"test")

        board = create_sim_test_nn(largeur,hauteur,nombre_spikes,nombre_food,0)
        create_new_gen(board, result)

        

def load_board_with_1_g():
    largeur =  5000
    hauteur = 5000
    res_width = 1000
    res_height = 1000
    nombre_spikes = 0
    nombre_food = 150
    nombre_boule = 64
    board = create_sim_test_nn(largeur,hauteur,nombre_spikes,nombre_food,0)
    add_boule_from_genome(board, load_genome_v1("test"))
    print(board.boules)
    print(board.boules[0].get_genome())
    return board


class Trainging_v1():
    def __init__(self,width, height, nb_generation,gen_size):
        self.nb_generation = nb_generation
        self.gen_size = gen_size
        self.width = width
        self.height = height
        self.boards : list[Board_train_v1] =  []
        self.finished_board : list[Board_train_v1]= []
        self.current_gen = 0
        for i in range(gen_size):
            print("creating board : "+str(i))
            new_board = Board_train_v1(width, height)
            self.boards.append(new_board)
            random_genome = random_genome_v1()
            self.create_boule_from_genome_v1(random_genome, int(self.width/2), int(self.height/2), new_board)
        self.game = False

    
    def get_sorted_gen(self):
        return sorted(self.finished_board, key = lambda b : b.get_single_boule().score)


    def make_next_gen(self, print_best_score : bool):
        #return best genome
        best_boule = self.get_sorted_gen()[-1].get_single_boule()
        best_genome =best_boule.get_genome()
        if print_best_score:
            print("\nGeneration "+str(self.current_gen)+" best score : " +str(best_boule.score) + "\n")
        for board in self.finished_board:

            new_genome = crossover_genome_v1(best_genome, board.get_genome())
            board.reset()

            add_boule_from_genome(board, new_genome)
            board.set_fixed_food()
            self.boards.append(board)
        self.finished_board = []
        return best_genome
    
    def create_boule_from_genome_v1(self,g, pos_x,pos_y,board :Board_train_v1):
        new_boule = Boule(pos_x, pos_y, 0, board)

        new_eyes = even_spaced_eyes(8,0, 100,new_boule)
        new_boule.set_eyes(new_eyes,"food")

       
        new_boule.set_pilot(Boule_NN_Pilot(new_boule,Boule_NN_v1(g), board))
        board.set_single_boule(new_boule)

    def set_window(self, game):
        self.game = game

    def train(self):

        nb_finished_board = 0
        while nb_finished_board<self.gen_size:
            t0 = time.time()
            for board in self.boards:

                if board.run():
                    self.boards.remove(board)
                    self.finished_board.append(board)
                    nb_finished_board+=1
            t = round(time.time()-t0,3)
            print(f"\rTime to run all board: {t} , nb finished board : {nb_finished_board} , current gen : {self.current_gen}  ", end="", flush=True)
            if self.game !=False:
                self.game.render()
        best_genome = self.make_next_gen(True)
        save_genome_v1(best_genome, "test-2")
        self.current_gen+=1
        if self.current_gen == self.nb_generation:
            return True
        else:
            return False

                
                
                



TEST_TRAIN =True

if __name__ == "__main__":
    if True:
        training = Trainging_v1(1000,1000, 100, 20)
        game = Game(1000,1000, training.boards[0])
        training.set_window(game)
        while not training.train():
            pass
        quit()

    # if True:
    #     board = Board_train_v1(1000,1000)
    #     game = Game(1000,1000, board)
    #     board.add_boule( Boule(500,500,0, board) )
    #     game.set_manual_control(board.boules[0], True)
    #     new_eyes = even_spaced_eyes(8,0, 100,board.boules[0])
    #     board.boules[0].set_eyes(new_eyes,"food")

    #     while game.running:
    #             game.run()
    #     quit()
            


    if not TEST_TRAIN:

        largeur =  1000
        hauteur = 1000
        res_width = 1000
        res_height = 1000
        nombre_spikes = 0
        nombre_food = 150
        nombre_boule = 64
        board = create_sim_test_nn(largeur,hauteur,nombre_spikes,nombre_food,nombre_boule)
        #const_board = create_constant_sim(500,500)
        new_game = Game(
            res_width, res_height,board,
        )
        print(len(board.boules))
        #new_game.set_manual_control(new_game.board.boules[0], True)
        #setup le controlle avec le clavier pour une boule (a mettre en commentaire pour désactiver)
        #2iem argument pour rendre la boule immortelle ou non
        torch.random.seed()
        with torch.inference_mode():

            while new_game.running:
                if new_game.run():
                    result= new_game.board.get_sorted_generation()
                    save_genome_v1(result[-1].get_genome(), "test")
    else:
        first_training_loop(1000, "first_test")
        
