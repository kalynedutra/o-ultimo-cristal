import pygame

from player import Player
from cristal import Cristal
from inimigo import Inimigo
from botao import Botao
from telas import Telas
from utils import aplicar_tint_vermelho
from fases import FASES, CHAO


class Jogo:

    # =========================================
    # ESTADOS POSSÍVEIS DO JOGO
    # =========================================

    MENU = "menu"
    JOGANDO = "jogando"
    GAME_OVER = "game_over"
    FASE_COMPLETA = "fase_completa"
    VITORIA = "vitoria"

    # Frames de espera depois do último cristal (para ver a explosão)
    ESPERA_FIM_DE_FASE = 55

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
        # MAPA (preenchido por carregar_fase)
        # =========================================

        self.chao = CHAO
        self.obstaculos = []

        self.indice_fase = 0
        self.fase = None
        self.fundo_atual = None
        self.cache_fundos = {}
        self.timer_fim_fase = 0

        # Placar no início da fase (usado ao tentar novamente)
        self.pontos_inicio_fase = 0
        self.eliminacoes_inicio_fase = 0

        # =========================================
        # SPRITES
        # =========================================

        self.sprite_chao = pygame.image.load(
            "sprites/chao.png"
        ).convert_alpha()

        # chão: 2 pedaços de 630px cobrem a largura da tela (1260)
        self.sprite_chao = pygame.transform.smoothscale(
            self.sprite_chao,
            (630, 162)
        )

        # deixa a terra roxa, combinando com o fundo
        self.ajustar_cor_chao(self.sprite_chao)

        # plataformas (cache: uma imagem por largura)
        self.cache_plataformas = {}

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

        self.fonte_botao = pygame.font.SysFont(
            "arial",
            30
        )

        self.fonte = pygame.font.SysFont(
            "Arial",
            24
        )

        # =========================================
        # TELAS (menu, game over, etc.)
        # =========================================

        self.telas = Telas(self.tela)

        # =========================================
        # BOTÕES
        # =========================================

        # -----------------------------------------
        # MENU
        # -----------------------------------------

        self.botao_jogar = Botao(
            "Jogar", 490, 425, 280, 60, self.fonte_botao
        )

        self.botao_sair = Botao(
            "Sair", 490, 515, 280, 60, self.fonte_botao
        )

        # -----------------------------------------
        # TELAS DE RESULTADO (mesma posição nas 3)
        # -----------------------------------------

        self.botao_reiniciar = Botao(
            "Tentar novamente", 480, 500, 300, 60, self.fonte_botao
        )

        self.botao_proxima_fase = Botao(
            "Próxima fase", 480, 500, 300, 60, self.fonte_botao
        )

        self.botao_jogar_de_novo = Botao(
            "Jogar novamente", 480, 500, 300, 60, self.fonte_botao
        )

        self.botao_sair_game_over = Botao(
            "Sair", 480, 585, 300, 60, self.fonte_botao
        )

        self.botao_sair_fase = Botao(
            "Sair", 480, 585, 300, 60, self.fonte_botao
        )

        self.botao_sair_vitoria = Botao(
            "Sair", 480, 585, 300, 60, self.fonte_botao
        )

        # =========================================
        # ENTIDADES DA PARTIDA
        # =========================================

        self.player = None
        self.eliminacoes = 0

        self.cristais = []
        self.inimigos = []

    # =========================================
    # CONTROLE DE ESTADO
    # =========================================

    def mudar_estado(self, novo_estado):
        self.estado = novo_estado
        self.telas.reiniciar_animacao()

    # =========================================
    # FASES
    # =========================================

    def carregar_fase(self, indice):
        """Monta a fase `indice` (cristais e inimigos novinhos)."""

        self.indice_fase = indice
        self.fase = FASES[indice]()
        self.timer_fim_fase = 0
        self.fundo_atual = self.carregar_fundo(self.fase.fundo)

        self.obstaculos = self.fase.plataformas

        self.cristais = [
            Cristal(x, y) for x, y in self.fase.cristais
        ]

        self.inimigos = [
            Inimigo(x, y) for x, y in self.fase.inimigos
        ]

        # princesa volta ao ponto de partida da fase
        self.player.rect.topleft = self.fase.spawn
        self.player.vely = 0
        self.player.invencivel_timer = 0
        self.player.particulas = []

        self.pontos_inicio_fase = self.player.pontuacao
        self.eliminacoes_inicio_fase = self.eliminacoes

    def ajustar_cor_chao(self, sprite):
        """Muda a terra marrom do chao.png para um tom roxo-avermelhado
        (a grama continua verde), para combinar com o fundo."""

        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                r, g, b, a = sprite.get_at((x, y))

                if a > 0 and r > g + 12 and r >= b:
                    sprite.set_at((x, y), (
                        int(r * 0.85),
                        int(g * 0.78),
                        min(255, int(b + 0.6 * (r - b))),
                        a
                    ))

    def superficie_plataforma(self, largura, altura):
        """Imagem do chao.png esticada para uma plataforma."""

        chave = (largura, altura)

        if chave not in self.cache_plataformas:
            self.cache_plataformas[chave] = pygame.transform.smoothscale(
                self.sprite_chao,
                (largura, altura)
            )

        return self.cache_plataformas[chave]

    def carregar_fundo(self, caminho):
        """Carrega a imagem de fundo da fase, preenchendo a tela inteira
        (sem distorcer: escala pela altura e corta o excesso do centro)."""

        if not caminho:
            return None

        if caminho not in self.cache_fundos:
            img = pygame.image.load(caminho).convert()
            larg, alt = img.get_size()
            escala = max(1260 / larg, 720 / alt)
            novo = (round(larg * escala), round(alt * escala))
            img = pygame.transform.smoothscale(img, novo)
            recorte = pygame.Rect(0, 0, 1260, 720)
            recorte.center = img.get_rect().center
            self.cache_fundos[caminho] = img.subsurface(recorte).copy()

        return self.cache_fundos[caminho]

    def fase_concluida(self):
        return bool(self.cristais) and all(
            c.coletado for c in self.cristais
        )

    # =========================================
    # INÍCIO / REINÍCIO DA PARTIDA
    # =========================================

    def iniciar_partida(self):
        """Começa o jogo do zero, pela primeira fase."""

        self.player = Player(*FASES[0]().spawn)
        self.eliminacoes = 0

        self.carregar_fase(0)

        self.mudar_estado(self.JOGANDO)

    def tentar_fase_novamente(self):
        """Depois do game over: refaz a fase com 3 vidas novas."""

        pontos = self.pontos_inicio_fase
        eliminacoes = self.eliminacoes_inicio_fase

        self.player = Player(*self.fase.spawn)
        self.player.pontuacao = pontos
        self.eliminacoes = eliminacoes

        self.carregar_fase(self.indice_fase)

        self.mudar_estado(self.JOGANDO)

    def proxima_fase(self):
        self.carregar_fase(self.indice_fase + 1)
        self.mudar_estado(self.JOGANDO)

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

            # ESC sai do jogo
            if (
                evento.type == pygame.KEYDOWN
                and evento.key == pygame.K_ESCAPE
            ):
                self.rodando = False

            # ENTER aciona o botão principal da tela
            enter = (
                evento.type == pygame.KEYDOWN
                and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
            )

            # =====================================
            # MENU
            # =====================================

            if self.estado == self.MENU:

                if self.botao_jogar.clicado(evento) or enter:
                    self.iniciar_partida()

                elif self.botao_sair.clicado(evento):
                    self.rodando = False

            # =====================================
            # GAME OVER
            # =====================================

            elif self.estado == self.GAME_OVER:

                if self.botao_reiniciar.clicado(evento) or enter:
                    self.tentar_fase_novamente()

                elif self.botao_sair_game_over.clicado(evento):
                    self.rodando = False

            # =====================================
            # FASE CONCLUÍDA
            # =====================================

            elif self.estado == self.FASE_COMPLETA:

                if self.botao_proxima_fase.clicado(evento) or enter:
                    self.proxima_fase()

                elif self.botao_sair_fase.clicado(evento):
                    self.rodando = False

            # =====================================
            # VITÓRIA
            # =====================================

            elif self.estado == self.VITORIA:

                if self.botao_jogar_de_novo.clicado(evento) or enter:
                    self.iniciar_partida()

                elif self.botao_sair_vitoria.clicado(evento):
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

            self.mudar_estado(self.GAME_OVER)

            return

        # =========================================
        # FIM DA FASE
        # =========================================

        if self.timer_fim_fase == 0 and self.fase_concluida():

            self.timer_fim_fase = self.ESPERA_FIM_DE_FASE

        elif self.timer_fim_fase > 0:

            self.timer_fim_fase -= 1

            if self.timer_fim_fase == 0:

                if self.indice_fase + 1 < len(FASES):
                    self.mudar_estado(self.FASE_COMPLETA)
                else:
                    self.mudar_estado(self.VITORIA)

    # =========================================
    # DESENHO
    # =========================================

    def desenhar(self):

        if self.estado == self.MENU:

            self.telas.desenhar_menu(
                [self.botao_jogar, self.botao_sair]
            )

        elif self.estado == self.JOGANDO:

            self.desenhar_jogo()

        elif self.estado == self.GAME_OVER:

            self.telas.desenhar_game_over(
                [self.botao_reiniciar, self.botao_sair_game_over],
                self.player.pontuacao,
                self.eliminacoes,
                self.indice_fase + 1,
                len(FASES)
            )

        elif self.estado == self.FASE_COMPLETA:

            self.telas.desenhar_fase_completa(
                [self.botao_proxima_fase, self.botao_sair_fase],
                self.fase.nome,
                self.player.pontuacao,
                self.eliminacoes,
                self.player.vidas
            )

        elif self.estado == self.VITORIA:

            self.telas.desenhar_vitoria(
                [self.botao_jogar_de_novo, self.botao_sair_vitoria],
                self.player.pontuacao,
                self.eliminacoes,
                self.player.vidas
            )

    # =========================================
    # DESENHO DO JOGO
    # =========================================

    def desenhar_jogo(self):

        if self.fundo_atual:
            self.tela.blit(self.fundo_atual, (0, 0))
        else:
            self.tela.fill((10, 5, 30))

        # =========================================
        # CHÃO
        # =========================================

        # base escura que cobre o chão pintado no fundo
        pygame.draw.rect(
            self.tela,
            (14, 7, 12),
            (0, self.chao.top, 1260, 720 - self.chao.top)
        )

        # a linha da grama fica exatamente no topo do chão (colisão)
        topo_chao = self.chao.top - round(
            self.sprite_chao.get_height() * 0.2
        )

        for x in range(0, 1260, self.sprite_chao.get_width()):

            self.tela.blit(
                self.sprite_chao,
                (x, topo_chao)
            )

        # =========================================
        # PLATAFORMAS
        # =========================================

        for obs in self.obstaculos:

            altura = obs.height + 12

            self.tela.blit(
                self.superficie_plataforma(obs.width, altura),
                (obs.x, obs.y - round(altura * 0.2))
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

        coletados = sum(1 for c in self.cristais if c.coletado)

        hud = self.fonte.render(
            f"{self.fase.nome}   "
            f"Cristais: {coletados}/{len(self.cristais)}   "
            f"Pontos: {self.player.pontuacao}   "
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