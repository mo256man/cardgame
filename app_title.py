import sys
import time
import pygame
from pygame.locals import *

from app_game import Game
from app_card import Card
from app_constant import *

class Title(Game):
    def __init__(self):
        super().__init__()
        self.card_group = pygame.sprite.Group()
        self.card_list = []
        word = "コトダマモンスター"
        y = self.height / 4
        for i, letter in enumerate(word):
            card = Card("title", word=letter)
            x = (i+0.5)  / len(word) * self.width
            card.pos1 = self.width/2, 600
            card.pos2 = x, y
            card.rect.center = card.pos1
            self.card_group.add(card)
            self.card_list.append(card)

    def draw(self):
        self.screen.fill(GRAY)
        word = "コトダマモンスター"
        font = pygame.font.SysFont("ｄｆｇ麗雅宋", 30)
        text = font.render(word, True, WHITE)
        self.screen.blit(text, (100,100))
        button = pygame.Rect(10, 20, 30, 40)
        pygame.draw.rect(self.screen, RED, button)
        pygame.display.flip()

    def show(self):
        moved = [False] * len(self.card_list)       # 移動が完了したかどうかを追跡するフラグ
        duration_time = 0.5                         # カード移動にかかる時間
        while True:
            self.draw()
            for i in range(len(self.card_list)):
                start_time = pygame.time.get_ticks()
                while True:
                    if not moved[i]:
                        self.draw()
                        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 経過時間（秒）
                        if elapsed_time > duration_time:
                            moved[i] = True

                        self.card_list[i].move_linear(duration_time, elapsed_time)
                        self.card_group.update()
                        self.card_group.draw(self.screen)
                        pygame.display.flip()
                    else:
                        break

            self.card_group.update()
            self.card_group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("start")
                    pygame.quit()
                    sys.exit()
            self.clock.tick(60)