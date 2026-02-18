import pygame
from create_sim import *
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
            #pygame.draw.circle(self.screen, "black", (spike.get_x(), spike.get_y()), spike.get_radius())
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

    def run(self):
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


        self.board.run()
        self.screen.fill("white")

        #self.quadrillage()
        self.printf_food()
        self.printf_spikes()
        self.printf_boules()
        self.output_screen.blit(pygame.transform.scale(self.screen, (self.win_w,self.win_h)), (0,0))

        pygame.display.flip()
        self.clock.tick(120)

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

   




if __name__ == "__main__":
    largeur =  500
    hauteur = 500
    res_width = 1000
    res_height = 1000
    nombre_spikes = 0
    nombre_food = 50
    nombre_boule = 5
    board = create_sim_test_nn(largeur,hauteur,nombre_spikes,nombre_food,nombre_boule)
    new_game = Game(
        res_width, res_height,board,
    )
    #new_game.set_manual_control(new_game.board.boules[0], True)
    #setup le controlle avec le clavier pour une boule (a mettre en commentaire pour désactiver)
    #2iem argument pour rendre la boule immortelle ou non
    with torch.inference_mode():

        while new_game.running:
            new_game.run()
