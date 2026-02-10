import pygame
from simulation import *

class game:
    def __init__(self, largeur, hauteur):
        pygame.init()
        self.echelle = 200
        self.screen = pygame.display.set_mode((self.echelle*largeur,self.echelle*hauteur))
        self.clock = pygame.time.Clock()
        self.running = True
        self.param_rect = [self.echelle,self.echelle,3* self.echelle, 3 * self.echelle, 5]
        self.rect = pygame.Rect(self.param_rect[0],self.param_rect[1],self.param_rect[2],self.param_rect[3])

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.screen.fill("white")
        pygame.draw.rect(self.screen,"black",self.rect,self.param_rect[4])
        self.quadrillage()
        # render simultation
        pygame.display.flip()

        self.clock.tick(60)  
    def quadrillage(self):
        for i in range(self.echelle+(self.param_rect[0]+self.param_rect[4]), self.param_rect[0]+self.param_rect[2]+self.param_rect[4], self.echelle):
            pygame.draw.line(self.screen,"grey",(i,self.param_rect[1]),(i,self.param_rect[1]+self.param_rect[3]),2)
        for i in range(self.echelle+ self.param_rect[1]+self.param_rect[4], self.param_rect[1]+self.param_rect[3]+self.param_rect[4], self.echelle):
            pygame.draw.line(self.screen,"grey",(self.param_rect[0],i),(self.param_rect[0]+self.param_rect[2],i),2)


if __name__ == "__main__":
    new_game = game(5,5)
    while(new_game.running):
        new_game.run()

