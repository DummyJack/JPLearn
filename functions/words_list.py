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
from kivy.uix.image import Image
import re
from pymongo import MongoClient
from bson import ObjectId
from math import ceil

# 建立 MongoDB 連接
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()  # 測試連接
    db = client['japanese_words']
    words_collection = db['words']
except Exception as e:
    print(f"無法連接到 MongoDB: {e}")
    words_collection = None

class JapaneseTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring
        # 只允許日文字符（平假名、片假名、漢字）
        s = ''.join([c for c in s if '\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff'])
        return super().insert_text(s, from_undo=from_undo)

class EditWordPopup(Popup):
    def __init__(self, japanese, explanation, edit_callback, word_id, **kwargs):
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
        self.word_id = word_id

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

        explanation = explanation if explanation else ""

        self.edit_callback(japanese, explanation)
        self.dismiss()

class WordItem(BoxLayout):
    def __init__(self, word, explanation, delete_callback, edit_callback, word_id, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.padding = [dp(10), dp(5)]
        self.size_hint_y = None
        self.height = dp(80)

        self.word = word
        self.explanation = explanation

        # 單字列
        word_anchor = AnchorLayout(
            anchor_x='center', 
            anchor_y='center', 
            size_hint_x=0.3,
            padding=[0, 0, dp(10), 0]
        )
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
        button_layout = BoxLayout(orientation='horizontal', size_hint_x=0.2, spacing=dp(5))
        
        edit_btn = Button(
            size_hint=(None, None), 
            size=(dp(30), dp(30)),  # 調整大小為30x30
            background_normal='icons/edit_icon.png',
            background_down='icons/edit_icon.png',
            border=(0,0,0,0)
        )
        edit_btn.bind(on_press=self.edit_word)
        
        delete_btn = Button(
            size_hint=(None, None), 
            size=(dp(30), dp(30)),  # 調整大小為30x30
            background_normal='icons/delete_icon.png',
            background_down='icons/delete_icon.png',
            border=(0,0,0,0)
        )
        delete_btn.bind(on_press=self.delete_word)

        # 使用 AnchorLayout 來使按鈕垂直居中
        button_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=None, width=dp(70))
        button_inner_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint=(None, None), size=(dp(65), dp(30)))
        button_inner_layout.add_widget(edit_btn)
        button_inner_layout.add_widget(delete_btn)
        button_anchor.add_widget(button_inner_layout)
        
        explanation_button_layout.add_widget(button_anchor)

        self.add_widget(explanation_button_layout)

        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.word_id = word_id

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
        popup = EditWordPopup(self.word, self.explanation, self.update_word, self.word_id)
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
        self.layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, padding=[0, dp(5), 0, 0])
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.current_page = 1
        self.items_per_page = 5
        self.total_pages = 1
        self.load_words_from_db()

    def load_words_from_db(self):
        if words_collection is None:
            print("無法連接到數據庫，無法加載單詞")
            return
        self.layout.clear_widgets()
        total_words = words_collection.count_documents({})
        self.total_pages = ceil(total_words / self.items_per_page)
        
        skip = (self.current_page - 1) * self.items_per_page
        words = words_collection.find().skip(skip).limit(self.items_per_page)
        
        for word in words:
            self.add_word(word['japanese'], word['explanation'], word['_id'])

    def add_word(self, japanese, explanation, word_id=None):
        word_item = WordItem(japanese, explanation, self.delete_word, self.edit_word, word_id)
        self.layout.add_widget(word_item)

    def delete_word(self, word_item):
        words_collection.delete_one({'_id': word_item.word_id})
        self.layout.remove_widget(word_item)
        self.update_view()

    def edit_word(self, word_item, new_japanese, new_explanation):
        words_collection.update_one(
            {'_id': word_item.word_id},
            {'$set': {'japanese': new_japanese, 'explanation': new_explanation}}
        )

    def update_view(self):
        self.load_words_from_db()

class AddWordPopup(Popup):
    def __init__(
        self, add_word_callback, update_view_callback, **kwargs):
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
        self.update_view_callback = update_view_callback

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

        explanation = explanation if explanation else ""

        # 插入新單字到資料庫
        result = words_collection.insert_one({'japanese': japanese, 'explanation': explanation})
        self.add_word_callback(japanese, explanation, result.inserted_id)
        self.dismiss()
        self.update_view_callback()  # 新增這行來更新視圖

class WordsListPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=dp(5))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        word_header = AnchorLayout(
            anchor_x='center', 
            anchor_y='center', 
            size_hint_x=0.3,
            padding=[0, 0, dp(20), 0]
        )
        word_header.add_widget(Label(text="單字", font_name='ChineseFont', font_size=dp(28)))
        header.add_widget(word_header)
        
        explanation_layout = BoxLayout(orientation='horizontal', size_hint_x=0.7)
        explanation_layout.add_widget(Label(text="解釋", font_name='ChineseFont', font_size=dp(28), size_hint_x=0.8))
        
        add_btn = Button(text="+", size_hint=(None, None), size=(dp(40), dp(40)), font_size=dp(24), pos_hint={'center_y': 0.5})
        add_btn.bind(on_press=self.show_add_popup)
        explanation_layout.add_widget(add_btn)
        
        header.add_widget(explanation_layout)
        content.add_widget(header)
        
        self.words_list = WordsList()
        content.add_widget(self.words_list)
        
        pagination = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        self.prev_btn = Button(text="上一頁", size_hint_x=0.2, font_name='ChineseFont')
        self.prev_btn.bind(on_press=self.prev_page)
        self.page_label = Label(text="1/1", size_hint_x=0.6, font_name='ChineseFont')
        self.next_btn = Button(text="下一頁", size_hint_x=0.2, font_name='ChineseFont')
        self.next_btn.bind(on_press=self.next_page)
        
        pagination.add_widget(self.prev_btn)
        pagination.add_widget(self.page_label)
        pagination.add_widget(self.next_btn)
        
        content.add_widget(pagination)
        
        self.content = content
        self.update_pagination()

    def show_add_popup(self, instance):
        popup = AddWordPopup(add_word_callback=self.words_list.add_word, update_view_callback=self.update_view)
        popup.open()

    def update_view(self):
        self.words_list.update_view()
        self.update_pagination()

    def update_pagination(self):
        self.page_label.text = f"{self.words_list.current_page}/{self.words_list.total_pages}"
        self.prev_btn.disabled = self.words_list.current_page == 1
        self.next_btn.disabled = self.words_list.current_page == self.words_list.total_pages

    def prev_page(self, instance):
        if self.words_list.current_page > 1:
            self.words_list.current_page -= 1
            self.update_view()

    def next_page(self, instance):
        if self.words_list.current_page < self.words_list.total_pages:
            self.words_list.current_page += 1
            self.update_view()