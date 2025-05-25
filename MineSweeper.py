import sys, pygame
from math import floor
from random import randint
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_SPACE

WIDTH = 20
HEIGHT = 15
SIZE = 50
NUM_OF_BOMBS = 20
EMPTY = 0
BOMB = 1
OPENED = 2
OPEN_COUNT = 0
CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
flagxy = []

bombImage = pygame.image.load("bomb.png")
flagImage = pygame.image.load("flag.png")

pygame.init()
SURFACE = pygame.display.set_mode([WIDTH*SIZE, HEIGHT*SIZE])
pygame.display.set_caption("Mine Sweeper")
FPSCLOCK = pygame.time.Clock()

def num_of_bomb(field, x_pos, y_pos):
    count = 0
    for yoffset in range(-1, 2):
        for xoffset in range(-1, 2):
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == BOMB:
                count += 1
    return count

def open_tile(field, x_pos, y_pos):
    global OPEN_COUNT
    if CHECKED[y_pos][x_pos]:
        return

    CHECKED[y_pos][x_pos] = True

    if (y_pos, x_pos) in flagxy:
        flagxy.remove((y_pos, x_pos))

    if field[y_pos][x_pos] == EMPTY:
        field[y_pos][x_pos] = OPENED
        OPEN_COUNT += 1

    count = num_of_bomb(field, x_pos, y_pos)

    if count == 0:
        for yoffset in range(-1, 2):
            for xoffset in range(-1, 2):
                xpos, ypos = x_pos + xoffset, y_pos + yoffset
                if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT:
                    if not CHECKED[ypos][xpos] and field[ypos][xpos] != BOMB:
                        open_tile(field, xpos, ypos)



def runGame():
    global flagxy
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_clear = largefont.render("!!CLEARED!!", True, (0, 255, 225))
    message_over = largefont.render("GAME OVER!!", True, (0, 255, 225))
    message_rect = message_clear.get_rect()
    message_rect.center = (WIDTH*SIZE/2, HEIGHT*SIZE/2)
    game_over = False

    field = [[EMPTY for xpos in range(WIDTH)]
             for ypos in range(HEIGHT)]

    count = 0
    while count < NUM_OF_BOMBS:
        xpos, ypos = randint(0, WIDTH-1), randint(0, HEIGHT-1)
        if field[ypos][xpos] == EMPTY:
            field[ypos][xpos] = BOMB
            count += 1

    while True:
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                xpos, ypos = floor(event.pos[0] / SIZE), floor(event.pos[1] / SIZE)
                if field[ypos][xpos] == BOMB:
                    game_over = True
                else:
                    if (ypos, xpos) in flagxy:
                        flagxy.remove((ypos, xpos))
                    open_tile(field, xpos, ypos)

            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                xidx, yidx = floor(event.pos[0] / SIZE), floor(event.pos[1] / SIZE)
                if (yidx, xidx) not in flagxy:
                    if not CHECKED[yidx][xidx]:
                        flagxy.append((yidx, xidx))
                else:
                    flagxy.remove((yidx, xidx))

        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                tile = field[ypos][xpos]
                rect = (xpos*SIZE, ypos*SIZE, SIZE, SIZE)

                if tile == EMPTY or tile == BOMB:
                    pygame.draw.rect(SURFACE, (192, 192, 192), rect)
                    if game_over and tile == BOMB:
                        SURFACE.blit(bombImage, rect)
                elif tile == OPENED:
                    count = num_of_bomb(field, xpos, ypos)
                    if count > 0:
                        num_image = smallfont.render("{}".format(count), True, (255, 255, 0))
                        SURFACE.blit(num_image, (xpos*SIZE+10, ypos*SIZE+10))

        for index in range(0, WIDTH*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96), (index, 0), (index, HEIGHT*SIZE))
        for index in range(0, HEIGHT*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96), (0, index), (WIDTH*SIZE, index))

        for yidx, xidx in flagxy[:]:
            if CHECKED[yidx][xidx]:
                flagxy.remove((yidx, xidx))

        if game_over:
            font = pygame.font.SysFont(None, 50)
            for yidx, xidx in flagxy[:]:
                rect = (xidx * SIZE, yidx * SIZE, SIZE, SIZE)
                if field[yidx][xidx] != BOMB:
                    x_image = font.render('X', True, (255, 0, 0))
                    SURFACE.blit(x_image, (xidx*SIZE+10, yidx*SIZE+5))
                    flagxy.remove((yidx, xidx))
                else:
                    SURFACE.blit(flagImage, rect)
        else:
            for yidx, xidx in flagxy:
                rect = (xidx * SIZE, yidx * SIZE, SIZE, SIZE)
                SURFACE.blit(flagImage, rect)

        if OPEN_COUNT == WIDTH*HEIGHT - NUM_OF_BOMBS:
            SURFACE.blit(message_clear, message_rect.topleft)
        elif game_over:
            SURFACE.blit(message_over, message_rect.topleft)
            return restart()

        pygame.display.update()
        FPSCLOCK.tick(15)


def main():
    font = pygame.font.SysFont(None, 40)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return runGame()
        txt = font.render("Press space to start", True, (255, 255, 255))
        Rect = txt.get_rect()
        Rect.center = (WIDTH*SIZE/2, HEIGHT*SIZE/2)
        SURFACE.blit(txt, Rect.topleft)
        pygame.display.update()
        FPSCLOCK.tick(15)

def init():
    global WIDTH, HEIGHT, SIZE, NUM_OF_BOMBS, EMPTY, BOMB, OPENED, OPEN_COUNT, CHECKED, flagxy
    WIDTH = 20
    HEIGHT = 15
    SIZE = 50
    NUM_OF_BOMBS = 20
    EMPTY = 0
    BOMB = 1
    OPENED = 2
    OPEN_COUNT = 0
    CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    flagxy = []

def restart():
    font = pygame.font.SysFont(None, 40)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    init()
                    return runGame()
        txt = font.render("Press space to restart", True, (0, 255, 170))
        Rect = txt.get_rect()
        Rect.center = (WIDTH*SIZE/2, HEIGHT*SIZE/2+40)
        SURFACE.blit(txt, Rect.topleft)
        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
