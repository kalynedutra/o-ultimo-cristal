import pygame
from player import Player

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        self.clock = pygame.Clock()
        self.rodando = True
        self.player = Player(100, 100) 

    def executar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            teclas = pygame.key.get_pressed()
            self.player.mover(teclas, largura_mapa=800, altura_mapa=600)

            self.tela.fill((10, 5, 30))
            self.player.desenhar(self.tela)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

Jogo().executar()