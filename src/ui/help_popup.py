# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp

class HelpPopup(Popup):
    """幫助文檔彈窗：顯示應用程序的使用說明和學習建議"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 設置彈窗基本屬性
        self.title = ""                # 無標題
        self.separator_height = 0       # 無分隔線
        self.size_hint = (0.9, 0.8)    # 佔屏幕90%寬度和80%高度
        
        # 創建主佈局，設置垂直方向的間距和內邊距
        main_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(5),             # 元素間距
            padding=[dp(20), dp(10)]   # 左右20dp，上下10dp的內邊距
        )
        
        # 添加標題標籤
        title_label = Label(
            text="使用說明",
            font_name="ChineseFont",    
            font_size='24sp',           
            size_hint_y=None,           # 不自動調整高度
            height=dp(30),              # 固定高度30dp
            halign='center',            # 水平居中
            pos_hint={'top': 1}         # 頂部對齊
        )
        main_layout.add_widget(title_label)
        
        # 創建可滾動的內容區域
        scroll = ScrollView(
            size_hint=(1, 1),           # 填充父容器
            do_scroll_x=False           # 禁用水平滾動
        )
        
        # 創建內容網格佈局
        content_layout = GridLayout(
            cols=1,                     # 單列佈局
            spacing=dp(10),             # 元素間距10dp
            size_hint_y=None,           # 高度根據內容自動調整
            padding=[dp(20), dp(0)]     # 左右20dp內邊距
        )
        # 綁定最小高度，確保可以正確滾動
        content_layout.bind(
            minimum_height=content_layout.setter('height')
        )
        
        # 添加五十音學習部分的內容
        content_layout.add_widget(self._create_section_title("五十音學習"))
        content_layout.add_widget(self._create_bullet_point("點擊音節按鈕播放發音"))
        content_layout.add_widget(self._create_bullet_point("點擊「一首歌記住五十音」學習五十音歌曲"))
        
        # 添加單字學習部分的內容
        content_layout.add_widget(self._create_section_title("單字學習"))
        content_layout.add_widget(self._create_bullet_point("自行加入、修改、刪除自己的筆記單字"))
        content_layout.add_widget(self._create_bullet_point("搜索時，請用日文搜尋"))
        
        # 添加學習建議部分的內容
        content_layout.add_widget(self._create_section_title("學習建議"))
        content_layout.add_widget(self._create_bullet_point("先學習五十音，通過歌曲加深印象"))
        content_layout.add_widget(self._create_bullet_point("常忘單字，加入到筆記"))
        
        # 組裝界面
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        self.content = main_layout
    
    def _create_section_title(self, text):
        """
        創建段落標題標籤
        Args:
            text: 標題文本
        Returns:
            Label: 配置好的標題標籤
        """
        label = Label(
            text=text,
            font_name="ChineseFont",    
            font_size='22sp',           
            size_hint_y=None,           # 不自動調整高度
            height=dp(40),              # 固定高度40dp
            halign='left'               # 左對齊
        )
        # 綁定寬度以實現文本自動換行
        label.bind(width=lambda *x: setattr(label, 'text_size', (label.width, None)))
        return label
    
    def _create_bullet_point(self, text):
        """
        創建項目符號列表項標籤
        Args:
            text: 列表項文本
        Returns:
            Label: 配置好的列表項標籤
        """
        label = Label(
            text=f"• {text}",           # 添加項目符號
            font_name="ChineseFont",    
            font_size='20sp',           
            size_hint_y=None,           # 不自動調整高度
            height=dp(30),              # 固定高度30dp
            halign='left'               # 左對齊
        )
        # 綁定寬度以實現文本自動換行
        label.bind(width=lambda *x: setattr(label, 'text_size', (label.width, None)))
        return label