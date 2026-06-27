import pygame
from entidade import Entidade

class Cristal(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (0, 200, 255))
        self.coletado = False

    def coletar(self, player):
        if not self.coletado and self.colidiu_com(player):
            self.coletado = True
            return True
        return False