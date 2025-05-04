import pygame # Importa a biblioteca pygame, que é usada para criar e gerenciar elementos gráficos e de jogo, 
# como a exibição da tela, movimentação da cobra e detecção de eventos

from pygame.locals import * # Importa todas as constantes locais do pygame, como QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT e K_RIGHT. 
# Isso facilita o uso dessas constantes sem precisar referenciá-las com pygame.locals

import random # Importa a biblioteca random, que é usada para gerar números aleatórios. 
#No seu código, ela é utilizada para posicionar a maçã e os obstáculos de maneira imprevisível

import time # Importa a biblioteca time, que fornece funções relacionadas ao tempo. 
# No seu código, é usada para adicionar um atraso (time.sleep(1)) antes de encerrar o jogo quando o jogador perde

WINDOWS_WIDTH = 600 # Largura da janela do jogo
WINDOWS_HEIGHT = 600 # Altura da janela do jogo
POS_INICIAL_X = WINDOWS_WIDTH / 2 # Posição inicial da cobra no eixo X
POS_INICIAL_Y = WINDOWS_HEIGHT / 2 # Posição inicial da cobra no eixo Y
BLOCK = 10 # Tamanho de cada bloco da cobra, maçã e obstáculos

pontos = 0 # Inicializa a pontuação do jogador
velocidade = 10 # Inicializa a velocidade do jogo, que determina a taxa de atualização da tela

cor_cobra = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 0, 0), (255, 255, 255)] # Cores da cobra, alternando entre preto, branco e vermelho
cor_maca = (255, 0, 0) # Cor da maçã
cor_obstaculo = (140, 0, 170) # Cor dos obstáculos
cor_fundo = (130, 220, 140) # Cor de fundo da janela do jogo
cor_texto = (0, 0, 0) # Cor do texto que exibe a pontuação
cor_game_over = (255, 0, 0) # Cor do texto "Game Over"

pygame.font.init() # Inicializa o módulo de fontes do pygame, permitindo o uso de fontes personalizadas
fonte = pygame.font.SysFont('Orbiton', 35, bold=False, italic=True) # Cria uma fonte personalizada, especificando o nome da fonte, 
# tamanho, negrito e itálico

def colisao(pos1, pos2): # Função que verifica se duas posições colidem (ou seja, se estão na mesma posição)
    return pos1 == pos2 # Retorna True se as posições forem iguais, indicando uma colisão

def verifica_margens(pos): # Função que verifica se a cobra colidiu com as bordas da janela do jogo
    if 0 <= pos[0] < WINDOWS_WIDTH and 0 <= pos[1] < WINDOWS_HEIGHT: # Verifica se a posição da cobra está dentro dos limites da janela
    # posição X(pos[0]) entre 0 e largura da janela, posição Y(pos[1]) entre 0 e altura da janela
        return False # Retorna False se a cobra estiver dentro dos limites
    else: 
        return True # Retorna True, indicando que houve uma colisão com as bordas
    
def gera_pos_aleatoria(): # Função que gera uma posição aleatória para as maçãs e obstáculos dentro da janela do jogo
    x = random.randint(0, WINDOWS_WIDTH) # Gera uma posição aleatória no eixo X
    y = random.randint(0, WINDOWS_HEIGHT) # Gera uma posição aleatória no eixo Y

    if (x, y) in obstaculo_pos or (x, y) in cobra_pos: # Verifica se a posição gerada já está ocupada por um obstáculo ou pela cobra
        gera_pos_aleatoria() # Se estiver ocupada, chama a função novamente para gerar uma nova posição

    return x // BLOCK * BLOCK, y // BLOCK * BLOCK # Retorna a posição ajustada para o tamanho do bloco, 
    # garantindo que a maçã ou obstáculo fique alinhado com a grade do jogo

def game_over(): # Função que exibe a tela de "Game Over" quando o jogador perde
    fonte = pygame.font.SysFont('Orbiton', 80, bold=True, italic=True) # Cria uma fonte personalizada para o texto "Game Over"
    text_over = fonte.render('Game Over', True, (cor_game_over)) # Renderiza o texto "Game Over" com a cor especificada, 
    # O True indica que o texto terá antialiasing, deixando-o mais suave

    window.blit(text_over, (120, 250)) # Desenha o texto "Game Over" na janela do jogo, na posição (120, 250)
    pygame.display.update() # Atualiza a tela para exibir o texto "Game Over"
    time.sleep(1) # Adiciona um atraso de 1 segundo antes de encerrar o jogo
    pygame.quit() # Encerra o pygame, fechando a janela do jogo e liberando os recursos utilizados
    quit() # Encerra o programa 

pygame.init()
window = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")

cobra_pos = [(POS_INICIAL_X, POS_INICIAL_Y),(POS_INICIAL_X + BLOCK, POS_INICIAL_Y),(POS_INICIAL_X + 2 * BLOCK, POS_INICIAL_Y)]
cobra_surface = pygame.Surface((BLOCK, BLOCK))
cobra_surface.fill((cor_cobra[0]))
direcao = K_LEFT

obstaculo_pos = []
obstaculo_surface = pygame.Surface((BLOCK, BLOCK))
obstaculo_surface.fill((cor_obstaculo))

maca_surface = pygame.Surface((BLOCK, BLOCK), pygame.SRCALPHA)  # Permite transparência
maca_surface.fill((180, 0, 0, 0))
pygame.draw.circle(maca_surface, (cor_maca), (BLOCK // 2, BLOCK // 2), BLOCK // 2)  # Centro mais escuro
maca_pos = gera_pos_aleatoria()

while True:
    pygame.time.Clock().tick(velocidade)
    window.fill((cor_fundo))

    mensagem = f'Pontos: {pontos}'
    texto = fonte.render(mensagem, True, (cor_texto)) 

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            quit()

        elif evento.type == KEYDOWN:
            if evento.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if evento.key == K_UP and direcao == K_DOWN:
                    continue
                elif evento.key == K_DOWN and direcao == K_UP:
                    continue
                elif evento.key == K_LEFT and direcao == K_RIGHT:
                    continue
                elif evento.key == K_RIGHT and direcao == K_LEFT:
                    continue
                else:
                    direcao = evento.key 

    window.blit(maca_surface, maca_pos)

    # Desenhar folha verde acima da maçã
    pygame.draw.arc(window, (0, 150, 0), (maca_pos[0] - 2, maca_pos[1] - 8, BLOCK, BLOCK), 3.8, 6.0, 4)  # Semicírculo verde

    if (colisao(cobra_pos[0], maca_pos)):
        cobra_pos.append((-10, -10)) 
        maca_pos = gera_pos_aleatoria()
        obstaculo_pos.append(gera_pos_aleatoria())
        pontos += 1
        if pontos % 5 == 0:
            velocidade += 2

    for pos in obstaculo_pos:
        if colisao(cobra_pos[0], pos):
            game_over()
        window.blit(obstaculo_surface, pos)

    for i, pos in enumerate(cobra_pos):
        cobra_surface.fill(cor_cobra[i % len(cor_cobra)])  # Alterna as cores
        window.blit(cobra_surface, pos)

    for item in range(len(cobra_pos) -1,0,-1):
        if colisao(cobra_pos[0], cobra_pos[item]):
            game_over()
        cobra_pos[item] = cobra_pos[item - 1]   # Move the snake

    if verifica_margens(cobra_pos[0]):
        game_over()    

    if direcao == K_RIGHT:
        cobra_pos[0] = (cobra_pos[0][0] + BLOCK, cobra_pos[0][1]) # Move the snake to the right   

    if direcao == K_LEFT:
        cobra_pos[0] = (cobra_pos[0][0] - BLOCK, cobra_pos[0][1]) # Move the snake to the left

    if direcao == K_UP:   
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1]  - BLOCK) # Move the snake to the up

    if direcao == K_DOWN:
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1] + BLOCK) # Move the snake to the down

    window.blit(texto, (460, 10)) # Desenha o texto na tela
    
    pygame.display.update()