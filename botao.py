import pygame


class Botao:
    """
    Botao clicavel reutilizavel.
    Visual inspirado em cristais roxos e lilas.
    """

    def __init__(
        self,
        texto,
        x,
        y,
        largura,
        altura,
        fonte,
        cor=(38, 20, 70),
        cor_hover=(90, 45, 145)
    ):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.cor = cor
        self.cor_hover = cor_hover

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)

        # Brilho externo
        brilho = pygame.Surface(
            (self.rect.width + 24, self.rect.height + 24),
            pygame.SRCALPHA
        )

        alpha = 80 if hover else 35

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
        cor_atual = self.cor_hover if hover else self.cor

        pygame.draw.rect(
            tela,
            cor_atual,
            self.rect,
            border_radius=10
        )

        # Borda externa
        pygame.draw.rect(
            tela,
            (125, 75, 190) if not hover else (205, 165, 255),
            self.rect,
            2,
            border_radius=10
        )

        # Borda interna
        borda_interna = self.rect.inflate(-8, -8)

        pygame.draw.rect(
            tela,
            (70, 38, 110),
            borda_interna,
            1,
            border_radius=7
        )

        # Cristal decorativo esquerdo
        cor_cristal = (
            (220, 180, 255)
            if hover
            else (165, 110, 230)
        )

        x = self.rect.left + 17
        y = self.rect.centery

        cristal_esquerdo = [
            (x, y),
            (x + 6, y - 5),
            (x + 11, y),
            (x + 6, y + 5)
        ]

        pygame.draw.polygon(
            tela,
            cor_cristal,
            cristal_esquerdo
        )

        # Cristal decorativo direito
        x = self.rect.right - 17

        cristal_direito = [
            (x, y),
            (x - 6, y - 5),
            (x - 11, y),
            (x - 6, y + 5)
        ]

        pygame.draw.polygon(
            tela,
            cor_cristal,
            cristal_direito
        )

        # Texto
        cor_texto = (
            (250, 240, 255)
            if hover
            else (220, 205, 240)
        )

        texto_render = self.fonte.render(
            self.texto,
            True,
            cor_texto
        )

        texto_rect = texto_render.get_rect(
            center=self.rect.center
        )

        tela.blit(
            texto_render,
            texto_rect
        )

    def clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )