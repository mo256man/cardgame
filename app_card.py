from __future__ import annotations      # 型ヒントを遅延評価するために必要
import pygame
from pygame.locals import *
import pandas as pd
import numpy as np
import random
import sys
import math
from app_constant import *

class Words():
    def __init__(self):
        self.words = pd.read_csv("word.csv", header=0)

    def make_random_name(self):
        name_words = []
        for _ in range(2):
            df_word = self.words.sample()["word"]
            self.words.drop(df_word.index)
            word = df_word.iloc[0]
            name_words.append(word)
        return f"{name_words[0]}の{name_words[1]}"

    def make_deck(self, cnt=0):
        words_cnt = len(self.words) if cnt==0 else cnt
        deck1 = self.words.sample(n=words_cnt//2)
        deck2 = self.words.drop(deck1.index).sample(n=words_cnt//2)
        return deck1, deck2

class Player():
    def __init__(self, name, deck:pd.DataFrame, offset):
        self.name = name
        self.hp = 2000
        self.deck = deck
        self.offset = offset
        self.showing = [0] * 8      # カードの状態 0:存在しない（ドロー要）, 1:ドロー中:, 2:ターン中, 3:存在する
        self.card_list = []             # 場に出ているカードのリスト

    def call_random_monster(self):
        word1 = self.deck.sample()
        self.deck = self.deck.drop(word1.index)
        word2 = self.deck.sample()
        self.deck = self.deck.drop(word2.index)
        self.monster = Monster(word1.iloc[0].to_dict(), word2.iloc[0].to_dict())

    def select_random_card(self, pos1, pos2):
        df_word = self.deck.sample()["word"]
        self.deck = self.deck.drop(df_word.index)
        word = df_word.iloc[0]
        card = Card(type="word", is_face=True, word=word, pos1=pos1, pos2=pos2)
        return card

class Card(pygame.sprite.Sprite):
    def __init__(self, type=None, is_face=True, **kwargs):
        super(Card, self).__init__()
        # カードの種別
        if type == "word":
            width = 80
            height = 140
            font_size = 60
            font = pygame.font.SysFont(FONT_WORD, font_size)
        elif type == "title":
            width = 100
            height = 150
            font_size = 80
            font = pygame.font.SysFont(FONT_WORD, font_size)
        else:
            print("unknown type")
            sys.exit()

        self.x, self.y = 0, 0
        self.is_face = is_face
        surface = pygame.Surface((width, height), flags=SRCALPHA)
        self.rect = surface.get_rect()
        self.rect.center = 0, 0
        surface.fill(TRANS)

        if is_face:
            face = surface.copy()
            self.word = kwargs.get("word")
            pygame.draw.rect(face, WHITE, (0, 0, width, height), 0, 10)
            pygame.draw.rect(face, BLACK, (0, 0, width, height), 1, 10)
        # 表面（言葉）
            word_count = len(self.word)
            word_height = font_size * word_count
            word_area = height * 0.8
            x = (width - font_size)/2
            y = height * .1
            if word_height > word_area:
                resize = True
                letter_height = word_area / word_count
            else:
                resize = False
                letter_height = font_size
                y += (word_area - word_height) / 2

            # 縦書きで一文字ずつ描画
            for letter in self.word:
                temp = font.render(letter, True, BLACK)
                if resize:
                    temp = pygame.transform.scale(temp, (font_size, letter_height))
                face.blit(temp, (x,y))
                y += letter_height
            self.base_image = face
            self.image = face

        if not is_face:
        # 裏面: pos1とpos2が必要
            back = surface.copy()
#            color = kwargs["color"]
#            pygame.draw.rect(back, color, (0, 0, width, height), 0, 10)
#            pygame.draw.rect(back, BLACK, (0, 0, width, height), 3, 10)
            pygame.draw.rect(back, BLACK, (0, 0, width, height), 0, 10)
            image = pygame.image.load(r"./image/magicsquare.png")
            image_size = min(width, height)
            image = pygame.transform.scale(image, (image_size, image_size))
            image_rect = image.get_rect(center=(width//2, height//2))
            back.blit(image, image_rect)
            self.base_image = back
            self.image = back

        self.pos1 = kwargs.get("pos1")
        self.pos2 = kwargs.get("pos2")
        self.rect.center = self.pos1
        self.width = width
        self.height = height

    def move_linear(self, duration_time, elapsed_time):
        t = elapsed_time / duration_time
        t = min(t, 1)                           # 移動スピードが早いとt>1になってしまうので修正
        pos = pygame.math.Vector2(self.pos1) * (1 - t) + pygame.math.Vector2(self.pos2) * t
        self.rect.center = pos

    def animated_turn(self, opposite:Card, angle):
        cos = math.cos(math.radians(angle))
        width = abs(self.width * cos)
        height = self.height
        image = self.base_image if cos>0 else opposite.base_image
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=self.rect.center)




class Monster():
    def __init__(self, word1, word2):
        self.name = f"{word1['word']}の{word2['word']}"
        self.attack = word1["attack"] + word2["attack"]
        self.defend = (word1["defend"] + word2["defend"]) // 2
        self.speed = word1["speed"] + word2["speed"]
        self.attr = word1["attr"] if word1["attr"] == word2["attr"] else "無"


class Base():
    def __init__(self, card_size):
        width = card_size[0] + 20
        height = card_size[1] + 20
        surface = pygame.Surface((width, height), flags=SRCALPHA)
        pygame.draw.rect(surface, BLUE, (0, 0, width, height), 5, 20)
        self.surface = surface
        self.rect = surface.get_rect()
        self.rect.center = (width/2, height/2)


def make_deck():
    words = pd.read_csv("word.csv", header=0)
    words_cnt = len(words)
    deck1 = words.sample(n=words_cnt//2)
    deck2 = words.drop(deck1.index).sample(n=words_cnt//2)
    return deck1, deck2

def battle(player1:Player, player2:Player):
    print(f"{player1.monster.name} （{player1.monster.attr}属性）")
    print(f"{player2.monster.name} （{player2.monster.attr}属性）")

    if player1.monster.speed == player1.monster.speed:
        players = random.choice([[player1, player2], [player2, player1]])
    else:
        players = [player1, player2] if player1.monster.speed > player2.monster.speed else [player2, player1]
    winner = ""
    for player in players:
        attacker = player
        defender = player2 if player==player1 else player1
        print(f"{attacker.name}：{player.monster.name}の攻撃！")
        attr_combination = (attacker.monster.attr, defender.monster.attr)
        if attr_combination in [("火", "草"), ("草", "水"), ("水", "火")]:
            attack_multiplier = 2
        elif attr_combination in [("草", "火"), ("水", "草"), ("火", "水")]:
            attack_multiplier = 0.5
        elif attacker.monster.attr != "無" and defender.monster.attr == "無":
            attack_multiplier = 1.5
        elif attacker.monster.attr == "無" and defender.monster.attr != "無":
            attack_multiplier = 0.7
        else:
            attack_multiplier = 1
        print(f"{attacker.monster.attr}属性 → {defender.monster.attr}属性　攻撃力{attack_multiplier}倍")
        damage = int(attack_multiplier * attacker.monster.attack - defender.monster.defend)
        if damage > 0:
            defender.hp -= damage
            print(f"{defender.name}に{damage}のダメージ！ 残HP{defender.hp}")
            if defender.hp <= 0:
                winner = attacker
        else:
            print("ダメージを与えられない！")
    return winner


def game():
    words = Words()
    player1_name = words.make_random_name()
    player2_name = words.make_random_name()
    deck1, deck2 = words.make_deck()
    player1 = Player(player1_name, deck=deck1)
    player2 = Player(player2_name, deck=deck2)

    while True:
        for player in [player1, player2]:
            player.call_random_monster()

        winner = battle(player1, player2)
        if winner != "":
            print(f"winner {winner.name}")
            break

        if len(player1.deck) == 0:
            print("カード切れ")
            break

        input()


if __name__ == "__main__":
    game()
