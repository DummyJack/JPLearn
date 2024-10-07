# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class TitleBar(BoxLayout):
    def __init__(self, title, close_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 30  # 增加高度以適應更大的字體

        self.title_label = Label(text=title, font_name='ChineseFont', font_size=28, size_hint_x=0.9)  # 增大字體大小
        self.add_widget(self.title_label)

        self.close_button = Button(text='X', size_hint=(None, None), size=(40, 40))  # 增大按鈕大小
        self.close_button.bind(on_press=close_callback)
        self.add_widget(self.close_button)
