import pygame
import random
import math  


def aplicar_tint_vermelho(sprite):
    tintado = sprite.copy()
    tintado.fill((255, 60, 60, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tintado


class Particula:
    def __init__(self, x, y, cor=(200, 200, 200), vida=20, tamanho=4):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1.5, -0.5)
        self.vida = vida
        self.vida_max = vida
        self.tamanho = tamanho
        self.cor = cor

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vida -= 1

    def esta_viva(self):
        return self.vida > 0

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        alpha_fator = self.vida / self.vida_max
        raio = max(1, int(self.tamanho * alpha_fator))

        superficie = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        cor_com_alpha = (*self.cor, int(255 * alpha_fator))
        pygame.draw.circle(superficie, cor_com_alpha, (raio, raio), raio)
        tela.blit(superficie, (int(self.x - raio), int(self.y - raio)))


def criar_fumaca_pulo(x, y, quantidade=6):
    particulas = []
    for _ in range(quantidade):
        offset_x = random.uniform(-10, 10)
        particulas.append(
            Particula(x + offset_x, y, cor=(180, 180, 180), vida=18, tamanho=5)
        )
    return particulas


def criar_explosao(x, y, quantidade=20):
    cores = [(255, 90, 0), (255, 160, 0), (255, 220, 60), (220, 40, 40)]
    particulas = []

    for _ in range(quantidade):
        p = Particula(
            x, y,
            cor=random.choice(cores),
            vida=random.randint(20, 35),
            tamanho=random.randint(4, 8)
        )
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(2, 6)
        p.vel_x = math.cos(angulo) * velocidade
        p.vel_y = math.sin(angulo) * velocidade
        particulas.append(p)

    return particulas
def criar_poeira_passo(x, y, direcao):
    particulas = []
    for _ in range(2):
        offset_x = random.uniform(-3, 3)
        p = Particula(
            x - (direcao * 6) + offset_x,  
            y,
            cor=(190, 180, 160),
            vida=random.randint(10, 16),
            tamanho=random.randint(2, 4)
        )
        p.vel_x = -direcao * random.uniform(0.3, 0.8)
        p.vel_y = random.uniform(-0.3, -0.1)
        particulas.append(p)
    return particulas


def criar_impacto_queda(x, y, intensidade=1.0):
    quantidade = max(4, int(10 * intensidade))
    particulas = []

    for _ in range(quantidade):
        angulo = random.uniform(0, math.pi)  
        velocidade = random.uniform(1, 3) * intensidade

        p = Particula(
            x, y,
            cor=(190, 180, 160),
            vida=random.randint(14, 22),
            tamanho=random.randint(3, 6)
        )
        p.vel_x = math.cos(angulo + math.pi) * velocidade  
        p.vel_y = -abs(math.sin(angulo)) * velocidade
        particulas.append(p)

    return particulas

def criar_explosao_cristal(x, y, quantidade=16):
    cores = [(147, 90, 220), (180, 140, 240), (100, 50, 180), (210, 190, 255)]
    particulas = []

    for _ in range(quantidade):
        p = Particula(
            x, y,
            cor=random.choice(cores),
            vida=random.randint(18, 30),
            tamanho=random.randint(3, 7)
        )
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(1.5, 5)
        p.vel_x = math.cos(angulo) * velocidade
        p.vel_y = math.sin(angulo) * velocidade
        particulas.append(p)

    return particulas