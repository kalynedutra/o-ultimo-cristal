import pygame
import math
from entidade import Entidade
from utils import criar_explosao


class Inimigo(Entidade):

    ESQUERDA = -1
    DIREITA = 1

    def __init__(self, x, y):
        super().__init__(x, y, 39, 32, (200, 50, 50))

        # =========================
        # MOVIMENTO
        # =========================
        self.vel = 1.5
        self.direcao = self.ESQUERDA

        # =========================
        # VIDA
        # =========================
        self.vida = 2
        self.ativo = True
        self.dano = 1

        # =========================
        # IA
        # =========================
        self.estado = "patrulha"
        self.distancia_visao = 180

        self.contado = False

        # =========================
        # EXPLOSÃO 
        # =========================
        self.particulas = []

    # =========================
    # MORTE
    # =========================
    def morrer(self):
        self.ativo = False
        self.particulas = criar_explosao(self.rect.centerx, self.rect.centery)

    def definir_dano(self, eliminacoes):
        self.dano = math.ceil(1 + eliminacoes * 0.1)

    # =========================
    # DANO
    # =========================
    def tomar_dano(self, dano):
        self.vida -= dano

        if self.vida <= 0:
            self.morrer()

    # =========================
    # DIREÇÃO
    # =========================
    def virar_esquerda(self):
        self.direcao = self.ESQUERDA

    def virar_direita(self):
        self.direcao = self.DIREITA

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

    # =========================
    # UPDATE
    # =========================
    def update(self, player, plataformas, eliminacoes):

        if not self.ativo:
            return

        # =========================
        # DETECTA PLAYER
        # =========================

        distancia = abs(
            player.rect.centerx - self.rect.centerx
        )

        mesmo_nivel = abs(
            player.rect.bottom - self.rect.bottom
        ) < 25

        if distancia <= self.distancia_visao and mesmo_nivel:
            self.estado = "perseguindo"
        else:
            self.estado = "patrulha"

        # =========================
        # PERSEGUIÇÃO
        # =========================

        if self.estado == "perseguindo":

            if player.rect.centerx > self.rect.centerx:
                self.direcao = self.DIREITA

            elif player.rect.centerx < self.rect.centerx:
                self.direcao = self.ESQUERDA

        # =========================
        # TESTA SE VAI CAIR
        # =========================

        proximo_x = self.rect.centerx + (
            self.vel * self.direcao
        )

        ponto_pe = pygame.Rect(
            proximo_x - 2,
            self.rect.bottom,
            4,
            2
        )

        encontrou_chao = False

        for plataforma in plataformas:

            if ponto_pe.colliderect(plataforma):
                encontrou_chao = True
                break

        if not encontrou_chao:

            self.direcao *= -1

            return

        # =========================
        # MOVIMENTO
        # =========================

        self.rect.x += self.vel * self.direcao

        # =========================
        # COLISÃO COM PAREDES
        # =========================

        for plataforma in plataformas:

            if self.rect.colliderect(plataforma):

                if self.direcao == self.DIREITA:
                    self.rect.right = plataforma.left

                else:
                    self.rect.left = plataforma.right

                self.direcao *= -1

                break
        self.definir_dano(eliminacoes)