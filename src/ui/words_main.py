from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout

from components import Pagination, SearchBar, AddButton, HeaderLabel
from functions.words_manager import WordManager
from ui.word_popup import WordPopup


class WordsMain(Popup):
    """主要單字列表視窗：包含搜索、新增、列表顯示和分頁功能"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 設置彈窗基本屬性
        self.title = ""  # 無標題
        self.separator_height = 0  # 無分隔線
        self.size_hint = (0.9, 0.9)  # 佔屏幕90%寬度和高度

        # 創建主佈局容器
        content = BoxLayout(orientation="vertical", spacing=dp(5))

        # 構建界面元素
        content.add_widget(self._create_function_bar())  # 功能欄：搜索框和新增按鈕
        content.add_widget(self._create_header())  # 標題欄：單字和解釋的標題

        # 添加單字列表管理器
        self.words_list = WordManager()
        content.add_widget(self.words_list)

        # 添加分頁控制器
        self.pagination = Pagination(on_page_change=self._handle_page_change)
        content.add_widget(self.pagination)

        self.content = content
        self.update_pagination()  # 初始化分頁狀態

    def _create_function_bar(self):
        """創建功能欄：包含搜索框和新增按鈕"""
        function_bar = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), dp(5), dp(10), dp(5)],  # 左上右下內邊距
        )

        # 添加搜索欄
        self.search_bar = SearchBar(search_callback=self._on_search_text)
        function_bar.add_widget(self.search_bar)

        # 創建新增按鈕容器（用於居中對齊）
        add_button_container = AnchorLayout(
            anchor_x="center", anchor_y="center", size_hint_x=None, width=dp(40)
        )

        # 添加新增按鈕
        add_button = AddButton(callback=self.show_add_popup)
        add_button_container.add_widget(add_button)
        function_bar.add_widget(add_button_container)

        return function_bar

    def _create_header(self):
        """創建標題欄：顯示'單字'和'解釋'的標題"""
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))

        # 單字列標題（左側）
        word_header = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=0.5,  # 佔用較少寬度
            padding=[0, 0, dp(5), 0],  # 右側留出間距
        )
        word_header.add_widget(HeaderLabel(text="單字"))
        header.add_widget(word_header)

        # 解釋列標題（右側）
        explanation_header = AnchorLayout(
            anchor_x="center", anchor_y="center", size_hint_x=1.5  # 佔用較多寬度
        )
        explanation_header.add_widget(HeaderLabel(text="解釋"))
        header.add_widget(explanation_header)

        return header

    def _on_search_text(self, value):
        """處理搜索文本變化：更新列表顯示和分頁"""
        self.words_list.search_words(value)
        self.update_pagination()

    def show_add_popup(self, instance):
        """顯示新增單字彈窗"""
        popup = WordPopup(
            callback=self.words_list.add_word, update_view_callback=self.update_view
        )
        popup.open()

    def update_pagination(self):
        """更新分頁狀態：同步當前頁碼和總頁數"""
        self.pagination.update_state(
            self.words_list.current_page, self.words_list.total_pages
        )

    def _handle_page_change(self, new_page):
        """處理頁碼變化：更新列表顯示"""
        self.words_list.current_page = new_page
        self.update_view()

    def update_view(self):
        """更新整個視圖：包括列表顯示和分頁狀態"""
        self.words_list.update_view()
        self.update_pagination()
