from entidade import Entidade
import pygame

class Player(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 60, (255, 255, 255))

        # movimento
        self.velocidade = 5
        self.velx = 0
        self.vely = 0
        self.direcao = None

        # física
        self.gravidade = 0.5
        self.forca_pulo = -10
        self.no_chao = False

        # combate
        self.vidas = 3
        self.pontuacao = 0
        self.invencivel_timer = 0

    # =====================
    # DANO (KNOCKBACK SEGURO)
    # =====================
    def tomar_dano(self, dano, direcao):
        if self.invencivel_timer <= 0:
            self.vidas -= dano
            self.invencivel_timer = 60

            # knockback vertical
            self.vely = -7

            # knockback horizontal (com segurança)
            self.rect.x += 10 * direcao

    # =====================
    # MOVIMENTO PRINCIPAL
    # =====================
    def mover(self, teclas, largura_mapa, altura_mapa, chao, obstaculos, inimigos):

        # invencibilidade
        if self.invencivel_timer > 0:
            self.invencivel_timer -= 1

        # =====================
        # INPUT HORIZONTAL
        # =====================
        self.velx = 0

        if teclas[pygame.K_LEFT]:
            self.velx = -self.velocidade
            self.direcao = "ESQUERDA"
        if teclas[pygame.K_RIGHT]:
            self.velx = self.velocidade
            self.direcao = "DIREITA"

        # =====================
        # MOVIMENTO X + COLISÃO
        # =====================
        self.rect.x += self.velx

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                if self.velx > 0:
                    self.rect.right = obs.left
                elif self.velx < 0:
                    self.rect.left = obs.right

        # =====================
        # PULO
        # =====================
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vely = self.forca_pulo
            self.no_chao = False

        # =====================
        # GRAVIDADE
        # =====================
        self.vely += self.gravidade
        if self.vely > 12:
            self.vely = 12

        # =====================
        # MOVIMENTO Y + COLISÃO
        # =====================
        self.rect.y += self.vely

        self.no_chao = False

        # chão
        if self.rect.colliderect(chao):
            if self.vely > 0:
                self.rect.bottom = chao.top
                self.vely = 0
                self.no_chao = True

        # plataformas
        for obs in obstaculos:
            if self.rect.colliderect(obs):

                if self.vely > 0:
                    self.rect.bottom = obs.top
                    self.vely = 0
                    self.no_chao = True

                elif self.vely < 0:
                    self.rect.top = obs.bottom
                    self.vely = 0

        # =====================
        # INIMIGOS
        # =====================
        for inimigo in inimigos:
            if not inimigo.ativo:
                continue

            if self.rect.colliderect(inimigo.rect):

                # STOMP (mata inimigo)
                if self.vely > 0 and self.rect.bottom - inimigo.rect.top < 15:
                    inimigo.tomar_dano(1)
                    self.vely = -8
                    self.pontuacao += 2

                # DANO LATERAL
                else:
                    direcao = 1 if self.rect.centerx < inimigo.rect.centerx else -1
                    self.tomar_dano(inimigo.dano, -direcao)

        # =====================
        # LIMITES DA TELA
        # =====================
        self.rect.x = max(0, min(self.rect.x, largura_mapa - self.rect.width))
        self.rect.y = min(self.rect.y, altura_mapa - self.rect.height)