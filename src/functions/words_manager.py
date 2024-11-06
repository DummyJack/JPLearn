# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from math import ceil

from database.mongodb import words_collection
from components.buttons import (
    ConfirmButton,
    CancelButton,
    EditButton, 
    DeleteButton
)
from components.labels import (
    ConfirmLabel,
    WordLabel,
    ExplanationLabel
)
from ui.word_popup import WordPopup

# UI 配置常量
UI_CONFIG = {
    "BUTTON_SIZE": dp(100),
    "BUTTON_HEIGHT": dp(50),
    "SPACING": dp(20),
    "PADDING": dp(20),
    "FONT_SIZE": dp(18),
    "TITLE_FONT_SIZE": dp(24)
}

class WordItem(BoxLayout):
    """單字列表項：顯示單個單字的詳細信息和操作按鈕"""
    def __init__(
        self, word, explanation, delete_callback, edit_callback, word_id, **kwargs
    ):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = dp(5)
        self.padding = [dp(10), dp(5)]
        self.size_hint_y = None
        self.height = dp(80)

        self.word = word
        self.explanation = explanation
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.word_id = word_id

        self._create_word_section()
        self._create_explanation_section()

    def _create_word_section(self):
        """創建單字部分"""
        word_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=0.3,
            padding=[dp(-20), 0, dp(20), 0]
        )
        self.word_label = WordLabel(text=str(self.word))
        word_anchor.add_widget(self.word_label)
        self.add_widget(word_anchor)

    def _create_explanation_section(self):
        """創建解釋和按鈕部分"""
        explanation_button_layout = BoxLayout(
            orientation="horizontal", 
            size_hint_x=0.7,
            padding=[dp(60), 0, 0, 0]
        )

        explanation_layout = self._create_explanation_layout()
        explanation_button_layout.add_widget(explanation_layout)

        button_container = self._create_button_container()
        explanation_button_layout.add_widget(button_container)

        self.add_widget(explanation_button_layout)

    def _create_explanation_layout(self):
        """創建解釋部分的佈局"""
        explanation_layout = BoxLayout(orientation="vertical", size_hint_x=0.8)
        explanation_scroll = ScrollView(size_hint=(1, None), height=dp(70))
        self.explanation_label = ExplanationLabel(text=str(self.explanation))
        explanation_scroll.add_widget(self.explanation_label)
        explanation_layout.add_widget(explanation_scroll)
        return explanation_layout

    def _create_button_container(self):
        """創建按鈕容器"""
        button_container = BoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            width=dp(100),
            spacing=dp(5)
        )

        edit_button = EditButton(callback=self.edit_word)
        delete_button = DeleteButton(callback=self.delete_word)

        button_container.add_widget(edit_button)
        button_container.add_widget(delete_button)

        return button_container

    def delete_word(self, instance):
        """刪除單字"""
        self.delete_callback(self)

    def edit_word(self, instance):
        """編輯單字"""
        popup = WordPopup(
            mode="edit",
            japanese=str(self.word),
            explanation=str(self.explanation),
            word_id=self.word_id,
            callback=self.update_word,
            update_view_callback=lambda: None
        )
        popup.open()

    def update_word(self, new_word, new_explanation):
        """更新單字內容"""
        self.word = new_word
        self.explanation = new_explanation
        self.word_label.text = str(new_word)
        self.explanation_label.text = str(new_explanation)
        self.edit_callback(self, new_word, new_explanation)

class WordManager(ScrollView):
    """單字管理器：負責單字的增刪改查和分頁顯示"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None,
            padding=[0, dp(5), 0, 0],
        )
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.add_widget(self.layout)
        self.current_page = 1
        self.items_per_page = 5
        self.total_pages = 1
        self.search_mode = False
        self.search_results = []
        self.last_search_term = ""
        self.load_words_from_db()

    def search_words(self, search_term):
        self.last_search_term = search_term
        if not search_term:
            self.search_mode = False
            self.load_words_from_db()
            return

        self.search_mode = True
        self.search_results = list(
            words_collection.find(
                {"japanese": {"$regex": search_term, "$options": "i"}}
            )
        )
        self.total_pages = max(1, ceil(len(self.search_results) / self.items_per_page))
        self.current_page = 1
        self.update_view()

    def load_words_from_db(self):
        if words_collection is None:
            print("無法連接到數據庫，無法加載單詞")
            return
        self.layout.clear_widgets()

        if self.search_mode:
            total_words = len(self.search_results)
            words = self.search_results[
                (self.current_page - 1)
                * self.items_per_page : self.current_page
                * self.items_per_page
            ]
        else:
            total_words = words_collection.count_documents({})
            skip = (self.current_page - 1) * self.items_per_page
            # Update the sort syntax to use a list of tuples
            words = list(
                words_collection.find()
                .sort([("_id", -1)])
                .skip(skip)
                .limit(self.items_per_page)
            )

        self.total_pages = max(1, ceil(total_words / self.items_per_page))

        for word in words:
            self.add_word(word["japanese"], word["explanation"], word["_id"])

    def add_word(self, japanese, explanation, word_id=None):
        word_item = WordItem(
            japanese,
            explanation,
            self.show_delete_confirmation,
            self.edit_word,
            word_id,
        )
        if self.current_page == 1:
            self.layout.add_widget(word_item, index=0)
        else:
            self.layout.add_widget(word_item)

        # 如果當前頁面已滿,移除最後一個單詞
        if len(self.layout.children) > self.items_per_page:
            self.layout.remove_widget(self.layout.children[-1])

    def show_delete_confirmation(self, word_item):
        content = BoxLayout(
            orientation="vertical", 
            spacing=dp(40), 
            padding=dp(20)
        )
        content.add_widget(ConfirmLabel(text="是否刪除單字？"))

        buttons = BoxLayout(
            orientation="horizontal", 
            spacing=dp(20), 
            size_hint_y=None, 
            height=dp(50)
        )
        
        confirm_btn = ConfirmButton(
            text="確定",
            on_press=lambda x: self.delete_word(word_item, popup)
        )
        
        cancel_btn = CancelButton(
            on_press=lambda x: popup.dismiss()
        )
        
        buttons.add_widget(Widget(size_hint_x=0.5))
        buttons.add_widget(confirm_btn)
        buttons.add_widget(cancel_btn)
        buttons.add_widget(Widget(size_hint_x=0.5))
        content.add_widget(buttons)

        popup = Popup(
            content=content, 
            size_hint=(0.6, 0.3), 
            title="", 
            separator_height=0
        )

        popup.open()

    def delete_word(self, word_item, popup):
        words_collection.delete_one({"_id": word_item.word_id})
        self.layout.remove_widget(word_item)

        # 更新總單字數和頁數
        total_words = words_collection.count_documents({})
        new_total_pages = max(1, ceil(total_words / self.items_per_page))

        # 檢查是否需要調整當前頁數
        if self.current_page > new_total_pages:
            self.current_page = new_total_pages

        self.update_view()
        popup.dismiss()

    def edit_word(self, word_item, new_japanese, new_explanation):
        words_collection.update_one(
            {"_id": word_item.word_id},
            {"$set": {"japanese": new_japanese, "explanation": new_explanation}},
        )

    def update_view(self):
        if self.search_mode:
            total_words = len(self.search_results)
        else:
            total_words = words_collection.count_documents({})

        new_total_pages = max(1, ceil(total_words / self.items_per_page))

        self.total_pages = new_total_pages
        self.current_page = min(self.current_page, self.total_pages)

        self.load_words_from_db()
        if hasattr(self, "parent") and hasattr(self.parent, "update_pagination"):
            self.parent.update_pagination()