from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from functions import FiftySoundsGrid

# 常量定義
COLORS = {
    "INITIAL": (0.5, 0.7, 1, 1),
}

POPUP_CONFIG = {
    "SIZE": (dp(800), dp(600)),
    "GRID_SIZE": (dp(720), dp(480)),
    "TITLE_HEIGHT": dp(50),
    "PADDING": (dp(20), dp(10), dp(40), dp(20))
}

class FiftySoundsMain(Popup):
    """五十音彈出窗口"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_popup()
        self._create_content()

    def _init_popup(self):
        """初始化彈出窗口設置"""
        self.title = ""
        self.separator_height = 0
        self.size_hint = (None, None)
        self.size = POPUP_CONFIG["SIZE"]
        self.background_color = COLORS["INITIAL"]

    def _create_content(self):
        """創建彈出窗口內容"""
        content = BoxLayout(orientation="vertical", spacing=dp(20))
        
        # 添加標題
        content.add_widget(self._create_title())
        
        # 添加五十音格子
        content.add_widget(self._create_grid())
        
        self.content = content

    def _create_title(self):
        """創建標題"""
        title_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=None,
            height=POPUP_CONFIG["TITLE_HEIGHT"]
        )
        
        title = Label(
            text="五十音",
            font_name="ChineseFont",
            font_size=dp(36),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(200), POPUP_CONFIG["TITLE_HEIGHT"])
        )
        
        title_layout.add_widget(title)
        return title_layout

    def _create_grid(self):
        """創建五十音格子容器"""
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        
        grid_container = BoxLayout(
            orientation="vertical",
            padding=POPUP_CONFIG["PADDING"],
            size_hint=(None, None),
            size=POPUP_CONFIG["GRID_SIZE"]
        )
        
        self.grid = FiftySoundsGrid()
        grid_container.add_widget(self.grid)
        
        anchor_layout.add_widget(grid_container)
        return anchor_layout
