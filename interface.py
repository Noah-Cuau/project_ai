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

        self.spike_w=self.spike_h = self.board.spikes[0].get_radius()
        #self.radius = self.board.boules[0].get_radius()

        #self.intern_surf = pygame.surface.Surface()
    

        self.screen = pygame.display.set_mode((self.win_w, self.win_h), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

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

    # def printf_boules(self):
    #     for boule in self.board.boules:
    #         px, py = self.grid_to_pixel(boule.get_x(), boule.get_y())
    #         rect = pygame.Rect(int(px), int(py), self.boule_w, self.boule_h)
    #         pygame.draw.circle(self.screen, "blue", (board.boules.get_x(), board.boules.get_y()),self.radius)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill("white")

        self.board.run()

        self.quadrillage()
        self.printf_spikes()
        #self.printf_boules()

        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    gen_size = [200,200, 5]
    board = create_sim_test(gen_size[0],gen_size[1], gen_size[2])
    new_game = Game(
        gen_size[0], gen_size[1],board,
        grid_cols=gen_size[0]//200, grid_rows=gen_size[1]//200  
    )
    while new_game.running:
        new_game.run()
