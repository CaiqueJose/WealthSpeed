import pygame
import sys
from scripts.interface import Interface
from scripts.cenas import CenaMenu, CenaJogando, CenaGameOver


# ─── Inicialização do Pygame ────────────────────────────────
pygame.init()
pygame.font.init()

# ─── Configurações da tela ──────────────────────────────────
LARGURA = 600
ALTURA = 400
tela = pygame.display.set_mode([LARGURA, ALTURA])
pygame.display.set_caption("Abundance Speed")
relogio = pygame.time.Clock()
FPS = 60

# ─── Criar interface (compartilhada entre cenas) ────────────
interface = Interface(tela)

# ─── Estado inicial ─────────────────────────────────────────
recorde = 0
cena_atual = CenaMenu(tela, interface)


# ═══════════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Passar evento para a cena atual
        cena_atual.processar_evento(evento)

    # Atualizar a cena atual
    cena_atual.atualizar()

    # Desenhar a cena atual
    cena_atual.desenhar()

    # ─── Transição de cenas ─────────────────────────────────
    if cena_atual.proxima_cena is not None:
        nome = cena_atual.proxima_cena
        cena_atual.proxima_cena = None

        if nome == "jogando":
            # Salvar recorde se veio do game over
            if isinstance(cena_atual, CenaGameOver):
                recorde = cena_atual.cena_jogando.recorde
            elif isinstance(cena_atual, CenaJogando):
                recorde = cena_atual.recorde

            # Criar nova partida
            nova_cena = CenaJogando(tela, interface)
            nova_cena.set_recorde(recorde)
            cena_atual = nova_cena

        elif nome == "game_over":
            # Salvar recorde
            if isinstance(cena_atual, CenaJogando):
                recorde = cena_atual.recorde
            # Ir para game over mantendo referência da partida
            cena_atual = CenaGameOver(tela, interface, cena_atual)

        elif nome == "menu":
            # Salvar recorde se veio do game over
            if isinstance(cena_atual, CenaGameOver):
                recorde = cena_atual.cena_jogando.recorde
            cena_atual = CenaMenu(tela, interface)

    relogio.tick(FPS)
    pygame.display.flip()