import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_card import *

class Word():
    def __init__(self, data):
        self.name = data[0]
        self.attack = data[1]
        self.defend = data[2]
        self.speed = data[3]
        self.attr = data[4]


class Game():
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption = "コトダマモンスター"
        self.clock = pygame.time.Clock()


    def title(self):
        card_group = pygame.sprite.Group()
        card_list = []
        word = "コトダマモンスター"
        xs = []
        y = self.height / 4
        for i, letter in enumerate(word):
            card = Card("title", word=letter)
            x = (i+0.5)  / len(word) * self.width
            card.pos1 = self.width/2, 600
            card.pos2 = x, y
            card_group.add(card)
            card_list.append(card)
            xs.append(x)
        base = Base((card.width, card.height))

        moved = [False] * len(word)             # 移動が完了したかどうかを追跡するフラグ
        duration_time = 0.1                     # カード移動にかかる時間
        while True:
            self.screen.fill(GRAY)
            pygame.display.flip()
            for i in range(len(word)):
                start_time = pygame.time.get_ticks()
                while True:
                    if not moved[i]:
                        #self.screen.draw_title(base)
                        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 経過時間（秒）
                        if elapsed_time > duration_time:
                            moved[i] = True

                        card_list[i].move_linear(duration_time, elapsed_time)
                        card_group.update()
                        card_group.draw(self.screen)
                        pygame.display.flip()
                    else:
                        break

            card_group.update()
            card_group.draw(self.screen)
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

            # 移動が完了したら移動フラグをTrueにしてループを継続
#            if elapsed_time >= duration_time:
#                moved = True


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.title()
