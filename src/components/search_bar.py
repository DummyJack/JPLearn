from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

class SearchIconButton(ButtonBehavior, Image):
    """可點擊的搜索圖標：將圖片轉換為可點擊的按鈕"""
    pass

class SearchBar(BoxLayout):
    """搜索欄：包含搜索圖標和輸入框的組合控件"""
    def __init__(self, search_callback=None, **kwargs):
        super().__init__(**kwargs)
        # 基本佈局設置
        self.orientation = "horizontal"      # 水平佈局
        self.size_hint_y = None             # 不自動調整高度
        self.height = dp(50)                # 固定高度
        self.padding = [dp(10), dp(10), dp(10), dp(5)]  # 內邊距 [左, 上, 右, 下]
        self.spacing = dp(10)               # 元素間距
        self.search_callback = search_callback  # 搜索回調函數

        # 創建搜索框容器：包含圖標和輸入框
        search_container = BoxLayout(
            orientation="horizontal",
            size_hint_x=0.85  # 佔父容器85%寬度
        )

        # 設置搜索框背景
        with search_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # 淺灰色背景
            self.bg = RoundedRectangle(
                pos=search_container.pos,
                size=search_container.size,
                radius=[5]  # 圓角效果
            )
        # 綁定位置和大小變化事件
        search_container.bind(pos=self._update_bg, size=self._update_bg)

        # 創建搜索圖標區域
        icon_layout = AnchorLayout(
            size_hint=(None, 1),  # 固定寬度，高度填充
            width=dp(40),         # 圖標區域寬度
            padding=[dp(10), dp(10)]  # 內邊距，使圖標居中
        )
        # 創建可點擊的搜索圖標
        self.search_icon = SearchIconButton(
            source='resources/icons/search_icon.png',
            size_hint=(None, None),
            size=(dp(20), dp(20)),  # 圖標大小
            on_press=self._on_search_press  # 點擊事件
        )
        icon_layout.add_widget(self.search_icon)
        search_container.add_widget(icon_layout)

        # 創建搜索輸入框
        self.search_input = TextInput(
            multiline=False,          # 單行輸入
            hint_text="搜索單字...",   # 提示文字
            font_name="ChineseFont",  # 中文字體
            font_size=dp(18),         # 字體大小
            background_color=(0, 0, 0, 0),  # 透明背景
            padding=[0, dp(5), dp(10), dp(5)],  # 文字內邊距
            cursor_color=(0, 0, 0, 1),      # 黑色光標
            foreground_color=(0, 0, 0, 1),  # 黑色文字
            hint_text_color=(0.5, 0.5, 0.5, 1),  # 灰色提示文字
            size_hint_y=None,
            height=dp(37),            # 輸入框高度
            halign='left',            # 文字左對齊
        )

        # 綁定輸入框事件
        self.search_input.bind(text=self._on_text_change)      # 文字變化時觸發搜索
        self.search_input.bind(size=self._maintain_text_pos)   # 保持文字位置固定

        search_container.add_widget(self.search_input)
        self.add_widget(search_container)

    def _update_bg(self, instance, value):
        """更新搜索框背景的位置和大小"""
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _on_search_press(self, instance):
        """搜索圖標點擊事件：執行搜索回調"""
        if self.search_callback:
            self.search_callback(self.search_input.text)

    def _maintain_text_pos(self, instance, value):
        """保持輸入框文字位置：確保文字位置在大小變化時保持固定"""
        instance.padding = [0, dp(5), dp(10), dp(5)]

    def _on_text_change(self, instance, value):
        """輸入框文字變化事件：即時搜索"""
        if self.search_callback:
            self.search_callback(value)
