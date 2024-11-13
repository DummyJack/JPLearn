from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from components import ConfirmButton, CancelButton

class ConfirmPopup(Popup):
    """確認彈窗：用於顯示確認對話框"""
    def __init__(self, title_text="請確認以下內容", content_text="", on_confirm=None, **kwargs):
        super().__init__(**kwargs)
        
        # 設置彈窗基本屬性
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.4, 0.38)
        self.background_color = (0.98, 0.98, 0.98, 1)
        self.auto_dismiss = False
        
        # 創建主佈局
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(25), dp(10), dp(25), dp(20)]
        )
        
        # 創建標題容器
        title_container = self._create_title_container(title_text)
        content.add_widget(title_container)
        
        # 添加內容
        content_label = Label(
            text=content_text,
            font_name="ChineseFont",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(80)
        )
        content.add_widget(content_label)
        
        # 添加按鈕
        button_layout = self._create_button_layout(on_confirm)
        content.add_widget(button_layout)
        
        self.content = content

    def _create_title_container(self, title_text):
        """創建標題容器"""
        title_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(60),
            padding=[0, dp(10)]
        )
        
        title_label = Label(
            text=title_text,
            font_name="ChineseFont",
            font_size=dp(22),
            size_hint_y=None,
            height=dp(0),
            color=(0.8, 0.8, 0.8, 1),
            bold=True
        )
        title_container.add_widget(title_label)
        
        separator = self._create_separator()
        title_container.add_widget(separator)
        
        return title_container

    def _create_separator(self):
        """創建分隔線"""
        separator = Widget(
            size_hint_y=None,
            height=dp(2)
        )
        with separator.canvas:
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(pos=separator.pos, size=separator.size)
        return separator

    def _create_button_layout(self, on_confirm):
        """創建按鈕佈局"""
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(35),
            pos_hint={'center_x': 0.7}
        )
        
        # 使用 ConfirmButton 組件
        confirm_btn = ConfirmButton(
            text="確認",
            size=(dp(70), dp(32)),
            on_press=lambda x: self._handle_confirm(on_confirm)
        )
        
        # 使用 CancelButton 組件
        cancel_btn = CancelButton(
            size=(dp(70), dp(32)),
            on_press=self.dismiss
        )
        
        button_container = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint_x=None,
            width=dp(155)
        )
        button_container.add_widget(confirm_btn)
        button_container.add_widget(cancel_btn)
        
        button_layout.add_widget(button_container)
        
        return button_layout

    def _handle_confirm(self, on_confirm):
        """處理確認按鈕的點擊事件"""
        if on_confirm:
            on_confirm()
        self.dismiss()
