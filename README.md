readme
# O Último Cristal: Em Busca da Luz

## Descrição Geral

O jogo é uma aventura de plataforma com exploração. Ele se passa em um universo de cristais que foi destruído, onde o equilíbrio foi perdido após a quebra do cristal principal. A ideia é acompanhar uma princesa guardiã que precisa restaurar o equilíbrio do mundo recuperando a energia perdida.

## Objetivo do Jogo

O jogador controla a princesa, sobe pelas plataformas de cada fase e coleta todos os fragmentos de cristal. Ao reunir todos os fragmentos de uma fase, o caminho para a próxima se ilumina. Ao concluir a última fase, o cristal fonte é restaurado e o universo volta a brilhar.

## Personagem Principal

Uma princesa guardiã do reino de cristais. Ela anda para os lados, pula entre as plataformas e pode derrotar inimigos pisando neles. Atributos:

- Vida (começa com 3)
- Velocidade
- Pontuação

## Inimigos

Criaturas corrompidas pelo caos que patrulham as plataformas e o chão. Elas viram ao chegar na borda, e quando a princesa passa perto (no mesmo nível) elas passam a perseguí-la. O jogador perde vida ao encostar de lado em um inimigo, e pode derrotá-lo pulando em cima dele. Quanto mais inimigos são derrotados, maior o dano dos que restam.

## Cenário e Fases

O ambiente é um mundo mágico de cristais destruído, formado por plataformas flutuantes sobre um chão de grama e pedra. Cada fase é um percurso de plataformas com cristais para coletar e inimigos para enfrentar.

| Fase | Nome                    | Cristais | Inimigos |
|------|-------------------------|----------|----------|
| 1    | Os Primeiros Fragmentos | 8        | 6        |
| 2    | A Ascensão Cintilante   | 10       | 7        |

A **Fase 2 é a fase-modelo**: ela usa a mesma mecânica da Fase 1 e está toda comentada em `fases.py`, para servir de base na criação das próximas fases.

## Sistema de Pontuação

- Fragmento de cristal = 1 ponto
- Inimigo pisado = 2 pontos

A pontuação e as vidas acompanham a jogadora de uma fase para a outra.

## Sistema de Vida

A jogadora começa com 3 vidas e perde vida ao encostar nos inimigos (depois do dano ela fica piscando e invencível por um instante). Quando a vida chega a 0, aparece a tela de **Game Over**, onde é possível tentar a fase novamente, com 3 vidas e o placar que ela tinha ao começar aquela fase.

## Controles

```
←  →     - andar para esquerda / direita
ESPAÇO   - pular
ENTER    - confirmar (menu e telas de resultado)
ESC      - sair do jogo
```

## Fluxo do Jogo

1. **Menu inicial** → Jogar
2. **Fase** → coletar todos os cristais (evitando ou pisando nos inimigos)
3. **Fase concluída** → próxima fase
4. **Vitória** (última fase concluída) ou **Game Over** (vidas zeradas)

## Estrutura do Projeto

```
o-ultimo-cristal/
├── main.py       → loop principal, estados do jogo e HUD
├── fases.py      → todas as fases + guia para criar novas
├── telas.py      → menu, game over, fase concluída e vitória
├── botao.py      → botão clicável reutilizável
├── player.py     → movimentação, pulo, dano e atributos
├── inimigo.py    → patrulha, perseguição e dano
├── cristal.py    → fragmentos coletáveis
├── entidade.py   → classe base dos objetos do jogo
├── utils.py      → partículas e efeitos visuais
└── sprites/      → imagens do jogo
```

## Planos Futuros

No jogo **O Último Cristal**, pretendo continuar criando novas fases e aperfeiçoando as que já existem. A base do jogo já está pronta, então o foco agora é aprimorar essas fases, deixando-as:

- **Mais difíceis**, com desafios que exijam mais habilidade da jogadora;
- **Mais interessantes**, com percursos, inimigos e situações mais variados;
- **Mais bonitas**, com um visual mais caprichado e fiel ao universo de cristais.