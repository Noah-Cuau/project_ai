import pygame
from simulation import *

class Game:
    def __init__(self, win_w, win_h,board, grid_cols=10, grid_rows=10,
                ):
        pygame.init()

        self.win_w = win_w
        self.win_h = win_h

        self.grid_cols = grid_cols
        self.grid_rows = grid_rows
        self.board =board
        self.show_eyes = True

        self.spike_w=self.spike_h = self.board.spikes[0].get_radius()
        #self.radius = self.board.boules[0].get_radius()

        #self.intern_surf = pygame.surface.Surface()
    

        self.screen = pygame.display.set_mode((self.win_w, self.win_h), pygame.RESIZABLE)
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
            rect = pygame.Rect(int(spike.get_x()), int(spike.get_y()), self.spike_w, self.spike_h)
            pygame.draw.rect(self.screen, "red", rect)

    def printf_food(self):
        for food in self.board.foods:
            if food.get_eaten() == False:
                pygame.draw.circle(self.screen, "green",(food.get_x(),food.get_y()),food.get_radius())

    def printf_boules(self):
        for boule in self.board.boules:
            if boule.is_dead() == False:
                pygame.draw.circle(self.screen, "blue", (boule.get_x(), boule.get_y()),boule.get_radius())
                for eye in boule.get_eyes():
                    if eye.saw_spike:
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


        self.screen.fill("white")

        self.board.run()

        self.quadrillage()
        self.printf_food()
        self.printf_spikes()
        self.printf_boules()

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
    largeur =  1000
    hauteur = 1000
    nombre_spikes = 1
    nombre_food = 200
    nombre_boule = 100
    board = create_sim_test(largeur,hauteur,nombre_spikes,nombre_food,nombre_boule)
    board.get_spikes()[0].set_pilot(False)
    new_game = Game(
        largeur, hauteur,board,
        grid_cols=largeur//200, grid_rows=hauteur//200  
    )
    #setup le controlle avec le clavier pour une boule (a mettre en commentaire pour désactiver)
    #2iem argument pour rendre la boule immortelle ou non
    new_game.set_manual_control(new_game.board.get_boules()[0], True)
    while new_game.running:
        new_game.run()
