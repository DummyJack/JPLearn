# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.text import LabelBase    
from functions.fifty_sounds import FiftySoundsPopup
from functions.words_list import WordsListPopup
from kivy.metrics import dp

class MainView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 添加標題
        title = Label(
            text='日語快樂學', 
            font_size=dp(60), 
            size_hint_y=None, 
            height=dp(100), 
            color=(0,0,0,1), 
            pos_hint={'top': 0.95, 'center_x': 0.5}, 
            font_name='ChineseFont'
        )
        self.add_widget(title)

        # 創建按鈕
        button_width = dp(250)  # 減小按鈕寬度
        button_height = dp(80)  # 減小按鈕高度

        self.btn_50on = Button(
            text='五十音',
            font_size=dp(36),  # 減小字體大小
            size_hint=(None, None),
            size=(button_width, button_height),
            background_color=(0, 0, 1, 1),
            pos_hint={'center_x': 0.3, 'center_y': 0.5},  # 調整位置
            font_name='ChineseFont'
        )
        self.btn_50on.bind(on_press=self.on_50on_press)
        self.add_widget(self.btn_50on)

        self.btn_words = Button(
            text='單字',
            font_size=dp(36),  # 減小字體大小
            size_hint=(None, None),
            size=(button_width, button_height),
            background_color=(0, 1, 0, 1),
            pos_hint={'center_x': 0.7, 'center_y': 0.5},  # 調整位置
            font_name='ChineseFont'
        )
        self.btn_words.bind(on_press=self.on_words_press)
        self.add_widget(self.btn_words)

        # 添加製作人文字
        creator_label = Label(
            text='製作人：書賢',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(30),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            color=(0,0,0,1), 
            font_name='ChineseFont'
        )
        self.add_widget(creator_label)

    def on_50on_press(self, instance):
        popup = FiftySoundsPopup()
        popup.open()

    def on_words_press(self, instance):
        popup = WordsListPopup()
        popup.open()

class JapaneseLearnApp(App):
    def build(self):
        LabelBase.register(name='ChineseFont', fn_regular='./fonts/NotoSansTC-VariableFont_wght.ttf')
        Window.clearcolor = (0.94, 0.97, 1, 1)  # 設置窗口背景顏色
        return MainView()

if __name__ == '__main__':
    JapaneseLearnApp().run()
