import pygame
import random
from RedeNeural import RedeNeural

pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cópia Flappy Bird")

# Configurações de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configuração Treinamento
QTD_INDIVIDUOS = 10000  # Recomendavel diminuir para evitar lag


class Passaro:
    def __init__(self):
        self.width = 40
        self.height = 30
        self.x = 10
        self.y = SCREEN_HEIGHT // 2
        self.gravidade = 0.5
        self.jump_force = -10
        self.velocidade = 0
        self.cor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.rede = RedeNeural(1, 2, 2, 1)

    def jump(self):
        self.velocidade = self.jump_force

    def set_entrada(self, arr_entradas):
        self.rede.copiar_para_entrada(arr_entradas)

    def update_rede(self):
        self.rede.calcular_saida()
        saida = []
        self.rede.copiar_da_saida(saida)

        if saida[0] >= 1:
            self.jump()

    def update(self):

        self.update_rede()

        self.velocidade += self.gravidade
        self.y += self.velocidade

        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocidade = 0
        if self.y < 0:
            self.y = 0
            self.velocidade = 0

    def draw(self):
        pygame.draw.rect(SCREEN, self.cor, (self.x, self.y, self.width, self.height))


class Cano:
    def __init__(self):
        self.width = 60
        self.gap = 150
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - self.gap
        self.x = SCREEN_WIDTH
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(SCREEN, GREEN, (self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height))
        # w, h = self.get_coords()
        # pygame.draw.ellipse(SCREEN, RED, (w - 1, h - 1, 2, 2))

    def get_coords(self):
        height_center = self.top_height + self.gap / 2
        width_center = self.x + self.width / 2
        return width_center, height_center

    def collide(self, passaro):
        passaro_rect = pygame.Rect(passaro.x, passaro.y, passaro.width, passaro.height)
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)

        return passaro_rect.colliderect(top_rect) or passaro_rect.colliderect(bottom_rect)


class Jogo:
    def __init__(self):
        self.passaros = [Passaro() for i in range(QTD_INDIVIDUOS)]
        self.canos = [Cano()]
        self.score = 0
        self.geracao = 0
        self.font = pygame.font.SysFont(None, 36)

    def reset(self):
        self.passaros = [Passaro() for i in range(QTD_INDIVIDUOS)]
        self.canos = [Cano()]
        print(f"Melhor pontuação da geração {self.geracao}: {self.score}")
        self.score = 0
        self.geracao += 1

    def update(self):
        for passaro in self.passaros:
            x, y = self.get_distance(passaro)
            passaro.set_entrada([x, y])
            passaro.update()

        if self.canos[-1].x < SCREEN_WIDTH // 2:
            self.canos.append(Cano())

        for pipe in self.canos:
            pipe.update()

        if self.canos[0].x < -self.canos[0].width:
            self.canos.pop(0)
            self.score += 1

        for pipe in self.canos:
            for passaro in self.passaros:
                if pipe.collide(passaro):
                    self.passaros.remove(passaro)

        if len(self.passaros) == 0:
            self.reset()

    def draw(self):
        SCREEN.fill(BLACK)
        for passaro in self.passaros[:50]:
            passaro.draw()

        x, y = self.canos[0].get_coords()

        # pygame.draw.line(SCREEN, RED, (self.passaros[0].x + self.passaros[0].width/2, y), (x, y))
        # pygame.draw.line(SCREEN, BLUE, (self.passaros[0].x + self.passaros[0].width / 2, y), (self.passaros[0].x +
        #                                 self.passaros[0].width / 2, self.passaros[0].y + self.passaros[0].height / 2))

        for pipe in self.canos:
            pipe.draw()
        score_text = self.font.render(f"Pontos: {self.score}", True, WHITE)
        alive_text = self.font.render(f"Vivos: {len(self.passaros)}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(alive_text, (SCREEN_WIDTH - score_text.get_width() - 20, 10))

    def get_distance(self, passaro: Passaro):
        x, y = self.canos[0].get_coords()
        horizontal_distance = x - (passaro.x + passaro.width/2)
        vertical_distance = y - (passaro.y + passaro.height / 2)
        return horizontal_distance, vertical_distance

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


# Inicializar e executar o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()
