import pygame
import random


class Cone:
    def __init__(self, tela, velocidade):
        self.tela = tela
        self.tamanho = [32, 32]
        self.velocidade = velocidade

        # Posição aleatória dentro da pista
        largura_tela = tela.get_width()
        margem_pista = 80
        x = random.randint(margem_pista, largura_tela - margem_pista - self.tamanho[0])
        self.posicao = [x, -self.tamanho[1]]

        # Carregar imagem
        self.imagem = pygame.image.load('assets/cone.png')
        self.imagem = pygame.transform.scale(self.imagem, self.tamanho)

        self.rect = pygame.Rect(self.posicao, self.tamanho)

    def atualizar(self):
        self.posicao[1] += self.velocidade
        self.rect = pygame.Rect(self.posicao, self.tamanho)

    def desenhar(self):
        self.tela.blit(self.imagem, self.posicao)

    def fora_da_tela(self):
        return self.posicao[1] > self.tela.get_height()

    def getRect(self):
        return pygame.Rect(self.posicao, self.tamanho)