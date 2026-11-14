
# =====================================================================
#  FASES DO JOGO "O ÚLTIMO CRISTAL"
# =====================================================================

import pygame

LARGURA_TELA = 1260
ALTURA_TELA = 720

# Retângulo do chão (igual para todas as fases)
CHAO = pygame.Rect(0, 540, LARGURA_TELA, 50)

ALTURA_INIMIGO = 32
ALTURA_CRISTAL_ACIMA = 30


# =====================================================================
#  FERRAMENTAS PARA MONTAR FASES
# =====================================================================

def plataforma(x, y, largura, altura=20):
    """Cria uma plataforma (retângulo) do mesmo estilo das fases atuais."""
    return pygame.Rect(x, y, largura, altura)


def cristal_sobre(plat, deslocamento_x):
    """Posição (x, y) de um cristal flutuando acima de uma plataforma."""
    return (plat.x + deslocamento_x, plat.top - ALTURA_CRISTAL_ACIMA)


def inimigo_sobre(plat, deslocamento_x):
    """Posição (x, y) de um inimigo em pé em cima de uma plataforma."""
    return (plat.x + deslocamento_x, plat.top - ALTURA_INIMIGO)


class Fase:
    """
    Descrição de uma fase. Guarda apenas DADOS (posições).
    Os objetos Cristal e Inimigo são criados na hora de jogar, para que
    reiniciar a fase sempre comece do zero.
    """

    def __init__(self, nome, subtitulo, plataformas, cristais, inimigos,
                 spawn=(50, 100)):
        self.nome = nome
        self.subtitulo = subtitulo
        self.plataformas = plataformas
        self.cristais = cristais      # lista de (x, y)
        self.inimigos = inimigos      # lista de (x, y)
        self.spawn = spawn            # onde a princesa nasce
        self.validar()

    def validar(self):
        """Avisa no terminal se algo na fase estiver fora do mapa."""
        for i, p in enumerate(self.plataformas):
            if p.left < 0 or p.right > LARGURA_TELA or p.top < 80:
                print(f"[AVISO] {self.nome}: plataforma {i} "
                      f"está fora da área segura ({p}).")
        if not self.cristais:
            print(f"[AVISO] {self.nome}: a fase não tem nenhum cristal, "
                  f"ela terminaria imediatamente.")
        for x, y in self.cristais:
            if not (0 <= x <= LARGURA_TELA - 20 and 0 <= y <= CHAO.top):
                print(f"[AVISO] {self.nome}: cristal em ({x}, {y}) "
                      f"fora do mapa.")


# ==================================
#  FASE 1  
# ==================================
def criar_fase_1():

    plataformas = [
        plataforma(140, 450, 170),   # 0
        plataforma(380, 400, 140),   # 1
        plataforma(600, 340, 180),   # 2
        plataforma(900, 410, 160),   # 3
        plataforma(250, 280, 150),   # 4
        plataforma(500, 220, 170),   # 5
        plataforma(800, 270, 180),   # 6
        plataforma(1050, 170, 150),  # 7
    ]

    cristais = [
        cristal_sobre(plataformas[0], 60),
        cristal_sobre(plataformas[1], 70),
        cristal_sobre(plataformas[2], 90),
        cristal_sobre(plataformas[3], 70),
        cristal_sobre(plataformas[4], 75),
        cristal_sobre(plataformas[5], 85),
        cristal_sobre(plataformas[6], 90),
        cristal_sobre(plataformas[7], 75),
    ]

    inimigos = [
        inimigo_sobre(plataformas[0], 80),
        inimigo_sobre(plataformas[1], 70),
        inimigo_sobre(plataformas[2], 80),
        inimigo_sobre(plataformas[3], 50),
        inimigo_sobre(plataformas[5], 50),
        inimigo_sobre(plataformas[7], 70),
    ]

    return Fase(
        nome="Fase 1",
        subtitulo="Os Primeiros Fragmentos",
        plataformas=plataformas,
        cristais=cristais,
        inimigos=inimigos,
    )


# ==================================
#  FASE 2  
# ==================================

def criar_fase_2():

    # ---------------------------------------------------------------
    # 1) PLATAFORMAS 
    # ---------------------------------------------------------------
    plataformas = [
        plataforma(100, 460, 150),    # 0  início
        plataforma(310, 410, 130),    # 1
        plataforma(500, 360, 140),    # 2
        plataforma(700, 420, 150),    # 3  desce um pouco
        plataforma(900, 360, 150),    # 4
        plataforma(1070, 290, 150),   # 5  ponto mais à direita
        plataforma(820, 230, 130),    # 6  começa a voltar
        plataforma(580, 200, 140),    # 7
        plataforma(330, 240, 150),    # 8
        plataforma(110, 170, 140),    # 9  topo: último cristal
    ]

    # ---------------------------------------------------------------
    # 2) CRISTAIS 
    # ---------------------------------------------------------------
    cristais = [
        cristal_sobre(plataformas[0], 60),
        cristal_sobre(plataformas[1], 50),
        cristal_sobre(plataformas[2], 60),
        cristal_sobre(plataformas[3], 65),
        cristal_sobre(plataformas[4], 65),
        cristal_sobre(plataformas[5], 65),
        cristal_sobre(plataformas[6], 50),
        cristal_sobre(plataformas[7], 60),
        cristal_sobre(plataformas[8], 65),
        cristal_sobre(plataformas[9], 60),
    ]

    # ---------------------------------------------------------------
    # 3) INIMIGOS  
    # ---------------------------------------------------------------
    inimigos = [
        inimigo_sobre(plataformas[1], 70),
        inimigo_sobre(plataformas[2], 90),
        inimigo_sobre(plataformas[3], 100),
        inimigo_sobre(plataformas[4], 100),
        inimigo_sobre(plataformas[6], 80),
        inimigo_sobre(plataformas[8], 100),
        (900, CHAO.top - ALTURA_INIMIGO),   # patrulheiro do chão
    ]

    return Fase(
        nome="Fase 2",
        subtitulo="A Ascensão Cintilante",
        plataformas=plataformas,
        cristais=cristais,
        inimigos=inimigos,
        spawn=(30, 100),
    )


# =====================================================================
#  LISTA DE FASES  
# =====================================================================

FASES = [
    criar_fase_1,
    criar_fase_2,
]