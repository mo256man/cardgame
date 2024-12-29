import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_card import *
from app_constant import *
from app_screen import Screen

class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        words = Words()
        player1_name = words.make_random_name()                     # プレイヤー1の名前
        player2_name = words.make_random_name()                     # プレイヤー2の名前
        deck1, deck2 = words.make_deck()                            # 両者のデッキ構築
        player1 = Player(player1_name, deck=deck1, offset=0)        # プレイヤー1のインスタンス
        player2 = Player(player2_name, deck=deck2, offset=1)        # プレイヤー2のインスタンス
        players = [player1, player2]                                # プレイヤ1とプレイヤー2

        screen = Screen(player1, player2)                           # 画面
        sp_list = [[], []]                                          # スプライトグループとは別の、スプライトを特定するためのリスト
        sp_group = pygame.sprite.LayeredUpdates()                   # スプライトグループ（レイヤーを使うのでGroupではない）
        sp_group.add(Card(type="word", is_face=False, pos1=screen.deckpos[0], pos2=screen.deckpos[0]))
        sp_group.add(Card(type="word", is_face=False, pos1=screen.deckpos[1], pos2=screen.deckpos[1]))
        duration_time = 0.2                                         # カードドローの時間

        # カード座標を定義
        for p, (player, deckpos, cardpos) in enumerate(zip(players, screen.deckpos, screen.cardpos)):
            for i in range(8):                                      # 各カードについて
                card = Card(type="word", is_face=False, pos1=deckpos, pos2=cardpos[i], color=BLUE)       # カード定義
                sp_group.add(card)                                  # カードをグループに追加
                sp_list[p].append(card)                             # カードをリストに追加

        # 両者にカードを配るデモ
        while True:
            for p, player in enumerate([player1, player2]):         # 各プレイヤーについて
                for i in range(8):                                  # 各カードについて
                    while True:
                        if player.showing[i] == 3:                      # 場にカードが出ている状態ならば
                            break                                       # スルーして次のカードへ

                        elif player.showing[i] == 0:                    # そこにカードが無いならば
                            card = sp_list[p][i]                        # 注目するカードはそこに向かうカード
                            face = player.select_random_card(pos1=card.pos2, pos2=card.pos2)    # カードの表 決定
                            sp_group.move_to_front(card)                # アニメーションするカードをレイヤーの一番上へ移動
                            start_time = pygame.time.get_ticks()        # スタート時間
                            player.showing[i] = 1                       # ドロー中にする

                        elif player.showing[i] == 1:                    # ドロー中ならば
                            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 経過時間（秒）
                            card.move_linear(duration_time, elapsed_time)   # 時間経過に従い移動する
                            if elapsed_time > duration_time:            # 一定時間経過したら
                                player.showing[i] = 2                   # ターン中にする

                        elif player.showing[i] == 2:                    # ターン中ならば
                            for angle in range(0, 180+1, 10):           # 0度から180度まで
                                card.animated_turn(face, angle)
                                screen.show()
                                sp_group.draw(screen.screen)
                                pygame.display.flip()
                                self.clock.tick(60)
                            player.showing[i] = 3

                        screen.show()
                        sp_group.draw(screen.screen)
                        pygame.display.flip()
                        self.clock.tick(60)

            screen.show()
            sp_group.draw(screen.screen)
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("start")
                    pygame.quit()
                    sys.exit()

def demo():
    game = Game()
    game.show()

if __name__ == "__main__":
    demo()