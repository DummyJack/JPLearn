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
import re

class EditWordPopup(Popup):
    def __init__(self, japanese, explanation, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (None, None)
        self.width = min(dp(700), Window.width * 0.8)
        self.height = min(dp(500), Window.height * 0.6)
        
        content = BoxLayout(orientation='vertical', spacing=dp(20))
        
        title_bar = TitleBar("修改單字", self.dismiss)
        content.add_widget(title_bar)
        
        # 添加一個空白Widget來將輸入框往下移
        content.add_widget(Widget(size_hint_y=None, height=dp(40)))
        
        main_content = BoxLayout(orientation='vertical', spacing=dp(20), padding=[dp(20), dp(20), dp(20), dp(20)])
        
        self.word_input = TextInput(
            text=f"{japanese} {explanation}",  # 使用空格分隔
            multiline=True,
            font_name='ChineseFont', 
            font_size=dp(24), 
            size_hint=(1, None),
            height=dp(150),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
            hint_text='請先輸入日文單字，再做解釋',
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        main_content.add_widget(self.word_input)
        
        self.error_label = Label(text="", color=(1, 0, 0, 1), font_name='ChineseFont', font_size=dp(16))
        main_content.add_widget(self.error_label)
        
        content.add_widget(main_content)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(70), padding=[dp(20), 0, dp(20), dp(20)])
        
        confirm_btn = Button(
            text="確定", 
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            font_name='ChineseFont', 
            font_size=dp(18)
        )
        confirm_btn.bind(on_press=self.edit_word)
        
        cancel_btn = Button(
            text="取消", 
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            font_name='ChineseFont', 
            font_size=dp(18)
        )
        cancel_btn.bind(on_press=self.dismiss)
        
        button_layout.add_widget(Widget())
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(Widget())
        
        content.add_widget(button_layout)
        
        self.content = content
        self.edit_callback = edit_callback

    def edit_word(self, instance):
        word = self.word_input.text.strip()
        if self.validate_input(word):
            japanese, explanation = self.split_input(word)
            self.edit_callback(japanese, explanation)
            self.dismiss()
        else:
            self.error_label.text = "請先打日文單字"

    def validate_input(self, text):
        if not text:
            return False
        first_char = text[0]
        return self.is_japanese_char(first_char)

    def is_japanese_char(self, char):
        # 檢查單個字符是否為日文（平假名、片假名或漢字）
        return '\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9fff'

    def split_input(self, text):
        # 使用正則表達式分割日文和非日文部分
        japanese_pattern = r'^[\u3040-\u30ff\u4e00-\u9fff]+'
        match = re.match(japanese_pattern, text)
        if match:
            japanese = match.group()
            explanation = text[len(japanese):].strip()
        else:
            japanese = ""
            explanation = text
        return japanese, explanation

class WordItem(BoxLayout):
    def __init__(self, word, explanation, delete_callback, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(10)
        self.padding = [dp(10), dp(5)]
        self.size_hint_y = None
        self.height = dp(80)  # 增加整體高度

        self.word = word
        self.explanation = explanation

        # 單字列
        word_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.word_label = Label(
            text=word, 
            font_size=dp(24), 
            font_name='ChineseFont', 
            size_hint_x=1, 
            text_size=(dp(150), None), 
            halign='center',
            valign='middle'
        )
        word_layout.add_widget(self.word_label)
        self.add_widget(word_layout)

        # 解釋列和按鈕列的容器
        explanation_button_layout = BoxLayout(orientation='horizontal', size_hint_x=0.7)

        # 解釋列
        explanation_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)
        explanation_scroll = ScrollView(size_hint=(1, None), height=dp(70))  # 固定高度的滾動視圖
        self.explanation_label = Label(
            text=explanation, 
            font_size=dp(20), 
            font_name='ChineseFont', 
            size_hint_y=None,  # 允許標籤高度自適應
            height=dp(70),  # 初始高度
            text_size=(dp(200), None),  # 設置文本寬度，高度自適應
            halign='left',  # 左對齊
            valign='top'  # 頂部對齊
        )
        self.explanation_label.bind(texture_size=self._update_label_height)
        explanation_scroll.add_widget(self.explanation_label)
        explanation_layout.add_widget(explanation_scroll)
        explanation_button_layout.add_widget(explanation_layout)

        # 按鈕列
        button_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.2)
        buttons = BoxLayout(orientation='vertical', spacing=dp(5), size_hint=(None, None), size=(dp(70), dp(75)))
        
        edit_btn = Button(text='修改', size_hint=(None, None), size=(dp(70), dp(35)), font_name='ChineseFont', font_size=dp(16))
        edit_btn.bind(on_press=self.edit_word)
        buttons.add_widget(edit_btn)
        
        delete_btn = Button(text='刪除', size_hint=(None, None), size=(dp(70), dp(35)), font_name='ChineseFont', font_size=dp(16))
        delete_btn.bind(on_press=self.delete_word)
        buttons.add_widget(delete_btn)

        button_layout.add_widget(buttons)
        explanation_button_layout.add_widget(button_layout)

        self.add_widget(explanation_button_layout)

        self.delete_callback = delete_callback
        self.edit_callback = edit_callback

    def _update_label_height(self, instance, size):
        instance.height = max(size[1], dp(70))  # 確保最小高度為70dp
        # 檢查是否只有一行文字
        if size[1] <= dp(30):  # 假設單行文字的高度不超過30dp
            instance.halign = 'center'
            instance.valign = 'middle'
        else:
            instance.halign = 'left'
            instance.valign = 'top'

    def delete_word(self, instance):
        self.delete_callback(self)

    def edit_word(self, instance):
        popup = EditWordPopup(self.word, self.explanation, self.update_word)
        popup.open()

    def update_word(self, new_word, new_explanation):
        self.word = new_word
        self.explanation = new_explanation
        self.word_label.text = new_word
        self.explanation_label.text = new_explanation
        self.edit_callback(self, new_word, new_explanation)

class WordsList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=[0, dp(10), 0, 0])
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_word(self, japanese, chinese):
        word_item = WordItem(japanese, chinese, self.delete_word, self.edit_word)
        self.layout.add_widget(word_item)

    def delete_word(self, word_item):
        self.layout.remove_widget(word_item)

    def edit_word(self, word_item, new_japanese, new_chinese):
        pass

class AddWordPopup(Popup):
    def __init__(self, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (None, None)
        self.width = min(dp(700), Window.width * 0.8)  # 增加寬度
        self.height = min(dp(500), Window.height * 0.6)  # 增加高度
        
        content = BoxLayout(orientation='vertical', spacing=dp(20))
        
        title_bar = TitleBar("新增單字", self.dismiss)
        content.add_widget(title_bar)
        
        # 添加一個空白Widget來將輸入框往下移
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        main_content = BoxLayout(orientation='vertical', spacing=dp(20), padding=[dp(20), dp(20), dp(20), dp(20)])
        
        self.word_input = TextInput(
            multiline=True,
            font_name='ChineseFont', 
            font_size=dp(24), 
            size_hint=(1, None),  # 設置高度為固定值
            height=dp(150),  # 增加高度
            padding=[dp(10), dp(10), dp(10), dp(10)],
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
            hint_text='請先輸入日文單字，再做解釋',
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        main_content.add_widget(self.word_input)
        
        self.error_label = Label(text="", color=(1, 0, 0, 1), font_name='ChineseFont', font_size=dp(16))
        main_content.add_widget(self.error_label)
        
        content.add_widget(main_content)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(70), padding=[dp(20), 0, dp(20), dp(20)])
        
        confirm_btn = Button(
            text="確定", 
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            font_name='ChineseFont', 
            font_size=dp(18)
        )
        confirm_btn.bind(on_press=self.add_word)
        
        cancel_btn = Button(
            text="取消", 
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            font_name='ChineseFont', 
            font_size=dp(18)
        )
        cancel_btn.bind(on_press=self.dismiss)
        
        button_layout.add_widget(Widget())
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(Widget())
        
        content.add_widget(button_layout)
        
        self.content = content
        self.add_callback = add_callback

    def add_word(self, instance):
        word = self.word_input.text.strip()
        if self.validate_input(word):
            japanese, explanation = self.split_input(word)
            self.add_callback(japanese, explanation)
            self.dismiss()
        else:
            self.error_label.text = "請先打日文單字"

    def validate_input(self, text):
        if not text:
            return False
        first_char = text[0]
        return self.is_japanese_char(first_char)

    def is_japanese_char(self, char):
        # 檢查單個字符是否為日文（平假名、片假名或漢字）
        return '\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9fff'

    def split_input(self, text):
        # 使用正則表達式分割日文和非日文部分
        japanese_pattern = r'^[\u3040-\u30ff\u4e00-\u9fff]+'
        match = re.match(japanese_pattern, text)
        if match:
            japanese = match.group()
            explanation = text[len(japanese):].strip()
        else:
            japanese = ""
            explanation = text
        return japanese, explanation

class WordsListPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header.add_widget(Label(text="單字", font_name='ChineseFont', font_size=dp(28), size_hint_x=0.4))
        header.add_widget(Label(text="解釋", font_name='ChineseFont', font_size=dp(28), size_hint_x=0.4))
        header.add_widget(Widget(size_hint_x=0.2))  # 為了對齊按鈕
        content.add_widget(header)
        
        self.words_list = WordsList()
        content.add_widget(self.words_list)
        
        add_btn = Button(text="新增單字", size_hint=(None, None), size=(dp(200), dp(60)), pos_hint={'center_x': 0.5}, font_name='ChineseFont', font_size=dp(24))
        add_btn.bind(on_press=self.show_add_popup)
        content.add_widget(add_btn)
        
        self.content = content

    def show_add_popup(self, instance):
        popup = AddWordPopup(add_callback=self.words_list.add_word)
        popup.open()