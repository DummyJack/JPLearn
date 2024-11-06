# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

class Pagination(BoxLayout):
    """分頁控制組件"""
    
    def __init__(self, on_page_change=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(50)
        
        self.current_page = 1
        self.total_pages = 1
        self.on_page_change = on_page_change
        
        self._init_ui()
        
    def _init_ui(self):
        """初始化 UI 組件"""
        # 上一頁按鈕
        self.prev_btn = Button(
            text="上一頁",
            size_hint_x=0.2,
            font_name="ChineseFont",
            disabled=True
        )
        self.prev_btn.bind(on_press=self._on_prev_page)
        
        # 頁碼標籤
        self.page_label = Label(
            text="1/1",
            size_hint_x=0.6,
            font_name="ChineseFont"
        )
        
        # 下一頁按鈕
        self.next_btn = Button(
            text="下一頁",
            size_hint_x=0.2,
            font_name="ChineseFont",
            disabled=True
        )
        self.next_btn.bind(on_press=self._on_next_page)
        
        # 添加組件
        self.add_widget(self.prev_btn)
        self.add_widget(self.page_label)
        self.add_widget(self.next_btn)
    
    def update_state(self, current_page, total_pages):
        """更新分頁狀態"""
        self.current_page = current_page
        self.total_pages = total_pages
        
        # 更新頁碼顯示
        self.page_label.text = f"{current_page}/{total_pages}"
        
        # 更新按鈕狀態
        self.prev_btn.disabled = current_page == 1
        self.next_btn.disabled = current_page == total_pages
    
    def _on_prev_page(self, instance):
        """處理上一頁點擊"""
        if self.current_page > 1:
            self.current_page -= 1
            if self.on_page_change:
                self.on_page_change(self.current_page)
    
    def _on_next_page(self, instance):
        """處理下一頁點擊"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            if self.on_page_change:
                self.on_page_change(self.current_page) 