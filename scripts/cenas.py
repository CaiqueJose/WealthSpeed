import pygame
from scripts.jogador import Jogador
from scripts.cone import Cone


# ─── Cores da pista ─────────────────────────────────────────
COR_ASFALTO = (50, 50, 55)
COR_FAIXA = (220, 200, 50)
COR_GRAMA = (34, 120, 50)
COR_BORDA = (180, 180, 180)

# ─── Constantes ─────────────────────────────────────────────
MARGEM_PISTA = 80
LARGURA_FAIXA = 4


class Cena:
    """Classe base para todas as cenas do jogo."""

    def __init__(self, tela):
        self.tela = tela
        self.largura = tela.get_width()
        self.altura = tela.get_height()
        self.proxima_cena = None  # nome da próxima cena para transição

    def processar_evento(self, evento):
        """Processa eventos do pygame. Deve ser sobrescrito."""
        pass

    def atualizar(self):
        """Atualiza a lógica da cena. Deve ser sobrescrito."""
        pass

    def desenhar(self):
        """Desenha a cena. Deve ser sobrescrito."""
        pass


class CenaMenu(Cena):
    """Cena do menu principal."""

    def __init__(self, tela, interface):
        super().__init__(tela)
        self.interface = interface

    def processar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.interface.clicou_jogar(evento.pos):
                self.proxima_cena = "jogando"

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            self.proxima_cena = "jogando"

    def atualizar(self):
        pass

    def desenhar(self):
        self.interface.desenhar_menu()


class CenaJogando(Cena):
    """Cena principal do jogo (partida em andamento)."""

    def __init__(self, tela, interface):
        super().__init__(tela)
        self.interface = interface

        # Jogador
        self.jogador = Jogador(tela, self.largura // 2 - 20, self.altura - 80)

        # Cones (obstáculos)
        self.cones = []
        self.velocidade_cones = 5
        self.timer_cone = 0
        self.intervalo_cone = 25  # frames entre cones

        # Pontuação
        self.pontuacao = 0
        self.recorde = 0

        # Animação da pista
        self.offset_faixa = 0

    def set_recorde(self, recorde):
        """Define o recorde vindo do gerenciador de cenas."""
        self.recorde = recorde

    def processar_evento(self, evento):
        pass  # Controles são via get_pressed() no atualizar

    def atualizar(self):
        # Animar faixas
        self.offset_faixa += self.velocidade_cones

        # Atualizar jogador
        self.jogador.atualizar()

        # Gerar cones
        self.timer_cone += 1
        if self.timer_cone >= self.intervalo_cone:
            self.timer_cone = 0
            self.cones.append(Cone(self.tela, self.velocidade_cones))

        # Atualizar cones e verificar colisão/pontuação
        for cone in self.cones[:]:
            cone.atualizar()

            # Cone ultrapassou o jogador → pontua
            if cone.posicao[1] > self.jogador.posicao[1] + self.jogador.tamanho[1]:
                if not hasattr(cone, 'pontuou'):
                    cone.pontuou = True
                    self.pontuacao += 1

                    # Aumentar dificuldade a cada 10 pontos
                    if self.pontuacao % 10 == 0:
                        self.velocidade_cones = min(self.velocidade_cones + 0.5, 14)
                        self.intervalo_cone = max(self.intervalo_cone - 2, 12)

            # Remover cones fora da tela
            if cone.fora_da_tela():
                self.cones.remove(cone)
                continue

            # Colisão com jogador
            if self.jogador.getRect().colliderect(cone.getRect()):
                if self.pontuacao > self.recorde:
                    self.recorde = self.pontuacao
                self.proxima_cena = "game_over"

    def desenhar(self):
        self._desenhar_pista()
        self.jogador.desenhar()
        for cone in self.cones:
            cone.desenhar()
        self.interface.desenhar_hud(self.pontuacao, self.recorde)

    def _desenhar_pista(self):
        """Desenha a pista de corrida com grama, asfalto e faixas animadas."""
        # Grama
        self.tela.fill(COR_GRAMA)

        # Asfalto
        pygame.draw.rect(
            self.tela, COR_ASFALTO,
            (MARGEM_PISTA, 0, self.largura - 2 * MARGEM_PISTA, self.altura)
        )

        # Bordas brancas da pista
        pygame.draw.rect(self.tela, COR_BORDA, (MARGEM_PISTA - 3, 0, 6, self.altura))
        pygame.draw.rect(
            self.tela, COR_BORDA,
            (self.largura - MARGEM_PISTA - 3, 0, 6, self.altura)
        )

        # Faixas centrais tracejadas (animadas)
        centro_x = self.largura // 2
        tamanho_traco = 40
        espaco_traco = 30
        y = -tamanho_traco + (self.offset_faixa % (tamanho_traco + espaco_traco))
        while y < self.altura:
            pygame.draw.rect(
                self.tela, COR_FAIXA,
                (centro_x - LARGURA_FAIXA // 2, y, LARGURA_FAIXA, tamanho_traco)
            )
            y += tamanho_traco + espaco_traco


class CenaGameOver(Cena):
    """Cena de fim de jogo."""

    def __init__(self, tela, interface, cena_jogando):
        super().__init__(tela)
        self.interface = interface
        self.cena_jogando = cena_jogando  # referência para manter o visual de fundo

    def processar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.interface.clicou_reiniciar(evento.pos):
                self.proxima_cena = "jogando"
            elif self.interface.clicou_menu(evento.pos):
                self.proxima_cena = "menu"

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            self.proxima_cena = "jogando"

    def atualizar(self):
        pass

    def desenhar(self):
        # Desenhar a pista congelada ao fundo
        self.cena_jogando.desenhar()
        # Overlay de game over por cima
        self.interface.desenhar_game_over(
            self.cena_jogando.pontuacao, self.cena_jogando.recorde
        )
