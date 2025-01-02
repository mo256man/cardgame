import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_sprite import *
from app_constant import *

class UI():
    def __init__(self, player1:Player, player2:Player):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption = "コトダマモンスター"
        surface = pygame.Surface((self.width, self.height))
        surface.fill(BLACK)
        self.clock = pygame.time.Clock()
        self.sp_group = pygame.sprite.LayeredUpdates()      # スプライトグループ（正確にはレイヤー）はScreenに属するようにする

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
        positions = [[(r*100+220, 480+150*c) for r in range(4)] for c in range(2)]  # 2行3列の座標群
        cardpos1 = np.array(positions).reshape(-1,2)                                # プレイヤー1のカードの座標 1次元にする
        cardpos2 = cardpos1 + np.array((self.width//2, 0))                      # プレイヤー2のカードの座標
        self.cardpos = (cardpos1.tolist(),  cardpos2.tolist())

        # カード開示位置
        positions = [(self.width//4 , 100+150*c) for c in range(2)]              # 座標群
        showpos1 = np.array(positions).reshape(-1,2)                            # プレイヤー1のカードの座標 1次元にする
        showpos2 = cardpos1 + np.array((self.width//2, 0))                      # プレイヤー2のカードの座標
        self.showpos = (showpos1.tolist(),  showpos2.tolist())

        # 魔法陣
        x1, x2 = self.width//4, self.width//4 * 3
        y = 500
        magicsquare1 = MagicSquare("magicsquare1", (x1, y))
        magicsquare2 = MagicSquare("magicsquare2", (x2, y))
        self.sp_group.add(magicsquare1)
        self.sp_group.add(magicsquare2)
        self.magicsquares = [magicsquare1, magicsquare2]

        # 召喚の演出
        flame1 = Flame("frame1", (self.width//4, 300))
        flame2 = Flame("frame2", (3 * self.width//4, 300))
        self.flames = [flame1, flame2]
        self.base_surface = surface
        self.surface = surface

    def move_card(self, card:Card):
        DURATION_TIME = 0.2                                                 # カードドローに要する時間
        self.sp_group.move_to_front(card)                                   # アニメーションするカードをレイヤーの一番上へ移動
        start_time = pygame.time.get_ticks()                                # スタート時間
        elapsed_time = 0                                                    # 経過時間
        while elapsed_time < DURATION_TIME:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000    # 経過時間（秒）
            t = min(1, elapsed_time / DURATION_TIME)                        # スタート～ゴールを0～1で表す
            x = card.pos1[0] * (1-t) + card.pos2[0] * t
            y = card.pos1[1] * (1-t) + card.pos2[1] * t
            card.rect.center = (x, y)
            self.show()

    def turn_card(self, card:Card):
        for angle in range(0, 180+1, 10):                                   # 0度から180度まで
            card.animated_turn(angle)                                       # カードをめくる
            self.show()

    def fade_sprite(self, is_fade_in):
        rng = range(0, 255+1, 32) if is_fade_in else range(255, 0-1-1, -32)
        for alpha in rng:
            for sprite in self.sp_group:
                if sprite.fade:
                    sprite.image.set_alpha(alpha)
            self.show()
            pygame.time.delay(200)
    
    def show_magicsquare(self):
        for sprite in self.sp_group:
            sprite.visible = False
        for magicsquare in self.magicsquares:
            magicsquare.visible = True
        self.fade_sprite(is_fade_in=True)
    """
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

            self.show()
    """

#    def draw(self, player:Player, cnt):
#        cardpos = self.cardpos1 if player.offset == 0 else self.cardpos2
#        return cardpos[cnt]

    def show(self):
        self.surface = self.base_surface.copy()
        self.screen.blit(self.surface, (0, 0))
        for sprite in self.sp_group:
            if sprite.visible:
                self.screen.blit(sprite.image, sprite.rect)
        pygame.display.flip()
        self.clock.tick(60)


