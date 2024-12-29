import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_card import *
from app_constant import *

class Screen():
    def __init__(self, player1:Player, player2:Player):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption = "コトダマモンスター"
        surface = pygame.Surface((self.width, self.height))
        surface.fill(WHITE)
        self.clock = pygame.time.Clock()

        # プレイヤー名
        x, y = 20, 10
        font = pygame.font.SysFont(FONT_WORD, 40)
        for i, player in enumerate((player1, player2)):
            text = font.render(player.name, True, BLACK)
            x = x if i==0 else self.width - text.get_width() - x
            surface.blit(text, (x, y))

        # 体力ゲージ
        x, y, w, h = 20, 60, 600, 40
        pygame.draw.rect(surface, BLACK, (x, y, w, h), 3)
        pygame.draw.rect(surface, BLACK, (self.width - x - w, y, w, h), 3)

        # デッキ（裏面）
        deckpos1 = (100, 555)
        deckpos2 = (deckpos1[0] + self.width//2, deckpos1[1])
        self.deckpos = (deckpos1, deckpos2)                                     # テープル上のデッキの座標

        # カード配置位置
        pos2d = [[(r*100+220, 480+150*c) for r in range(4)] for c in range(2)]  # 2行3列の座標群
        cardpos1 = np.array(pos2d).reshape(-1,2)                                # プレイヤー1のカードの座標 1次元にする
        cardpos2 = cardpos1 + np.array((self.width//2, 0))                      # プレイヤー2のカードの座標
        self.cardpos = (cardpos1.tolist(),  cardpos2.tolist())

        self.base_surface = surface
        self.surface = surface

    def deal_card(self, player:Player, i, sp_group:pygame.sprite.Group, turn:bool):
        DURATION_TIME = 0.2                                         # カードドローに要する時間
        while True:
            if player.showing[i] == 0:                      # そこにカードが無いならば
                card = player.card_list[i]                  # 注目するカードはそこに向かうカード
                face = player.select_random_card(pos1=card.pos2, pos2=card.pos2)    # カードの表 決定
                sp_group.move_to_front(card)                # アニメーションするカードをレイヤーの一番上へ移動
                start_time = pygame.time.get_ticks()        # スタート時間
                player.showing[i] = 1                       # ドロー中にする

            elif player.showing[i] == 1:                    # ドロー中ならば
                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 経過時間（秒）
                card.move_linear(DURATION_TIME, elapsed_time)   # 時間経過に従い移動する
                if elapsed_time > DURATION_TIME:            # 一定時間経過したら
                    player.showing[i] = 2                   # ターン中にする

            elif player.showing[i] == 2:                    # ターン中ならば
                if turn:                                    # ターンする必要があるならば
                    for angle in range(0, 180+1, 10):       # 0度から180度まで
                        card.animated_turn(face, angle)     # カードをめくる
                        self.show(sp_group)
                        player.card_list[i] = face          # スプライトを裏から表に定義し直す
                player.showing[i] = 3                       # 設置完了
                break                                       # 無限ループを抜ける

            self.show(sp_group)

    def draw(self, player:Player, cnt):
        cardpos = self.cardpos1 if player.offset == 0 else self.cardpos2
        return cardpos[cnt]

    def show(self, sp_group:pygame.sprite.Group):
        self.surface = self.base_surface.copy()
        self.screen.blit(self.surface, (0, 0))
        sp_group.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


