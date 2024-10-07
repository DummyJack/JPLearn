# -*- coding: utf-8 -*-

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.scrollview import ScrollView
from custom_widgets import TitleBar
from kivy.core.window import Window

class FiftySoundsGrid(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=5, size_hint=(1, None))
        self.bind(minimum_height=self.setter('height'))

        sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn"
        sounds = sounds.split("|")

        # 計算每行可以容納的按鈕數量
        button_width = 70
        button_spacing = 5
        screen_width = Window.width * 0.9 - 20  # 假設彈出窗口寬度為屏幕寬度的90%，減去padding
        buttons_per_row = int(screen_width / (button_width + button_spacing))

        for i in range(0, len(sounds), buttons_per_row):
            row = GridLayout(cols=buttons_per_row, spacing=[5, 5], size_hint=(1, None), height=70)
            for sound in sounds[i:i+buttons_per_row]:
                japanese, romaji = sound[0], sound[1:]
                btn = Button(
                    text=f'[size=20]{japanese}[/size]\n[size=14]{romaji}[/size]',
                    markup=True,
                    font_name='ChineseFont',
                    background_color=(0.5, 0.7, 1, 1),
                    size_hint=(None, None),
                    size=(button_width, 70)
                )
                btn.bind(on_press=self.play_sound)
                row.add_widget(btn)
            self.add_widget(row)

    def play_sound(self, instance):
        sound = instance.text.split()[0]  # 獲取日文字符
        print(f"播放音頻: {sound}")

class FiftySoundsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=20)  # 增加間距

        title_bar = TitleBar("五十音", self.dismiss)
        content.add_widget(title_bar)

        grid = FiftySoundsGrid()
        content.add_widget(grid)
        
        self.content = content

