import pygame 
from pygame.locals import * 
import random 
import time 

WINDOWS_WIDTH = 600 
WINDOWS_HEIGHT = 600 
POS_INICIAL_X = WINDOWS_WIDTH / 2
POS_INICIAL_Y = WINDOWS_HEIGHT / 2 
BLOCK = 10 

pontos = 0 
velocidade = 10

cor_cobra = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 0, 0), (255, 255, 255)]
cor_maca = (255, 0, 0)
cor_obstaculo = (140, 0, 170)
cor_fundo = (130, 220, 140)
cor_texto = (0, 0, 0)
cor_game_over = (255, 0, 0)

pygame.font.init() 
fonte = pygame.font.SysFont('Orbiton', 35, bold=False, italic=True) 

def colisao(pos1, pos2):
    return pos1 == pos2

def verifica_margens(pos):
    if 0 <= pos[0] < WINDOWS_WIDTH and 0 <= pos[1] < WINDOWS_HEIGHT:
        return False
    else: 
        return True
    
def gera_pos_aleatoria():
    x = random.randint(0, WINDOWS_WIDTH)
    y = random.randint(0, WINDOWS_HEIGHT)

    if (x, y) in obstaculo_pos or (x, y) in cobra_pos:
        gera_pos_aleatoria()

    return x // BLOCK * BLOCK, y // BLOCK * BLOCK

def game_over():
    fonte = pygame.font.SysFont('Orbiton', 80, bold=True, italic=True) 
    text_over = fonte.render('Game Over', True, (cor_game_over))
    window.blit(text_over, (120, 250)) 
    pygame.display.update()
    time.sleep(1) 
    pygame.quit()
    quit()

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

maca_surface = pygame.Surface((BLOCK, BLOCK), pygame.SRCALPHA)
maca_surface.fill((180, 0, 0, 0))
pygame.draw.circle(maca_surface, (cor_maca), (BLOCK // 2, BLOCK // 2), BLOCK // 2)
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

    pygame.draw.arc(window, (0, 150, 0), (maca_pos[0] - 2, maca_pos[1] - 8, BLOCK, BLOCK), 3.8, 6.0, 4)

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
        cobra_surface.fill(cor_cobra[i % len(cor_cobra)])
        window.blit(cobra_surface, pos)

    for item in range(len(cobra_pos) -1,0,-1):
        if colisao(cobra_pos[0], cobra_pos[item]):
            game_over()
        cobra_pos[item] = cobra_pos[item - 1]

    if verifica_margens(cobra_pos[0]):
        game_over()    

    if direcao == K_RIGHT:
        cobra_pos[0] = (cobra_pos[0][0] + BLOCK, cobra_pos[0][1])  

    if direcao == K_LEFT:
        cobra_pos[0] = (cobra_pos[0][0] - BLOCK, cobra_pos[0][1])

    if direcao == K_UP:   
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1]  - BLOCK)

    if direcao == K_DOWN:
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1] + BLOCK)

    window.blit(texto, (460, 10))
    
    pygame.display.update()