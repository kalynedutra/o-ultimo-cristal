# o-ultimo-cristal
1. Título do Jogo
O Último Cristal: Em Busca da Luz

2. Descrição Geral
O jogo é do tipo aventura com exploração.
Ele se passa em um universo de cristais que foi destruído, onde o equilíbrio foi perdido após a quebra do cristal principal.
A ideia principal é acompanhar uma princesa que precisa restaurar o equilíbrio do mundo recuperando a energia perdida.

3. Objetivo do Jogo
O jogador deve:
Controlar a personagem principal
Explorar o mapa
Coletar fragmentos de cristal

Meta principal:
Reunir os fragmentos e restaurar o cristal fonte para salvar o universo.

4. Personagem Principal
Quem é: Uma princesa guardiã do reino de cristais
Movimento: Se move em quatro direções (cima, baixo, esquerda, direita)
Atributos:
Vida
Velocidade
Pontuação

5. Inimigos e Obstáculos
Tipos:
Criaturas corrompidas pelo caos
Barreiras e áreas perigosas
Comportamento:
Alguns ficam parados
Outros se movimentam automaticamente
Alguns podem perseguir o jogador
Colisão:
Jogador perde vida ao encostar

6. Cenário (Mapa)
Ambiente: Mundo mágico de cristais destruído
Elementos:
Caminhos
Paredes
Áreas bloqueadas
Regiões perigosas
Distribuição:
Fragmentos espalhados pelo mapa
Objetivo final localizado em uma área protegida

7. Sistema de Pontuação
O jogador ganha pontos ao:
Coletar fragmentos de cristal
Fragmento de cristal = 10 pontos

8. Sistema de Vida
Vida inicial: 3 
Perde vida ao:
Encostar em inimigos
Cair em áreas perigosas
Quando a vida chega a 0:
O jogo mostra tela de derrota
9. Controles
↑ → mover para cima
↓ → mover para baixo
← → mover para esquerda
→ → mover para direita
ESC → sair do jogo

10. Fluxo do Jogo
O jogo inicia com uma tela inicial
O jogador começa no mapa
Durante a partida:
Explora o cenário
Evita inimigos
Coleta itens
Vitória:
Coletar todos os fragmentos e restaurar o cristal
Derrota:
Perder todas as vidas

11. Regras do Jogo
Deve coletar os itens para avançar
Colidir com inimigos causa dano
Respeitar limites do mapa

12. Estrutura do Projeto
jogo
│
├── main.py
├── player.py
├── inimigo.py
├── mapa.py
├── item.py
├── utils.py
└── assets/
    ├── imagens
    └── sons
Separação por responsabilidades:
Player → movimentação e atributos
Inimigos → comportamento
Mapa → cenário
Itens → coleta e pontuação

13. Funcionalidades Mínimas
Movimentação do personagem
Um mapa funcional
Sistema de colisão
Pelo menos 1 inimigo
Sistema de vida
Sistema de pontuação
14. Melhorias Futuras
Novas fases
Mais tipos de inimigos
Poderes especiais
Sistema de salvar progresso
Sons e música
