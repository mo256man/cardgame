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
        words = Words()
        player1_name = words.make_random_name()                     # プレイヤー1の名前
        player2_name = words.make_random_name()                     # プレイヤー2の名前
        deck1, deck2 = words.make_deck()                            # 両者のデッキ構築
        player1 = Player(player1_name, deck=deck1, offset=0)        # プレイヤー1のインスタンス
        player2 = Player(player2_name, deck=deck2, offset=1)        # プレイヤー2のインスタンス
        players = [player1, player2]                                # プレイヤ1とプレイヤー2

        screen = Screen(player1, player2)                           # 画面
        sp_group = pygame.sprite.LayeredUpdates()                   # スプライトグループ（レイヤーを使うのでGroupではない）
        sp_group.add(Card(type="word", is_face=False, pos1=screen.deckpos[0], pos2=screen.deckpos[0]))
        sp_group.add(Card(type="word", is_face=False, pos1=screen.deckpos[1], pos2=screen.deckpos[1]))
        duration_time = 0.2                                         # カードドローの時間

        # カード座標を定義
        for p, (player, deckpos, cardpos) in enumerate(zip(players, screen.deckpos, screen.cardpos)):
            for i in range(8):                                      # 各カードについて
                card = Card(type="word", is_face=False, pos1=deckpos, pos2=cardpos[i], color=BLUE)       # カード定義
                sp_group.add(card)                                  # カードをグループに追加
                player.card_list.append(card)                       # カードをリストに追加

        # 両者にカードを配るデモ
        while True:
            for p, player in enumerate([player1, player2]):         # 各プレイヤーについて
                for i in range(8):                                  # 各カードについて
                    if player.showing[i] != 3:                      # 3（配置済み）でなければ
                        is_turn = not bool(player.offset)           # プレイヤー1はカードをめくる　プレイヤー2はめくらない
                        screen.deal_card(player, i, sp_group, is_turn)       # その場所にカードを配ってカードをめくる

            screen.show(sp_group)

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