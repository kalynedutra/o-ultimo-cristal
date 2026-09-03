import pygame

from player import Player
from cristal import Cristal
from inimigo import Inimigo
from botao import Botao
from utils import aplicar_tint_vermelho


class Jogo:

    # =========================================
    # ESTADOS POSSÍVEIS DO JOGO
    # =========================================

    MENU = "menu"
    JOGANDO = "jogando"
    GAME_OVER = "game_over"

    # =========================================
    # INICIALIZAÇÃO
    # =========================================

    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((1260, 720))
        pygame.display.set_caption("O Último Cristal")

        self.clock = pygame.time.Clock()
        self.rodando = True

        self.estado = self.MENU

        # =========================================
        # MAPA
        # =========================================

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

        # =========================================
        # SPRITES
        # =========================================

        self.sprite_chao = pygame.image.load(
            "sprites/chao.png"
        ).convert_alpha()

        self.sprite_chao = pygame.transform.scale(
            self.sprite_chao,
            (273, 70)
        )

        self.sprite_player = pygame.image.load(
            "sprites/princesa_direita.png"
        ).convert_alpha()

        self.sprite_player = pygame.transform.scale(
            self.sprite_player,
            (50, 60)
        )

        self.sprite_player_esquerda = pygame.transform.flip(
            self.sprite_player,
            True,
            False
        )

        self.sprite_player_dano = aplicar_tint_vermelho(
            self.sprite_player
        )

        self.sprite_player_esquerda_dano = aplicar_tint_vermelho(
            self.sprite_player_esquerda
        )

        self.sprite_inimigo_esquerda = pygame.image.load(
            "sprites/inimigo.png"
        ).convert_alpha()

        self.sprite_inimigo_esquerda = pygame.transform.scale(
            self.sprite_inimigo_esquerda,
            (39, 32)
        )

        self.sprite_inimigo_direita = pygame.transform.flip(
            self.sprite_inimigo_esquerda,
            True,
            False
        )

        self.sprite_cristal = pygame.image.load(
            "sprites/cristal.png"
        ).convert_alpha()

        self.sprite_cristal = pygame.transform.scale(
            self.sprite_cristal,
            (30, 30)
        )

        # =========================================
        # FONTES
        # =========================================

        self.fonte_titulo = pygame.font.SysFont(
            "arial",
            70,
            bold=True
        )

        self.fonte_botao = pygame.font.SysFont(
            "arial",
            30
        )

        self.fonte = pygame.font.SysFont(
            "Arial",
            24
        )

        # =========================================
        # BOTÕES
        # =========================================

        largura_botao = 260
        altura_botao = 60

        centro_x = 1260 // 2 - largura_botao // 2

        # -----------------------------------------
        # MENU
        # -----------------------------------------

        self.botao_jogar = Botao(
            "Jogar",
            centro_x,
            520,
            largura_botao,
            altura_botao,
            self.fonte_botao
        )

        self.botao_sair = Botao(
            "Sair",
            centro_x,
            595,
            largura_botao,
            altura_botao,
            self.fonte_botao
        )

        # -----------------------------------------
        # GAME OVER
        # -----------------------------------------

        self.botao_reiniciar = Botao(
            "Jogar novamente",
            centro_x - 40,
            490,
            largura_botao + 80,
            altura_botao,
            self.fonte_botao
        )

        self.botao_sair_game_over = Botao(
            "Sair",
            centro_x,
            565,
            largura_botao,
            altura_botao,
            self.fonte_botao
        )

        # =========================================
        # ENTIDADES DA PARTIDA
        # =========================================

        self.player = None
        self.eliminacoes = 0

        self.cristais = []
        self.inimigos = []

    # =========================================
    # INÍCIO / REINÍCIO DA PARTIDA
    # =========================================

    def iniciar_partida(self):

        self.player = Player(50, 100)

        self.eliminacoes = 0

        # =========================================
        # CRISTAIS
        # =========================================

        self.cristais = [
            Cristal(200, 420),
            Cristal(450, 370),
            Cristal(690, 310),
            Cristal(970, 380),
            Cristal(325, 250),
            Cristal(585, 190),
            Cristal(890, 240),
            Cristal(1125, 140),
        ]

        # =========================================
        # INIMIGOS
        # =========================================

        self.inimigos = [
            Inimigo(
                220,
                self.obstaculos[0].top - 32
            ),

            Inimigo(
                450,
                self.obstaculos[1].top - 32
            ),

            Inimigo(
                680,
                self.obstaculos[2].top - 32
            ),

            Inimigo(
                950,
                self.obstaculos[3].top - 32
            ),

            Inimigo(
                550,
                self.obstaculos[5].top - 32
            ),

            Inimigo(
                1120,
                self.obstaculos[7].top - 32
            ),
        ]

        self.estado = self.JOGANDO

    # =========================================
    # LOOP PRINCIPAL
    # =========================================

    def executar(self):

        while self.rodando:

            self.tratar_eventos()

            if self.estado == self.JOGANDO:
                self.atualizar()

            self.desenhar()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    # =========================================
    # EVENTOS
    # =========================================

    def tratar_eventos(self):

        for evento in pygame.event.get():

            # Fechar janela
            if evento.type == pygame.QUIT:
                self.rodando = False

            # =====================================
            # MENU
            # =====================================

            if self.estado == self.MENU:

                if self.botao_jogar.clicado(evento):
                    self.iniciar_partida()

                elif self.botao_sair.clicado(evento):
                    self.rodando = False

            # =====================================
            # GAME OVER
            # =====================================

            elif self.estado == self.GAME_OVER:

                if self.botao_reiniciar.clicado(evento):
                    self.iniciar_partida()

                elif self.botao_sair_game_over.clicado(evento):
                    self.rodando = False

    # =========================================
    # UPDATE DO JOGO
    # =========================================

    def atualizar(self):

        teclas = pygame.key.get_pressed()

        # =========================================
        # PLAYER
        # =========================================

        self.player.mover(
            teclas,
            1260,
            720,
            self.chao,
            self.obstaculos,
            self.inimigos
        )

        # =========================================
        # INIMIGOS
        # =========================================

        for inimigo in self.inimigos:

            if inimigo.ativo:

                inimigo.update(
                    self.player,
                    self.obstaculos + [self.chao],
                    self.eliminacoes
                )

            else:

                inimigo.atualizar_particulas()

                if not inimigo.contado:

                    self.eliminacoes += 1

                    inimigo.contado = True

        # =========================================
        # CRISTAIS
        # =========================================

        for cristal in self.cristais:

            cristal.update()

            if cristal.coletar(self.player):

                self.player.pontuacao += 1

            if cristal.coletado:

                cristal.atualizar_particulas()

        # =========================================
        # GAME OVER
        # =========================================

        if self.player.vidas <= 0:

            self.estado = self.GAME_OVER

    # =========================================
    # DESENHO
    # =========================================

    def desenhar(self):

        if self.estado == self.MENU:

            self.desenhar_menu()

        elif self.estado == self.JOGANDO:

            self.desenhar_jogo()

        elif self.estado == self.GAME_OVER:

            self.desenhar_game_over()

    # =========================================
    # MENU
    # =========================================

    def desenhar_menu(self):

        # =========================================
        # FUNDO
        # =========================================

        self.tela.fill((8, 4, 25))

        for y in range(720):

            intensidade = int(18 * (y / 720))

            pygame.draw.line(
                self.tela,
                (
                    8 + intensidade // 3,
                    4 + intensidade // 4,
                    25 + intensidade
                ),
                (0, y),
                (1260, y)
            )

        # =========================================
        # BRILHO CENTRAL
        # =========================================

        brilho = pygame.Surface(
            (700, 500),
            pygame.SRCALPHA
        )

        for raio in range(240, 20, -20):

            alpha = max(
                2,
                int(35 * (1 - raio / 250))
            )

            pygame.draw.circle(
                brilho,
                (120, 55, 220, alpha),
                (350, 250),
                raio
            )

        self.tela.blit(
            brilho,
            (280, 130)
        )

        # =========================================
        # ESTRELAS
        # =========================================

        estrelas = [
            (75, 90),
            (140, 155),
            (220, 75),
            (310, 125),
            (405, 65),
            (500, 155),
            (760, 80),
            (850, 145),
            (940, 70),
            (1040, 130),
            (1150, 85),

            (90, 600),
            (180, 650),
            (290, 580),
            (390, 650),
            (850, 620),
            (960, 570),
            (1080, 640),
            (1170, 590)
        ]

        for x, y in estrelas:

            pygame.draw.rect(
                self.tela,
                (175, 125, 235),
                (x, y, 2, 2)
            )

        # =========================================
        # MOLDURA
        # =========================================

        moldura = pygame.Rect(
            35,
            30,
            1190,
            660
        )

        pygame.draw.rect(
            self.tela,
            (24, 11, 50),
            moldura,
            border_radius=18
        )

        pygame.draw.rect(
            self.tela,
            (100, 55, 155),
            moldura,
            2,
            border_radius=18
        )

        pygame.draw.rect(
            self.tela,
            (52, 28, 82),
            moldura.inflate(-12, -12),
            1,
            border_radius=15
        )

        # =========================================
        # CRISTAL DO TOPO
        # =========================================

        cristal_topo = pygame.transform.scale(
            self.sprite_cristal,
            (65, 65)
        )

        self.tela.blit(
            cristal_topo,
            (598, 48)
        )

        # =========================================
        # TÍTULO
        # =========================================

        titulo_sombra = self.fonte_titulo.render(
            "O ÚLTIMO CRISTAL",
            True,
            (70, 35, 110)
        )

        titulo = self.fonte_titulo.render(
            "O ÚLTIMO CRISTAL",
            True,
            (225, 205, 250)
        )

        titulo_rect = titulo.get_rect(
            center=(630, 145)
        )

        self.tela.blit(
            titulo_sombra,
            (
                titulo_rect.x + 4,
                titulo_rect.y + 4
            )
        )

        self.tela.blit(
            titulo,
            titulo_rect
        )

        # =========================================
        # SUBTÍTULO
        # =========================================

        subtitulo = self.fonte.render(
            "EM BUSCA DE LUZ",
            True,
            (165, 125, 210)
        )

        subtitulo_rect = subtitulo.get_rect(
            center=(630, 210)
        )

        self.tela.blit(
            subtitulo,
            subtitulo_rect
        )

        pygame.draw.line(
            self.tela,
            (105, 55, 160),
            (450, 240),
            (810, 240),
            1
        )

        # =========================================
        # FRASE
        # =========================================

        frase = self.fonte.render(
            "Encontre os cristais e restaure a luz.",
            True,
            (145, 115, 185)
        )

        frase_rect = frase.get_rect(
            center=(630, 475)
        )

        self.tela.blit(
            frase,
            frase_rect
        )

        # =========================================
        # BOTÕES
        # =========================================

        self.botao_jogar.desenhar(
            self.tela
        )

        self.botao_sair.desenhar(
            self.tela
        )

        # =========================================
        # CRISTAIS DECORATIVOS
        # =========================================

        cristal_pequeno = pygame.transform.scale(
            self.sprite_cristal,
            (45, 45)
        )

        self.tela.blit(
            cristal_pequeno,
            (70, 605)
        )

        self.tela.blit(
            cristal_pequeno,
            (1145, 605)
        )

    # =========================================
    # GAME OVER
    # =========================================

    def desenhar_game_over(self):

        # =========================================
        # FUNDO
        # =========================================

        self.tela.fill((8, 3, 22))

        for y in range(720):

            intensidade = int(
                15 * (y / 720)
            )

            pygame.draw.line(
                self.tela,
                (
                    8 + intensidade // 3,
                    3 + intensidade // 5,
                    22 + intensidade
                ),
                (0, y),
                (1260, y)
            )

        # =========================================
        # BRILHO CENTRAL
        # =========================================

        brilho = pygame.Surface(
            (700, 500),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            brilho,
            (65, 30, 110, 70),
            (0, 0, 700, 500)
        )

        self.tela.blit(
            brilho,
            (280, 100)
        )

        # =========================================
        # MOLDURA
        # =========================================

        moldura = pygame.Rect(
            250,
            45,
            760,
            625
        )

        pygame.draw.rect(
            self.tela,
            (22, 9, 45),
            moldura,
            border_radius=20
        )

        pygame.draw.rect(
            self.tela,
            (100, 55, 160),
            moldura,
            2,
            border_radius=20
        )

        pygame.draw.rect(
            self.tela,
            (50, 25, 80),
            moldura.inflate(-12, -12),
            1,
            border_radius=17
        )

        # =========================================
        # CRISTAL DO TOPO
        # =========================================

        cristal_topo = pygame.transform.scale(
            self.sprite_cristal,
            (65, 65)
        )

        cristal_topo = cristal_topo.copy()

        cristal_topo.fill(
            (75, 40, 120, 255),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        self.tela.blit(
            cristal_topo,
            (598, 65)
        )

        # =========================================
        # TÍTULO
        # =========================================

        titulo_sombra = self.fonte_titulo.render(
            "GAME OVER",
            True,
            (65, 30, 95)
        )

        titulo = self.fonte_titulo.render(
            "GAME OVER",
            True,
            (215, 180, 245)
        )

        titulo_rect = titulo.get_rect(
            center=(630, 175)
        )

        self.tela.blit(
            titulo_sombra,
            (
                titulo_rect.x + 4,
                titulo_rect.y + 4
            )
        )

        self.tela.blit(
            titulo,
            titulo_rect
        )

        # =========================================
        # MENSAGEM
        # =========================================

        mensagem = self.fonte.render(
            "A luz do cristal se apagou...",
            True,
            (160, 125, 195)
        )

        mensagem_rect = mensagem.get_rect(
            center=(630, 250)
        )

        self.tela.blit(
            mensagem,
            mensagem_rect
        )

        # =========================================
        # PAINEL DE RESULTADOS
        # =========================================

        painel = pygame.Rect(
            390,
            295,
            480,
            130
        )

        pygame.draw.rect(
            self.tela,
            (16, 7, 34),
            painel,
            border_radius=15
        )

        pygame.draw.rect(
            self.tela,
            (90, 50, 145),
            painel,
            2,
            border_radius=15
        )

        # =========================================
        # DIVISÓRIA
        # =========================================

        pygame.draw.line(
            self.tela,
            (65, 35, 105),
            (630, 315),
            (630, 405),
            1
        )

        # =========================================
        # CRISTAIS ENCONTRADOS
        # =========================================

        cristal_resultado = pygame.transform.scale(
            self.sprite_cristal,
            (38, 38)
        )

        self.tela.blit(
            cristal_resultado,
            (430, 315)
        )

        numero_cristais = self.fonte_botao.render(
            str(self.player.pontuacao),
            True,
            (225, 195, 255)
        )

        self.tela.blit(
            numero_cristais,
            (475, 317)
        )

        texto_cristais = self.fonte.render(
            "CRISTAIS",
            True,
            (145, 115, 180)
        )

        self.tela.blit(
            texto_cristais,
            (425, 365)
        )

        # =========================================
        # ELIMINAÇÕES
        # =========================================

        numero_eliminacoes = self.fonte_botao.render(
            str(self.eliminacoes),
            True,
            (225, 195, 255)
        )

        numero_rect = numero_eliminacoes.get_rect(
            center=(680, 330)
        )

        self.tela.blit(
            numero_eliminacoes,
            numero_rect
        )

        texto_eliminacoes = self.fonte.render(
            "ELIMINAÇÕES",
            True,
            (145, 115, 180)
        )

        texto_eliminacoes_rect = texto_eliminacoes.get_rect(
            center=(750, 375)
        )

        self.tela.blit(
            texto_eliminacoes,
            texto_eliminacoes_rect
        )

        # =========================================
        # FRASE
        # =========================================

        frase = self.fonte.render(
            "A jornada ainda não terminou.",
            True,
            (145, 110, 180)
        )

        frase_rect = frase.get_rect(
            center=(630, 455)
        )

        self.tela.blit(
            frase,
            frase_rect
        )

        # =========================================
        # BOTÕES
        # =========================================

        self.botao_reiniciar.desenhar(
            self.tela
        )

        self.botao_sair_game_over.desenhar(
            self.tela
        )

        # =========================================
        # CRISTAIS DECORATIVOS
        # =========================================

        cristal_pequeno = pygame.transform.scale(
            self.sprite_cristal,
            (50, 50)
        )

        self.tela.blit(
            cristal_pequeno,
            (325, 570)
        )

        self.tela.blit(
            cristal_pequeno,
            (885, 570)
        )

    # =========================================
    # DESENHO DO JOGO
    # =========================================

    def desenhar_jogo(self):

        self.tela.fill((10, 5, 30))

        # =========================================
        # CHÃO
        # =========================================

        pygame.draw.rect(
            self.tela,
            (139, 69, 19),
            self.chao
        )

        for x in range(
            self.chao.left,
            self.chao.right,
            100
        ):

            self.tela.blit(
                self.sprite_chao,
                (x, self.chao.top - 15)
            )

        # =========================================
        # PLATAFORMAS
        # =========================================

        for obs in self.obstaculos:

            pygame.draw.rect(
                self.tela,
                (120, 120, 120),
                obs
            )

        # =========================================
        # CRISTAIS
        # =========================================

        for cristal in self.cristais:

            if not cristal.coletado:

                self.tela.blit(
                    self.sprite_cristal,
                    (
                        cristal.rect.x - 5,
                        cristal.rect.y - 10
                    )
                )

            else:

                cristal.desenhar_particulas(
                    self.tela
                )

        # =========================================
        # INIMIGOS
        # =========================================

        for inimigo in self.inimigos:

            if inimigo.ativo:

                if inimigo.direcao == Inimigo.ESQUERDA:

                    sprite = self.sprite_inimigo_esquerda

                else:

                    sprite = self.sprite_inimigo_direita

                x = (
                    inimigo.rect.centerx
                    - sprite.get_width() // 2
                )

                y = (
                    inimigo.rect.bottom
                    - sprite.get_height()
                )

                self.tela.blit(
                    sprite,
                    (x, y)
                )

            else:

                inimigo.desenhar_particulas(
                    self.tela
                )

        # =========================================
        # PLAYER
        # =========================================

        if self.player.direcao == "ESQUERDA":

            sprite_atual = (
                self.sprite_player_esquerda_dano
                if self.player.esta_piscando()
                else self.sprite_player_esquerda
            )

        else:

            sprite_atual = (
                self.sprite_player_dano
                if self.player.esta_piscando()
                else self.sprite_player
            )

        self.tela.blit(
            sprite_atual,
            self.player.rect
        )

        # =========================================
        # PARTÍCULAS DO PLAYER
        # =========================================

        for p in self.player.particulas:

            p.desenhar(
                self.tela
            )

        # =========================================
        # HUD
        # =========================================

        hud = self.fonte.render(
            f"Pontos: {self.player.pontuacao}  "
            f"Vidas: {self.player.vidas}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            hud,
            (10, 10)
        )


# =============================================
# INICIAR JOGO
# =============================================

if __name__ == "__main__":
    Jogo().executar()