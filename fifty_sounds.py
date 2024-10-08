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

        self.main_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))

        sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn"
        self.sounds = sounds.split("|")
        self.button_size = dp(70)
        self.spacing = dp(5)

        self.update_layout()

        self.add_widget(self.main_layout)

    def update_layout(self):
        self.main_layout.clear_widgets()
        width = self.width if self.width else Window.width
        max_buttons_per_row = max(1, int((width - self.spacing) / (self.button_size + self.spacing)))
        
        current_row = None
        for i, sound in enumerate(self.sounds):
            if i % max_buttons_per_row == 0:
                current_row = GridLayout(cols=max_buttons_per_row, spacing=self.spacing, size_hint_y=None, height=self.button_size)
                self.main_layout.add_widget(current_row)

            japanese, romaji = sound[0], sound[1:]
            btn = Button(
                text=f'[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]',
                markup=True,
                font_name='ChineseFont',
                background_color=(0.5, 0.7, 1, 1),
                size_hint=(None, None),
                size=(self.button_size, self.button_size),
                halign='center',
                valign='middle',
                text_size=(self.button_size, self.button_size)
            )
            btn.bind(on_press=self.play_sound)
            current_row.add_widget(btn)

        # 填充最後一行
        if current_row:
            remaining_buttons = max_buttons_per_row - (len(self.sounds) % max_buttons_per_row)
            if remaining_buttons < max_buttons_per_row:
                for _ in range(remaining_buttons):
                    empty_btn = Button(
                        background_color=(0, 0, 0, 0),
                        size_hint=(None, None),
                        size=(self.button_size, self.button_size)
                    )
                    current_row.add_widget(empty_btn)

    def play_sound(self, instance):
        sound = instance.text.split()[0]  # 獲取日文字符
        print(f"播放音頻: {sound}")

    def on_size(self, *args):
        self.update_layout()

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
            self.grid.update_layout()
