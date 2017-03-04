# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/3
import cocos
import struct
import math
import pyglet
from pyaudio import PyAudio, paInt16


# 主菜单(继承Menu类)
class TitleMenu(cocos.menu.Menu):
    # 初始化(标题)
    def __init__(self):
        super(TitleMenu, self).__init__('Go Go Go!')
        # 设置标题细节
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 120, 120, 255)
        # 设置选项细节
        self.font_item['font_name'] = 'Bauhaus 93'
        self.font_item['font_size'] = 37
        self.font_item['color'] = (0, 0, 0, 150)
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['color'] = (0, 0, 0, 255)
        # 添加菜单选项
        item1 = cocos.menu.MenuItem('New Game', self.on_new_game)
        item2 = cocos.menu.MenuItem('Option', self.on_option)
        item3 = cocos.menu.MenuItem('Quit', self.on_quit)
        self.create_menu([item1, item2, item3],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(320, 175), (320, 125), (320, 75)]
                         ))

    # 编辑各选项
    def on_new_game(self):
        pass

    def on_option(self):
        self.parent.switch_to(1)

    def on_quit(self):
        # 退出
        pyglet.app.exit()


# 选项菜单
class OptionMenu(cocos.menu.Menu):
    def __init__(self):
        super(OptionMenu, self).__init__('Go Go Go!')
        # 设置标题细节
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 120, 120, 255)
        # 设置选项细节
        self.font_item['font_name'] = 'Bauhaus 93'
        self.font_item['font_size'] = 37
        self.font_item['color'] = (0, 0, 0, 150)
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['color'] = (0, 0, 0, 255)
        # 选项
        item1 = cocos.menu.MenuItem('Full Screen', self.on_full_screen)
        item2 = cocos.menu.MenuItem('Back', self.on_back)
        self.create_menu([item1, item2],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(320, 125), (320, 75)]
                         ))

    def on_full_screen(self):
        cocos.director.director.window.set_fullscreen(
            not cocos.director.director.window.fullscreen
        )

    def on_back(self):
        self.parent.switch_to(0)


# 标题背景
class TitleBackGround(cocos.layer.ColorLayer):
    def __init__(self):
        super(TitleBackGround, self).__init__(255, 255, 255, 255)


# 游戏主界面
class VoiceGame(cocos.layer.ColorLayer):
    # 开启监听
    is_event_handler = True

    # 初始化
    def __init__(self):
        super(VoiceGame, self).__init__(255, 255, 255, 255)
        # 添加提示信息
        self.info = cocos.text.Label(
            '音量大小',
            font_size=18,
            bold=True,
            color=(255, 73, 49, 255)
        )
        self.info.position = 50, 420
        self.add(self.info)
        # 添加音量条
        self.voice = cocos.text.Label(
            '▉',
            font_size=20,
            color=(94, 245, 94, 255)
        )
        self.voice.position = 50, 380
        self.add(self.voice, z=2)
        # 添加背景
        # self.bg = BackGround()
        # self.add(self.bg)
        # 添加皮卡丘
        self.pika = Pika()
        self.add(self.pika, z=1)
        # 声音输入(这部分还不熟悉)
        self.NUM_SAMPLES = 1000  # 内部缓存块大小
        self.LEVEL = 1500  # 声音保存阈值
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(
            format=paInt16,
            channels=1,
            rate=SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES
        )
        # 实时更新
        self.schedule(self.update)

    def update(self, dt):
        # 按输入的音量大小获得一个level值
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('1000h', string_audio_data))
        level = math.ceil(k/500)
        # 更新音量条显示
        self.update_voice(level)
        if level > 2:
            # self.bg.move()
            if level > 4:
                self.pika.jump(level)

    def update_voice(self, level):
        text = ''
        for i in range(level):
            text += '▉'
        self.voice.element.text = text


# pika类(sprite)
class Pika(cocos.sprite.Sprite):
    def __init__(self):
        super(Pika, self).__init__('pika.png')
        # 设置图像的锚点
        self.image_anchor_x = 85
        self.image_anchor_y = 0
        # 设置图像初始位置
        self.position = 300, 0
        # 设置跳跃初始速度
        self.jump_speed = 0
        # 设置实时更新(每帧都调用一次)
        self.schedule(self.update)

    # 更新函数第一个参数固定为dt(表示经过了多少秒)
    def update(self, dt):
        self.jump_speed -= dt*2
        self.y += self.jump_speed
        # 落地便重置
        if self.y <= 0:
            self.reset()

    # 跳跃
    def jump(self, level):
        # 如果不在地面上就不能跳
        if self.y != 0:
            return
        # 跳跃(得到一个起跳初速度)
        self.jump_speed = level - 1

    # 走
    def run(self):
        floor = 5
        self.x += floor

    # 重置位置与速度
    def reset(self):
        self.jump_speed = 0
        self.y = 0


# 背景
class BackGround(cocos.sprite.Sprite):
    def __init__(self):
        super(BackGround, self).__init__('bg.png')
        self.image_anchor = 0, 0
        self.position = 0, 0

    def move(self):
        self.x -= 5


if __name__ == '__main__':
    pyglet.font.add_directory('resource')
    # 运行
    cocos.director.director.init(caption="不要停,皮卡丘!")
    s = cocos.scene.Scene()
    s.add(cocos.layer.MultiplexLayer(
            TitleMenu(), OptionMenu()
         ), z=1)
    s.add(TitleBackGround(), z=0)
    cocos.director.director.run(s)
