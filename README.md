# O Último Cristal: Em Busca da Luz

## Descrição Geral

O jogo é do tipo aventura com exploração. Ele se passa em um universo de cristais que foi destruído, onde o equilíbrio foi perdido após a quebra do cristal principal. A ideia principal é acompanhar uma princesa que precisa restaurar o equilíbrio do mundo recuperando a energia perdida.

## Objetivo do Jogo

O jogador deve controlar a personagem principal, explorar o mapa e coletar fragmentos de cristal. A meta principal é reunir os fragmentos e restaurar o cristal fonte para salvar o universo.

## Personagem Principal

Uma princesa guardiã do reino de cristais. Ela se move em quatro direções (cima, baixo, esquerda, direita) e possui os seguintes atributos:

- Vida
- Velocidade
- Pontuação

## Inimigos e Obstáculos

Os inimigos são criaturas corrompidas pelo caos, além de barreiras e áreas perigosas espalhadas pelo mapa. O comportamento varia: alguns ficam parados, outros se movimentam automaticamente e alguns podem perseguir o jogador. O jogador perde vida ao encostar em qualquer um deles.

## Cenário (Mapa)

O ambiente é um mundo mágico de cristais destruído. O mapa é composto por caminhos, paredes, áreas bloqueadas e regiões perigosas. Os fragmentos ficam espalhados pelo cenário, e o objetivo final está localizado em uma área protegida.

## Sistema de Pontuação

O jogador ganha pontos ao coletar fragmentos de cristal.

- Fragmento de cristal = 10 pontos

## Sistema de Vida

O jogador começa com 3 vidas e perde uma ao encostar em inimigos ou cair em áreas perigosas. Quando a vida chega a 0, o jogo mostra a tela de derrota.

## Controles

```
↑   - mover para cima
↓   - mover para baixo
←   - mover para esquerda
→   - mover para direita
ESC - sair do jogo
```

## Fluxo do Jogo

O jogo inicia com uma tela inicial e o jogador começa no mapa. Durante a partida, ele explora o cenário, evita inimigos e coleta itens.

- **Vitória:** coletar todos os fragmentos e restaurar o cristal
- **Derrota:** perder todas as vidas

## Regras do Jogo

- Deve coletar os itens para avançar
- Colidir com inimigos causa dano
- Respeitar limites do mapa

## Estrutura do Projeto

```
jogo/
├── main.py
├── player.py
├── inimigo.py
├── mapa.py
├── item.py
├── utils.py
└── assets/
    ├── imagens/
    └── sons/
```

Separação por responsabilidades:

- `player.py` → movimentação e atributos
- `inimigo.py` → comportamento
- `mapa.py` → cenário
- `item.py` → coleta e pontuação

## Funcionalidades Mínimas

- Movimentação do personagem
- Um mapa funcional
- Sistema de colisão
- Pelo menos 1 inimigo
- Sistema de vida
- Sistema de pontuação

## Melhorias Futuras

- Novas fases
- Mais tipos de inimigos
- Poderes especiais
- Sistema de salvar progresso
- Sons e música
