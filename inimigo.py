import pygame
from entidade import Entidade

class Inimigo(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, (200, 50, 50))

        # movimento
        self.vel = 1.5
        self.direcao = -1

        # vida
        self.vida = 2
        self.ativo = True
        self.dano = 1

        # IA
        self.estado = "patrulha"  # patrulha / perseguindo
        self.distancia_visao = 180

    def morrer(self):
        self.ativo = False

    def tomar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.morrer()

    def update(self, player, plataformas):

        if not self.ativo:
            return

        # =========================
        # IA: DETECTA PLAYER
        # =========================
        distancia = abs(player.rect.centerx - self.rect.centerx)
        mesmo_nivel = abs(player.rect.bottom - self.rect.bottom) < 25

        if distancia < self.distancia_visao and mesmo_nivel:
            self.estado = "perseguindo"
        else:
            self.estado = "patrulha"

        # =========================
        # MOVIMENTO
        # =========================
        if self.estado == "perseguindo":
            self.direcao = 1 if player.rect.centerx > self.rect.centerx else -1

        self.rect.x += self.vel * self.direcao

        # =========================
        # COLISÃO COM PAREDES
        # =========================
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.direcao > 0:
                    self.rect.right = p.left
                else:
                    self.rect.left = p.right
                self.direcao *= -1

        # =========================
        # DETECÇÃO DE BORDA (ROBUSTA)
        # =========================
        no_chao = False

        for p in plataformas:
            if (
                self.rect.bottom == p.top and
                self.rect.centerx >= p.left and
                self.rect.centerx <= p.right
            ):
                no_chao = True
                break

        if not no_chao:
            # evita cair
            self.rect.x -= self.vel * self.direcao
            self.direcao *= -1