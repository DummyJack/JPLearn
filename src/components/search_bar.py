from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

class SearchIconButton(ButtonBehavior, Image):
    """可點擊的搜索圖標"""
    pass

class SearchBar(BoxLayout):
    def __init__(self, search_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        self.spacing = dp(10)
        self.search_callback = search_callback

        # 搜索框容器
        search_container = BoxLayout(
            orientation="horizontal",
            size_hint_x=0.85
        )

        # 搜索框背景
        with search_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # 淺灰色背景
            self.bg = RoundedRectangle(
                pos=search_container.pos,
                size=search_container.size,
                radius=[5]
            )
        search_container.bind(pos=self._update_bg, size=self._update_bg)

        # 搜索圖標
        icon_layout = AnchorLayout(
            size_hint=(None, 1),
            width=dp(40),
            padding=[dp(10), dp(10)]
        )
        self.search_icon = SearchIconButton(
            source='resources/icons/search_icon.png',
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            on_press=self._on_search_press
        )
        icon_layout.add_widget(self.search_icon)
        search_container.add_widget(icon_layout)

        # 搜索輸入框
        self.search_input = TextInput(
            multiline=False,
            hint_text="搜索單字...",
            font_name="ChineseFont",
            font_size=dp(18),
            background_color=(0, 0, 0, 0),  # 透明背景
            padding=[0, dp(14), dp(10), dp(10)],
            cursor_color=(0, 0, 0, 1),
            foreground_color=(0, 0, 0, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,  # 禁用垂直大小提示
            height=dp(50),    # 固定高度
            halign='left',    # 水平左對齊
        )

        # 綁定大小變化事件
        self.search_input.bind(size=self._maintain_text_pos)

        search_container.add_widget(self.search_input)

        self.add_widget(search_container)

    def _update_bg(self, instance, value):
        """更新背景位置和大小"""
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _on_search_press(self, instance):
        """當搜索圖標被點擊時執行搜索"""
        if self.search_callback:
            self.search_callback(self.search_input.text)

    def _maintain_text_pos(self, instance, value):
        """保持文字位置固定"""
        instance.padding = [0, dp(14), dp(10), dp(10)]  # 重新設置padding確保位置不變
