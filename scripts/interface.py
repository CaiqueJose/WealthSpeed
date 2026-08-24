import pygame


# ─── Cores ──────────────────────────────────────────────────
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 50, 50)
AMARELO = (255, 215, 0)
COR_MENU_BG = (16, 20, 35)
COR_BOTAO = (200, 60, 60)
COR_BOTAO_HOVER = (240, 80, 80)


class Interface:
    """Classe responsável por todos os elementos visuais de interface (menus, HUD, botões)."""

    def __init__(self, tela):
        self.tela = tela
        self.largura = tela.get_width()
        self.altura = tela.get_height()

        # Fontes
        self.fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
        self.fonte_botao = pygame.font.SysFont("Arial", 32, bold=True)
        self.fonte_pontos = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_game_over = pygame.font.SysFont("Arial", 52, bold=True)
        self.fonte_instrucao = pygame.font.SysFont("Arial", 22)

        # Guardar retângulos dos botões para detecção de clique
        self.botao_jogar_rect = pygame.Rect(0, 0, 0, 0)
        self.botao_reiniciar_rect = pygame.Rect(0, 0, 0, 0)
        self.botao_menu_rect = pygame.Rect(0, 0, 0, 0)

    def desenhar_menu(self):
        """Desenha a tela de menu com título e botão jogar."""
        self.tela.fill(COR_MENU_BG)

        # Decoração: linhas horizontais sutis (fundo estático para não piscar)
        for i in range(20):
            y = 25 * i + 10
            s = pygame.Surface((self.largura, 1), pygame.SRCALPHA)
            s.fill((255, 255, 255, 8))
            self.tela.blit(s, (0, y))

        # Título
        texto_titulo = self.fonte_titulo.render("ABUNDANCE SPEED", True, BRANCO)
        rect_titulo = texto_titulo.get_rect(center=(self.largura // 2, 130))
        self.tela.blit(texto_titulo, rect_titulo)

        # Subtítulo
        texto_sub = self.fonte_instrucao.render(
            "Desvie dos cones e va o mais longe possivel!", True, (180, 180, 200)
        )
        rect_sub = texto_sub.get_rect(center=(self.largura // 2, 170))
        self.tela.blit(texto_sub, rect_sub)

        # Botão Jogar
        mouse_pos = pygame.mouse.get_pos()
        self.botao_jogar_rect = pygame.Rect(self.largura // 2 - 120, 220, 240, 60)
        cor_btn = COR_BOTAO_HOVER if self.botao_jogar_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(self.tela, cor_btn, self.botao_jogar_rect, border_radius=12)
        pygame.draw.rect(self.tela, BRANCO, self.botao_jogar_rect, width=2, border_radius=12)

        texto_botao = self.fonte_botao.render("JOGAR", True, BRANCO)
        rect_texto_btn = texto_botao.get_rect(center=self.botao_jogar_rect.center)
        self.tela.blit(texto_botao, rect_texto_btn)

        # Instruções de controle
        texto_ctrl = self.fonte_instrucao.render(
            "<-  -> ou A  D para mover o carro", True, (140, 140, 160)
        )
        rect_ctrl = texto_ctrl.get_rect(center=(self.largura // 2, 320))
        self.tela.blit(texto_ctrl, rect_ctrl)

    def desenhar_game_over(self, pontuacao, recorde):
        """Desenha a tela de game over com pontuação e botões."""
        # Overlay escuro
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.tela.blit(overlay, (0, 0))

        # Texto Game Over
        texto_go = self.fonte_game_over.render("GAME OVER", True, VERMELHO)
        rect_go = texto_go.get_rect(center=(self.largura // 2, 80))
        self.tela.blit(texto_go, rect_go)

        # Pontuação
        texto_pts = self.fonte_botao.render(f"Pontuacao: {pontuacao}", True, BRANCO)
        rect_pts = texto_pts.get_rect(center=(self.largura // 2, 150))
        self.tela.blit(texto_pts, rect_pts)

        # Recorde
        texto_rec = self.fonte_instrucao.render(f"Recorde: {recorde}", True, AMARELO)
        rect_rec = texto_rec.get_rect(center=(self.largura // 2, 195))
        self.tela.blit(texto_rec, rect_rec)

        # Botão Reiniciar
        mouse_pos = pygame.mouse.get_pos()
        self.botao_reiniciar_rect = pygame.Rect(self.largura // 2 - 140, 240, 280, 60)
        cor_btn = (
            COR_BOTAO_HOVER
            if self.botao_reiniciar_rect.collidepoint(mouse_pos)
            else COR_BOTAO
        )
        pygame.draw.rect(self.tela, cor_btn, self.botao_reiniciar_rect, border_radius=12)
        pygame.draw.rect(self.tela, BRANCO, self.botao_reiniciar_rect, width=2, border_radius=12)

        texto_botao = self.fonte_botao.render("JOGAR DE NOVO", True, BRANCO)
        rect_texto_btn = texto_botao.get_rect(center=self.botao_reiniciar_rect.center)
        self.tela.blit(texto_botao, rect_texto_btn)

        # Botão Menu
        self.botao_menu_rect = pygame.Rect(self.largura // 2 - 100, 315, 200, 50)
        cor_menu = (
            (110, 110, 140)
            if self.botao_menu_rect.collidepoint(mouse_pos)
            else (80, 80, 100)
        )
        pygame.draw.rect(self.tela, cor_menu, self.botao_menu_rect, border_radius=10)
        pygame.draw.rect(self.tela, BRANCO, self.botao_menu_rect, width=2, border_radius=10)

        texto_menu = self.fonte_instrucao.render("MENU", True, BRANCO)
        rect_texto_menu = texto_menu.get_rect(center=self.botao_menu_rect.center)
        self.tela.blit(texto_menu, rect_texto_menu)

    def desenhar_hud(self, pontuacao, recorde):
        """Desenha o HUD com pontuação e recorde durante o jogo."""
        hud_surface = pygame.Surface((200, 70), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 120))
        self.tela.blit(hud_surface, (self.largura - 210, 10))

        texto_pts = self.fonte_pontos.render(f"Pontos: {pontuacao}", True, BRANCO)
        self.tela.blit(texto_pts, (self.largura - 200, 18))

        texto_rec = self.fonte_instrucao.render(f"Recorde: {recorde}", True, AMARELO)
        self.tela.blit(texto_rec, (self.largura - 200, 50))

    def clicou_jogar(self, pos):
        """Verifica se o clique foi no botão Jogar."""
        return self.botao_jogar_rect.collidepoint(pos)

    def clicou_reiniciar(self, pos):
        """Verifica se o clique foi no botão Reiniciar."""
        return self.botao_reiniciar_rect.collidepoint(pos)

    def clicou_menu(self, pos):
        """Verifica se o clique foi no botão Menu."""
        return self.botao_menu_rect.collidepoint(pos)
