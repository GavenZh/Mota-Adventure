import sys
import os
import pygame



'''按钮类'''
class Button(pygame.sprite.Sprite):
    def __init__(self, text, fontpath, fontsize, position, color_selected=(255, 0, 0), color_default=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.color_selected = color_selected
        self.color_default = color_default
        self.font = pygame.font.Font(fontpath, fontsize)
        self.font_render = self.font.render(text, True, color_default)
        self.rect = self.font_render.get_rect()
        self.rect.center = position

    '''更新函数: 不断地更新检测鼠标是否在按钮上'''
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.font_render = self.font.render(self.text, True, self.color_selected)
        else:
            self.font_render = self.font.render(self.text, True, self.color_default)

    '''绑定到屏幕上'''
    def draw(self, screen):
        screen.blit(self.font_render, self.rect)


'''退出程序'''
def QuitGame(use_pygame=True):
    if use_pygame: pygame.quit()
    sys.exit()


'''游戏地图解析类'''
class MapParser():
    def __init__(self, blocksize, filepath, element_images, offset=(0, 0), **kwargs):
        self.count = 0
        self.switch_times = 15
        self.image_pointer = 0
        self.offset = offset
        self.blocksize = blocksize
        self.element_images = element_images
        self.map_matrix = self.parse(filepath)
        self.map_size = (len(self.map_matrix), len(self.map_matrix[0]))
        # 地图上所有怪物的属性: 名字, 生命值, 攻击力, 防御力, 金币, 经验
        self.monsters_dict = {
            '40': ('绿头怪', 50, 20, 1, 1, 1),
            '41': ('红头怪', 70, 15, 2, 2, 2),
            '42': ('小蝙蝠', 100, 20, 5, 3, 3),
            '43': ('青头怪', 200, 35, 10, 5, 5),
            '44': ('骷髅人', 110, 25, 5, 5, 4),
            '45': ('骷髅士兵', 150, 40, 20, 8, 6),
            '46': ('兽面人', 300, 75, 45, 13, 10),
            '47': ('初级卫兵', 450, 150, 90, 22, 19),
            '48': ('大蝙蝠', 150, 65, 30, 10, 8),
            '49': ('红蝙蝠', 550, 160, 90, 25, 20),
            '50': ('白衣武士', 1300, 300, 150, 40, 35),
            '51': ('怪王', 700, 250, 125, 32, 30),
            '52': ('红衣法师', 500, 400, 260, 47, 45),
            '53': ('红衣魔王', 15000, 1000, 1000, 100, 100),
            '54': ('金甲卫士', 850, 350, 200, 45, 40),
            '55': ('金甲队长', 900, 750, 650, 77, 70),
            '56': ('骷髅队长', 400, 90, 50, 15, 12),
            '57': ('灵法师', 1500, 830, 730, 80, 70),
            '58': ('灵武士', 1200, 980, 900, 88, 75),
            '59': ('冥灵魔王', 30000, 1700, 1500, 250, 220),
            '60': ('麻衣法师', 250, 120, 70, 20, 17),
            '61': ('冥战士', 2000, 680, 590, 70, 65),
            '62': ('冥队长', 2500, 900, 850, 84, 75),
            '63': ('初级法师', 125, 50, 25, 10, 7),
            '64': ('高级法师', 100, 200, 110, 30, 25),
            '65': ('石头怪人', 500, 115, 65, 15, 15),
            '66': ('兽面战士', 900, 450, 330, 50, 50),
            '67': ('双手剑士', 1200, 620, 520, 65, 75),
            '68': ('冥卫兵', 1250, 500, 400, 55, 55),
            '69': ('高级卫兵', 1500, 560, 460, 60, 60),
            '70': ('影子战士', 3100, 1150, 1050, 92, 80),
            '188': ('血影', 99999, 5000, 4000, 0, 0),
            '198': ('魔龙', 99999, 9999, 5000, 0, 0),
        }

    '''解析'''
    def parse(self, filepath):
        map_matrix = []
        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                line = line.strip()
                if not line: continue
                map_matrix.append([c.strip() for c in line.split(',')])
        return map_matrix

    '''获得所有怪物信息'''
    def getallmonsters(self):
        monsters = []
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, elem in enumerate(row):
                if elem in self.monsters_dict:
                    monster = list(self.monsters_dict[elem])
                    monster.append(elem)
                    monsters.append(tuple(monster))
        return list(set(monsters))

    '''获得英雄的位置'''
    def getheroposition(self, pos_type='block'):
        assert pos_type in ['pixel', 'block']
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, elem in enumerate(row):
                position = col_idx * self.blocksize + self.offset[0], row_idx * self.blocksize + self.offset[1]
                if elem == 'hero':
                    if pos_type == 'pixel':
                        return position
                    else:
                        return (col_idx, row_idx)
        return None

    '''将游戏地图画到屏幕上'''
    def draw(self, screen):
        self.count += 1
        if self.count == self.switch_times:
            self.count = 0
            self.image_pointer = int(not self.image_pointer)
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, elem in enumerate(row):
                position = col_idx * self.blocksize + self.offset[0], row_idx * self.blocksize + self.offset[1]
                if elem in self.element_images:
                    image = self.element_images[elem][self.image_pointer]
                    image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
                    screen.blit(image, position)
                elif elem in ['00', 'hero']:
                    image = self.element_images['0'][self.image_pointer]
                    image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
                    screen.blit(image, position)


'''定义我们的主角勇士'''
class Hero(pygame.sprite.Sprite):
    def __init__(self, images, blocksize, block_position, offset=(0, 0), fontpath=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 设置基础属性
        self.blocksize = blocksize
        self.block_position = block_position
        self.offset = offset
        self.fontpath = fontpath
        self.font = pygame.font.Font(fontpath, 40)
        for key, value in kwargs.items(): setattr(self, key, value)
        # 对应的图片
        self.images = {}
        for key, value in images.items():
            self.images[key] = pygame.transform.scale(value, (blocksize, blocksize))
        self.image = self.images['down']
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = block_position[0] * blocksize + offset[0], block_position[1] * blocksize + \
                                        offset[1]
        # 设置等级等信息
        self.level = 1
        self.life_value = 1000
        self.attack_power = 10
        self.defense_power = 10
        self.num_coins = 0
        self.experience = 0
        self.num_yellow_keys = 1
        self.num_purple_keys = 1
        self.num_red_keys = 1
        # 是否拥有一些宝物
        # --幸运十字架
        self.has_cross = False
        # --圣光徽
        self.has_forecast = False
        # --风之罗盘
        self.has_jump = False
        # --星光神榔
        self.has_hammer = False
        # 行动冷却
        self.move_cooling_count = 0
        self.move_cooling_time = 5
        self.freeze_move_flag = False
        # 获得物品提示
        self.obtain_tips = None
        self.show_obtain_tips_count = 0
        self.max_obtain_tips_count = 20

    '''行动'''

    def move(self, direction, map_parser, screen):
        # 判断是否冷冻行动
        if self.freeze_move_flag: return
        assert direction in self.images
        self.image = self.images[direction]
        # 移动勇士
        move_vector = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}[direction]
        block_position = self.block_position[0] + move_vector[0], self.block_position[1] + move_vector[1]
        # 判断该移动是否合法, 并触发对应的事件
        events = []
        if block_position[0] >= 0 and block_position[0] < map_parser.map_size[1] and \
                block_position[1] >= 0 and block_position[1] < map_parser.map_size[0]:
            # --合法移动
            if map_parser.map_matrix[block_position[1]][block_position[0]] in ['0', '00', 'hero']:
                self.block_position = block_position
            # --触发事件
            else:
                flag, events = self.dealcollideevent(
                    elem=map_parser.map_matrix[block_position[1]][block_position[0]],
                    block_position=block_position,
                    map_parser=map_parser,
                    screen=screen,
                )
                if flag:
                    self.block_position = block_position
                    map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
        # 重新设置勇士位置
        self.rect.left, self.rect.top = self.block_position[0] * self.blocksize + self.offset[0], self.block_position[
            1] * self.blocksize + self.offset[1]
        # 冷冻行动
        self.freeze_move_flag = True
        # 返回需要在主循环里触发的事件
        return events

    '''放置到上/下楼梯口旁'''

    def placenexttostairs(self, map_parser, stairs_type='up'):
        assert stairs_type in ['up', 'down']
        for row_idx, row in enumerate(map_parser.map_matrix):
            for col_idx, elem in enumerate(row):
                if (stairs_type == 'up' and elem == '13') or (stairs_type == 'down' and elem == '14'):
                    if row_idx > 0 and map_parser.map_matrix[row_idx - 1][col_idx] == '00':
                        self.block_position = col_idx, row_idx - 1
                    elif row_idx < map_parser.map_size[0] - 1 and map_parser.map_matrix[row_idx + 1][col_idx] == '00':
                        self.block_position = col_idx, row_idx + 1
                    elif col_idx > 0 and map_parser.map_matrix[row_idx][col_idx - 1] == '00':
                        self.block_position = col_idx - 1, row_idx
                    elif col_idx < map_parser.map_size[1] - 1 and map_parser.map_matrix[row_idx][col_idx + 1] == '00':
                        self.block_position = col_idx + 1, row_idx
        self.rect.left, self.rect.top = self.block_position[0] * self.blocksize + self.offset[0], self.block_position[
            1] * self.blocksize + self.offset[1]

    '''处理撞击事件'''

    def dealcollideevent(self, elem, block_position, map_parser, screen):
        # 遇到不同颜色的门, 有钥匙则打开, 否则无法前进
        if elem in ['2', '3', '4']:
            flag = False
            if elem == '2' and self.num_yellow_keys > 0:
                self.num_yellow_keys -= 1
                flag = True
            elif elem == '3' and self.num_purple_keys > 0:
                self.num_purple_keys -= 1
                flag = True
            elif elem == '4' and self.num_red_keys > 0:
                self.num_red_keys -= 1
                flag = True
            return flag, []
        # 捡到不同颜色的钥匙
        elif elem in ['6', '7', '8']:
            if elem == '6':
                self.num_yellow_keys += 1
                self.obtain_tips = '得到一把黄钥匙'
            elif elem == '7':
                self.num_purple_keys += 1
                self.obtain_tips = '得到一把蓝钥匙'
            elif elem == '8':
                self.num_red_keys += 1
                self.obtain_tips = '得到一把红钥匙'
            return True, []
        # 捡到宝石
        elif elem in ['9', '10']:
            if elem == '9':
                self.defense_power += 3
                self.obtain_tips = '得到一个蓝宝石 防御力加3'
            elif elem == '10':
                self.attack_power += 3
                self.obtain_tips = '得到一个红宝石 攻击力加3'
            return True, []
        # 捡到血瓶
        elif elem in ['11', '12']:
            if elem == '11':
                self.life_value += 200
                self.obtain_tips = '得到一个小血瓶 生命加200'
            elif elem == '12':
                self.life_value += 500
                self.obtain_tips = '得到一个大血瓶 生命加500'
            return True, []
        # 上下楼梯
        elif elem in ['13', '14']:
            if elem == '13':
                events = ['upstairs']
            elif elem == '14':
                events = ['downstairs']
            return False, events
        # 商店
        elif elem in ['22', '26', '27']:
            if elem == '22':
                return False, ['buy_from_shop']
            elif elem == '26':
                return False, ['buy_from_oldman']
            elif elem == '27':
                return False, ['buy_from_businessman']
        # 遇到仙女, 进行对话, 并左移一格
        elif elem in ['24']:
            if map_parser.map_matrix[block_position[1]][block_position[0] - 1] == '0':
                map_parser.map_matrix[block_position[1]][block_position[0] - 1] = elem
                map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return False, ['conversation_hero_and_fairy']
        # 捡到道具飞羽
        elif elem in ['30', '31']:
            if elem == '30':
                self.level += 1
                self.life_value += 1000
                self.attack_power += 7
                self.defense_power += 7
                self.obtain_tips = '得到小飞羽 等级提升一级'
            elif elem == '31':
                self.level += 3
                self.life_value += 3000
                self.attack_power += 21
                self.defense_power += 21
                self.obtain_tips = '得到大飞羽 等级提升三级'
            return True, []
        # 捡到幸运十字架
        elif elem in ['32']:
            self.has_cross = True
            self.obtain_tips = ['【幸运十字架】把它交给序章中的仙子', '可以将自身的所有能力提升一些(攻击防御和生命值)']
            return True, []
        # 捡到圣水瓶
        elif elem in ['33']:
            self.life_value *= 2
            self.obtain_tips = '【圣水瓶】它可以将你的体质增加一倍'
            return True, []
        # 捡到圣光徽
        elif elem in ['34']:
            self.has_forecast = True
            self.obtain_tips = '【圣光徽】按L键使用 查看怪物的基本情况'
            return True, []
        # 捡到风之罗盘
        elif elem in ['35']:
            self.has_jump = True
            self.obtain_tips = '【风之罗盘】按J键使用 在已经走过的楼层间进行跳跃'
            return True, []
        # 捡到钥匙盒
        elif elem in ['36']:
            self.num_yellow_keys += 1
            self.num_purple_keys += 1
            self.num_red_keys += 1
            self.obtain_tips = '得到钥匙盒 各种钥匙数加1'
            return True, []
        # 捡到星光神榔
        elif elem in ['38']:
            self.has_hammer = True
            self.obtain_tips = ['【星光神榔】把它交给第四层的小偷', '小偷便会用它打开第十八层的隐藏地面']
            return True, []
        # 捡到金块
        elif elem in ['39']:
            self.num_coins += 300
            self.obtain_tips = '得到金块 金币数加300'
            return True, []
        # 遇到怪物
        elif elem in map_parser.monsters_dict:
            monster = map_parser.monsters_dict[elem]
            if self.winmonster(monster)[0]:
                self.battle(monster, map_parser.element_images[elem][0], map_parser, screen)
                self.num_coins += monster[4]
                self.experience += monster[5]
                self.obtain_tips = f'获得金币数{monster[4]} 经验值{monster[5]}'
                return True, []
            else:
                return False, []
        # 得到铁剑
        elif elem in ['71']:
            self.attack_power += 10
            self.obtain_tips = '得到铁剑 攻击力加10'
            return True, []
        # 得到钢剑
        elif elem in ['73']:
            self.attack_power += 30
            self.obtain_tips = '得到钢剑 攻击力加30'
            return True, []
        # 得到圣光剑
        elif elem in ['75']:
            self.attack_power += 120
            self.obtain_tips = '得到圣光剑 攻击力加120'
            return True, []
        # 得到铁盾
        elif elem in ['76']:
            self.defense_power += 10
            self.obtain_tips = '得到铁盾 防御力加10'
            return True, []
        # 得到钢盾
        elif elem in ['78']:
            self.defense_power += 30
            self.obtain_tips = '得到钢盾 防御力加30'
            return True, []
        # 得到星光盾
        elif elem in ['80']:
            self.defense_power += 120
            self.obtain_tips = '得到星光盾 防御力加120'
            return True, []
        # 其他
        else:
            return False, []

    '''游戏事件提示'''

    def showinfo(self, screen):
        if self.obtain_tips is None: return
        self.show_obtain_tips_count += 1
        if self.show_obtain_tips_count > self.max_obtain_tips_count:
            self.show_obtain_tips_count = 0
            self.obtain_tips = None
        # 画框
        left, top = self.cfg.BLOCKSIZE // 2, 100
        width, height = self.cfg.SCREENSIZE[0] // self.cfg.BLOCKSIZE - 1, 2
        pygame.draw.rect(screen, (199, 97, 20),
                         (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
        for col in range(width):
            for row in range(height):
                image = self.resource_loader.images['mapelements']['0'][0]
                image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
        # 文字
        font = pygame.font.Font(self.fontpath, 30)
        if isinstance(self.obtain_tips, list):
            assert len(self.obtain_tips) == 2
            font_render1 = font.render(self.obtain_tips[0], True, (255, 255, 255))
            font_render2 = font.render(self.obtain_tips[1], True, (255, 255, 255))
            rect1 = font_render1.get_rect()
            rect2 = font_render2.get_rect()
            rect1.midtop = left + width * self.cfg.BLOCKSIZE // 2, top + 10
            rect2.midtop = left + width * self.cfg.BLOCKSIZE // 2, top + 10 + self.blocksize
            screen.blit(font_render1, rect1)
            screen.blit(font_render2, rect2)
        else:
            font_render = font.render(self.obtain_tips, True, (255, 255, 255))
            rect = font_render.get_rect()
            rect.midtop = left + width * self.cfg.BLOCKSIZE // 2, top + height * self.cfg.BLOCKSIZE // 2 - 15
            screen.blit(font_render, rect)

    '''判断勇士是否可以打赢怪物'''
    def winmonster(self, monster):
        # 如果攻击力低于怪物防御力, monster: [名字, 生命值, 攻击力, 防御力, 金币, 经验]
        if self.attack_power <= monster[3]: return False, '???'
        # 如果防御力高于怪物攻击力
        if self.defense_power >= monster[2]: return True, '0'
        # 我方打怪物一次扣多少血
        diff_our = self.attack_power - monster[3]
        # 怪物打我方一次扣多少血
        diff_monster = monster[2] - self.defense_power
        # 计算谁可以win
        if round(monster[1] / diff_our) <= round(self.life_value / diff_monster):
            return True, str(diff_monster * round(monster[1] / diff_our))
        return False, '???'

    '''将勇士绑定到屏幕上'''
    def draw(self, screen):
        if self.freeze_move_flag:
            self.move_cooling_count += 1
            if self.move_cooling_count > self.move_cooling_time:
                self.move_cooling_count = 0
                self.freeze_move_flag = False
        screen.blit(self.image, self.rect)
        font_renders = [
            self.font.render(str(self.level), True, (255, 255, 255)),
            self.font.render(str(self.life_value), True, (255, 255, 255)),
            self.font.render(str(self.attack_power), True, (255, 255, 255)),
            self.font.render(str(self.defense_power), True, (255, 255, 255)),
            self.font.render(str(self.num_coins), True, (255, 255, 255)),
            self.font.render(str(self.experience), True, (255, 255, 255)),
            self.font.render(str(self.num_yellow_keys), True, (255, 255, 255)),
            self.font.render(str(self.num_purple_keys), True, (255, 255, 255)),
            self.font.render(str(self.num_red_keys), True, (255, 255, 255)),
        ]
        rects = [fr.get_rect() for fr in font_renders]
        rects[0].topleft = (160, 80)
        for idx in range(1, 6):
            rects[idx].topleft = 160, 127 + 42 * (idx - 1)
        for idx in range(6, 9):
            rects[idx].topleft = 160, 364 + 55 * (idx - 6)
        for fr, rect in zip(font_renders, rects):
            screen.blit(fr, rect)

    '''战斗画面'''
    def battle(self, monster, monster_image, map_parser, screen):
        monster = list(monster).copy()
        # 我方打怪物一次扣多少血
        diff_our = self.attack_power - monster[3]
        # 怪物打我方一次扣多少血
        diff_monster = max(monster[2] - self.defense_power, 0)
        # 更新战斗面板的频率
        update_count, update_interval, update_hero = 0, 5, False
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.fontpath, 40)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            map_parser.draw(screen)
            for scene in self.cur_scenes:
                screen.blit(scene[0], scene[1])
            self.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
            # --更新战斗面板
            update_count += 1
            if update_count > update_interval:
                update_count = 0
                if update_hero:
                    self.life_value = self.life_value - (monster[2] - self.defense_power)
                else:
                    monster[1] = max(monster[1] - (self.attack_power - monster[3]), 0)
                update_hero = not update_hero
                if monster[1] <= 0: return
            screen.blit(self.background_images['battlebg'], (20, 40))
            screen.blit(monster_image, (90, 140))
            font_renders = [
                font.render(str(monster[1]), True, (255, 255, 255)),
                font.render(str(monster[2]), True, (255, 255, 255)),
                font.render(str(monster[3]), True, (255, 255, 255)),
                font.render(str(self.life_value), True, (255, 255, 255)),
                font.render(str(self.attack_power), True, (255, 255, 255)),
                font.render(str(self.defense_power), True, (255, 255, 255)),
            ]
            rects = [fr.get_rect() for fr in font_renders]
            for idx in range(3):
                rects[idx].top, rects[idx].left = 78 + idx * 95, 320
            for idx in range(3, 6):
                rects[idx].top, rects[idx].right = 78 + (idx - 3) * 95, 655
            for fr, rect in zip(font_renders, rects):
                screen.blit(fr, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)


'''魔塔小游戏主要逻辑实现'''
class GameLevels():
    def __init__(self, cfg, resource_loader):
        self.cfg = cfg
        self.resource_loader = resource_loader
        # 游戏地图中的所有图片
        self.map_element_images = resource_loader.images['mapelements']
        # 游戏背景图片
        self.background_images = {
            'gamebg': pygame.transform.scale(resource_loader.images['gamebg'], cfg.SCREENSIZE),
            'battlebg': pygame.transform.scale(resource_loader.images['battlebg'], (932, 407)),
            'blankbg': resource_loader.images['blankbg'],
        }
        # 游戏地图解析类
        self.map_parsers_dict = {}
        self.max_map_level_pointer = 0
        self.map_level_pointer = 0
        self.loadmap()
        # 英雄类
        self.hero = Hero(
            images=resource_loader.images['hero'],
            blocksize=cfg.BLOCKSIZE,
            block_position=self.map_parser.getheroposition(),
            offset=(325, 55),
            fontpath=cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'],
            background_images=self.background_images,
            cfg=cfg,
            resource_loader=resource_loader,
        )

    '''导入地图'''
    def loadmap(self):
        if self.map_level_pointer in self.map_parsers_dict:
            self.map_parser = self.map_parsers_dict[self.map_level_pointer]
        else:
            self.map_parser = MapParser(
                blocksize=self.cfg.BLOCKSIZE,
                filepath=self.cfg.MAPPATHS[self.map_level_pointer],
                element_images=self.map_element_images,
                offset=(325, 55),
            )
            self.map_parsers_dict[self.map_level_pointer] = self.map_parser

    '''运行'''
    def run(self, screen):
        # 游戏主循环
        clock, is_running = pygame.time.Clock(), True
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
            key_pressed = pygame.key.get_pressed()
            move_events = []
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                move_events = self.hero.move('up', self.map_parser, screen)
            elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                move_events = self.hero.move('down', self.map_parser, screen)
            elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                move_events = self.hero.move('left', self.map_parser, screen)
            elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                move_events = self.hero.move('right', self.map_parser, screen)
            elif key_pressed[pygame.K_j] and self.hero.has_jump:
                move_events = ['jump_level']
            elif key_pressed[pygame.K_l] and self.hero.has_forecast:
                move_events = ['forecast_level']
            if not move_events: move_events = []
            # --画游戏地图
            self.map_parser.draw(screen)
            # --左侧面板栏
            font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
            font_renders = [
                self.hero.font.render(str(self.map_level_pointer), True, (255, 255, 255)),
                font.render('游戏时间: ' + str(pygame.time.get_ticks() // 60000) + ' 分 ' + str(
                    pygame.time.get_ticks() // 1000 % 60) + ' 秒', True, (255, 255, 255)),
            ]
            rects = [fr.get_rect() for fr in font_renders]
            rects[0].topleft = (150, 530)
            rects[1].topleft = (75, 630)
            for fr, rect in zip(font_renders, rects):
                screen.blit(fr, rect)
            # --画英雄
            self.hero.draw(screen)
            self.hero.cur_scenes = [
                [font_renders[0], rects[0]], [font_renders[1], rects[1]]
            ]
            self.hero.showinfo(screen)
            # --触发游戏事件
            for event in move_events:
                if event == 'upstairs':
                    self.map_level_pointer += 1
                    self.max_map_level_pointer = max(self.max_map_level_pointer, self.map_level_pointer)
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'down')
                elif event == 'downstairs':
                    self.map_level_pointer -= 1
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'up')
                elif event == 'conversation_hero_and_fairy':
                    self.showconversationheroandfairy(screen, self.hero.cur_scenes)
                elif event in ['buy_from_shop', 'buy_from_businessman', 'buy_from_oldman']:
                    self.showbuyinterface(screen, self.hero.cur_scenes, event)
                elif event == 'jump_level':
                    ori_level = self.map_level_pointer
                    self.map_level_pointer = self.showjumplevel(screen, self.hero.cur_scenes)
                    self.loadmap()
                    if ori_level > self.map_level_pointer:
                        self.hero.placenexttostairs(self.map_parser, 'up')
                    else:
                        self.hero.placenexttostairs(self.map_parser, 'down')
                elif event == 'forecast_level':
                    self.showforecastlevel(screen, self.hero.cur_scenes)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    '''显示关卡怪物信息'''
    def showforecastlevel(self, screen, scenes):
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        monsters = self.map_parser.getallmonsters()
        if len(monsters) < 1: return
        monsters_show_pointer, max_monsters_show_pointer = 1, round(len(monsters) / 4)
        show_tip_text, show_tip_text_count, max_show_tip_text_count = True, 1, 15
        return_flag = False
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        return_flag = True
                    elif event.key == pygame.K_SPACE:
                        monsters_show_pointer = monsters_show_pointer + 1
                        if monsters_show_pointer > max_monsters_show_pointer: monsters_show_pointer = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_l and return_flag:
                        return
            # --对话框
            # ----底色
            width, height = 14, 5
            left, top = self.cfg.SCREENSIZE[0] // 2 - width // 2 * self.cfg.BLOCKSIZE, self.cfg.SCREENSIZE[
                1] // 2 - height * self.cfg.BLOCKSIZE
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----边框
            pygame.draw.rect(screen, (199, 97, 20),
                             (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
            # ----展示选项
            for idx, monster in enumerate(monsters[(monsters_show_pointer - 1) * 4: monsters_show_pointer * 4]):
                id_image = self.resource_loader.images['mapelements'][monster[6]][0]
                id_image = pygame.transform.scale(id_image, (self.cfg.BLOCKSIZE - 10, self.cfg.BLOCKSIZE - 10))
                screen.blit(id_image, (left + 10, top + 20 + idx * self.cfg.BLOCKSIZE))
                text = f'名称: {monster[0]}  生命: {monster[1]}  攻击: {monster[2]}  防御: {monster[3]}  金币: {monster[4]}  经验: {monster[5]}  损失: {self.hero.winmonster(monster)[1]}'
                font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + 15 + self.cfg.BLOCKSIZE, top + 30 + idx * self.cfg.BLOCKSIZE
                screen.blit(font_render, rect)
            # ----操作提示
            show_tip_text_count += 1
            if show_tip_text_count == max_show_tip_text_count:
                show_tip_text_count = 1
                show_tip_text = not show_tip_text
            if show_tip_text:
                tip_text = '空格键'
                font_render = font.render(tip_text, True, (255, 255, 255))
                rect.left, rect.bottom = self.cfg.BLOCKSIZE * width + 30, self.cfg.BLOCKSIZE * (height + 1) + 10
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    '''显示关卡跳转'''
    def showjumplevel(self, screen, scenes):
        # 主循环
        clock, selected_level = pygame.time.Clock(), self.map_level_pointer
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return selected_level
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_level = max(selected_level - 1, 0)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_level = min(selected_level + 1, self.max_map_level_pointer)
            # --对话框
            # ----底色
            width, height = 11, 4
            left, top = self.cfg.SCREENSIZE[0] // 2 - width // 2 * self.cfg.BLOCKSIZE, self.cfg.SCREENSIZE[
                1] // 2 - height * self.cfg.BLOCKSIZE
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----边框
            pygame.draw.rect(screen, (199, 97, 20),
                             (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
            # ----展示选项
            for idx in list(range(self.max_map_level_pointer + 1)):
                if selected_level == idx:
                    text = f'➤第 {idx} 层'
                    font_render = font.render(text, True, (255, 0, 0))
                else:
                    text = f'    第 {idx} 层'
                    font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + 20 + idx // 6 * self.cfg.BLOCKSIZE * 2, top + 20 + (idx % 6) * 30
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    '''显示商店'''
    def showbuyinterface(self, screen, scenes, shop_type):
        # 购买函数
        def buy(hero, coins_cost=0, experience_cost=0, add_life_value=0, add_attack_power=0, add_defense_power=0,
                add_level=0, add_yellow_keys=0, add_purple_keys=0, add_red_keys=0):
            if hero.num_coins < coins_cost: return
            if hero.experience < experience_cost: return
            if add_yellow_keys < 0 and hero.num_yellow_keys < 1: return
            if add_purple_keys < 0 and hero.num_purple_keys < 1: return
            if add_red_keys < 0 and hero.num_red_keys < 1: return
            hero.num_coins -= coins_cost
            hero.experience -= experience_cost
            hero.life_value += add_life_value + 1000 * add_level
            hero.attack_power += add_attack_power + 7 * add_level
            hero.defense_power += add_defense_power + 7 * add_level
            hero.level += add_level
            hero.num_yellow_keys += add_yellow_keys
            hero.num_purple_keys += add_purple_keys
            hero.num_red_keys += add_red_keys

        # 选项定义
        # --第三层商店
        if self.map_level_pointer == 3 and shop_type == 'buy_from_shop':
            choices_dict = {
                '增加 800 点生命（25 金币）': lambda: buy(self.hero, coins_cost=25, add_life_value=800),
                '增加 4 点攻击（25 金币）': lambda: buy(self.hero, coins_cost=25, add_attack_power=4),
                '增加 4 点防御（25 金币）': lambda: buy(self.hero, coins_cost=25, add_defense_power=4),
                '离开商店': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['22'][0]
        # --第十一层商店
        elif self.map_level_pointer == 11 and shop_type == 'buy_from_shop':
            choices_dict = {
                '增加 4000 点生命（100 金币）': lambda: buy(self.hero, coins_cost=100, add_life_value=4000),
                '增加 20 点攻击（100 金币）': lambda: buy(self.hero, coins_cost=100, add_attack_power=20),
                '增加 20 点防御（100 金币）': lambda: buy(self.hero, coins_cost=100, add_defense_power=20),
                '离开商店': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['22'][0]
        # --第五层神秘老人
        elif self.map_level_pointer == 5 and shop_type == 'buy_from_oldman':
            choices_dict = {
                '提升一级（100 经验）': lambda: buy(self.hero, experience_cost=100, add_level=1),
                '增加 5 点攻击（30 经验）': lambda: buy(self.hero, experience_cost=30, add_attack_power=5),
                '增加 5 点防御（30 经验）': lambda: buy(self.hero, experience_cost=30, add_defense_power=5),
                '离开商店': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['26'][0]
        # --第十三层神秘老人
        elif self.map_level_pointer == 13 and shop_type == 'buy_from_oldman':
            choices_dict = {
                '提升三级（270 经验）': lambda: buy(self.hero, experience_cost=270, add_level=1),
                '增加 17 点攻击（95 经验）': lambda: buy(self.hero, experience_cost=95, add_attack_power=17),
                '增加 17 点防御（95 经验）': lambda: buy(self.hero, experience_cost=95, add_defense_power=17),
                '离开商店': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['26'][0]
        # --第五层商人
        elif self.map_level_pointer == 5 and shop_type == 'buy_from_businessman':
            choices_dict = {
                '购买 1 把黄钥匙（10 金币）': lambda: buy(self.hero, coins_cost=10, add_yellow_keys=1),
                '购买 1 把蓝钥匙（50 金币）': lambda: buy(self.hero, coins_cost=50, add_purple_keys=1),
                '购买 1 把红钥匙（100 金币）': lambda: buy(self.hero, coins_cost=100, add_red_keys=1),
                '离开商店': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['27'][0]
        # --第十二层商人
        elif self.map_level_pointer == 12 and shop_type == 'buy_from_businessman':
            choices_dict = {
                '卖出 1 把黄钥匙（7 金币）': lambda: buy(self.hero, coins_cost=-7, add_yellow_keys=-1),
                '卖出 1 把蓝钥匙（35 金币）': lambda: buy(self.hero, coins_cost=-35, add_purple_keys=-1),
                '卖出 1 把红钥匙（70 金币）': lambda: buy(self.hero, coins_cost=-70, add_red_keys=-1),
                '离开商店': lambda: buy(self.hero),
            }
            id_image = self.resource_loader.images['mapelements']['27'][0]
        id_image = pygame.transform.scale(id_image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
        # 主循环
        clock, selected_idx = pygame.time.Clock(), 1
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        list(choices_dict.values())[selected_idx - 1]()
                        if selected_idx == 4: return
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_idx = max(selected_idx - 1, 1)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_idx = min(selected_idx + 1, 4)
            # --对话框
            # ----底色
            width, height = 8, 3
            left, bottom = self.hero.rect.left + self.hero.rect.width // 2 - width // 2 * self.cfg.BLOCKSIZE, self.hero.rect.bottom
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, bottom + row * self.cfg.BLOCKSIZE))
            # ----边框
            pygame.draw.rect(screen, (199, 97, 20),
                             (left - 4, bottom - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
            # ----展示选项
            for idx, choice in enumerate(['请选择:'] + list(choices_dict.keys())):
                if selected_idx == idx and idx > 0:
                    choice = '➤' + choice
                    font_render = font.render(choice, True, (255, 0, 0))
                elif idx > 0:
                    choice = '    ' + choice
                    font_render = font.render(choice, True, (255, 255, 255))
                else:
                    font_render = font.render(choice, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + self.cfg.BLOCKSIZE + 20, bottom + 10 + idx * 30
                screen.blit(font_render, rect)
            # ----展示头像
            screen.blit(id_image, (left + 10, bottom + 10))
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    '''仙女和勇士对话'''
    def showconversationheroandfairy(self, screen, scenes):
        # 对话框指针
        conversation_pointer = 0
        # 定义所有对话
        if self.hero.has_cross:
            conversations = [
                ['剧情未写'],
            ]
            self.hero.has_cross = False
            self.hero.life_value = int(self.hero.life_value * 4 / 3)
            self.hero.attack_power = int(self.hero.attack_power * 4 / 3)
            self.hero.defense_power = int(self.hero.defense_power * 4 / 3)
        else:
            conversations = [
                ['剧情未写'],
            ]
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        conversation_pointer += 1
                        if conversation_pointer >= len(conversations): return
            # --画对话框
            conversation = conversations[conversation_pointer]
            # ----勇士
            if conversation_pointer % 2 == 0:
                left, top, width, height = 510, 430, 8, 2
                pygame.draw.rect(screen, (199, 97, 20),
                                 (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8),
                                 7)
                id_image = self.hero.images['down']
            # ----仙子
            else:
                left, top, width, height = 300, 250, 8, 2
                if len(conversation) > 3: height = 3
                if len(conversation) > 5: height = 4
                if len(conversation) > 7: height = 5
                pygame.draw.rect(screen, (199, 97, 20),
                                 (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8),
                                 7)
                id_image = self.resource_loader.images['mapelements']['24'][0]
            # ----底色
            for col in range(width):
                for row in range(height):
                    image = self.resource_loader.images['mapelements']['0'][0]
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----左上角图标
            screen.blit(id_image, (left + 10, top + 10))
            # ----对话框中的文字
            for idx, text in enumerate(conversation):
                font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + self.cfg.BLOCKSIZE + 40, top + 10 + idx * 30
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 屏幕大小
    BLOCKSIZE = 54
    SCREENBLOCKSIZE = (18, 13)
    SCREENSIZE = (BLOCKSIZE * SCREENBLOCKSIZE[0], BLOCKSIZE * SCREENBLOCKSIZE[1])
    # 标题
    TITLE = '魔塔探险：拯救之旅-Gaven'
    # FPS
    FPS = 30
    # 字体路径
    FONT_PATHS_NOPRELOAD_DICT = {
        'font_cn': os.path.join(rootdir, 'resources/fonts/font_cn.ttf'),
        'font_en': os.path.join(rootdir, 'resources/fonts/font_en.ttf')
    }
    # 游戏地图路径
    MAPPATHS = [
        os.path.join(os.path.split(os.path.abspath(__file__))[0], f'resources/levels/{idx}.lvl') for idx in
        range(len(os.listdir(os.path.join(rootdir, f'resources/levels/'))))
    ]
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'battlebg': os.path.join(rootdir, f'resources/images/battlebg.png'),
        'blankbg': os.path.join(rootdir, f'resources/images/blankbg.png'),
        'gamebg': os.path.join(rootdir, f'resources/images/gamebg.png'),
        'hero': {},
        'mapelements': {},
    }
    for filename in os.listdir(os.path.join(rootdir, 'resources/images/map0/')):
        IMAGE_PATHS_DICT['mapelements'][filename.split('.')[0]] = [
            os.path.join(rootdir, f'resources/images/map0/{filename}'),
            os.path.join(rootdir, f'resources/images/map1/{filename}'),
        ]
    for filename in os.listdir(os.path.join(rootdir, 'resources/images/player/')):
        IMAGE_PATHS_DICT['hero'][filename.split('.')[0]] = os.path.join(rootdir, f'resources/images/player/{filename}')

'''游戏开始界面'''
class StartGameInterface():
    def __init__(self, cfg):
        self.cfg = cfg
        self.play_btn = Button('开始游戏', cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 50,
                               (cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] - 300))
        self.intro_btn = Button('游戏说明', cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 50,
                                (cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] - 200))
        self.quit_btn = Button('离开游戏', cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 50,
                               (cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] - 100))

    '''外部调用'''
    def run(self, screen):
        # 魔塔
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 80)
        font_render_cn = font.render('魔塔探险：拯救之旅', True, (255, 255, 255))
        rect_cn = font_render_cn.get_rect()
        rect_cn.center = self.cfg.SCREENSIZE[0] // 2, 100
        # Magic Tower
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_en'], 80)
        font_render_en = font.render('Magic Tower', True, (255, 255, 255))
        rect_en = font_render_en.get_rect()
        rect_en.center = self.cfg.SCREENSIZE[0] // 2, 250
        # (Ver 1.12)
        font = pygame.font.Font(self.cfg.FONT_PATHS_NOPRELOAD_DICT['font_cn'], 40)
        font_render_version = font.render('(Ver 1.00)', True, (255, 255, 255))
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
            font.render('游戏代码参考: https://github.com/oscarcx123/MagicTower-Python', True, (255, 255, 255)),
            font.render('游戏素材来自: http://www.4399.com/flash/1749_1.htm.', True, (255, 255, 255)),
            font.render('游戏背景故事为公主被大魔王抓走, 需要勇士前往魔塔将其救出.', True, (255, 255, 255)),
            font.render('张佳文-2021214037', True, (255, 255, 255)),
            font.render('Python-作业.', True, (255, 255, 255)),
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




'''基于pygame的游戏初始化'''
def InitPygame(screensize, title='Python作业-张佳文', init_mixer=True):
    pygame.init()
    if init_mixer: pygame.mixer.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption(title)
    return screen


'''基于pygame的游戏导入游戏素材'''
class PygameResourceLoader():
    def __init__(self, image_paths_dict=None, sound_paths_dict=None, font_paths_dict=None, bgm_path=None, **kwargs):
        # 设置属性
        self.bgm_path = bgm_path
        self.font_paths_dict = font_paths_dict
        self.image_paths_dict = image_paths_dict
        self.sound_paths_dict = sound_paths_dict
        # 导入字体
        self.fonts = self.fontload(font_paths_dict)
        # 导入图像
        self.images = self.defaultload(image_paths_dict, pygame.image.load)
        # 导入声音
        self.sounds = self.defaultload(sound_paths_dict, pygame.mixer.Sound)

    '''默认的素材导入函数'''
    def defaultload(self, resources_dict, load_func):
        if resources_dict is None: return dict()
        assert isinstance(resources_dict, dict)
        resources = dict()
        for key, value in resources_dict.items():
            if isinstance(value, dict):
                resources[key] = self.defaultload(value, load_func)
            elif isinstance(value, list):
                resources[key] = list()
                for path in value: resources[key].append(load_func(path))
            else:
                resources[key] = load_func(value)
        return resources

    '''导入字体'''
    def fontload(self, font_paths_dict):
        if font_paths_dict is None: return dict()
        assert isinstance(font_paths_dict, dict)
        fonts = dict()
        for key, value in font_paths_dict.items():
            if not value.get('system_font', False):
                fonts[key] = pygame.font.Font(value['name'], value['size'])
            else:
                fonts[key] = pygame.font.SysFont(value['name'], value['size'])
        return fonts

    '''播放背景音乐'''
    def playbgm(self):
        pygame.mixer.music.load(self.bgm_path)
        pygame.mixer.music.play(-1, 0.0)


'''Pygame的游戏基类'''
class PygameBaseGame():
    def __init__(self, config, **kwargs):
        # 设置属性
        self.config = config
        # 初始化
        self.initialize()
        # 用户可以覆盖默认参数
        for key, value in kwargs.items():
            if hasattr(self, key): setattr(self, key, value)

    '''运行游戏'''
    def run(self):
        raise NotImplementedError('not to be implemented...')

    '''初始化'''
    def initialize(self):
        self.screen = InitPygame(screensize=self.config.SCREENSIZE, title=self.config.TITLE)
        bgm_path = self.config.BGM_PATH if hasattr(self.config, 'BGM_PATH') else None
        font_paths_dict = self.config.FONT_PATHS_DICT if hasattr(self.config, 'FONT_PATHS_DICT') else None
        image_paths_dict = self.config.IMAGE_PATHS_DICT if hasattr(self.config, 'IMAGE_PATHS_DICT') else None
        sound_paths_dict = self.config.SOUND_PATHS_DICT if hasattr(self.config, 'SOUND_PATHS_DICT') else None
        self.resource_loader = PygameResourceLoader(
            bgm_path=bgm_path,
            font_paths_dict=font_paths_dict,
            image_paths_dict=image_paths_dict,
            sound_paths_dict=sound_paths_dict,
        )

'''魔塔小游戏'''
'''  game_type = 'magictower'''
class MagicTowerGame(PygameBaseGame):
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MagicTowerGame, self).__init__(config=self.cfg, **kwargs)

    def run(self):
        # 开始界面
        sg_interface = StartGameInterface(self.cfg)
        sg_interface.run(self.screen)
        # 游戏进行中界面
        game_client = GameLevels(self.cfg, self.resource_loader)
        game_client.run(self.screen)
