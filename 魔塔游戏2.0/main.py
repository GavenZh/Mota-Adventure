import css
import copy
import pygame, sys


def main():
    pygame.init()  # 需要初始化，必须
    pygame.mixer.init()  # 导入音乐初始化
    logo = pygame.image.load("./imgs/logo.png")  # 导入logo图片
    pygame.display.set_icon(logo)  # 设置图片为logo
    root = pygame.display.set_mode((900, 650), 0, 32)
    pygame.display.set_caption("魔塔探险：拯救之旅")
    clock = pygame.time.Clock()

    class Mt:
        def __init__(self):
            pygame.mouse.set_visible(False)  # 将鼠标隐藏
            # 导入字体
            self.font = pygame.font.Font("./font/simhei.ttf", 28)
            # 导入音效
            self.yy_bj0 = pygame.mixer.Sound("./sound/0背景音乐.wav")
            self.yy_bj1 = pygame.mixer.Sound("./sound/1背景音乐.wav")
            self.yy_bj13 = pygame.mixer.Sound("./sound/13背景音乐.wav")
            self.yy_bj18 = pygame.mixer.Sound("./sound/18背景音乐.wav")
            self.yy_yx0 = pygame.mixer.Sound("./sound/打击音效.wav")
            self.yy_yx1 = pygame.mixer.Sound("./sound/怪物死亡音效.wav")
            self.yy_yx2 = pygame.mixer.Sound("./sound/获得物品音效.wav")
            self.yy_yx3 = pygame.mixer.Sound("./sound/开门音效.wav")
            self.yy_yx4 = pygame.mixer.Sound("./sound/魔法音效.wav")
            self.yy_yx5 = pygame.mixer.Sound("./sound/升级音效.wav")
            self.yy_yx6 = pygame.mixer.Sound("./sound/提升音效.wav")
            self.yy_yx7 = pygame.mixer.Sound("./sound/不能攻击音效.wav")
            # 导入界面图片
            self.a0 = pygame.image.load("./imgs/jm/a0.png")
            self.a1 = pygame.image.load("./imgs/jm/a1.png")
            self.a2 = pygame.image.load("./imgs/jm/a2.png")
            self.b0 = pygame.image.load("./imgs/jm/b0.png")
            self.b1 = pygame.image.load("./imgs/jm/b1.png")
            self.b2 = pygame.image.load("./imgs/jm/b2.png")
            self.b3 = pygame.image.load("./imgs/jm/b3.png")
            self.c0 = pygame.image.load("./imgs/jm/c0.png")
            self.d0 = pygame.image.load("./imgs/jm/d0.png")
            self.e0 = pygame.image.load("./imgs/jm/e0.png")
            self.f0 = pygame.image.load("./imgs/jm/f0.png")
            self.g0 = pygame.image.load("./imgs/jm/g0.png")
            self.h0 = pygame.image.load("./imgs/jm/h0.png")
            self.i0 = pygame.image.load("./imgs/jm/i0.png")
            self.k0 = pygame.image.load("./imgs/jm/k0.png")
            self.sb = pygame.image.load("./imgs/jm/sb.png")
            # 导入游戏图片
            self.dx0 = pygame.image.load("./imgs/img/dx0.png")
            self.gw0 = pygame.image.load("./imgs/img/gw0.png")
            self.js0 = pygame.image.load("./imgs/img/js0.png")
            self.npc0 = pygame.image.load("./imgs/img/npc0.png")
            self.wp0 = pygame.image.load("./imgs/img/wp0.png")
            # 导入对话图片
            self.dh0 = pygame.image.load("./imgs/dh/dh0.png")
            self.jgn0 = pygame.image.load("./imgs/dh/jgn0.png")
            self.jgn1 = pygame.image.load("./imgs/dh/jgn1.png")
            self.lgn0 = pygame.image.load("./imgs/dh/lgn0.png")
            self.sr0 = pygame.image.load("./imgs/dh/sr0.png")
            self.sr1 = pygame.image.load("./imgs/dh/sr1.png")
            # 设置界面所在位置
            self.jmnum = 0
            self.jm0num = 569
            self.escy = 0  # 用于控制d0的y切图
            self.esckg = False  # 用于控制是否打开退出按钮
            self.jm1num = 0
            self.f4kg = False  # 用于处理说明按钮 F4键
            self.initkg = False  # 用于处理F5键的按钮
            self.f5y = 0
            self.endkg = False  # 处理游戏通关
            self.endy = 474  # 处理游戏通关
            self.swkg = False  # 角色失败
            # 导入CSS文件内容
            # 导入22层的地图,需要使用copy深度拷贝，当数据修改时候不会对列表进行修改
            self.css = copy.deepcopy(
                [css.cs0, css.cs1, css.cs2, css.cs3, css.cs4, css.cs5, css.cs6, css.cs7, css.cs8, css.cs9, css.cs10,
                 css.cs11, css.cs12, css.cs13, css.cs14, css.cs15, css.cs16, css.cs17, css.cs18, css.cs19, css.cs20,
                 css.cs21])
            # 导入怪物信息
            self.gwlist = css.gwlist

            self.cs = 0  # 当前楼层数
            self.npcyd = 0  # 让渲染动起来
            self.jsx, self.jsy = 0, 0
            # 设置开启关闭快速战斗
            self.pksd = False

            self.puvskg = False  # 打开普通战斗
            self.pu_gw, self.pu_xy = None, None

            # 角色信息 等级 生命、攻击、防御、金币、钥匙1/2/3
            self.dj, self.sm, self.gj, self.fy, self.jb, self.jy, self.ys0, self.ys1, self.ys2 = 0, 1000, 10000, 100000, 0, 0, 0, 0, 0
            # 设置动态的帧率
            self.clock_s = 0
            self.clock_ts = 0  # 用于提示的闪烁计时
            self.baocunkg = None
            # 锁定方向键
            self.yidongkg = True
            # 处理对话
            # 和精灵的对话
            self.jldh = 0
            self.dh_200 = False
            self.wp_309 = False

            # 和侠盗的对话
            self.xddh = 0
            self.dh_201 = False
            self.wp_305 = False
            # 和公主的对话
            self.dh_202 = False
            self.gz_18 = False

            self.dh_211 = False
            self.dh_212 = False
            self.dh_213 = False
            self.dh_214 = False
            # 处理商店
            self.sdnum = [None, None]  # 0表示商店属性，1表示选择到那个位置。
            self.sdkg = False
            self.sdxz = [[415, 244], [415, 286], [415, 327], [415, 370]]
            # 处理J功能 实现楼层间的跳转
            self.lc = 0  # 已经到过的楼层
            self.lpkg = False  # 是否启用该功能
            self.leapgn = False  # 用于是否获得该功能
            self.list_yes = (
                (1, 1, 2), (2, 10, 1), (3, 10, 11), (4, 10, 1), (5, 10, 10), (6, 10, 5), (7, 1, 2), (8, 5, 8),
                (9, 8, 7),
                (10, 10, 1), (11, 11, 10), (12, 11, 2), (13, 11, 5), (14, 1, 4), (15, 1, 8), (16, 7, 6), (17, 11, 2),
                (18, 11, 10), (19, 5, 6), (20, 8, 5))
            self.list_nos = (
                (1, 10, 6), (2, 2, 1), (3, 11, 2), (4, 10, 11), (5, 11, 2), (6, 11, 9), (7, 11, 6), (8, 2, 1),
                (9, 4, 7),
                (10, 7, 5), (11, 11, 2), (12, 11, 10), (13, 11, 2), (14, 10, 6), (15, 1, 4), (16, 1, 6), (17, 9, 6),
                (18, 11, 2), (19, 11, 10), (20, 5, 6))
            self.jgn1_list = (
                (342, 111), (342, 171), (342, 232), (342, 293), (342, 354), (342, 414), (342, 475), (342, 537),
                (520, 111),
                (520, 171), (520, 232), (520, 293), (520, 354), (520, 414), (520, 475), (520, 537), (712, 111),
                (712, 171),
                (712, 232), (712, 293), (712, 354))
            self.lpxz = 0
            # 处理L功能
            self.cxkg = False
            self.cxgn = False
            # 用于读取保存
            self.list_list = []
            self.yypd = None

        def yyfun(self):  # 处理背景音乐的功能
            if self.cs == 0:
                if self.yypd == 0:
                    pass
                else:
                    self.yy_bj0.play(-1)
                    self.yy_bj1.stop()
                    self.yy_bj13.stop()
                    self.yy_bj18.stop()
                    self.yypd = 0
            elif 0 < self.cs < 13:
                if self.yypd == 1:
                    pass
                else:
                    self.yy_bj0.stop()
                    self.yy_bj1.play(-1)
                    self.yy_bj13.stop()
                    self.yy_bj18.stop()
                    self.yypd = 1
            elif 13 <= self.cs < 17:
                if self.yypd == 2:
                    pass
                else:
                    self.yy_bj0.stop()
                    self.yy_bj1.stop()
                    self.yy_bj13.play(-1)
                    self.yy_bj18.stop()
                    self.yypd = 2
            elif self.cs >= 17:
                if self.yypd == 3:
                    pass
                else:
                    self.yy_bj0.stop()
                    self.yy_bj1.stop()
                    self.yy_bj13.stop()
                    self.yy_bj18.play(-1)
                    self.yypd = 3

        def cxxrfun(self):  # L查询功能能的渲染
            if self.cxkg == True and self.cxgn == True:
                root.blit(self.lgn0, (300, 50))
                gwa, gwb = [], []
                for i in self.css[self.cs]:
                    for n in i:
                        if 600 <= n:
                            gwa.append(n)
                gwa = set(gwa)
                gwa = list(gwa)
                ty = [100, 162, 224, 286, 348, 410, 472, 534]
                wy = [110, 174, 236, 294, 357, 419, 482, 544]
                for i in range(len(gwa)):
                    for n in self.gwlist:
                        if n[0] == gwa[i]:
                            gwb.append(n)
                for i in range(len(gwb)):
                    root.blit(self.gw0, (317, ty[i]), (gwb[i][6] + self.npcyd, gwb[i][7], 50, 50))
                    gw_sm = self.font.render(str(gwb[i][1]), True, (255, 255, 255))
                    gw_gj = self.font.render(str(gwb[i][2]), True, (255, 255, 255))
                    gw_fy = self.font.render(str(gwb[i][3]), True, (255, 255, 255))
                    gw_jb = self.font.render(str(gwb[i][4]), True, (255, 255, 255))
                    gw_jy = self.font.render(str(gwb[i][5]), True, (255, 255, 255))
                    sh = self.shfun(gwb[i])  # 损耗计算
                    gw_sh = self.font.render(str(sh), True, (255, 255, 255))
                    root.blit(gw_sm, (377, wy[i]))
                    root.blit(gw_gj, (467, wy[i]))
                    root.blit(gw_fy, (545, wy[i]))
                    root.blit(gw_jb, (630, wy[i]))
                    root.blit(gw_jy, (708, wy[i]))
                    root.blit(gw_sh, (775, wy[i]))

        def shfun(self, gw):  # 对战时属性更新
            sm = copy.deepcopy(self.sm)
            if self.gj >= gw[3] and gw[2] <= self.fy:
                return 0
            if self.gj <= gw[3]:
                return "???"
            if gw[1] < self.gj:
                return 0
            xsm = sm - (gw[1] // (self.gj - gw[3]) * (gw[2] - self.fy))  # 【快速战斗算法！】
            if xsm <= 0:
                return "???"
            else:
                return self.sm - xsm

        def lpxrfun(self):  # J飞跃功能的渲染
            if self.lpkg == True and self.leapgn == True:
                root.blit(self.jgn0, (300, 50))
                root.blit(self.jgn1, (self.jgn1_list[self.lpxz][0], self.jgn1_list[self.lpxz][1]))

        def sdxrfun(self):  # 处理商店的渲染
            if self.sdnum[0] == 0 and self.sdkg == True:  # 3层金币商店
                root.blit(self.sr0, (396, 125), (0, 0, 360, 300))
                root.blit(self.sr1, (self.sdxz[self.sdnum[1]][0], self.sdxz[self.sdnum[1]][1]))
            elif self.sdnum[0] == 1 and self.sdkg == True:  # 高级金币商店
                root.blit(self.sr0, (396, 125), (0, 300, 360, 300))
                root.blit(self.sr1, (self.sdxz[self.sdnum[1]][0], self.sdxz[self.sdnum[1]][1]))
            elif self.sdnum[0] == 2 and self.sdkg == True:  # 经验商店
                root.blit(self.sr0, (396, 125), (0, 600, 360, 300))
                root.blit(self.sr1, (self.sdxz[self.sdnum[1]][0], self.sdxz[self.sdnum[1]][1]))
            elif self.sdnum[0] == 3 and self.sdkg == True:  # 高级经验商店
                root.blit(self.sr0, (396, 125), (0, 900, 360, 300))
                root.blit(self.sr1, (self.sdxz[self.sdnum[1]][0], self.sdxz[self.sdnum[1]][1]))
            elif self.sdnum[0] == 4 and self.sdkg == True:  # 卖钥匙
                root.blit(self.sr0, (396, 125), (0, 1200, 360, 300))
                root.blit(self.sr1, (self.sdxz[self.sdnum[1]][0], self.sdxz[self.sdnum[1]][1]))
            elif self.sdnum[0] == 5 and self.sdkg == True:  # 买钥匙回收
                root.blit(self.sr0, (396, 125), (0, 1500, 360, 300))
                root.blit(self.sr1, (self.sdxz[self.sdnum[1]][0], self.sdxz[self.sdnum[1]][1]))

        def fontfun(self):  # 信息栏字体渲染
            # 等级、生命、攻击、防御、金币、经验、楼层层数。3种钥匙
            dj_font = self.font.render(f'{self.dj}', True, (255, 255, 255))
            sm_font = self.font.render(f'{self.sm}', True, (255, 255, 255))
            gj_font = self.font.render(f'{self.gj}', True, (255, 255, 255))
            fy_font = self.font.render(f'{self.fy}', True, (255, 255, 255))
            jb_font = self.font.render(f'{self.jb}', True, (255, 255, 255))
            jy_font = self.font.render(f'{self.jy}', True, (255, 255, 255))
            cs_font = self.font.render(f'{self.cs}', True, (255, 255, 255))
            ys0_font = self.font.render(f'{self.ys0}', True, (255, 255, 255))
            ys1_font = self.font.render(f'{self.ys1}', True, (255, 255, 255))
            ys2_font = self.font.render(f'{self.ys2}', True, (255, 255, 255))
            root.blit(dj_font, (144, 73))
            root.blit(sm_font, (140, 118))
            root.blit(gj_font, (140, 153))
            root.blit(fy_font, (140, 183))
            root.blit(jb_font, (140, 218))
            root.blit(jy_font, (140, 253))
            root.blit(cs_font, (154, 298))
            root.blit(ys0_font, (155, 340))
            root.blit(ys1_font, (155, 380))
            root.blit(ys2_font, (155, 420))

        def movefun(self, num):  # 角色移动
            if self.yidongkg:
                if num == 4:
                    self.pzfun((-1, 0))
                    self.jsy = 50
                elif num == 8:
                    self.pzfun((0, -1))
                    self.jsy = 150
                elif num == 6:
                    self.pzfun((1, 0))
                    self.jsy = 100
                elif num == 2:
                    self.pzfun((0, 1))
                    self.jsy = 0

        def pzfun(self, xy):  # 碰撞处理
            if self.clock_s % 2 == 0:  # 与速度有关
                for y in range(len(self.css[self.cs])):
                    for x in range(len(self.css[self.cs][y])):
                        if self.css[self.cs][y][x] == 555:
                            if self.css[self.cs][y + xy[1]][x + xy[0]] == 101 or self.css[self.cs][y + xy[1]][
                                x + xy[0]] == 105:  # 开锁（过梯子）
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 108:  # 上楼
                                self.cs += 1
                                if self.lc < self.cs:
                                    self.lc = copy.deepcopy(self.cs)
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 109:  # 下楼
                                self.cs -= 1
                                return

                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 300:
                                self.sm += 200
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 301:
                                self.sm += 500
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 302:
                                self.gj += 3
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 303:
                                self.fy += 3
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 304:
                                self.jb += 200
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 305:
                                self.wp_305 = True  # 获得镐子
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 306:
                                self.ys0 += 1
                                self.ys1 += 1
                                self.ys2 += 1
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 307:
                                self.leapgn = True  # 获得J功能实现已去过楼层跳转
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 308:
                                self.cxgn = True  # 实现L功能
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 309:
                                self.wp_309 = True  # 获得十字架
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 310:
                                self.dj += 1
                                self.sm += 1000
                                self.gj += 7
                                self.fy += 7
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx5.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 311:
                                self.dj += 3
                                self.sm += 3000
                                self.gj += 21
                                self.fy += 21
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx5.play()
                                return
                            # 捡拾道具
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 321:
                                self.ys0 += 1
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx5.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 312:
                                self.sm = self.sm * 2
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 313:
                                self.gj += 10
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 314:
                                self.fy += 10
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 315:
                                self.gj += 70
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 316:
                                self.fy += 85
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 317:
                                self.gj += 150
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 318:
                                self.fy += 190
                                self.yy_yx2.play()
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                return
                                # 获得钥匙的时候
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 319:
                                self.ys0 += 1
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 320:
                                self.ys1 += 1
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 321:
                                self.ys2 += 1
                                self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                self.css[self.cs][y][x] = 101
                                self.yy_yx2.play()
                                return
                            # 碰撞建筑物
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 110:  # 黄门
                                if self.ys0 >= 1:
                                    self.ys0 -= 1
                                    self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                    self.css[self.cs][y][x] = 101
                                    self.yy_yx3.play()
                                    return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 111:  # 蓝门
                                if self.ys1 >= 1:
                                    self.ys1 -= 1
                                    self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                    self.css[self.cs][y][x] = 101
                                    self.yy_yx3.play()
                                    return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 112:  # 红门
                                if self.ys2 >= 1:
                                    self.ys2 -= 1
                                    self.css[self.cs][y + xy[1]][x + xy[0]] = 555
                                    self.css[self.cs][y][x] = 101
                                    self.yy_yx3.play()
                                    return
                            # 碰撞任务
                            # 处理和精灵的对话
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 200:
                                self.yidongkg, self.dh_200 = False, True
                                return
                            # 处理和侠盗的对话
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 201:
                                self.yidongkg, self.dh_201 = False, True
                                return
                            # 处理和公主的对话
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 202:
                                if self.gz_18 == True:
                                    self.yidongkg, self.dh_202 = False, True
                            # 处理4个对话
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 211:
                                self.yidongkg, self.dh_211 = False, True
                                self.yy_yx5.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 212:
                                self.yidongkg, self.dh_212 = False, True
                                self.yy_yx5.play()
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 213:
                                self.yidongkg, self.dh_213 = False, True
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 214:
                                self.yidongkg, self.dh_214 = False, True
                                return
                            # 处理商店
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 207:  # 3层金币商店
                                self.sdnum = [0, 0]
                                self.sdkg = True
                                self.yidongkg = False
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 208:  # 11层金币商店
                                self.sdnum = [1, 0]
                                self.sdkg = True
                                self.yidongkg = False
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 205:
                                self.sdnum = [2, 0]
                                self.sdkg = True
                                self.yidongkg = False
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 206:
                                self.sdnum = [3, 0]
                                self.sdkg = True
                                self.yidongkg = False
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 203:
                                self.sdnum = [4, 0]
                                self.sdkg = True
                                self.yidongkg = False
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 204:
                                self.sdnum = [5, 0]
                                self.sdkg = True
                                self.yidongkg = False
                                return
                            # 怪物碰撞
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 600:
                                self.vsfun(0, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 601:
                                self.vsfun(1, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 602:
                                self.vsfun(2, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 603:
                                self.vsfun(3, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 604:
                                self.vsfun(4, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 605:
                                self.vsfun(5, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 606:
                                self.vsfun(6, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 607:
                                self.vsfun(7, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 608:
                                self.vsfun(8, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 609:
                                self.vsfun(9, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 610:
                                self.vsfun(10, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 611:
                                self.vsfun(11, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 612:
                                self.vsfun(12, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 613:
                                self.vsfun(13, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 614:
                                self.vsfun(14, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 615:
                                self.sm -= 100
                                self.yy_yx4.play()
                                self.vsfun(15, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 616:
                                self.sm -= 300
                                self.yy_yx4.play()
                                self.vsfun(16, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 617:
                                self.sm -= int(self.sm * 0.3)
                                self.yy_yx4.play()
                                self.vsfun(17, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 618:
                                self.vsfun(18, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 619:
                                self.vsfun(19, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 620:
                                self.vsfun(20, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 621:
                                self.vsfun(21, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 622:
                                self.vsfun(22, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 623:
                                self.vsfun(23, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 624:
                                self.sm -= int(self.sm * 0.3)
                                self.yy_yx4.play()
                                self.vsfun(24, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 625:
                                self.vsfun(25, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 626:
                                self.vsfun(26, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 627:
                                self.vsfun(27, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 628:
                                self.vsfun(28, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 629:
                                self.vsfun(29, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 630:
                                self.vsfun(30, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 631:
                                self.vsfun(31, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 632:
                                self.vsfun(32, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 633:
                                self.vsfun(33, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 634:
                                self.yy_yx4.play()
                                self.sm -= int(self.sm * 0.3)
                                self.vsfun(34, [y, x, xy[1], xy[0]])
                                return
                            elif self.css[self.cs][y + xy[1]][x + xy[0]] == 635:
                                self.vsfun(35, [y, x, xy[1], xy[0]])

        def vsfun(self, num, xy):
            gw = copy.deepcopy(self.gwlist[num])
            sm = copy.deepcopy(self.sm)
            if self.pksd == True:  # 快速战斗状态下
                if self.gj <= gw[3]:  # 自身攻击小于怪物防御的时候
                    if self.fy < gw[2]:  # 怪物攻击大于自身防御的时候
                        self.swkg = True
                    elif self.fy >= gw[2]:  # 自身防御超过了怪物的攻击
                        self.yy_yx7.play()
                elif self.gj >= gw[1]:
                    self.jb += gw[4]
                    self.jy += gw[5]
                    self.css[self.cs][xy[0] + xy[2]][xy[1] + xy[3]] = 555
                    self.css[self.cs][xy[0]][xy[1]] = 101
                    self.puvskg = False
                    self.yidongkg = True
                    self.yy_yx1.play()
                    if num == 35:
                        self.endkg = True
                        self.yidongkg = False
                else:
                    self.yy_yx0.play()
                    while True:
                        gw[1] -= self.gj - gw[3]
                        if gw[2] - self.fy > 0:
                            sm -= gw[2] - self.fy
                        if gw[1] <= self.gj:
                            self.sm = int(sm)
                            self.jb += gw[4]
                            self.jy += gw[5]
                            self.css[self.cs][xy[0] + xy[2]][xy[1] + xy[3]] = 555
                            self.css[self.cs][xy[0]][xy[1]] = 101
                            self.yy_yx1.play()
                            if num == 35:
                                self.endkg = True
                                self.yidongkg = False
                            return
                        elif sm <= 0:
                            self.swkg = True
                            return
            else:
                self.puvskg = True
                self.yidongkg = False  # 按键启用关闭
                self.pu_gw, self.pu_xy = gw, xy  # 快速战斗模式

        def puvsfun(self, gw, xy):  # 普通战斗画面
            sm = self.sm
            if self.puvskg == True and self.yidongkg == False:
                if self.clock_s % 30 == 0:
                    if self.gj <= gw[3]:  # 自身攻击小于怪物防御的时候
                        if self.fy < gw[2]:  # 怪物攻击大于自身防御的时候
                            self.swkg = True
                        elif self.fy >= gw[2]:  # 自身防御超过了怪物的攻击
                            self.yy_yx7.play()
                            self.puvskg = False
                            self.yidongkg = True
                    elif self.gj >= gw[1]:
                        self.jb += gw[4]
                        self.jy += gw[5]
                        self.css[self.cs][xy[0] + xy[2]][xy[1] + xy[3]] = 555
                        self.css[self.cs][xy[0]][xy[1]] = 101
                        self.puvskg = False
                        self.yidongkg = True
                        self.yy_yx1.play()
                        if gw[0] == 635:
                            self.endkg = True
                            self.yidongkg = False
                    else:
                        gw[1] -= self.gj - gw[3]
                        if gw[2] - self.fy > 0:
                            sm -= gw[2] - self.fy
                        self.sm = int(sm)
                        self.yy_yx0.play()
                        if gw[1] <= self.gj:
                            self.jb += gw[4]
                            self.jy += gw[5]
                            self.css[self.cs][xy[0] + xy[2]][xy[1] + xy[3]] = 555
                            self.css[self.cs][xy[0]][xy[1]] = 101
                            self.puvskg = False
                            self.yidongkg = True
                            self.yy_yx1.play()
                            if gw[0] == 635:
                                self.endkg = True
                                self.yidongkg = False
                        elif self.sm <= 0:
                            self.swkg = True
                            self.puvskg = False

                root.blit(self.k0, (335, 125))
                root.blit(self.gw0, (367, 149), (gw[6] + self.npcyd, gw[7], 50, 50))
                gw_sm = self.font.render(f"{gw[1]}", True, (255, 255, 255))
                gw_gj = self.font.render(f"{gw[2]}", True, (255, 255, 255))
                gw_fy = self.font.render(f"{gw[3]}", True, (255, 255, 255))
                js_sm = self.font.render(f"{sm}", True, (255, 255, 255))
                js_gj = self.font.render(f"{self.gj}", True, (255, 255, 255))
                js_fy = self.font.render(f"{self.fy}", True, (255, 255, 255))
                # 怪物生命渲染
                root.blit(gw_sm, (437, 210))
                root.blit(gw_gj, (437, 239))
                root.blit(gw_fy, (437, 268))
                root.blit(js_sm, (724, 210))
                root.blit(js_gj, (724, 239))
                root.blit(js_fy, (724, 268))

        def dhfun(self):  # 对话处理
            if self.yidongkg == False:
                if self.dh_200 == True and self.jldh == 0:
                    root.blit(self.dh0, (353, 141), (0, 0, 450, 160))
                elif self.dh_200 == True and self.jldh == 1:
                    root.blit(self.dh0, (353, 141), (0, 160, 450, 160))
                elif self.dh_200 == True and self.jldh == 2:
                    root.blit(self.dh0, (353, 141), (0, 320, 450, 160))
                elif self.dh_200 == True and self.jldh == 3:
                    root.blit(self.dh0, (353, 141), (0, 160, 450, 160))
                elif self.dh_200 == True and self.jldh == 4:
                    root.blit(self.dh0, (353, 141), (0, 480, 450, 160))
                elif self.dh_201 == True and self.xddh == 0:
                    root.blit(self.dh0, (353, 141), (0, 640, 450, 160))
                elif self.dh_201 == True and self.xddh == 1:
                    root.blit(self.dh0, (353, 141), (0, 800, 450, 160))
                elif self.dh_201 == True and self.xddh == 2:
                    root.blit(self.dh0, (353, 141), (0, 960, 450, 160))
                elif self.dh_202 == True and self.gz_18 == True:
                    root.blit(self.dh0, (353, 141), (0, 1120, 450, 160))
                elif self.dh_212 == True:
                    root.blit(self.dh0, (353, 141), (0, 1280, 450, 160))
                elif self.dh_214 == True:
                    root.blit(self.dh0, (353, 141), (0, 1440, 450, 160))
                elif self.dh_211 == True:
                    root.blit(self.dh0, (353, 141), (0, 1600, 450, 160))
                elif self.dh_213 == True:
                    root.blit(self.dh0, (353, 141), (0, 1760, 450, 160))

        def jmfun(self):  # 处理界面的渲染
            if self.jmnum == 0:  # 打开程序的一个文字滚动
                self.jm0num -= 1
                root.blit(self.a2, (0, 0))
                root.blit(self.a1, (172, self.jm0num))
                root.blit(self.a0, (0, 0))
                if self.jm0num <= -400:  # 让a1文字图片往上移动
                    self.jm0num = 569
                    self.jmnum = 1
            elif self.jmnum == 1:
                root.blit(self.b0, (0, 0))
                self.yy_bj0.stop()
                self.yy_bj1.stop()
                self.yy_bj13.stop()
                self.yy_bj18.stop()
                if self.jm1num == 1:
                    root.blit(self.b1, (638, 458))
                elif self.jm1num == 2:
                    root.blit(self.b2, (638, 522))
                elif self.jm1num == 3:
                    root.blit(self.b3, (638, 586))
            elif self.jmnum == 2:  # 进入游戏
                root.blit(self.f0, (0, 0))
                self.xrfun()
                self.fontfun()
                self.lpxrfun()  # 实现J功能
                self.cxxrfun()
                self.puvsfun(self.pu_gw, self.pu_xy)  # 普通战斗状态下的渲染
                self.dhfun()  # 处理对话信息
                self.xpfun()  # 处理游戏失败后
                self.sdxrfun()  # 渲染商店
                self.tsxrfun()  # 提示闪烁
                self.yyfun()  # 处理音乐

        # 按键功能渲染
        def escfun(self):  # 处理退出游戏
            if self.esckg == True:
                root.blit(self.d0, (197, 171), (0, self.escy, 513, 221))

        def f4fun(self):  # 处理说明窗口 F4键
            if self.f4kg == True:
                root.blit(self.c0, (0, 0))

        def initfun(self):  # 处理重新开始游戏 F5
            if self.initkg == True and self.jmnum == 2:
                root.blit(self.e0, (197, 171), (0, self.f5y, 513, 221))  # 图片素材和esc功能按键一样

        def endfun(self):  # 处理游戏通关的画面
            if self.endkg == True and self.jmnum == 2:
                root.blit(self.a2, (0, 0))
                root.blit(self.h0, (172, self.endy))
                root.blit(self.a0, (0, 0))
                self.endy -= 1
                if self.endy <= -550:
                    self.yy_bj0.stop()
                    self.yy_bj1.stop()
                    self.yy_bj13.stop()
                    self.yy_bj18.stop()
                    self.__init__()
                    self.jmnum = 1

        def xpfun(self):  # 游戏失败后
            if self.swkg == True:
                self.yidongkg = False
                root.blit(self.i0, (0, 0))

        def tsxrfun(self):  # 功能键的渲染
            self.clock_ts += 1
            if self.clock_ts <= 60:
                if self.baocunkg == 0 and self.pksd == True:
                    root.blit(self.g0, (397, 77), (0, 0, 356, 56))
                elif self.baocunkg == 0 and self.pksd == False:
                    root.blit(self.g0, (397, 77), (0, 56, 356, 56))
                elif self.baocunkg == 1:
                    root.blit(self.g0, (397, 77), (0, 112, 356, 56))
                elif self.baocunkg == 2:
                    root.blit(self.g0, (397, 77), (0, 168, 356, 56))
            else:
                self.clock_ts = 0
                self.baocunkg = None

        def xrfun(self):
            for y in range(len(self.css[self.cs])):
                for x in range(len(self.css[self.cs][y])):
                    # 渲染建筑
                    if self.css[self.cs][x][y] == 100:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (0, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 101:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (50, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 102:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (50, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 103:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (100, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 104:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (150, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 105:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (150, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 106:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (0 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 107:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (100 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 108:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (0, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 109:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (50, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 110:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (100, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 111:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (150, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 112:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (0, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 113:
                        root.blit(self.dx0, (250 + y * 50, x * 50), (50, 150, 50, 50))
                    # 渲染角色
                    elif self.css[self.cs][x][y] == 555:
                        root.blit(self.js0, (250 + y * 50, x * 50), (self.jsx, self.jsy, 50, 50))
                    # 渲染NPC
                    elif self.css[self.cs][x][y] == 200:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0 + self.npcyd, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 201:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100 + self.npcyd, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 202:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 203:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 204:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 205:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 206:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 207 or self.css[self.cs][x][y] == 208:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 209:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 210:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 211:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 212:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 213:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (0 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 214:
                        root.blit(self.npc0, (250 + y * 50, x * 50), (100 + self.npcyd, 50, 50, 50))
                    # 渲染物品
                    elif self.css[self.cs][x][y] == 300:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (0, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 301:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (50, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 302:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (100, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 303:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (150, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 304:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (0, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 305:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (50, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 306:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (100, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 307:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (150, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 308:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (0, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 309:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (50, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 310:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (100, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 311:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (150, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 312:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (0, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 313:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (50, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 314:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (0, 200, 50, 50))
                    elif self.css[self.cs][x][y] == 315:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (100, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 316:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (50, 200, 50, 50))
                    elif self.css[self.cs][x][y] == 317:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (150, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 318:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (100, 200, 50, 50))
                    elif self.css[self.cs][x][y] == 319:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (150, 200, 50, 50))
                    elif self.css[self.cs][x][y] == 320:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (0, 250, 50, 50))
                    elif self.css[self.cs][x][y] == 321:
                        root.blit(self.wp0, (250 + y * 50, x * 50), (50, 250, 50, 50))
                    # 渲染怪物
                    elif self.css[self.cs][x][y] == 600:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 601:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 0, 50, 50))
                    elif self.css[self.cs][x][y] == 602:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 200, 50, 50))
                    elif self.css[self.cs][x][y] == 603:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 604:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 605:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 100, 50, 50))
                    elif self.css[self.cs][x][y] == 606:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 550, 50, 50))
                    elif self.css[self.cs][x][y] == 607:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 300, 50, 50))
                    elif self.css[self.cs][x][y] == 608:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 200, 50, 50))
                    elif self.css[self.cs][x][y] == 609:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 250, 50, 50))
                    elif self.css[self.cs][x][y] == 610:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 400, 50, 50))
                    elif self.css[self.cs][x][y] == 611:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 50, 50, 50))
                    elif self.css[self.cs][x][y] == 612:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 550, 50, 50))
                    elif self.css[self.cs][x][y] == 613:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 350, 50, 50))
                    elif self.css[self.cs][x][y] == 614:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 615:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 600, 50, 50))
                    elif self.css[self.cs][x][y] == 616:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 600, 50, 50))
                    elif self.css[self.cs][x][y] == 617:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 750, 50, 50))
                    elif self.css[self.cs][x][y] == 618:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 300, 50, 50))
                    elif self.css[self.cs][x][y] == 619:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 400, 50, 50))
                    elif self.css[self.cs][x][y] == 620:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 450, 50, 50))
                    elif self.css[self.cs][x][y] == 621:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 350, 50, 50))
                    elif self.css[self.cs][x][y] == 622:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 700, 50, 50))
                    elif self.css[self.cs][x][y] == 623:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 700, 50, 50))
                    elif self.css[self.cs][x][y] == 624:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 650, 50, 50))
                    elif self.css[self.cs][x][y] == 625:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 850, 50, 50))
                    elif self.css[self.cs][x][y] == 626:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 750, 50, 50))
                    elif self.css[self.cs][x][y] == 627:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 150, 50, 50))
                    elif self.css[self.cs][x][y] == 628:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 250, 50, 50))
                    elif self.css[self.cs][x][y] == 629:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 900, 50, 50))
                    elif self.css[self.cs][x][y] == 630:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (0 + self.npcyd, 800, 50, 50))
                    elif self.css[self.cs][x][y] == 631:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 500, 50, 50))
                    elif self.css[self.cs][x][y] == 632:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 800, 50, 50))
                    elif self.css[self.cs][x][y] == 633:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 900, 50, 50))
                    elif self.css[self.cs][x][y] == 634:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 650, 50, 50))
                    elif self.css[self.cs][x][y] == 635:
                        root.blit(self.gw0, (250 + y * 50, x * 50), (100 + self.npcyd, 850, 50, 50))

        def rootfun(self):  # 实机测试
            while True:
                # 获得鼠标实时位置的坐标
                sbxy = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.esckg = True
                    elif event.type == pygame.KEYDOWN:  # 按键操作
                        if event.key == 27 and self.jmnum == 0:  # 27是esc键
                            self.jmnum = 1
                        elif self.swkg == True and event.key == 32:  # 游戏失败的时候
                            self.yy_bj0.stop()
                            self.yy_bj1.stop()
                            self.yy_bj13.stop()
                            self.yy_bj18.stop()
                            self.__init__()
                            self.jmnum = 1
                        elif event.key == pygame.K_F4 and self.jmnum != 0 and self.esckg == False and self.initkg == False:
                            self.f4kg = not self.f4kg
                        elif event.key == 27 and self.jmnum == 2 and self.initkg == False and self.endkg == False:  # 进入游戏以后按esc退出游戏
                            self.esckg = True
                        elif event.key == pygame.K_F5 and self.esckg == False and self.jmnum == 2:  # 进入游戏后按F5键
                            self.initkg = not self.initkg
                        elif event.key == 27 and self.endkg == True:  # 游戏结束滚动的结束
                            self.yy_bj0.stop()
                            self.yy_bj1.stop()
                            self.yy_bj13.stop()
                            self.yy_bj18.stop()
                            self.__init__()
                            self.jmnum = 1
                        elif event.key == pygame.K_F1 and self.jmnum == 2 and self.esckg == False and self.initkg == False:
                            self.pksd = not self.pksd
                            self.baocunkg = 0
                        # 处理商店
                        elif event.key == 32 and self.sdkg == True:
                            if self.sdnum[0] == 0 and self.sdnum[1] == 0:
                                if self.jb >= 25:
                                    self.jb -= 25
                                    self.sm += 800
                                    self.yy_yx6.play()
                            elif self.sdnum[0] == 0 and self.sdnum[1] == 1:
                                if self.jb >= 25:
                                    self.jb -= 25
                                    self.gj += 4
                                    self.yy_yx6.play()
                            elif self.sdnum[0] == 0 and self.sdnum[1] == 2:
                                if self.jb >= 25:
                                    self.jb -= 25
                                    self.fy += 4
                                    self.yy_yx6.play()

                            elif self.sdnum[0] == 1 and self.sdnum[1] == 0:
                                if self.jb >= 100:
                                    self.jb -= 100
                                    self.sm += 4000
                                    self.yy_yx6.play()
                            elif self.sdnum[0] == 1 and self.sdnum[1] == 1:
                                if self.jb >= 100:
                                    self.jb -= 100
                                    self.gj += 20
                                    self.yy_yx6.play()
                            elif self.sdnum[0] == 1 and self.sdnum[1] == 2:
                                if self.jb >= 100:
                                    self.jb -= 100
                                    self.fy += 20
                                    self.yy_yx6.play()

                            elif self.sdnum[0] == 2 and self.sdnum[1] == 0:
                                if self.jy >= 100:
                                    self.jy -= 100
                                    self.dj += 1
                                    self.sm += 1000
                                    self.gj += 7
                                    self.fy += 7
                                    self.yy_yx5.play()
                            elif self.sdnum[0] == 2 and self.sdnum[1] == 1:
                                if self.jy >= 30:
                                    self.jy -= 30
                                    self.gj += 5
                                    self.yy_yx6.play()
                            elif self.sdnum[0] == 2 and self.sdnum[1] == 2:
                                if self.jy >= 30:
                                    self.jy -= 30
                                    self.fy += 5
                                    self.yy_yx6.play()

                            elif self.sdnum[0] == 3 and self.sdnum[1] == 0:
                                if self.jy >= 270:
                                    self.jy -= 270
                                    self.dj += 3
                                    self.sm += 3000
                                    self.gj += 21
                                    self.fy += 21
                                    self.yy_yx5.play()
                            elif self.sdnum[0] == 3 and self.sdnum[1] == 1:
                                if self.jy >= 95:
                                    self.jy -= 95
                                    self.gj += 17
                                    self.yy_yx6.play()
                            elif self.sdnum[0] == 3 and self.sdnum[1] == 2:
                                if self.jy >= 95:
                                    self.jy -= 95
                                    self.fy += 17
                                    self.yy_yx6.play()

                            elif self.sdnum[0] == 4 and self.sdnum[1] == 0:
                                if self.jb >= 10:
                                    self.jb -= 10
                                    self.ys0 += 1
                                    self.yy_yx2.play()
                            elif self.sdnum[0] == 4 and self.sdnum[1] == 1:
                                if self.jb >= 50:
                                    self.jb -= 50
                                    self.ys1 += 1
                                    self.yy_yx2.play()
                            elif self.sdnum[0] == 4 and self.sdnum[1] == 2:
                                if self.jb >= 100:
                                    self.jb -= 100
                                    self.ys2 += 1
                                    self.yy_yx2.play()

                            elif self.sdnum[0] == 5 and self.sdnum[1] == 0:
                                if self.ys0 >= 1:
                                    self.ys0 -= 1
                                    self.jb += 7
                                    self.yy_yx2.play()
                            elif self.sdnum[0] == 5 and self.sdnum[1] == 1:
                                if self.ys1 >= 1:
                                    self.ys1 -= 1
                                    self.jb += 35
                                    self.yy_yx2.play()
                            elif self.sdnum[0] == 5 and self.sdnum[1] == 2:
                                if self.ys2 >= 1:
                                    self.ys2 -= 1
                                    self.jb += 75
                                    self.yy_yx2.play()

                            elif self.sdnum[1] == 3:
                                self.sdkg == False
                                self.sdnum = [None, None]
                                self.yidongkg = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w and self.sdkg == True:
                            if self.sdnum[1] != None:
                                if 3 >= self.sdnum[1] >= 1:
                                    self.sdnum[1] -= 1
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s and self.sdkg == True:
                            if self.sdnum[1] != None:
                                if 0 <= self.sdnum[1] < 3:
                                    self.sdnum[1] += 1
                        # 处理J功能
                        elif event.key == pygame.K_j and self.leapgn == True and self.puvskg == False:
                            self.lpkg = not self.lpkg
                            if self.lpkg == True:
                                self.yidongkg = False
                            else:
                                self.yidongkg = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w and self.lpkg == True:
                            if 0 < self.lpxz <= 20:
                                self.lpxz -= 1
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s and self.lpkg == True:
                            if 0 <= self.lpxz <= 19:
                                self.lpxz += 1
                        elif event.key == 32 and self.lpkg == True and self.cxkg == False:
                            if self.lpxz + 1 < self.lc:
                                self.cs = copy.deepcopy(self.lpxz + 1)
                                self.lpkg = False
                                self.yidongkg = True
                                # 需要清空所有的角色  yes 上，nos下
                                # 到的楼层数，往下全部在上楼梯口，往上的全部在下楼梯口
                                for i in range(22):
                                    for y in range(len(self.css[i])):
                                        for x in range(len(self.css[i][y])):
                                            if self.css[i][y][x] == 555:
                                                self.css[i][y][x] = 101
                                self.css[0][2][6] = 555  # 第0层从新写入角色
                                for i in range(self.lpxz + 1, len(self.list_nos)):
                                    self.css[self.list_nos[i][0]][self.list_nos[i][1]][self.list_nos[i][2]] = 555
                                for i in range(0, self.lpxz):
                                    self.css[self.list_yes[i][0]][self.list_yes[i][1]][self.list_yes[i][2]] = 555
                                self.css[self.list_yes[self.lpxz][0]][self.list_yes[self.lpxz][1]][
                                    self.list_yes[self.lpxz][2]] = 555

                        # 处理L功能
                        elif event.key == pygame.K_l and self.cxgn == True and self.lpkg == False and self.puvskg == False:
                            self.cxkg = not self.cxkg
                            if self.cxkg == True:
                                self.yidongkg = False
                            else:
                                self.yidongkg = True
                        # 保存和读取
                        # 保存
                        elif event.key == pygame.K_F2 and self.lpkg == False and self.puvskg == False and self.cxkg == False:
                            self.list_list = copy.deepcopy([self.cxgn, self.leapgn, self.lc, self.cs, self.css,
                                                            self.dj, self.sm, self.gj, self.fy, self.jb, self.jy,
                                                            self.ys0, self.ys1, self.ys2,
                                                            self.wp_309, self.wp_305])
                            self.baocunkg = 1
                        elif event.key == pygame.K_F3 and self.lpkg == False and self.puvskg == False and self.cxkg == False:
                            # 读取
                            if len(self.list_list) > 0:
                                self.cxgn = self.list_list[0]
                                self.leapgn = self.list_list[1]
                                self.lc = self.list_list[2]
                                self.cs = self.list_list[3]
                                self.css = self.list_list[4]
                                self.dj = self.list_list[5]
                                self.sm = self.list_list[6]
                                self.gj = self.list_list[7]
                                self.fy = self.list_list[8]
                                self.jb = self.list_list[9]
                                self.jy = self.list_list[10]
                                self.ys0 = self.list_list[11]
                                self.ys1 = self.list_list[12]
                                self.ys2 = self.list_list[13]
                                self.wp_309 = self.list_list[14]
                                self.wp_305 = self.list_list[15]
                                self.baocunkg = 2
                        # 处理对话精灵
                        elif event.key == 32 and self.dh_200 == True and self.jldh == 0:
                            self.jldh = 1
                        elif event.key == 32 and self.dh_200 == True and self.jldh == 1:
                            self.jldh = 2
                        elif event.key == 32 and self.dh_200 == True and self.jldh == 2:
                            self.jldh = 3
                            self.ys0, self.ys1, self.ys2 = 1, 1, 1
                            self.dh_200, self.yidongkg = False, True
                        elif event.key == 32 and self.dh_200 == True and self.jldh == 3 and self.wp_309 == True:
                            self.jldh = 4
                        elif event.key == 32 and self.dh_200 == True and self.jldh == 4 and self.wp_309 == True:
                            self.sm = int(self.sm * 1.33)
                            self.gj = int(self.gj * 1.33)
                            self.fy = int(self.fy * 1.33)
                            self.css[self.cs][9][5] = 101
                            self.yy_yx6.play()
                            self.dh_200, self.yidongkg = False, True
                        elif event.key == 32 and self.dh_200 == True and self.jldh == 3:
                            self.dh_200, self.yidongkg = False, True
                        # 处理侠盗的对话
                        elif event.key == 32 and self.dh_201 == True and self.xddh == 0:
                            self.xddh+= 1
                            self.dh_201, self.yidongkg = False, True
                            # self.css[2][7][2] = 101
                        elif event.key == 32 and self.dh_201 == True and self.xddh == 1:
                            if self.wp_305 == True:
                                self.xddh = 2
                                self.gz_18 = True
                                self.css[2][7][2] = 101
                                self.dh_201, self.yidongkg = False, True
                            else:
                                self.dh_201, self.yidongkg = False, True
                        elif event.key == 32 and self.dh_201 == True and self.xddh == 2:
                            self.dh_201, self.yidongkg = False, True
                            self.css[4][1][6] = 101
                        # 处理和公主的对话：
                        elif event.key == 32 and self.dh_202 == True and self.gz_18 == True:
                            self.css[18][11][11] = 108
                            self.dh_202, self.yidongkg = False, True
                        elif event.key == 32 and self.dh_211 == True:
                            self.yidongkg, self.dh_211 = True, False
                            self.css[2][11][8] = 101
                            self.gj += 30
                        elif event.key == 32 and self.dh_212 == True:
                            self.yidongkg, self.dh_212 = True, False
                            self.css[2][11][10] = 101
                            self.fy += 30
                        elif event.key == 32 and self.dh_213 == True:
                            if self.jy >= 500:
                                self.yidongkg, self.dh_213 = True, False
                                self.jy -= 500
                                self.gj += 120
                                self.css[15][4][5] = 101
                                self.yy_yx5.play()
                            else:
                                self.yidongkg, self.dh_213 = True, False
                        elif event.key == 32 and self.dh_214 == True:
                            if self.jb >= 500:
                                self.yidongkg, self.dh_214 = True, False
                                self.jb -= 500
                                self.fy += 120
                                self.css[15][4][7] = 101
                                self.yy_yx5.play()
                            else:
                                self.yidongkg, self.dh_214 = True, False
                    elif event.type == pygame.MOUSEMOTION:  # 处理鼠标移动
                        # 处理退出游戏事件
                        if self.esckg == True and 215 <= sbxy[0] <= 215 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.escy = 221
                        elif self.esckg == True and 517 <= sbxy[0] <= 517 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.escy = 442
                        else:
                            self.escy = 0
                        # 处理是否重新开始游戏的选择
                        if self.initkg == True and 215 <= sbxy[0] <= 215 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.f5y = 221
                        elif self.initkg == True and 517 <= sbxy[0] <= 517 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.f5y = 442
                        else:
                            self.f5y = 0
                        # 处理界面1的三个选择
                        if self.jmnum == 1 and 638 <= sbxy[0] <= 638 + 235 and 458 <= sbxy[1] <= 458 + 45:
                            self.jm1num = 1
                        elif self.jmnum == 1 and 638 <= sbxy[0] <= 638 + 235 and 522 <= sbxy[1] <= 522 + 45:
                            self.jm1num = 2
                        elif self.jmnum == 1 and 638 <= sbxy[0] <= 638 + 235 and 586 <= sbxy[1] <= 586 + 45:
                            self.jm1num = 3
                        else:
                            self.jm1num = 0

                    elif event.type == pygame.MOUSEBUTTONUP:  # 处理鼠标放开
                        # 处理退出游戏事件
                        if self.esckg == True and 215 <= sbxy[0] <= 215 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            pygame.quit()
                            sys.exit()
                        elif self.esckg == True and 517 <= sbxy[0] <= 517 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.escy = 0
                            self.esckg = False
                        # 处理是否重新开始游戏的选择
                        if self.initkg == True and 215 <= sbxy[0] <= 215 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.yy_bj0.stop()
                            self.yy_bj1.stop()
                            self.yy_bj13.stop()
                            self.yy_bj18.stop()
                            self.__init__()
                            self.jmnum = 2
                        elif self.initkg == True and 517 <= sbxy[0] <= 517 + 174 and 289 <= sbxy[1] <= 289 + 44:
                            self.initkg = False
                        # 处理界面1的三个选择
                        if self.jmnum == 1 and 638 <= sbxy[0] <= 638 + 235 and 458 <= sbxy[1] <= 458 + 45:
                            self.jmnum = 2
                        elif self.jmnum == 1 and 638 <= sbxy[0] <= 638 + 235 and 522 <= sbxy[
                            1] <= 522 + 45 and self.esckg == False:
                            # 相当于进入F4游戏说明
                            self.f4kg = True
                        elif self.jmnum == 1 and 638 <= sbxy[0] <= 638 + 235 and 586 <= sbxy[1] <= 586 + 45:
                            self.esckg = True

                self.jmfun()
                self.f4fun()  # 处理F4功能按键
                self.initfun()  # 用于处理重新游戏按钮
                self.endfun()  # 处理游戏结束
                self.escfun()  # 处理退出游戏按键

                eventlist = pygame.key.get_pressed()
                if eventlist[pygame.K_LEFT] or eventlist[pygame.K_a]:
                    self.movefun(4)
                elif eventlist[pygame.K_UP] or eventlist[pygame.K_w]:
                    self.movefun(8)
                elif eventlist[pygame.K_RIGHT] or eventlist[pygame.K_d]:
                    self.movefun(6)
                elif eventlist[pygame.K_DOWN] or eventlist[pygame.K_s]:
                    self.movefun(2)

                root.blit(self.sb, (sbxy[0], sbxy[1]))
                pygame.display.update()
                clock.tick(60)
                self.clock_s += 1
                if self.clock_s < 15:
                    self.npcyd = 0
                    self.jsx = 0
                elif 15 <= self.clock_s < 30:
                    self.npcyd = 50
                    self.jsx = 50
                elif 30 <= self.clock_s < 45:
                    self.npcyd = 0
                    self.jsx = 100
                elif 45 <= self.clock_s <= 60:
                    self.npcyd = 50
                    self.jsx = 150
                if self.clock_s > 60:
                    self.clock_s = 0

    mt = Mt()
    mt.rootfun()


if __name__ == '__main__':
    main()
