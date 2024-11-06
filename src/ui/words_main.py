from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout

from components import Pagination, SearchBar, AddButton, HeaderLabel
from functions.words_manager import WordManager
from ui.word_popup import WordPopup

class WordsMain(Popup):
    """主要單字列表視窗"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation="vertical", spacing=dp(5))
        
        # 添加功能欄
        content.add_widget(self._create_function_bar())
        
        # 添加標題欄
        content.add_widget(self._create_header())
        
        # 添加單字列表
        self.words_list = WordManager()
        content.add_widget(self.words_list)
        
        # 添加分頁控制
        self.pagination = Pagination(on_page_change=self._handle_page_change)
        content.add_widget(self.pagination)
        
        self.content = content
        self.update_pagination()

    def _create_function_bar(self):
        """創建功能欄（搜索框和新增按鈕）"""
        function_bar = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), dp(5), dp(10), dp(5)]
        )
        
        # 添加搜索欄
        self.search_bar = SearchBar(search_callback=self._on_search_text)
        function_bar.add_widget(self.search_bar)
        
        # 新增按鈕容器
        add_button_container = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_x=None,
            width=dp(40)
        )
        
        # 添加新增按鈕
        add_button = AddButton(callback=self.show_add_popup)
        add_button_container.add_widget(add_button)
        function_bar.add_widget(add_button_container)
        
        return function_bar
    
    def _create_header(self):
        """創建標題欄"""
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        
        # 單字標題
        word_header = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=0.5,
            padding=[0, 0, dp(5), 0]
        )
        word_header.add_widget(HeaderLabel(text="單字"))
        header.add_widget(word_header)
        
        # 解釋標題
        explanation_header = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=1.6
        )
        explanation_header.add_widget(HeaderLabel(text="解釋"))
        header.add_widget(explanation_header)
        
        return header
    
    def _on_search_text(self, value):
        """處理搜索文本變化"""
        self.words_list.search_words(value)
        self.update_pagination()
    
    def show_add_popup(self, instance):
        """顯示新增單字彈窗"""
        popup = WordPopup(
            callback=self.words_list.add_word,
            update_view_callback=self.update_view
        )
        popup.open()
    
    def update_pagination(self):
        """更新分頁狀態"""
        self.pagination.update_state(
            self.words_list.current_page,
            self.words_list.total_pages
        )
    
    def _handle_page_change(self, new_page):
        """處理頁碼變化"""
        self.words_list.current_page = new_page
        self.update_view()
    
    def update_view(self):
        """更新視圖"""
        self.words_list.update_view()
        self.update_pagination()
 