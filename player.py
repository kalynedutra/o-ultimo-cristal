from entidade import Entidade
import pygame
from utils import criar_fumaca_pulo, criar_poeira_passo, criar_impacto_queda


class Player(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 60, (200, 50, 50))

        # movimento
        self.velocidade = 5
        self.velx = 0
        self.vely = 0
        self.direcao = None

        # física
        self.gravidade = 0.5
        self.forca_pulo = -15
        self.no_chao = False

        # combate
        self.vidas = 3
        self.pontuacao = 0
        self.invencivel_timer = 0

        # partículas
        self.particulas = []
        self.contador_passos = 0
        self.estava_no_chao = True
        self.vely_antes_de_pousar = 0

    # =====================
    # DANO 
    # =====================
    def tomar_dano(self, dano, direcao):
        if self.invencivel_timer <= 0:
            self.vidas -= dano
            self.invencivel_timer = 60

            self.vely = -7

            self.rect.x += 10 * direcao

    # =====================
    # VISUAL: PISCAR VERMELHO
    # =====================
    def esta_piscando(self):
        if self.invencivel_timer <= 0:
            return False
        return (self.invencivel_timer // 6) % 2 == 0

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
        # EFEITO: POEIRA AO ANDAR
        # =====================
        if self.no_chao and self.velx != 0:
            self.contador_passos += 1
            if self.contador_passos >= 8:
                self.contador_passos = 0
                direcao_num = 1 if self.velx > 0 else -1
                self.particulas.extend(
                    criar_poeira_passo(self.rect.centerx, self.rect.bottom, direcao_num)
                )
        else:
            self.contador_passos = 0

        # =====================
        # PULO
        # =====================
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vely = self.forca_pulo
            self.no_chao = False

            # fumacinha ao pular
            self.particulas.extend(
                criar_fumaca_pulo(self.rect.centerx, self.rect.bottom)
            )

        # =====================
        # GRAVIDADE
        # =====================
        self.vely += self.gravidade
        if self.vely > 12:
            self.vely = 12

        if self.vely > 0:
            self.vely_antes_de_pousar = self.vely

        # =====================
        # MOVIMENTO Y + COLISÃO
        # =====================
        self.rect.y += self.vely

        self.estava_no_chao = self.no_chao
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
        # EFEITO: IMPACTO AO CAIR
        # =====================
        acabou_de_pousar = (not self.estava_no_chao) and self.no_chao

        if acabou_de_pousar:
            intensidade = min(self.vely_antes_de_pousar / 8, 2.5)

            if intensidade > 0.3:  
                self.particulas.extend(
                    criar_impacto_queda(self.rect.centerx, self.rect.bottom, intensidade)
                )

        # =====================
        # INIMIGOS
        # =====================
        for inimigo in inimigos:
            if not inimigo.ativo:
                continue

            if self.rect.colliderect(inimigo.rect):

                # STOMP 
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

        # =====================
        # UPDATE DAS PARTÍCULAS
        # =====================
        for p in self.particulas:
            p.update()
        self.particulas = [p for p in self.particulas if p.esta_viva()]