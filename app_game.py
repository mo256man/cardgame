import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_card import *
from app_constant import *
from app_screen import UI

class Game():
    def __init__(self):
        pygame.init()
        words = Words()
        player1_name = words.make_random_name()                         # プレイヤー1の名前
        player2_name = words.make_random_name()                         # プレイヤー2の名前
        deck1, deck2 = words.make_deck()                                # 両者のデッキ構築
        self.player1 = Player(player1_name, deck=deck1, offset=0)       # プレイヤー1のインスタンス
        self.player2 = Player(player2_name, deck=deck2, offset=1)       # プレイヤー2のインスタンス
        self.players = [self.player1, self.player2]                     # プレイヤ1とプレイヤー2
        self.ui = UI(self.player1, self.player2)                        # UI画面

        # デッキのカード（裏）
        for p in [0, 1]:                                                # プレイヤー1とプレイヤー2について
            deckpos = self.ui.deckpos[p]                                # デッキの位置
            card = Card(type="word", pos1=deckpos, pos2=deckpos, is_face=False)        # カードの裏
            self.ui.sp_group.add(card)                                  # グループに定義

        # 最初に場に出すカードを定義し、配る
        for p, player in enumerate(self.players):
            deckpos = self.ui.deckpos[p]
            for i in range(SHOW_CARD_NUM):
                deckpos = self.ui.deckpos[p]                            # デッキの位置
                cardpos = self.ui.cardpos[p][i]                         # カードの位置
                card = player.select_random_card(pos1=deckpos, pos2=cardpos)
#                 card = Card(type="word", pos=deckpos, is_face=False, pos2=cardpos)
                self.ui.sp_group.add(card)
                player.card_list.append(card)
                self.ui.move_card(card)
                if p == 0:
                    self.ui.turn_card(card)

        """"
        for p, (player, deckpos, cardpos) in enumerate(zip(self.players, self.ui.deckpos, self.ui.cardpos)):
            for i in range(8):                                          # 各カードについて
                card = Card(type="word", is_face=False, pos1=deckpos, pos2=cardpos[i])       # カード定義
                self.ui.sp_group.add(card)                                 # カードをグループに追加
                player.card_list.append(card)                           # カードをリストに追加
        """
        # カーソル
        self.cursor1 = Card(type="cursor")
        self.cursor1.rect.center = self.ui.cardpos[0][0]                  # カーソル位置の初期値


    """
    def draw_demo(self):
        # 両者にカードを配るデモ
        for p, player in enumerate(self.players):                       # 各プレイヤーについて
            for i in range(8):                                          # 各カードについて
                if player.showing[i] != 3:                              # 3（配置済み）でなければ
                    is_turn = not bool(player.offset)                   # プレイヤー1はカードをめくる　プレイヤー2はめくらない
                    self.ui.deal_card(player, i, self.sp_group, is_turn)       # その場所にカードを配ってカードをめくる
        pygame.event.clear()
    """

    def play(self):
        self.cursor1.visible = True
        self.ui.sp_group.add(self.cursor1)
        while True:
            show_cnt = 0
            self.ui.show()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_RIGHT:
                        self.player1.select = (self.player1.select + 1) % 8
                    elif key == pygame.K_LEFT:
                        self.player1.select = (self.player1.select - 1) % 8
                    elif key == pygame.K_UP:
                        self.player1.select = (self.player1.select + 4) % 8
                    elif key == pygame.K_DOWN:
                        self.player1.select = (self.player1.select - 4) % 8
                    elif key == pygame.K_SPACE:
                        card = self.player1.card_list[self.player1.select]
                        card.pos1 = card.pos2
                        card.pos2 = self.ui.showpos[0][show_cnt]
                        self.ui.deal_card(self.player1, self.player1.select, self.sp_group, False)

                    self.cursor1.rect.center = self.ui.cardpos[0][self.player1.select]
                    self.ui.screen.blit(self.cursor1.image, self.cursor1.rect)
                    pygame.display.flip()
                    self.ui.clock.tick(60)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("start")
                    pygame.quit()
                    sys.exit()

def demo():
    game = Game()
    game.deal_cards()
#    game.draw_demo()
    game.play()
    print("done.")

if __name__ == "__main__":
    demo()