import pygame
from pygame.locals import *
import random
import sys
import cv2
import numpy as np
from app_sprite import *
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
            name = f"ura{p}"                                            # デッキの名前
            card = Card(type="word",name=name, pos1=deckpos, pos2=deckpos, is_face=False)        # カードの裏
            self.ui.sp_group.add(card)                                  # グループに定義

        # 最初に場に出すカードを定義し、配る
        for p, player in enumerate(self.players):
            deckpos = self.ui.deckpos[p]
            for i in range(SHOW_CARD_NUM):
                deckpos = self.ui.deckpos[p]                            # デッキの位置
                cardpos = self.ui.cardpos[p][i]                         # カードの位置
                name = f"card{p}_{i}"
                card = player.select_random_card(name, pos1=deckpos, pos2=cardpos)
                self.ui.sp_group.add(card)
                player.card_list[i] = card
                self.ui.move_card(card)
                if p == 0:
                    self.ui.turn_card(card)

        # カーソル
        pos = self.ui.cardpos[0][0]
        self.cursor1 = Card("cursor", "cursor1", pos1=pos, pos2=pos)

    def play(self):
        self.cursor1.visible = True
        self.ui.sp_group.add(self.cursor1)

        while True:                                     # 勝負がつくまでループ
            show_cnt = 0
            while True:                                 # 1ターン分
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
                            if show_cnt < 2:
                                i = self.player1.select                         # 選択された位置
                                if self.player1.card_list[i] is not None:       # そこにカードがあるならば
                                    card = self.player1.card_list[i]
                                    self.player1.card_list[i] = None
                                    card.pos1 = card.pos2
                                    card.pos2 = self.ui.showpos[0][show_cnt]
                                    # self.ui.deal_card(self.player1, self.player1.select, self.sp_group, False)
                                    self.ui.move_card(card)
                                    show_cnt += 1
                            if show_cnt == 2:
                                self.ui.fade_sprite(is_fade_in=False)
                                print("モンスター召喚")
                                self.ui.show_magicsquare()
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
#    game.deal_cards()
#    game.draw_demo()
    game.play()
    print("done.")

if __name__ == "__main__":
    demo()