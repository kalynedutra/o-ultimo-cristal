# telas.py
# =====================================================================
#  TELAS DO JOGO (menu, game over, fase concluída e vitória)
#  Tudo aqui é só desenho: a lógica do jogo continua no main.py.
# =====================================================================

import math
import random
import pygame


LARGURA = 1260
ALTURA = 720


# =====================================================================
#  FERRAMENTAS DE DESENHO
# =====================================================================

def gradiente_vertical(tamanho, cor_topo, cor_base):
    largura, altura = tamanho
    superficie = pygame.Surface(tamanho)

    for y in range(altura):
        t = y / max(1, altura - 1)
        cor = tuple(
            int(a + (b - a) * t)
            for a, b in zip(cor_topo, cor_base)
        )
        pygame.draw.line(superficie, cor, (0, y), (largura, y))

    return superficie


def brilho_radial(raio, cor, alpha_max):
    """Círculo de luz que vai sumindo do centro para a borda."""
    superficie = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)

    for r in range(raio, 0, -3):
        alpha = int(alpha_max * (1 - r / raio) ** 2)
        pygame.draw.circle(superficie, (*cor, alpha), (raio, raio), r)

    return superficie


def texto_gradiente(texto, fonte, cor_topo, cor_base):
    base = fonte.render(texto, True, (255, 255, 255))
    grad = gradiente_vertical(base.get_size(), cor_topo, cor_base)
    base.blit(grad, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return base


def brilho_texto(texto, fonte, cor, expansao=40):
    """Halo bem desfocado para colocar atrás do título."""
    base = fonte.render(texto, True, cor)
    w, h = base.get_size()

    # margem extra para o desfoque não ser cortado nas bordas
    tela = pygame.Surface((w + expansao * 2, h + expansao * 2), pygame.SRCALPHA)
    tela.blit(base, (expansao, expansao))

    pequeno = pygame.transform.smoothscale(
        tela, (max(1, tela.get_width() // 14), max(1, tela.get_height() // 14))
    )
    pequeno = pygame.transform.smoothscale(
        pequeno, (max(1, tela.get_width() // 8), max(1, tela.get_height() // 8))
    )

    return pygame.transform.smoothscale(pequeno, tela.get_size())


def estrela_brilho(tela, centro, tamanho, cor, alpha=255):
    """Brilho de 4 pontas (o 'cintilar' dos cristais)."""
    cx, cy = centro
    fino = max(1, tamanho // 5)

    superficie = pygame.Surface(
        (tamanho * 2 + 2, tamanho * 2 + 2), pygame.SRCALPHA
    )
    c = tamanho + 1
    pontos = [
        (c, c - tamanho), (c + fino, c - fino),
        (c + tamanho, c), (c + fino, c + fino),
        (c, c + tamanho), (c - fino, c + fino),
        (c - tamanho, c), (c - fino, c - fino),
    ]
    pygame.draw.polygon(superficie, (*cor, alpha), pontos)
    tela.blit(superficie, (cx - c, cy - c))


def coracao(tamanho, cor):
    s = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    r = tamanho // 4
    pygame.draw.circle(s, cor, (r + 1, r + 1), r)
    pygame.draw.circle(s, cor, (tamanho - r - 2, r + 1), r)
    pygame.draw.polygon(
        s, cor,
        [(1, r + 3), (tamanho - 2, r + 3),
         (tamanho // 2, tamanho - 1)]
    )
    return s


def escurecer(sprite, fator):
    s = sprite.copy()
    f = int(255 * fator)
    s.fill((f, f, f, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return s


# =====================================================================
#  CLASSE DAS TELAS
# =====================================================================

class Telas:

    def __init__(self, tela):
        self.tela = tela
        self.tempo = 0
        self.tempo_estado = 0

        random.seed(7)  # estrelas sempre nos mesmos lugares

        # -------------------------------------------------------------
        # FONTES
        # -------------------------------------------------------------
        self.fonte_titulo = pygame.font.SysFont(
            "georgia,palatino linotype,garamond,times new roman",
            80, bold=True
        )
        self.fonte_titulo_menor = pygame.font.SysFont(
            "georgia,palatino linotype,garamond,times new roman",
            64, bold=True
        )
        self.fonte_subtitulo = pygame.font.SysFont("arial", 26, bold=True)
        self.fonte = pygame.font.SysFont("arial", 24)
        self.fonte_numero = pygame.font.SysFont("arial", 40, bold=True)
        self.fonte_rotulo = pygame.font.SysFont("arial", 17, bold=True)
        self.fonte_dica = pygame.font.SysFont("arial", 18)

        # -------------------------------------------------------------
        # SPRITES EM ALTA QUALIDADE (os originais são grandes)
        # -------------------------------------------------------------
        cristal = pygame.image.load("sprites/cristal.png").convert_alpha()
        princesa = pygame.image.load(
            "sprites/princesa_direita.png"
        ).convert_alpha()
        inimigo = pygame.image.load("sprites/inimigo.png").convert_alpha()

        self.cristal_grande = pygame.transform.smoothscale(cristal, (104, 104))
        self.cristal_medio = pygame.transform.smoothscale(cristal, (76, 76))
        self.cristal_pequeno = pygame.transform.smoothscale(cristal, (44, 44))
        self.cristal_icone = pygame.transform.smoothscale(cristal, (40, 40))

        self.princesa = pygame.transform.smoothscale(princesa, (95, 150))
        self.inimigo = pygame.transform.smoothscale(inimigo, (112, 92))
        self.inimigo_icone = pygame.transform.smoothscale(inimigo, (50, 41))
        self.coracao_icone = coracao(34, (235, 85, 135))

        # versão "apagada" do cristal para o game over
        self.cristal_apagado = escurecer(self.cristal_grande, 0.32)

        # -------------------------------------------------------------
        # FUNDOS (pré-renderizados: muito mais leve que redesenhar)
        # -------------------------------------------------------------
        self.fundo_menu = gradiente_vertical(
            (LARGURA, ALTURA), (7, 3, 22), (30, 13, 66)
        )
        self.fundo_derrota = gradiente_vertical(
            (LARGURA, ALTURA), (9, 3, 16), (42, 9, 38)
        )
        self.fundo_vitoria = gradiente_vertical(
            (LARGURA, ALTURA), (9, 5, 30), (46, 22, 82)
        )

        self.brilho_lilas = brilho_radial(360, (125, 60, 230), 120)
        self.brilho_vermelho = brilho_radial(320, (170, 40, 90), 105)
        self.brilho_dourado = brilho_radial(360, (230, 175, 90), 105)
        self.brilho_aura = brilho_radial(110, (170, 110, 255), 150)
        self.mote = brilho_radial(7, (190, 150, 255), 200)

        # -------------------------------------------------------------
        # ESTRELAS, MOTES DE LUZ E ESTILHAÇOS
        # -------------------------------------------------------------
        self.estrelas = [
            (
                random.randint(52, LARGURA - 52),
                random.randint(48, ALTURA - 48),
                random.choice((2, 2, 3)),
                random.uniform(0, 6.28),
                random.uniform(0.02, 0.07),
            )
            for _ in range(90)
        ]

        self.motes = [
            (
                random.randint(80, LARGURA - 80),
                random.uniform(0, ALTURA),
                random.uniform(0.25, 0.8),
                random.uniform(0, 6.28),
            )
            for _ in range(26)
        ]

        self.estilhacos = [
            (
                random.randint(300, 960),
                random.uniform(0, 600),
                random.uniform(0.4, 1.1),
                random.randint(4, 9),
            )
            for _ in range(16)
        ]

        # -------------------------------------------------------------
        # TÍTULOS PRÉ-RENDERIZADOS (gradiente + halo)
        # -------------------------------------------------------------
        self.titulos = {}

        self._criar_titulo(
            "menu", "O ÚLTIMO CRISTAL", self.fonte_titulo,
            (250, 238, 255), (165, 120, 235), (150, 80, 255)
        )
        self._criar_titulo(
            "game_over", "GAME OVER", self.fonte_titulo_menor,
            (245, 215, 250), (205, 85, 130), (200, 45, 110)
        )
        self._criar_titulo(
            "fase_completa", "FASE CONCLUÍDA", self.fonte_titulo_menor,
            (255, 248, 215), (200, 160, 255), (230, 180, 90)
        )
        self._criar_titulo(
            "vitoria", "A LUZ VOLTOU", self.fonte_titulo_menor,
            (255, 250, 220), (225, 180, 110), (235, 185, 90)
        )

    def _criar_titulo(self, chave, texto, fonte, topo, base, cor_halo):
        sombra = fonte.render(texto, True, (45, 20, 80))
        corpo = texto_gradiente(texto, fonte, topo, base)
        halo = brilho_texto(texto, fonte, cor_halo)
        self.titulos[chave] = (sombra, corpo, halo)

    # -----------------------------------------------------------------
    # CONTROLE DE TEMPO / ANIMAÇÃO
    # -----------------------------------------------------------------

    def reiniciar_animacao(self):
        """Chame quando a tela muda (reinicia o fade-in)."""
        self.tempo_estado = 0

    def _tick(self):
        self.tempo += 1
        self.tempo_estado += 1

    def _fade_in(self, duracao=36):
        if self.tempo_estado >= duracao:
            return

        alpha = int(255 * (1 - self.tempo_estado / duracao))
        veu = pygame.Surface((LARGURA, ALTURA))
        veu.set_alpha(alpha)
        self.tela.blit(veu, (0, 0))

    # -----------------------------------------------------------------
    # PEÇAS REUTILIZÁVEIS
    # -----------------------------------------------------------------

    def _estrelas(self):
        for x, y, tam, fase, vel in self.estrelas:
            brilho = 0.45 + 0.55 * math.sin(self.tempo * vel + fase)
            cor = (
                int(150 + 90 * brilho),
                int(110 + 90 * brilho),
                int(210 + 40 * brilho),
            )
            pygame.draw.rect(self.tela, cor, (x, y, tam, tam))

            if tam == 3 and brilho > 0.8:
                estrela_brilho(
                    self.tela, (x + 1, y + 1), 6, (210, 185, 255), 150
                )

    def _motes(self, area_topo=60, area_base=660):
        altura = area_base - area_topo

        for x, y0, vel, fase in self.motes:
            y = area_base - ((y0 + self.tempo * vel) % altura)
            dx = math.sin(self.tempo * 0.02 + fase) * 14

            alpha = 1 - abs((y - area_topo) / altura - 0.5) * 2
            mote = self.mote.copy()
            mote.set_alpha(int(255 * max(0, alpha)))
            self.tela.blit(mote, (x + dx - 7, y - 7))

    def _moldura(self, rect, cor_fundo, cor_borda, cor_interna):
        # fundo translúcido: deixa o brilho de trás aparecer um pouco
        fundo = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            fundo, (*cor_fundo, 228), fundo.get_rect(), border_radius=20
        )
        self.tela.blit(fundo, rect.topleft)

        pygame.draw.rect(self.tela, cor_borda, rect, 2, border_radius=20)
        pygame.draw.rect(
            self.tela, cor_interna, rect.inflate(-14, -14), 1,
            border_radius=16
        )

        # losangos ornamentais nos 4 cantos
        for cx, cy in (
            rect.topleft, rect.topright,
            rect.bottomleft, rect.bottomright
        ):
            pygame.draw.polygon(
                self.tela, cor_borda,
                [(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)]
            )
            pygame.draw.polygon(
                self.tela, cor_fundo,
                [(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)]
            )

    def _divisoria(self, centro_x, y, metade, cor):
        pygame.draw.line(
            self.tela, cor, (centro_x - metade, y), (centro_x - 18, y), 1
        )
        pygame.draw.line(
            self.tela, cor, (centro_x + 18, y), (centro_x + metade, y), 1
        )
        pygame.draw.polygon(
            self.tela, cor,
            [(centro_x, y - 6), (centro_x + 6, y),
             (centro_x, y + 6), (centro_x - 6, y)]
        )

    def _titulo(self, chave, centro, pulsar=True):
        sombra, corpo, halo = self.titulos[chave]
        rect = corpo.get_rect(center=centro)

        pulso = 0.5 + 0.5 * math.sin(self.tempo * 0.04) if pulsar else 1
        halo_atual = halo.copy()
        halo_atual.set_alpha(int(150 + 105 * pulso))
        self.tela.blit(
            halo_atual, halo.get_rect(center=centro)
        )

        self.tela.blit(sombra, (rect.x + 4, rect.y + 5))
        self.tela.blit(corpo, rect)

    def _texto_central(self, texto, fonte, cor, centro):
        render = fonte.render(texto, True, cor)
        self.tela.blit(render, render.get_rect(center=centro))

    def _plataforma_decorativa(self, x, y, largura):
        """Plataforma cinza igual à do jogo, com brilho lilás no topo."""
        pygame.draw.rect(self.tela, (120, 120, 120), (x, y, largura, 20))
        pygame.draw.rect(self.tela, (160, 140, 200), (x, y, largura, 3))

    # -----------------------------------------------------------------
    # MENU
    # -----------------------------------------------------------------

    def desenhar_menu(self, botoes):
        self._tick()
        t = self.tempo
        tela = self.tela

        tela.blit(self.fundo_menu, (0, 0))

        # brilho central pulsante
        glow = self.brilho_lilas
        glow.set_alpha(int(190 + 60 * math.sin(t * 0.03)))
        tela.blit(glow, glow.get_rect(center=(630, 250)))

        self._moldura(
            pygame.Rect(35, 30, 1190, 660),
            (20, 9, 44), (110, 62, 170), (52, 28, 82)
        )

        self._estrelas()
        self._motes()

        # cristal flutuante com aura e brilhos orbitando
        cy = 112 + math.sin(t * 0.05) * 7
        tela.blit(self.brilho_aura, self.brilho_aura.get_rect(center=(630, cy)))
        tela.blit(
            self.cristal_grande,
            self.cristal_grande.get_rect(center=(630, cy))
        )

        for i in range(3):
            ang = t * 0.025 + i * 2.094
            sx = 630 + math.cos(ang) * 68
            sy = cy + math.sin(ang) * 30
            brilho = 0.5 + 0.5 * math.sin(t * 0.1 + i)
            estrela_brilho(
                tela, (sx, sy), int(6 + 5 * brilho),
                (225, 205, 255), int(120 + 120 * brilho)
            )

        self._titulo("menu", (630, 236))

        self._texto_central(
            "E M   B U S C A   D A   L U Z",
            self.fonte_subtitulo, (175, 135, 225), (630, 300)
        )
        self._divisoria(630, 335, 190, (115, 65, 170))

        self._texto_central(
            "Encontre os cristais e restaure a luz.",
            self.fonte, (150, 120, 190), (630, 372)
        )

        for botao in botoes:
            botao.desenhar(tela)

        # princesa e inimigo, cada um em sua plataforma
        self._plataforma_decorativa(150, 600, 220)
        flutua = math.sin(t * 0.06) * 3
        tela.blit(self.princesa, (210, 450 + flutua * 0))
        tela.blit(
            self.cristal_pequeno,
            (320, 550 + math.sin(t * 0.05) * 6)
        )

        self._plataforma_decorativa(890, 600, 220)
        inimigo_virado = pygame.transform.flip(self.inimigo, True, False)
        tela.blit(inimigo_virado, (940, 508))
        tela.blit(
            self.cristal_pequeno,
            (1030, 535 + math.sin(t * 0.05 + 1.5) * 6)
        )

        self._texto_central(
            "Setas: mover   |   Espaço: pular   |   ESC: sair",
            self.fonte_dica, (110, 85, 150), (630, 660)
        )

        self._fade_in()

    # -----------------------------------------------------------------
    # TELA DE RESULTADO (base de game over, fase concluída e vitória)
    # -----------------------------------------------------------------

    def _coluna_stat(self, icone, valor, rotulo, centro_x, y):
        numero = self.fonte_numero.render(str(valor), True, (232, 208, 255))
        largura_icone = icone.get_width() + 12 if icone else 0
        largura_total = largura_icone + numero.get_width()
        x0 = centro_x - largura_total // 2

        if icone:
            self.tela.blit(
                icone, icone.get_rect(midleft=(x0, y + 22))
            )

        self.tela.blit(
            numero, numero.get_rect(midleft=(x0 + largura_icone, y + 22))
        )

        self._texto_central(
            rotulo, self.fonte_rotulo, (150, 120, 190), (centro_x, y + 68)
        )

    def _painel_stats(self, stats, y=312, cor_borda=(95, 55, 150)):
        largura_col = 210
        largura = largura_col * len(stats)
        painel = pygame.Rect(0, y, largura, 128)
        painel.centerx = 630

        pygame.draw.rect(self.tela, (15, 6, 32), painel, border_radius=15)
        pygame.draw.rect(self.tela, cor_borda, painel, 2, border_radius=15)

        for i, (icone, valor, rotulo) in enumerate(stats):
            centro_x = painel.left + largura_col * i + largura_col // 2
            self._coluna_stat(icone, valor, rotulo, centro_x, painel.top + 18)

            if i > 0:
                x = painel.left + largura_col * i
                pygame.draw.line(
                    self.tela, (62, 34, 100),
                    (x, painel.top + 20), (x, painel.bottom - 20), 1
                )

    def _tela_resultado(self, botoes, fundo, glow, chave_titulo, mensagem,
                        stats, frase, cores_moldura, cristal, rachado=False):
        self._tick()
        t = self.tempo
        tela = self.tela

        tela.blit(fundo, (0, 0))

        glow.set_alpha(int(170 + 60 * math.sin(t * 0.03)))
        tela.blit(glow, glow.get_rect(center=(630, 260)))

        self._moldura(pygame.Rect(250, 45, 760, 625), *cores_moldura)

        self._estrelas_discretas()

        # cristal do topo
        cy = 108 + (0 if rachado else math.sin(t * 0.05) * 6)
        if not rachado:
            tela.blit(
                self.brilho_aura, self.brilho_aura.get_rect(center=(630, cy))
            )
        tela.blit(cristal, cristal.get_rect(center=(630, cy)))

        if rachado:
            self._rachadura(630, cy)
            self._estilhacos_caindo()
        else:
            for i in range(3):
                ang = t * 0.025 + i * 2.094
                brilho = 0.5 + 0.5 * math.sin(t * 0.1 + i)
                estrela_brilho(
                    tela,
                    (630 + math.cos(ang) * 66, cy + math.sin(ang) * 28),
                    int(5 + 5 * brilho), (255, 235, 190),
                    int(120 + 120 * brilho)
                )

        self._titulo(chave_titulo, (630, 200))

        self._texto_central(mensagem, self.fonte, (170, 135, 205), (630, 262))

        self._painel_stats(stats)

        self._texto_central(frase, self.fonte, (150, 118, 188), (630, 464))

        for botao in botoes:
            botao.desenhar(tela)

        self._fade_in()

    def _estrelas_discretas(self):
        """Estrelas só dentro da moldura central (menos distração)."""
        for x, y, tam, fase, vel in self.estrelas:
            if 270 < x < 990 and 65 < y < 650:
                brilho = 0.4 + 0.6 * math.sin(self.tempo * vel + fase)
                cor = (
                    int(90 + 70 * brilho),
                    int(65 + 60 * brilho),
                    int(130 + 70 * brilho),
                )
                pygame.draw.rect(self.tela, cor, (x, y, 2, 2))

    def _rachadura(self, cx, cy):
        pontos = [
            (cx + 6, cy - 50), (cx - 6, cy - 24), (cx + 8, cy - 6),
            (cx - 8, cy + 14), (cx + 4, cy + 50),
        ]
        pygame.draw.lines(self.tela, (255, 110, 160), False, pontos, 3)
        pygame.draw.lines(self.tela, (255, 215, 235), False, pontos, 1)

    def _estilhacos_caindo(self):
        for x, y0, vel, tam in self.estilhacos:
            y = 140 + ((y0 + self.tempo * vel) % 500)
            alpha = int(200 * (1 - (y - 140) / 500))
            if alpha <= 0:
                continue

            s = pygame.Surface((tam * 2, tam * 2), pygame.SRCALPHA)
            pygame.draw.polygon(
                s, (170, 110, 220, alpha),
                [(tam, 0), (tam * 2, tam * 2), (0, tam * 2 - 2)]
            )
            self.tela.blit(s, (x + math.sin(self.tempo * 0.03 + x) * 8, y))

    # -----------------------------------------------------------------
    # TELAS DE RESULTADO
    # -----------------------------------------------------------------

    def desenhar_game_over(self, botoes, pontos, eliminacoes, fase_atual,
                           total_fases):
        self._tela_resultado(
            botoes,
            self.fundo_derrota,
            self.brilho_vermelho,
            "game_over",
            "A luz do cristal se apagou...",
            [
                (self.cristal_icone, pontos, "PONTOS"),
                (self.inimigo_icone, eliminacoes, "ELIMINAÇÕES"),
                (None, f"{fase_atual}/{total_fases}", "FASE ALCANÇADA"),
            ],
            "A jornada ainda não terminou.",
            ((22, 8, 36), (150, 55, 110), (70, 28, 70)),
            self.cristal_apagado,
            rachado=True,
        )

    def desenhar_fase_completa(self, botoes, nome_fase, pontos, eliminacoes,
                               vidas):
        self._tela_resultado(
            botoes,
            self.fundo_vitoria,
            self.brilho_dourado,
            "fase_completa",
            f"{nome_fase}: todos os fragmentos foram recuperados!",
            [
                (self.cristal_icone, pontos, "PONTOS"),
                (self.inimigo_icone, eliminacoes, "ELIMINAÇÕES"),
                (self.coracao_icone, vidas, "VIDAS"),
            ],
            "O próximo caminho já se ilumina.",
            ((22, 10, 46), (190, 150, 90), (84, 56, 100)),
            self.cristal_grande,
        )

    def desenhar_vitoria(self, botoes, pontos, eliminacoes, vidas):
        self._tela_resultado(
            botoes,
            self.fundo_vitoria,
            self.brilho_dourado,
            "vitoria",
            "O cristal fonte foi restaurado.",
            [
                (self.cristal_icone, pontos, "PONTOS"),
                (self.inimigo_icone, eliminacoes, "ELIMINAÇÕES"),
                (self.coracao_icone, vidas, "VIDAS"),
            ],
            "O universo voltou a brilhar.",
            ((22, 10, 46), (200, 160, 95), (90, 60, 105)),
            self.cristal_grande,
        )
