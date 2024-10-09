# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget 
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
import re

class JapaneseTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring
        # 只允許日文字符（平假名、片假名、漢字）
        s = ''.join([c for c in s if '\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff'])
        return super().insert_text(s, from_undo=from_undo)

class EditWordPopup(Popup):
    def __init__(self, japanese, explanation, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.6)

        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        input_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(150))

        # 日文輸入框
        self.japanese_input = JapaneseTextInput(
            text=japanese,
            multiline=True,
            hint_text='請輸入單字',
            font_name='ChineseFont',
            font_size=dp(18),
            size_hint_x=0.3,
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        self.japanese_input.bind(text=self.on_japanese_input)
        input_layout.add_widget(self.japanese_input)

        # 解釋輸入框
        self.explanation_input = TextInput(
            text=explanation,
            multiline=True,
            hint_text='請輸入解釋',
            font_name='ChineseFont',
            font_size=dp(18),
            size_hint_x=0.7,
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        input_layout.add_widget(self.explanation_input)

        layout.add_widget(input_layout)

        # 錯誤訊息標籤
        self.error_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_name='ChineseFont',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.error_label)

        # 按鈕佈局
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(40))

        edit_button = Button(
            text='修改',
            on_press=self.edit_word,
            font_name='ChineseFont',
            font_size=dp(16),
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )

        cancel_button = Button(
            text='取消',
            on_press=self.dismiss,
            font_name='ChineseFont',
            font_size=dp(16),
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )

        button_layout.add_widget(Widget())
        button_layout.add_widget(edit_button)
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(Widget())

        layout.add_widget(button_layout)

        self.content = layout
        self.edit_callback = edit_callback

    def on_japanese_input(self, instance, value):
        if not all(self.is_japanese_char(c) for c in value if c.strip()):
            self.error_label.text = "請只輸入日文字符"
        else:
            self.error_label.text = ""

    def is_japanese_char(self, char):
        return '\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9fff'

    def edit_word(self, instance):
        japanese = self.japanese_input.text.strip()
        explanation = self.explanation_input.text.strip()
        
        if not japanese:
            self.error_label.text = "必須輸入單字"
            return
        
        if not all(self.is_japanese_char(c) for c in japanese if c.strip()):
            self.error_label.text = "請只輸入日文字符"
            return

        # 解釋可以為空
        explanation = explanation if explanation else ""

        self.edit_callback(japanese, explanation)
        self.dismiss()

class WordItem(BoxLayout):
    def __init__(self, word, explanation, delete_callback, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(10)
        self.padding = [dp(10), dp(5)]
        self.size_hint_y = None
        self.height = dp(80)

        self.word = word
        self.explanation = explanation

        # 單字列
        self.word_label = Label(
            text=word, 
            font_size=dp(24), 
            font_name='ChineseFont', 
            size_hint=(None, None),
            size=(dp(120), dp(70)),
            text_size=(dp(120), dp(70)),
            halign='center',
            valign='middle',
        )
        
        # 使用 AnchorLayout 來包裹 word_label，實現居中對齊，並添加右側內邊距
        word_anchor = AnchorLayout(
            anchor_x='center', 
            anchor_y='center', 
            size_hint_x=0.3,
            padding=[0, 0, dp(20), 0]  # 添加 20dp 的右側內邊距
        )
        word_anchor.add_widget(self.word_label)
        self.add_widget(word_anchor)

        # 解釋列和按鈕列的容器
        explanation_button_layout = BoxLayout(orientation='horizontal', size_hint_x=0.7)

        # 解釋列
        explanation_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)
        explanation_scroll = ScrollView(size_hint=(1, None), height=dp(70))
        self.explanation_label = Label(
            text=explanation, 
            font_size=dp(20), 
            font_name='ChineseFont', 
            size_hint_y=None,
            height=dp(70),
            text_size=(dp(200), None),
            halign='left',
            valign='middle'
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
            instance.valign = 'middle'
            instance.halign = 'center'  # 單行文字時居中對齊
        else:
            instance.valign = 'top'
            instance.halign = 'left'  # 多行文字時左對齊

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

    def add_word(self, japanese, explanation):
        word_item = WordItem(japanese, explanation, self.delete_word, self.edit_word)
        self.layout.add_widget(word_item)
        # 不需要額外的對齊設置，因為我們已經在 WordItem 中處理了對齊

    def delete_word(self, word_item):
        self.layout.remove_widget(word_item)

    def edit_word(self, word_item, new_japanese, new_explanation):
        pass

class AddWordPopup(Popup):
    def __init__(
        self, add_word_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.6)  # 增加高度以容納更高的輸入框

        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        input_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(150))  # 增加高度

        # 日文輸入框
        self.japanese_input = JapaneseTextInput(
            multiline=True,
            hint_text='請輸入單字',
            font_name='ChineseFont',
            font_size=dp(18),
            size_hint_x=0.3,
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        self.japanese_input.bind(text=self.on_japanese_input)
        input_layout.add_widget(self.japanese_input)

        # 解釋輸入框
        self.explanation_input = TextInput(
            multiline=True,
            hint_text='請輸入解釋',
            font_name='ChineseFont',
            font_size=dp(18),
            size_hint_x=0.7,
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        input_layout.add_widget(self.explanation_input)

        layout.add_widget(input_layout)

        # 錯誤訊息標籤
        self.error_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_name='ChineseFont',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.error_label)

        # 按鈕佈局
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(40))

        add_button = Button(
            text='新增',
            on_press=self.add_word,
            font_name='ChineseFont',
            font_size=dp(16),
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )

        cancel_button = Button(
            text='取消',
            on_press=self.dismiss,
            font_name='ChineseFont',
            font_size=dp(16),
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )

        button_layout.add_widget(Widget())  # 添加一個空白Widget來將按鈕置中
        button_layout.add_widget(add_button)
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(Widget())  # 添加一個空白Widget來將按鈕置中

        layout.add_widget(button_layout)

        self.content = layout
        self.add_word_callback = add_word_callback

    def on_japanese_input(self, instance, value):
        if not all(self.is_japanese_char(c) for c in value if c.strip()):
            self.error_label.text = "請只輸入日文字符"
        else:
            self.error_label.text = ""

    def is_japanese_char(self, char):
        return '\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9fff'

    def add_word(self, instance):
        japanese = self.japanese_input.text.strip()
        explanation = self.explanation_input.text.strip()
        
        if not japanese:
            self.error_label.text = "必須輸入單字"
            return
        
        if not all(self.is_japanese_char(c) for c in japanese if c.strip()):
            self.error_label.text = "請只輸入日文字符"
            return

        # 解釋可以為空
        explanation = explanation if explanation else ""

        self.add_word_callback(japanese, explanation)
        self.dismiss()

class WordsListPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        word_header = AnchorLayout(
            anchor_x='center', 
            anchor_y='center', 
            size_hint_x=0.3,
            padding=[0, 0, dp(20), 0]  # 添加 20dp 的右側內邊距
        )
        word_header.add_widget(Label(text="單字", font_name='ChineseFont', font_size=dp(28)))
        header.add_widget(word_header)
        header.add_widget(Label(text="解釋", font_name='ChineseFont', font_size=dp(28), size_hint_x=0.56))
        header.add_widget(Widget(size_hint_x=0.14))  # 為了對齊按鈕
        content.add_widget(header)
        
        self.words_list = WordsList()
        content.add_widget(self.words_list)
        
        add_btn = Button(text="新增單字", size_hint=(None, None), size=(dp(200), dp(60)), pos_hint={'center_x': 0.5}, font_name='ChineseFont', font_size=dp(24))
        add_btn.bind(on_press=self.show_add_popup)
        content.add_widget(add_btn)
        
        self.content = content

    def show_add_popup(self, instance):
        popup = AddWordPopup(add_word_callback=self.words_list.add_word)
        popup.open()