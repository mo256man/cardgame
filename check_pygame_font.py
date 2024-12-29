import pygame
from pygame.locals import *

def isSame_bitmap(font, char):
    surface1 = font.render(char[0], True, 'white', 'black')
    surface2 = font.render(char[1], True, 'white', 'black')
    if surface1.get_size() != surface2.get_size(): return False
    width, height = surface1.get_size()
    for y in range(height):
        for x in range(width):
            if surface1.get_at((x, y)) != surface2.get_at((x, y)): return False
    return True

pygame.init()
screen = pygame.display.set_mode((900, 400))

fontList = []
for fontname in sorted(pygame.font.get_fonts()):
    try:
        font = pygame.font.SysFont(fontname, 30)
        if isSame_bitmap(font, 'iW'): continue #⭐️
        if isSame_bitmap(font, 'あ漢'): continue
        fontList.append(fontname)
    except:
        pass

clock = pygame.time.Clock()

fontIndex, oldIndex = 0, -1
done = False
while not done:
    clock.tick(10)
    pygame.display.set_caption(f'[{fontIndex + 1}/{len(fontList)}] {fontList[fontIndex]}')
    if oldIndex != fontIndex:
        print(f'[{fontIndex + 1}] {fontList[fontIndex]}')
    oldIndex = fontIndex

    screen.fill('black')

    font = pygame.font.SysFont(fontList[fontIndex], 30)
    surface1 = font.render(fontList[fontIndex], True, 'white')
    surface2 = font.render("1234567890", True, 'white')
    surface3 = font.render("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~", True, 'white')
    surface4 = font.render("ABCDEFGHIJKLMNOPQRSTUVWXYZ", True, 'white')
    surface5 = font.render("abcdefghijklmnopqrstuvwxyz", True, 'white')
    try:
        surface6 = font.render("あいうえおアイウエオ漢字、日本語。", True, 'white')
    except Exception as e:
        surface6 = font.render(f"NIHONGO Exception: {str(e)}", True, 'white')

    screen.blit(surface1, [20,  20])
    screen.blit(surface2, [20,  70])
    screen.blit(surface3, [20, 120])
    screen.blit(surface4, [20, 170])
    screen.blit(surface5, [20, 220])
    screen.blit(surface6, [20, 270])

    pygame.display.update()

    if fontIndex < len(fontList) - 1:
        fontIndex += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True #exit
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                done = True #exit

pygame.quit()
