# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase    
from fifty_sounds import FiftySoundsPopup
from words_list import WordsListPopup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

class MainView(FloatLayout):  # 改用 FloatLayout
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.94, 0.97, 1, 1)  # 愛麗絲藍
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 添加標題
        title = Label(text='日文快樂學', font_size=60, size_hint_y=None, height=100,color=(0,0,0,1), pos_hint={'top': 1, 'center_x': 0.5}, font_name='ChineseFont')
        self.add_widget(title)

        # 創建按鈕
        self.btn_50on = Button(
            text='五十音',
            font_size=48,
            size_hint=(None, None),
            size=(300, 100),
            background_color=(0, 0, 1, 1),
            pos_hint={'center_x': 0.35, 'center_y': 0.5}, # 調整位置
            font_name='ChineseFont'
        )
        self.btn_50on.bind(on_press=self.on_50on_press)
        self.add_widget(self.btn_50on)

        self.btn_words = Button(
            text='單字',
            font_size=48,
            size_hint=(None, None),
            size=(300, 100),
            background_color=(0, 1, 0, 1),
            pos_hint={'center_x': 0.65, 'center_y': 0.5},  # 調整位置
            font_name='ChineseFont'
        )
        self.btn_words.bind(on_press=self.on_words_press)
        self.add_widget(self.btn_words)

        # 添加製作人文字
        creator_label = Label(
            text='製作人：書賢',
            font_size=24,
            size_hint_y=None,
            height=30,
            pos_hint={'center_x': 0.5, 'y': 0.02},  # 將標籤放在底部中央
            color=(0,0,0,1), 
            font_name='ChineseFont'
        )
        self.add_widget(creator_label)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_50on_press(self, instance):
        popup = FiftySoundsPopup()
        popup.open()

    def on_words_press(self, instance):
        popup = WordsListPopup()
        popup.open()

class JapaneseLearnApp(App):
    def build(self):
        LabelBase.register(name='ChineseFont', fn_regular='./NotoSansTC-VariableFont_wght.ttf')
        return MainView()

if __name__ == '__main__':
    JapaneseLearnApp().run()
