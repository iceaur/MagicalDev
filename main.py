import pygame
import random

pygame.init()

# -------------------------
# Configurações da tela
# -------------------------
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Magical Dev Girl")

# -------------------------
# Cores e fontes
# -------------------------
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 50, 50)
PRETO = (0, 0, 0)

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 70)

# -------------------------
# Carregar sprites
# -------------------------
player_img = pygame.image.load("assets/personagem.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))

enemy_img = pygame.image.load("assets/error.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

boss_img = pygame.image.load("assets/nave.png").convert_alpha()
boss_img = pygame.transform.scale(boss_img, (300, 80))

background = pygame.image.load("assets/cenario.png").convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))

# -------------------------
# Função para texto com sombra
# -------------------------
def render_texto_sombra(texto, fonte, cor_texto, cor_sombra, x, y, tela):
    sombra = fonte.render(texto, True, cor_sombra)
    tela.blit(sombra, (x + 2, y + 2))
    principal = fonte.render(texto, True, cor_texto)
    tela.blit(principal, (x, y))

# -------------------------
# Tela inicial
# -------------------------
def tela_inicial():
    while True:
        tela.blit(background, (0,0))
        render_texto_sombra("MAGICAL DEV GIRL", fonte_grande, BRANCO, PRETO, 200, 200, tela)
        render_texto_sombra("PRESSIONE ENTER PARA JOGAR", fonte, BRANCO, PRETO, 230, 350, tela)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        pygame.display.update()

# -------------------------
# Tela Game Over
# -------------------------
def tela_game_over(pontos):
    while True:
        tela.blit(background, (0,0))
        render_texto_sombra("GAME OVER", fonte_grande, BRANCO, PRETO, 260, 200, tela)
        render_texto_sombra(f"Pontuação: {pontos}", fonte, BRANCO, PRETO, 320, 300, tela)
        render_texto_sombra("ENTER para jogar de novo", fonte, BRANCO, PRETO, 230, 400, tela)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        pygame.display.update()

# -------------------------
# Tela Vitória
# -------------------------
def tela_vitoria(pontos):
    while True:
        tela.blit(background, (0,0))
        render_texto_sombra("VOCÊ VENCEU!", fonte_grande, BRANCO, PRETO, 230, 200, tela)
        render_texto_sombra(f"Pontuação Final: {pontos}", fonte, BRANCO, PRETO, 260, 300, tela)
        render_texto_sombra("ENTER para jogar novamente", fonte, BRANCO, PRETO, 210, 400, tela)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        pygame.display.update()

# -------------------------
# Mostrar mensagem (ex: fase)
# -------------------------
def mostrar_mensagem(msg, jogador, tiros, inimigos, chefe):
    for i in range(60):  # 1 segundo a 60 FPS
        tela.blit(background, (0, 0))
        tela.blit(player_img, jogador)
        for t in tiros:
            pygame.draw.rect(tela, VERDE, t)
        for i_inim in inimigos:
            tela.blit(enemy_img, i_inim)
        if chefe:
            tela.blit(boss_img, chefe)
        render_texto_sombra(msg, fonte_grande, BRANCO, PRETO, 200, 250, tela)
        pygame.display.update()
        clock.tick(60)

# -------------------------
# Jogo principal
# -------------------------
def jogar():
    jogador = pygame.Rect(370, 520, 60, 60)
    velocidade = 7
    vida = 5
    pontos = 0

    tiros = []
    inimigos = []
    tiros_inimigos = []

    fase = 1
    kills_para_proxima = 8
    kills = 0
    vel_inimigo = 4

    chefe = None
    vida_chefe = 0
    tempo_bug = 0
    tempo_tiro_chefe = 0
    direcao_chefe = 1

    rodando = True

    while rodando:
        clock.tick(60)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    tiros.append(pygame.Rect(jogador.centerx - 5, jogador.top, 10, 20))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador.left > 0:
            jogador.x -= velocidade
        if teclas[pygame.K_RIGHT] and jogador.right < LARGURA:
            jogador.x += velocidade

        # Criar inimigos
        if fase < 4 and random.randint(1, 30) == 1:
            inimigos.append(pygame.Rect(random.randint(0, 760), 0, 40, 40))

        # Chefe aparece na fase 4
        if fase == 4 and chefe is None:
            chefe = pygame.Rect(250, 50, 300, 80)
            vida_chefe = 30

        # Tiros jogador
        novos_tiros = []
        for tiro in tiros:
            tiro.y -= 10
            if tiro.bottom > 0:
                novos_tiros.append(tiro)
        tiros = novos_tiros

        # Inimigos
        novos_inimigos = []
        for inimigo in inimigos:
            inimigo.y += vel_inimigo
            if inimigo.colliderect(jogador):
                vida -= 1
                continue

            acertado = False
            for tiro in tiros[:]:
                if inimigo.colliderect(tiro):
                    tiros.remove(tiro)
                    pontos += 1
                    kills += 1
                    acertado = True
                    break
            if not acertado:
                novos_inimigos.append(inimigo)
        inimigos = novos_inimigos

        # Chefe
        if chefe is not None:
            chefe.x += 4 * direcao_chefe
            if chefe.right >= LARGURA:
                direcao_chefe = -1
            if chefe.left <= 0:
                direcao_chefe = 1

            tempo_bug += 1
            if tempo_bug > 40:
                inimigos.append(pygame.Rect(chefe.centerx, chefe.bottom, 40, 40))
                tempo_bug = 0

            tempo_tiro_chefe += 1
            if tempo_tiro_chefe > 30:
                tiros_inimigos.append(pygame.Rect(chefe.centerx, chefe.bottom, 12, 25))
                tempo_tiro_chefe = 0

            for tiro in tiros[:]:
                if chefe.colliderect(tiro):
                    tiros.remove(tiro)
                    vida_chefe -= 1
                    if vida_chefe <= 0:
                        pontos += 30
                        chefe = None
                        return ("vitoria", pontos)

        # Tiros chefe
        novos_tiros_chefe = []
        for t in tiros_inimigos:
            t.y += 8
            if t.colliderect(jogador):
                vida -= 1
            else:
                novos_tiros_chefe.append(t)
        tiros_inimigos = novos_tiros_chefe

        # Mudança de fase
        if kills >= kills_para_proxima and fase < 4:
            fase += 1
            vida += 1
            kills = 0
            kills_para_proxima += 4
            vel_inimigo += 1
            mostrar_mensagem(f"FASE {fase}", jogador, tiros, inimigos, chefe)

        # ---------------------
        # DESENHAR TELA
        # ---------------------
        tela.blit(background, (0, 0))

        # jogador
        tela.blit(player_img, jogador)

        # tiros jogador
        for t in tiros:
            pygame.draw.rect(tela, VERDE, t)

        # inimigos
        for i in inimigos:
            tela.blit(enemy_img, i)

        # tiros chefe
        for t in tiros_inimigos:
            pygame.draw.rect(tela, VERMELHO, t)

        # chefe
        if chefe is not None:
            tela.blit(boss_img, chefe)
            pygame.draw.rect(tela, VERMELHO, (chefe.x, chefe.y - 20, chefe.width, 10))
            pygame.draw.rect(tela, VERDE, (chefe.x, chefe.y - 20, chefe.width * (vida_chefe / 30), 10))

        # HUD
        render_texto_sombra(f"Vida: {vida}", fonte, BRANCO, PRETO, 10, 10, tela)
        render_texto_sombra(f"Pontos: {pontos}", fonte, BRANCO, PRETO, 10, 40, tela)
        render_texto_sombra(f"Fase: {fase}", fonte, BRANCO, PRETO, 10, 70, tela)

        pygame.display.update()

        if vida <= 0:
            return ("gameover", pontos)

# -------------------------
# LOOP PRINCIPAL
# -------------------------
tela_inicial()  # aparece só uma vez

while True:
    tipo, score = jogar()
    if tipo == "gameover":
        tela_game_over(score)
    else:
        tela_vitoria(score)
