import pygame
from player import Player
from cristal import Cristal
from inimigo import Inimigo

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((1260, 720))
        self.clock = pygame.time.Clock()
        self.rodando = True

        # =====================
        # PLAYER
        # =====================
        self.player = Player(50, 100)

        # =====================
        # MAPA
        # =====================
        self.chao = pygame.Rect(0, 540, 1260, 50)

        self.obstaculos = [
            pygame.Rect(140, 450, 170, 20),
            pygame.Rect(380, 400, 140, 20),
            pygame.Rect(600, 340, 180, 20),
            pygame.Rect(900, 410, 160, 20),
            pygame.Rect(250, 280, 150, 20),
            pygame.Rect(500, 220, 170, 20),
            pygame.Rect(800, 270, 180, 20),
            pygame.Rect(1050, 170, 150, 20),
        ]

        # =====================
        # CRISTAIS
        # =====================
        self.cristais = [
            Cristal(200, 420),
            Cristal(450, 370),
            Cristal(690, 310),
            Cristal(970, 380),
            Cristal(325, 250),
            Cristal(585, 190),
            Cristal(890, 240),
            Cristal(1125, 140)
        ]

        # =====================
        # INIMIGOS
        # =====================
        self.inimigos = [
            Inimigo(220,self.obstaculos[0].top - 32),
            Inimigo(450,self.obstaculos[1].top - 32),
            Inimigo(680,self.obstaculos[2].top - 32),
            Inimigo(950,self.obstaculos[3].top - 32),
            Inimigo(550,self.obstaculos[5].top - 32),
            Inimigo(1120,self.obstaculos[7].top - 32)
        ]

        #=====================
        # SPRITES
        #=====================
        self.sprite_chao = pygame.image.load("sprites/chao.png").convert_alpha()
        self.sprite_chao = pygame.transform.scale(self.sprite_chao,(273, 70))

        self.sprite_player = pygame.image.load("sprites/princesa_direita.jpeg").convert_alpha()
        self.sprite_player = pygame.transform.scale(self.sprite_player, (50, 60))
        self.sprite_player_esquerda = pygame.transform.flip(self.sprite_player,True, False)

        self.sprite_inimigo_esquerda = pygame.image.load("sprites/inimigo.png").convert_alpha()

        self.sprite_inimigo_esquerda = pygame.transform.scale(self.sprite_inimigo_esquerda,(39, 32))

        self.sprite_inimigo_direita = pygame.transform.flip(self.sprite_inimigo_esquerda,True,False)

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
                1260,
                720,
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
            for x in range(self.chao.left, self.chao.right, 100):
                self.tela.blit(self.sprite_chao, (x, self.chao.top - 15))

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
                
                    if inimigo.direcao == Inimigo.ESQUERDA:
                        sprite = self.sprite_inimigo_esquerda
                    else:
                        sprite = self.sprite_inimigo_direita

                    x = inimigo.rect.centerx - sprite.get_width() // 2
                    y = inimigo.rect.bottom - sprite.get_height()

                    self.tela.blit(sprite, (x, y))

            # player
            self.player.desenhar(self.tela)
            if self.player.direcao == "ESQUERDA":
                self.tela.blit(self.sprite_player_esquerda, self.player)
            else:
                self.tela.blit(self.sprite_player, self.player)


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