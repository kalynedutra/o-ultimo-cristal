import pygame
from player import Player
from cristal import Cristal
from inimigo import Inimigo

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.rodando = True

        # =====================
        # PLAYER
        # =====================
        self.player = Player(100, 100)

        # =====================
        # MAPA
        # =====================
        self.chao = pygame.Rect(0, 500, 800, 50)

        self.obstaculos = [
            pygame.Rect(200, 420, 120, 20),
            pygame.Rect(400, 350, 150, 20),
            pygame.Rect(600, 280, 100, 20),
            pygame.Rect(100, 300, 80, 80)
        ]

        # =====================
        # CRISTAIS
        # =====================
        self.cristais = [
            Cristal(150, 450),
            Cristal(250, 380),
            Cristal(450, 300),
            Cristal(650, 220)
        ]

        # =====================
        # INIMIGOS
        # =====================
        self.inimigos = [
            Inimigo(250, self.obstaculos[0].top - 32),
            Inimigo(450, self.obstaculos[1].top - 32),
            Inimigo(650, self.chao.top - 32)
        ]

        self.fonte = pygame.font.SysFont("Arial", 24)

    def executar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            teclas = pygame.key.get_pressed()

            # =====================
            # UPDATE PLAYER
            # =====================
            self.player.mover(
                teclas,
                800,
                600,
                self.chao,
                self.obstaculos,
                self.inimigos
            )

            # =====================
            # UPDATE INIMIGOS (IA)
            # =====================
            for inimigo in self.inimigos:
                if inimigo.ativo:
                    inimigo.update(self.player, self.obstaculos + [self.chao])

            # =====================
            # COLETA DE CRISTAIS
            # =====================
            for cristal in self.cristais:
                if cristal.coletar(self.player):
                    self.player.pontuacao += 1

            # =====================
            # RENDER
            # =====================
            self.tela.fill((10, 5, 30))

            # chão
            pygame.draw.rect(self.tela, (139, 69, 19), self.chao)

            # plataformas
            for obs in self.obstaculos:
                pygame.draw.rect(self.tela, (120, 120, 120), obs)

            # cristais
            for cristal in self.cristais:
                if not cristal.coletado:
                    cristal.desenhar(self.tela)

            # inimigos
            for inimigo in self.inimigos:
                if inimigo.ativo:
                    inimigo.desenhar(self.tela)

            # player
            self.player.desenhar(self.tela)

            # HUD
            hud = self.fonte.render(
                f"Pontos: {self.player.pontuacao}  Vidas: {self.player.vidas}",
                True,
                (255, 255, 255)
            )
            self.tela.blit(hud, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

Jogo().executar()