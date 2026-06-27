# entidade.py
import pygame

class Entidade:
    def __init__(self, x, y, largura, altura, cor):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)

    def atualizar_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def colidiu_com(self, outra):
        return self.rect.colliderect(outra.rect)