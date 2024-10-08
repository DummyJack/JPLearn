# -*- coding: utf-8 -*-

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.scrollview import ScrollView
from custom_widgets import TitleBar
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout

class FiftySoundsGrid(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        self.layout = GridLayout(cols=5, spacing=dp(5), size_hint_y=None, size_hint_x=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn"
        sounds = sounds.split("|")

        for sound in sounds:
            japanese, romaji = sound[0], sound[1:]
            btn = Button(
                text=f'[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]',
                markup=True,
                font_name='ChineseFont',
                background_color=(0.5, 0.7, 1, 1),
                size_hint=(None, None),
                size=(dp(70), dp(70)),
                halign='center',  # 文字水平居中
                valign='middle',  # 文字垂直居中
                text_size=(dp(70), dp(70))  # 設置文字區域大小
            )
            btn.bind(on_press=self.play_sound)
            self.layout.add_widget(btn)

        # 添加空白按鈕以填充最後一行
        remaining_buttons = 5 - (len(sounds) % 5)
        if remaining_buttons < 5:
            for _ in range(remaining_buttons):
                empty_btn = Button(
                    background_color=(0, 0, 0, 0),
                    size_hint=(None, None),
                    size=(dp(70), dp(70))
                )
                self.layout.add_widget(empty_btn)

        # 使用 AnchorLayout 來置中 GridLayout
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        anchor_layout.add_widget(self.layout)
        self.add_widget(anchor_layout)

    def play_sound(self, instance):
        sound = instance.text.split()[0]  # 獲取日文字符
        print(f"播放音頻: {sound}")

class FiftySoundsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=dp(20))  # 增加間距

        title_bar = TitleBar("五十音", self.dismiss)
        content.add_widget(title_bar)

        self.grid = FiftySoundsGrid()
        content.add_widget(self.grid)
        
        self.content = content

    def on_size(self, *args):
        # 當彈出窗口大小改變時，調整網格的列數和寬度
        if hasattr(self, 'grid'):
            grid = self.grid
            if isinstance(grid, FiftySoundsGrid):
                width = self.width - dp(40)  # 減去padding
                cols = max(3, int(width / (dp(70) + dp(5))))  # 最少3列，最多根據寬度決定
                grid.layout.cols = cols
                grid.layout.width = cols * (dp(70) + dp(5)) - dp(5)  # 設置GridLayout的寬度
