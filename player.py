# player.py
from entidade import Entidade
import pygame

class Player(Entidade): #Classe filha de entidade
    def __init__(self, x, y):
        super().__init__(x, y, largura=32, altura=32, cor=(255, 255, 255))
        self.velocidade = 4
        self.vidas = 3
        self.pontuacao = 0

    def mover(self, teclas, largura_mapa, altura_mapa):
        if teclas[pygame.K_UP]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidade
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade

        # Limites do mapa
        self.x = max(0, min(self.x, largura_mapa - self.largura))
        self.y = max(0, min(self.y, altura_mapa - self.altura))
        self.atualizar_rect()

    def perder_vida(self):
        self.vidas -= 1

    def coletar(self, pontos):
        self.pontuacao += pontos