import pygame


class Jogador:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.tamanho = [40, 40]
        self.posicao = [x, y]
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        self.velocidade = 6

        # Animação
        self.contador = 0
        self.imagemAtual = 0
        self.listaImagens = []

        for i in range(3):
            imagem = pygame.image.load('assets/carro.png')
            imagem = pygame.transform.scale(imagem, self.tamanho)
            self.listaImagens.append(imagem)

    def desenhar(self):
        self.contador += 1
        if self.contador > 5:
            self.contador = 0
            self.imagemAtual = (self.imagemAtual + 1) % 3
        self.tela.blit(self.listaImagens[self.imagemAtual], self.posicao)

    def atualizar(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.posicao[0] -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.posicao[0] += self.velocidade

        # Limitar dentro da pista
        largura_tela = self.tela.get_width()
        margem_pista = 80  # margem lateral da pista

        if self.posicao[0] < margem_pista:
            self.posicao[0] = margem_pista
        if self.posicao[0] + self.tamanho[0] > largura_tela - margem_pista:
            self.posicao[0] = largura_tela - margem_pista - self.tamanho[0]

        self.rect = pygame.Rect(self.posicao, self.tamanho)

    def getRect(self):
        return pygame.Rect(self.posicao, self.tamanho)
