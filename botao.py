import math
import pygame


def _gradiente(tamanho, cor_topo, cor_base):
    largura, altura = tamanho
    superficie = pygame.Surface(tamanho)

    for y in range(altura):
        t = y / max(1, altura - 1)
        cor = tuple(int(a + (b - a) * t) for a, b in zip(cor_topo, cor_base))
        pygame.draw.line(superficie, cor, (0, y), (largura, y))

    return superficie


class Botao:
    """
    Botao clicavel reutilizavel.
    Visual inspirado em cristais roxos e lilas: fundo em degrade,
    brilho externo que pulsa ao passar o mouse e losangos decorativos.
    """

    def __init__(
        self,
        texto,
        x,
        y,
        largura,
        altura,
        fonte,
        cor=(36, 18, 66),
        cor_hover=(88, 44, 142)
    ):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.cor = cor
        self.cor_hover = cor_hover
        self.tempo = 0

        self.fundo_normal = self._criar_fundo(cor)
        self.fundo_hover = self._criar_fundo(cor_hover)

    def _criar_fundo(self, cor_base):
        """Degrade com cantos arredondados (pre-renderizado)."""
        cor_topo = tuple(min(255, c + 30) for c in cor_base)
        fundo = _gradiente(self.rect.size, cor_topo, cor_base).convert_alpha()

        mascara = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            mascara,
            (255, 255, 255, 255),
            mascara.get_rect(),
            border_radius=10
        )
        fundo.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # reflexo fino no topo, como a faceta de um cristal
        pygame.draw.line(
            fundo,
            (255, 255, 255, 38),
            (12, 4),
            (self.rect.width - 12, 4),
            1
        )

        return fundo

    def desenhar(self, tela):
        self.tempo += 1

        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)

        # Brilho externo (pulsa quando o mouse esta em cima)
        brilho = pygame.Surface(
            (self.rect.width + 24, self.rect.height + 24),
            pygame.SRCALPHA
        )

        if hover:
            alpha = int(75 + 35 * math.sin(self.tempo * 0.12))
        else:
            alpha = 32

        pygame.draw.rect(
            brilho,
            (150, 85, 255, alpha),
            brilho.get_rect(),
            border_radius=15
        )

        tela.blit(
            brilho,
            (self.rect.x - 12, self.rect.y - 12)
        )

        # Fundo
        tela.blit(
            self.fundo_hover if hover else self.fundo_normal,
            self.rect
        )

        # Borda externa
        pygame.draw.rect(
            tela,
            (205, 165, 255) if hover else (125, 75, 190),
            self.rect,
            2,
            border_radius=10
        )

        # Borda interna
        pygame.draw.rect(
            tela,
            (70, 38, 110),
            self.rect.inflate(-8, -8),
            1,
            border_radius=7
        )

        # Texto
        cor_texto = (255, 245, 255) if hover else (222, 207, 242)

        texto_render = self.fonte.render(self.texto, True, cor_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)

        tela.blit(texto_render, texto_rect)

        # Losangos laterais (so aparecem no hover)
        if hover:
            for lado in (-1, 1):
                cx = texto_rect.centerx + lado * (texto_rect.width // 2 + 22)
                cy = self.rect.centery
                pygame.draw.polygon(
                    tela,
                    (205, 165, 255),
                    [(cx, cy - 6), (cx + 6, cy), (cx, cy + 6), (cx - 6, cy)]
                )

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )
