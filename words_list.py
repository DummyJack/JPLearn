# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from custom_widgets import TitleBar

class EditWordPopup(Popup):
    def __init__(self, word, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.8, 0.4)
        
        content = BoxLayout(orientation='vertical')
        
        title_bar = TitleBar("修改單字", self.dismiss)
        content.add_widget(title_bar)
        
        input_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.word_input = TextInput(text=word, multiline=False, font_name='ChineseFont', font_size=24)
        input_layout.add_widget(self.word_input)
        
        btn = Button(text="確定", size_hint_y=None, height=50, font_name='ChineseFont')
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
        self.spacing = 10  # 添加間距
        self.padding = [10, 5]  # 添加內邊距
        self.size_hint_y = None
        self.height = 50  # 設置固定高度
        self.word = word
        self.label = Label(text=word, font_size=24, font_name='ChineseFont', size_hint_x=0.6)
        self.add_widget(self.label)
        
        edit_btn = Button(text='修改', size_hint=(None, None), size=(80, 40), font_name='ChineseFont')
        edit_btn.bind(on_press=self.edit_word)
        self.add_widget(edit_btn)
        
        delete_btn = Button(text='刪除', size_hint=(None, None), size=(80, 40), font_name='ChineseFont')
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
        self.layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=[0, 20, 0, 0])  # 添加頂部內邊距
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_word(self, word):
        word_item = WordItem(word, self.delete_word, self.edit_word)
        self.layout.add_widget(word_item)

    def delete_word(self, word_item):
        self.layout.remove_widget(word_item)

    def edit_word(self, word_item, new_word):
        # 如果需要，可以在這裡添加額外的邏輯
        pass

class AddWordPopup(Popup):
    def __init__(self, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.8, 0.5)  # Increased height
        
        content = BoxLayout(orientation='vertical', spacing=20)
        
        title_bar = Label(text="新增單字", font_name='ChineseFont', font_size=28, size_hint_y=None, height=40)
        content.add_widget(title_bar)
        
        input_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        self.word_input = TextInput(multiline=False, font_name='ChineseFont', font_size=24, size_hint_y=None, height=100)  # Increased height
        input_layout.add_widget(self.word_input)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)  # Reduced height
        confirm_btn = Button(text="確定", size_hint_x=0.3, font_name='ChineseFont')  # Reduced width
        confirm_btn.bind(on_press=self.add_word)
        button_layout.add_widget(confirm_btn)
        
        cancel_btn = Button(text="取消", size_hint_x=0.3, font_name='ChineseFont')  # Reduced width
        cancel_btn.bind(on_press=self.dismiss)
        button_layout.add_widget(cancel_btn)
        
        input_layout.add_widget(button_layout)
        content.add_widget(input_layout)
        
        self.content = content
        self.add_callback = add_callback

    def add_word(self, instance):
        word = self.word_input.text
        if word:
            self.add_callback(word)
            self.dismiss()

class WordsListPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=20)  # 增加間距
        
        title_bar = TitleBar("單字筆記", self.dismiss)
        content.add_widget(title_bar)
        
        self.words_list = WordsList()
        content.add_widget(self.words_list)
        
        add_btn = Button(text="新增單字", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5}, font_name='ChineseFont')
        add_btn.bind(on_press=self.show_add_popup)
        content.add_widget(add_btn)
        
        self.content = content

    def show_add_popup(self, instance):
        popup = AddWordPopup(add_callback=self.words_list.add_word)
        popup.open()
