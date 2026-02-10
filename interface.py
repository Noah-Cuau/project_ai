import pygame
from simulation import *

class Game:
    def __init__(self, largeur, hauteur, echelle=100):
        pygame.init()
        self.largeur = largeur
        self.hauteur = hauteur
        self.echelle = echelle
        self.board = create_sim_test(1000,1000)
        self.screen = pygame.display.set_mode((self.largeur * self.echelle,
                                               self.hauteur * self.echelle))
        self.clock = pygame.time.Clock()
        self.running = True

        self.param_rect = [0, 0,
                           self.largeur * self.echelle,
                           self.hauteur * self.echelle,
                           5]
        self.rect = pygame.Rect(self.param_rect[0], self.param_rect[1],
                                self.param_rect[2], self.param_rect[3])

    def quadrillage(self):
        rows = self.param_rect[3] // self.echelle
        cols = self.param_rect[2] // self.echelle

        for row in range(rows):
            for col in range(cols):
                x = self.param_rect[0] + col * self.echelle
                y = self.param_rect[1] + row * self.echelle
                cell = pygame.Rect(x, y, self.echelle, self.echelle)

                color = "lightgrey" if (row + col) % 2 == 0 else "darkgrey"
                pygame.draw.rect(self.screen, color, cell)

    def printf_spikes(self):
        for spikes in self.board.spikes:
            rect = pygame.Rect(spikes.get_x(), spikes.get_y(),10,10)
            pygame.draw.rect(self.screen,"red",rect)

    def printf_boules(self):
        for spikes in self.board.spikes:
            rect = pygame.Rect(spikes.get_x(), spikes.get_y(),10,10)
            pygame.draw.rect(self.screen,"red",rect)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill("white")
        pygame.draw.rect(self.screen, "black", self.rect, self.param_rect[4])
        self.board.run()
        self.quadrillage()
        
        self.printf_spikes()

        pygame.display.update()
        self.clock.tick(60)

if __name__ == "__main__":
    new_game = Game(10, 10)
    while new_game.running:
        new_game.run()
