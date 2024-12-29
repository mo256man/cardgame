import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_card import *
from app_constant import *

class Game():
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption = "コトダマモンスター"
        self.clock = pygame.time.Clock()

        words = Words()
        player1_name = words.make_random_name()
        player2_name = words.make_random_name()
        deck1, deck2 = words.make_deck()
        self.player1 = Player(player1_name, deck=deck1, offset=0)
        self.player2 = Player(player2_name, deck=deck2, offset=self.width//2)
        self.show()

        cardpos = [item for item in [[(r*100, 400+200*c) for r in range(3)] for c in range(2)]]

    def show(self):
        surface = pygame.Surface((self.width, self.height))
        surface.fill(WHITE)

        # プレイヤー名
        x, y = 20, 10
        font = pygame.font.SysFont(FONT_WORD, 40)
        player1_surface = font.render(self.player1.name, True, BLACK)
        surface.blit(player1_surface, (x, y))
        player2_surface = font.render(self.player2.name, True, BLACK)
        surface.blit(player2_surface, (self.width - player2_surface.get_width() - x, y))

        # 体力ゲージ
        x, y, w, h = 20, 60, 600, 40
        pygame.draw.rect(surface, BLACK, (x, y, w, h), 3)
        pygame.draw.rect(surface, BLACK, (self.width - x - w, y, w, h), 3)

        # デッキ（裏面）
        ura = Card(type="word", is_face=False)
        ura.rect.center = (600, 400)

        while True:
            self.screen.blit(surface, (0,0))
            self.screen.blit(ura.image, ura.rect)
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

def demo():
    game = Game()
    game.show()

if __name__ == "__main__":
    demo()