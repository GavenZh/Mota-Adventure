import pygame
from modules.sprites import Button
from utils import QuitGame


'''游戏开始界面'''
class StartGameInterface():
    def __init__(self, cfg):
        self.cfg = cfg
        self.play_btn = Button('开始游戏', cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 50, (cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1] - 300))
        self.intro_btn = Button('游戏说明', cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 50, (cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1] - 200))
        self.quit_btn = Button('离开游戏', cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 50, (cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1] - 100))
    '''外部调用'''
    def run(self, screen):
        # 魔塔
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 80)
        font_render_cn = font.render('魔塔', True, (255, 255, 255))
        rect_cn = font_render_cn.get_rect()
        rect_cn.center = self.cfg.SCREENSIZE[0] // 2, 100
        # Magic Tower
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_en'], 80)
        font_render_en = font.render('Magic Tower', True, (255, 255, 255))
        rect_en = font_render_en.get_rect()
        rect_en.center = self.cfg.SCREENSIZE[0] // 2, 250
        # (Ver 1.12)
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 40)
        font_render_version = font.render('(Ver 1.12)', True, (255, 255, 255))
        rect_ver = font_render_version.get_rect()
        rect_ver.center = self.cfg.SCREENSIZE[0] // 2, 300
        # 主循环
        clock = pygame.time.Clock()
        while True:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.play_btn.rect.collidepoint(mouse_pos):
                            return True
                        elif self.quit_btn.rect.collidepoint(mouse_pos):
                            QuitGame()
                        elif self.intro_btn.rect.collidepoint(mouse_pos):
                            self.showgameintro(screen)
            for btn in [self.intro_btn, self.play_btn, self.quit_btn]:
                btn.update()
                btn.draw(screen)
            for fr, rect in zip([font_render_cn, font_render_en, font_render_version], [rect_cn, rect_en, rect_ver]):
                screen.blit(fr, rect)
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
    '''显示游戏简介'''
    def showgameintro(self, screen):
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        font_renders = [
            font.render('魔塔小游戏.', True, (255, 255, 255)),
            font.render('游戏素材来自: http://www.4399.com/flash/1749_1.htm.', True, (255, 255, 255)),
            font.render('游戏背景故事为公主被大魔王抓走, 需要勇士前往魔塔将其救出.', True, (255, 255, 255)),
            font.render('作者: GavenZh', True, (255, 255, 255)),
        ]
        rects = [fr.get_rect() for fr in font_renders]
        for idx, rect in enumerate(rects):
            rect.center = self.cfg.SCREENSIZE[0] // 2, 50 * idx + 50
        clock = pygame.time.Clock()
        while True:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.play_btn.rect.collidepoint(mouse_pos):
                            return True
                        elif self.quit_btn.rect.collidepoint(mouse_pos):
                            QuitGame()
                        elif self.intro_btn.rect.collidepoint(mouse_pos):
                            return
            for btn in [self.intro_btn, self.play_btn, self.quit_btn]:
                btn.update()
                btn.draw(screen)
            for fr, rect in zip(font_renders, rects):
                screen.blit(fr, rect)
            pygame.display.flip()
            clock.tick(self.cfg.FPS)