# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

class Pagination(BoxLayout):
    """分頁控制組件：用於實現列表的分頁導航"""
    
    def __init__(self, on_page_change=None, **kwargs):
        super().__init__(**kwargs)
        # 基本佈局設置
        self.orientation = "horizontal"      # 水平佈局
        self.size_hint_y = None             # 不自動調整高度
        self.height = dp(50)                # 固定高度為50dp
        self.spacing = dp(5)                # 元素間距為5dp
        self.padding = [dp(200), 0, dp(200), 0]  # 左右各留出200dp的內邊距
        
        # 分頁相關的狀態
        self.current_page = 1               # 當前頁碼
        self.total_pages = 1                # 總頁數
        self.on_page_change = on_page_change  # 頁碼變化時的回調函數
        
        self._init_ui()                     # 初始化UI組件
        
    def _init_ui(self):
        """初始化UI組件：創建上一頁按鈕、頁碼標籤和下一頁按鈕"""
        # 創建上一頁按鈕
        self.prev_btn = Button(
            text="上一頁",
            size_hint_x=0.5,                # 佔用水平空間的50%
            font_name="ChineseFont",        # 使用中文字體
            disabled=True                   # 初始時禁用（因為在第一頁）
        )
        self.prev_btn.bind(on_press=self._on_prev_page)  # 綁定點擊事件
        
        # 創建頁碼標籤
        self.page_label = Label(
            text="1/1",                     # 初始顯示"1/1"
            size_hint_x=0.5,                # 佔用水平空間的50%
            font_name="ChineseFont",        # 使用中文字體
            font_size=dp(20)                # 字體大小為20dp
        )
        
        # 創建下一頁按鈕
        self.next_btn = Button(
            text="下一頁",
            size_hint_x=0.5,                # 佔用水平空間的50%
            font_name="ChineseFont",        # 使用中文字體
            disabled=True                   # 初始時禁用（因為只有一頁）
        )
        self.next_btn.bind(on_press=self._on_next_page)  # 綁定點擊事件
        
        # 將所有組件添加到佈局中
        self.add_widget(self.prev_btn)
        self.add_widget(self.page_label)
        self.add_widget(self.next_btn)
    
    def update_state(self, current_page, total_pages):
        """
        更新分頁狀態
        Args:
            current_page: 當前頁碼
            total_pages: 總頁數
        """
        self.current_page = current_page
        self.total_pages = total_pages
        
        # 更新頁碼顯示文本
        self.page_label.text = f"{current_page}/{total_pages}"
        
        # 根據當前頁碼更新按鈕狀態
        self.prev_btn.disabled = current_page == 1  # 在第一頁時禁用"上一頁"
        self.next_btn.disabled = current_page == total_pages  # 在最後一頁時禁用"下一頁"
    
    def _on_prev_page(self, instance):
        """處理上一頁按鈕點擊：頁碼減1並觸發回調"""
        if self.current_page > 1:
            self.current_page -= 1
            if self.on_page_change:
                self.on_page_change(self.current_page)
    
    def _on_next_page(self, instance):
        """處理下一頁按鈕點擊：頁碼加1並觸發回調"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            if self.on_page_change:
                self.on_page_change(self.current_page) 