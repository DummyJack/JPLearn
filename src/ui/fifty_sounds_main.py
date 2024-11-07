from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from components import SoundButton, SongButton
from functions import FiftySoundsManager

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

BUTTON_CONFIG = {
    "SIZE": dp(70),
    "SPACING": dp(5),
    "BUTTONS_PER_ROW": 9
}

class FiftySoundsGrid(BoxLayout):
    """五十音格子UI"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = FiftySoundsManager()
        self._init_layout()
        self._create_sound_buttons()

    def _init_layout(self):
        """初始化佈局設置"""
        self.orientation = "vertical"
        self.spacing = BUTTON_CONFIG["SPACING"]
        self.padding = BUTTON_CONFIG["SPACING"]
        
        # 定義五十音數據
        self.sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn".split("|")

    def _create_sound_buttons(self):
        """創建五十音按鈕"""
        self.clear_widgets()
        self._create_main_grid()
        self._create_last_row()

    def _create_main_grid(self):
        """創建主要的五十音格子"""
        for i in range(0, len(self.sounds) - 1, BUTTON_CONFIG["BUTTONS_PER_ROW"]):
            row = self._create_row()
            for j in range(BUTTON_CONFIG["BUTTONS_PER_ROW"]):
                if i + j < len(self.sounds) - 1:
                    sound = self.sounds[i + j]
                    btn = self._create_sound_button(sound)
                    row.add_widget(btn)
            self.add_widget(row)

    def _create_last_row(self):
        """創建最後一行（包含ん和歌曲按鈕）"""
        row = self._create_row()
        
        # 添加ん按鈕
        n_sound = self.sounds[-1]
        n_btn = self._create_sound_button(n_sound)
        row.add_widget(n_btn)
        
        # 添加間隔
        spacer = BoxLayout(
            size_hint_x=None, 
            width=BUTTON_CONFIG["SIZE"] * 5 + BUTTON_CONFIG["SPACING"] * 4
        )
        row.add_widget(spacer)
        
        # 添加歌曲按鈕
        song_btn = self._create_song_button()
        row.add_widget(song_btn)
        
        self.add_widget(row)

    def _create_row(self):
        """創建一行的容器"""
        return BoxLayout(
            orientation="horizontal",
            spacing=BUTTON_CONFIG["SPACING"],
            size_hint_y=None,
            height=BUTTON_CONFIG["SIZE"]
        )

    def _create_sound_button(self, sound):
        """創建音節按鈕"""
        japanese, romaji = sound[0], sound[1:]
        btn = SoundButton(
            japanese=japanese,
            romaji=romaji,
            size=BUTTON_CONFIG["SIZE"]
        )
        btn.bind(on_press=self.sound_manager.play_sound)
        return btn

    def _create_song_button(self):
        """創建歌曲按鈕"""
        btn = SongButton(size=BUTTON_CONFIG["SIZE"])
        btn.bind(on_press=self.sound_manager.play_song)
        return btn

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
        content.add_widget(self._create_title())
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
