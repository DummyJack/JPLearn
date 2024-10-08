# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget 
from custom_widgets import TitleBar
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout

class EditWordPopup(Popup):
    def __init__(self, word, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (None, None)
        self.width = min(dp(500), Window.width * 0.7)
        self.height = min(dp(300), Window.height * 0.4)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        title_bar = TitleBar("修改單字", self.dismiss)
        content.add_widget(title_bar)
        
        input_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.word_input = TextInput(text=word, multiline=False, font_name='ChineseFont', font_size=dp(20), size_hint_y=None, height=dp(50))
        input_layout.add_widget(self.word_input)
        
        btn = Button(text="確定", size_hint=(None, None), size=(dp(100), dp(40)), font_name='ChineseFont', font_size=dp(18))
        btn.bind(on_press=self.edit_word)
        input_layout.add_widget(btn)
        
        content.add_widget(input_layout)
        
        self.content = content
        self.edit_callback = edit_callback

    def edit_word(self, instance):
        new_word = self.word_input.text
        if new_word:
            self.edit_callback(new_word)
            self.dismiss()

class WordItem(BoxLayout):
    def __init__(self, word, delete_callback, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(10)
        self.padding = [dp(10), dp(5)]
        self.size_hint_y = None
        self.height = dp(60)
        self.word = word
        self.label = Label(text=word, font_size=dp(24), font_name='ChineseFont', size_hint_x=0.7)
        self.add_widget(self.label)
        
        edit_btn = Button(text='修改', size_hint=(None, None), size=(dp(80), dp(40)), font_name='ChineseFont', font_size=dp(18))
        edit_btn.bind(on_press=self.edit_word)
        self.add_widget(edit_btn)
        
        delete_btn = Button(text='刪除', size_hint=(None, None), size=(dp(80), dp(40)), font_name='ChineseFont', font_size=dp(18))
        delete_btn.bind(on_press=self.delete_word)
        self.add_widget(delete_btn)

        self.delete_callback = delete_callback
        self.edit_callback = edit_callback

    def delete_word(self, instance):
        self.delete_callback(self)

    def edit_word(self, instance):
        popup = EditWordPopup(self.word, self.update_word)
        popup.open()

    def update_word(self, new_word):
        self.word = new_word
        self.label.text = new_word
        self.edit_callback(self, new_word)

class WordsList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=[0, dp(10), 0, 0])
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_word(self, word):
        word_item = WordItem(word, self.delete_word, self.edit_word)
        self.layout.add_widget(word_item)

    def delete_word(self, word_item):
        self.layout.remove_widget(word_item)

    def edit_word(self, word_item, new_word):
        pass

class AddWordPopup(Popup):
    def __init__(self, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (None, None)
        self.width = min(dp(600), Window.width * 0.7)
        self.height = min(dp(400), Window.height * 0.5)
        
        content = BoxLayout(orientation='vertical', spacing=dp(20))
        
        title_bar = TitleBar("新增單字", self.dismiss)
        content.add_widget(title_bar)
        
        # 主要內容區域
        main_content = BoxLayout(orientation='vertical', spacing=dp(20), padding=[dp(20), dp(20), dp(20), dp(20)])
        
        self.word_input = TextInput(
            multiline=True,
            font_name='ChineseFont', 
            font_size=dp(24), 
            size_hint=(1, 1),  # 填滿可用空間
            padding=[dp(10), dp(10), dp(10), dp(10)],
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
        )
        main_content.add_widget(self.word_input)
        
        content.add_widget(main_content)
        
        # 底部按鈕區域
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(70), padding=[dp(20), 0, dp(20), dp(20)])
        
        confirm_btn = Button(
            text="確定", 
            size_hint=(None, None),
            size=(dp(120), dp(50)),  # 調整按鈕大小
            font_name='ChineseFont', 
            font_size=dp(18)
        )
        confirm_btn.bind(on_press=self.add_word)
        
        cancel_btn = Button(
            text="取消", 
            size_hint=(None, None),
            size=(dp(120), dp(50)),  # 調整按鈕大小
            font_name='ChineseFont', 
            font_size=dp(18)
        )
        cancel_btn.bind(on_press=self.dismiss)
        
        button_layout.add_widget(Widget())  # 添加一個彈性空間
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(Widget())  # 添加一個彈性空間
        
        content.add_widget(button_layout)
        
        self.content = content
        self.add_callback = add_callback

    def add_word(self, instance):
        word = self.word_input.text.strip()  # 移除首尾空白
        if word:
            self.add_callback(word)
            self.dismiss()

class WordsListPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        title_bar = TitleBar("單字筆記", self.dismiss)
        content.add_widget(title_bar)
        
        self.words_list = WordsList()
        content.add_widget(self.words_list)
        
        add_btn = Button(text="新增單字", size_hint=(None, None), size=(dp(200), dp(60)), pos_hint={'center_x': 0.5}, font_name='ChineseFont', font_size=dp(24))
        add_btn.bind(on_press=self.show_add_popup)
        content.add_widget(add_btn)
        
        self.content = content

    def show_add_popup(self, instance):
        popup = AddWordPopup(add_callback=self.words_list.add_word)
        popup.open()