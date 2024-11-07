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
        """
        初始化單字項
        Args:
            word: 日語單字
            explanation: 單字解釋
            delete_callback: 刪除回調函數
            edit_callback: 編輯回調函數
            word_id: 單字ID
        """
        super().__init__(**kwargs)
        self.orientation = "horizontal"  # 水平佈局
        self.spacing = dp(5)            # 元素間距
        self.padding = [dp(10), dp(5)]  # 內邊距 [左右, 上下]
        self.size_hint_y = None         # 固定高度
        self.height = dp(80)            # 設置高度為80dp

        # 保存單字相關信息
        self.word = word
        self.explanation = explanation
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.word_id = word_id

        # 創建UI組件
        self._create_word_section()          # 創建單字顯示區域
        self._create_explanation_section()    # 創建解釋和按鈕區域

    def _create_word_section(self):
        """創建單字顯示區域：左側顯示日語單字"""
        word_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=0.3,  # 佔總寬度的30%
            padding=[dp(-20), 0, dp(20), 0]  # 調整內邊距使單字位置居中
        )
        self.word_label = WordLabel(text=str(self.word))
        word_anchor.add_widget(self.word_label)
        self.add_widget(word_anchor)

    def _create_explanation_section(self):
        """創建解釋和按鈕區域：右側顯示解釋文本和操作按鈕"""
        explanation_button_layout = BoxLayout(
            orientation="horizontal", 
            size_hint_x=0.7,  # 佔總寬度的70%
            padding=[dp(60), 0, 0, 0]  # 左側添加間距
        )

        # 創建解釋文本區域
        explanation_layout = self._create_explanation_layout()
        explanation_button_layout.add_widget(explanation_layout)

        # 創建按鈕區域
        button_container = self._create_button_container()
        explanation_button_layout.add_widget(button_container)

        self.add_widget(explanation_button_layout)

    def _create_explanation_layout(self):
        """創建解釋文本區域：可滾動的解釋文本"""
        explanation_layout = BoxLayout(
            orientation="vertical", 
            size_hint_x=0.8  # 佔解釋區域的80%寬度
        )
        # 創建滾動視圖，使長文本可以滾動顯示
        explanation_scroll = ScrollView(size_hint=(1, None), height=dp(70))
        self.explanation_label = ExplanationLabel(text=str(self.explanation))
        explanation_scroll.add_widget(self.explanation_label)
        explanation_layout.add_widget(explanation_scroll)
        return explanation_layout

    def _create_button_container(self):
        """創建按鈕容器：包含編輯和刪除按鈕"""
        button_container = BoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            width=dp(100),  # 固定按鈕區域寬度
            spacing=dp(5)   # 按鈕間距
        )

        # 添加編輯和刪除按鈕
        edit_button = EditButton(callback=self.edit_word)
        delete_button = DeleteButton(callback=self.delete_word)

        button_container.add_widget(edit_button)
        button_container.add_widget(delete_button)

        return button_container

    def delete_word(self, instance):
        """刪除單字：調用刪除回調函數"""
        self.delete_callback(self)

    def edit_word(self, instance):
        """編輯單字：打開編輯彈窗"""
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
        """
        更新單字內容
        Args:
            new_word: 新的日語單字
            new_explanation: 新的解釋文本
        """
        self.word = new_word
        self.explanation = new_explanation
        self.word_label.text = str(new_word)
        self.explanation_label.text = str(new_explanation)
        self.edit_callback(self, new_word, new_explanation)