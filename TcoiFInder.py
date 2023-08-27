import pygame
import random


def respawn_target(tcoi_flag):
    if tcoi_flag:
        target_tcoi_rect.x = random.randint(0, W - target_tcoi_rect.w)
        target_tcoi_rect.y = random.randint(0, H - target_tcoi_rect.h)
    else:
        target_netcoi_rect.x = random.randint(0, W - target_netcoi_rect.w)
        target_netcoi_rect.y = random.randint(0, H - target_netcoi_rect.h)

def random_for_tcoi():
    if random.randint(0, 10) < 2:
        tcoi_flag = False
    else:
        tcoi_flag = True
    return tcoi_flag


pygame.init()
pygame.font.init()
pygame.display.set_caption("TcoiFinder v0.0.1")

W = 600
H = 800
SCREEN_SIZE = (W, H)
SCREEN_CENTER = (W//2, H//2)
SCREEN_TOP = (W//2, 0)
SCREEN_BOT = (W//2, H-100)

screen = pygame.display.set_mode(SCREEN_SIZE)

FPS = 60
clock = pygame.time.Clock()

ARIAL_FONT_PATH = pygame.font.match_font('arial')
ARIAL_64 = pygame.font.Font(ARIAL_FONT_PATH, 64)
ARIAL_32 = pygame.font.Font(ARIAL_FONT_PATH, 32)

INIT_DELAY = 2000
finish_delay = INIT_DELAY
DECREASE_BASE = 1.002
last_respawn_time = 0

game_over = False
RETRY_SURFACE = ARIAL_32.render('Нажми любую кнопку', True, (0, 0, 0))
RETRY_RECT = RETRY_SURFACE.get_rect()
RETRY_RECT.midtop = SCREEN_CENTER

SKIP_SURFACE = ARIAL_32.render('SKIP', True, (0, 0, 0))
SKIP_RECT = SKIP_SURFACE.get_rect()
SKIP_RECT.midtop = SCREEN_BOT

score = 0

TARGET_TCOI_IMAGE = pygame.image.load('Tcoi.png')
TARGET_TCOI_IMAGE = pygame.transform.scale(TARGET_TCOI_IMAGE, (80, 120))
target_tcoi_rect = TARGET_TCOI_IMAGE.get_rect()

TARGET_NETCOI_IMAGE = pygame.image.load('NeTcoi.png')
TARGET_NETCOI_IMAGE = pygame.transform.scale(TARGET_NETCOI_IMAGE, (80, 120))
target_netcoi_rect = TARGET_NETCOI_IMAGE.get_rect()



tcoi_flag = True
running = True

respawn_target(tcoi_flag)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if game_over:
                score = 0
                finish_delay = INIT_DELAY
                game_over = False
                last_respawn_time = pygame.time.get_ticks()

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == pygame.BUTTON_LEFT:
                if not game_over:
                    if target_tcoi_rect.collidepoint(e.pos) or (SKIP_RECT.collidepoint(e.pos) and tcoi_flag == False):
                        score += 1
                        tcoi_flag = random_for_tcoi()
                        respawn_target(tcoi_flag)
                        last_respawn_time = pygame.time.get_ticks()
                        finish_delay = INIT_DELAY / (DECREASE_BASE ** score)
                    elif target_netcoi_rect.collidepoint(e.pos) or (SKIP_RECT.collidepoint(e.pos) and tcoi_flag == True):
                        game_over = True


    clock.tick(FPS)

    screen.fill((255, 255, 0))
    score_surface = ARIAL_64.render(str(score), True, (0, 0, 0))
    score_rect = score_surface.get_rect()

    now = pygame.time.get_ticks()
    elapsed = now - last_respawn_time
    if elapsed > finish_delay or game_over:
        game_over = True

        score_rect.midbottom = SCREEN_CENTER

        screen.blit(RETRY_SURFACE, RETRY_RECT)
    else:
        h = H - H * elapsed / finish_delay
        time_rect = pygame.Rect((0, 0), (W, h))
        time_rect.bottomleft = (0, H)
        pygame.draw.rect(screen, (233, 150, 122), time_rect)

        if tcoi_flag:
            screen.blit(TARGET_TCOI_IMAGE, target_tcoi_rect)
        else:
            screen.blit(TARGET_NETCOI_IMAGE, target_netcoi_rect)

        score_rect.midtop = SCREEN_TOP
        screen.blit(SKIP_SURFACE, SKIP_RECT)

    screen.blit(score_surface, score_rect)




    pygame.display.flip()
pygame.quit()






