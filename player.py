import pygame

class Princesa:
    def __init__(self, x, y):
        self.posicao_x = x
        self.posicao_y = y
        self.velocidade = 5 

    def movimentacao (self, direcao):
        if direcao == 'a':
            self.posicao_x -= 1 
        elif direcao == 'd':
            self.posicao_x += 1 
        elif direcao == 'w':
            self.posicao_y += 1
        elif direcao == 's':
            self.posicao_y -= 1


