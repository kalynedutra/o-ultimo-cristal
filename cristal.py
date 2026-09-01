import pygame
import math
from entidade import Entidade
from utils import criar_explosao_cristal


class Cristal(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (0, 200, 255))
        self.coletado = False

        # =========================
        # FLUTUAÇÃO (sobe e desce)
        # =========================
        self.y_base = y
        self.tempo = 0
        self.amplitude = 6   
        self.velocidade_flutuacao = 0.05
        self.offset_y = 0      

        # =========================
        # EXPLOSÃO AO COLETAR
        # =========================
        self.particulas = []

    def coletar(self, player):
        if not self.coletado and self.colidiu_com(player):
            self.coletado = True
            self.particulas = criar_explosao_cristal(self.rect.centerx, self.rect.centery)
            return True
        return False

    # =========================
    # UPDATE (flutuação)
    # =========================
    def update(self):
        if self.coletado:
            return
        self.tempo += self.velocidade_flutuacao
        self.offset_y = math.sin(self.tempo) * self.amplitude
        self.rect.y = int(self.y_base + self.offset_y)

    # =========================
    # PARTÍCULAS DA EXPLOSÃO 
    # =========================
    def atualizar_particulas(self):
        for p in self.particulas:
            p.update()
        self.particulas = [p for p in self.particulas if p.esta_viva()]

    def desenhar_particulas(self, tela):
        for p in self.particulas:
            p.desenhar(tela)