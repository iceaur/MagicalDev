import pygame
import random

pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Magical Dev Girl")

# Cores
BRANCO = (255, 255, 255)
ROSA = (255, 100, 180)
ROSA_FORTE = (255, 0, 120)
AZUL = (100, 150, 255)
ROXO = (150, 80, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 50, 50)
PRETO = (0, 0, 0)

clock = pygame.time.Clock()

fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 70)

# ---------------------------------------------------------
# TELA INICIAL  (APARECE SÓ NA PRIMEIRA VEZ)
# ---------------------------------------------------------
def tela_inicial():
    while True:
        tela.fill(PRETO)
        t1 = fonte_grande.render("MAGICAL DEV GIRL", True, BRANCO)
        t2 = fonte.render("PRESSIONE ENTER PARA JOGAR", True, BRANCO)
        tela.blit(t1, (200, 200))
        tela.blit(t2, (230, 350))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        pygame.display.update()


# ---------------------------------------------------------
# TELA GAME OVER
# ---------------------------------------------------------
def tela_game_over(pontos):
    while True:
        tela.fill(PRETO)
        over = fonte_grande.render("GAME OVER", True, BRANCO)
        pont = fonte.render(f"Pontuação: {pontos}", True, BRANCO)
        restart = fonte.render("ENTER para jogar de novo", True, BRANCO)

        tela.blit(over, (260, 200))
        tela.blit(pont, (320, 300))
        tela.blit(restart, (230, 400))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        pygame.display.update()


# ---------------------------------------------------------
# TELA VITÓRIA
# ---------------------------------------------------------
def tela_vitoria(pontos):
    while True:
        tela.fill((20, 0, 40))
        msg = fonte_grande.render("VOCÊ VENCEU!", True, BRANCO)
        pont = fonte.render(f"Pontuação Final: {pontos}", True, BRANCO)
        restart = fonte.render("ENTER para jogar novamente", True, BRANCO)

        tela.blit(msg, (230, 200))
        tela.blit(pont, (260, 300))
        tela.blit(restart, (210, 400))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return

        pygame.display.update()


# ---------------------------------------------------------
# JOGO PRINCIPAL
# ---------------------------------------------------------
def jogar():
    jogador = pygame.Rect(370, 520, 60, 60)
    velocidade = 7
    vida = 5
    pontos = 0

    tiros = []
    inimigos = []
    tiros_inimigos = []

    # fases
    fase = 1
    kills_para_proxima = 8
    kills = 0
    vel_inimigo = 4
    cor_jogadora = ROSA

    # chefe
    chefe = None
    vida_chefe = 0
    tempo_bug = 0
    tempo_tiro_chefe = 0
    direcao_chefe = 1   # ← NOVO: controla o movimento

    rodando = True

    while rodando:
        clock.tick(60)

        # EVENTOS
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

        # CRIAR INIMIGOS
        if fase < 4 and random.randint(1, 30) == 1:
            inimigos.append(pygame.Rect(random.randint(0, 760), 0, 40, 40))

        # CHEFE aparece na FASE 4
        if fase == 4 and chefe is None:
            chefe = pygame.Rect(250, 50, 300, 80)
            vida_chefe = 30

        # TIROS DO JOGADOR
        novos_tiros = []
        for tiro in tiros:
            tiro.y -= 10
            if tiro.bottom > 0:
                novos_tiros.append(tiro)
        tiros = novos_tiros

        # INIMIGOS
        novos_inimigos = []
        for inimigo in inimigos:
            inimigo.y += vel_inimigo

            if inimigo.colliderect(jogador):
                vida -= 1
                continue

            # tiro acertando inimigo
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

        # ATAQUE E MOVIMENTO DO CHEFE
        if chefe is not None:

            ### MOVIMENTO LATERAL CORRIGIDO ###
            chefe.x += 4 * direcao_chefe
            if chefe.right >= LARGURA:
                direcao_chefe = -1
            if chefe.left <= 0:
                direcao_chefe = 1

            # lançar mini bugs
            tempo_bug += 1
            if tempo_bug > 40:
                inimigos.append(pygame.Rect(chefe.centerx, chefe.bottom, 40, 40))
                tempo_bug = 0

            # tiros do chefe
            tempo_tiro_chefe += 1
            if tempo_tiro_chefe > 30:
                tiros_inimigos.append(pygame.Rect(chefe.centerx, chefe.bottom, 12, 25))
                tempo_tiro_chefe = 0

            # tomar dano
            for tiro in tiros[:]:
                if chefe.colliderect(tiro):
                    tiros.remove(tiro)
                    vida_chefe -= 1

                    if vida_chefe <= 0:
                        pontos += 30
                        chefe = None
                        return ("vitoria", pontos)

        # TIROS DO CHEFE
        novos_tiros_chefe = []
        for t in tiros_inimigos:
            t.y += 8
            if t.colliderect(jogador):
                vida -= 1
            else:
                novos_tiros_chefe.append(t)
        tiros_inimigos = novos_tiros_chefe

        # MUDAR DE FASE
        if kills >= kills_para_proxima and fase < 4:
            fase += 1
            vida += 1
            kills = 0
            kills_para_proxima += 4
            vel_inimigo += 1

            if fase == 2:
                cor_jogadora = ROSA_FORTE
            elif fase == 3:
                cor_jogadora = AZUL

        # DESENHAR TELA
        tela.fill(PRETO)
        pygame.draw.rect(tela, cor_jogadora, jogador)

        for t in tiros:
            pygame.draw.rect(tela, VERDE, t)

        for i in inimigos:
            pygame.draw.rect(tela, BRANCO, i)

        for t in tiros_inimigos:
            pygame.draw.rect(tela, VERMELHO, t)

        if chefe is not None:
            pygame.draw.rect(tela, ROXO, chefe)
            pygame.draw.rect(tela, VERMELHO, (chefe.x, chefe.y - 20, chefe.width, 10))
            pygame.draw.rect(tela, VERDE, (chefe.x, chefe.y - 20, chefe.width * (vida_chefe / 30), 10))

        tela.blit(fonte.render(f"Vida: {vida}", True, BRANCO), (10, 10))
        tela.blit(fonte.render(f"Pontos: {pontos}", True, BRANCO), (10, 40))
        tela.blit(fonte.render(f"Fase: {fase}", True, BRANCO), (10, 70))

        pygame.display.update()

        if vida <= 0:
            return ("gameover", pontos)


# ---------------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------------

tela_inicial()   # só aparece 1 vez

while True:
    tipo, score = jogar()

    if tipo == "gameover":
        tela_game_over(score)
    else:
        tela_vitoria(score)
