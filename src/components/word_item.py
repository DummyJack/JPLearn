# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

from components import EditButton, DeleteButton, WordLabel, ExplanationLabel
from ui.word_popup import WordPopup

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