from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from components import SoundButton, SongButton
from functions import FiftySoundsManager

# 常量定義：用於統一管理按鈕的尺寸和佈局
BUTTON_CONFIG = {
    "SIZE": dp(70),                # 按鈕大小
    "SPACING": dp(5),              # 按鈕間距
    "BUTTONS_PER_ROW": 9           # 每行按鈕數量
}

class FiftySoundsGrid(BoxLayout):
    """五十音格子UI：顯示五十音按鈕網格和播放控制"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = FiftySoundsManager()  # 音頻管理器
        self._init_layout()                        # 初始化佈局
        self._create_sound_buttons()               # 創建按鈕

    def _init_layout(self):
        """初始化佈局設置"""
        self.orientation = "vertical"              # 垂直佈局
        self.spacing = BUTTON_CONFIG["SPACING"]    # 設置間距
        self.padding = BUTTON_CONFIG["SPACING"]    # 設置內邊距
        
        # 定義五十音數據：格式為"平假名羅馬音"
        self.sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn".split("|")

    def _create_sound_buttons(self):
        """創建五十音按鈕網格"""
        self.clear_widgets()                       # 清空現有部件
        self._create_main_grid()                  # 創建主網格
        self._create_last_row()                   # 創建最後一行

    def _create_main_grid(self):
        """創建主要的五十音格子（除最後一行外）"""
        # 每9個音節一行
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
        
        # 添加間隔（用於平衡佈局）
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
        """創建音節按鈕：包含平假名和羅馬音"""
        japanese, romaji = sound[0], sound[1:]     # 分離平假名和羅馬音
        btn = SoundButton(
            japanese=japanese,
            romaji=romaji,
            size=BUTTON_CONFIG["SIZE"]
        )
        btn.bind(on_press=self.sound_manager.play_sound)  # 綁定播放事件
        return btn

    def _create_song_button(self):
        """創建歌曲按鈕：用於播放五十音之歌"""
        btn = SongButton(size=BUTTON_CONFIG["SIZE"])
        btn.bind(on_press=self.sound_manager.play_song)   # 綁定播放事件
        return btn

class FiftyWordsMain(Popup):
    """五十音彈出窗口：主要容器"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_popup()          # 初始化彈窗設置
        self._create_content()      # 創建內容
        # 綁定關閉事件
        self.bind(on_dismiss=self._cleanup)

    def _init_popup(self):
        """初始化彈出窗口設置"""
        self.title = ""             # 無標題
        self.separator_height = 0   # 無分隔線
        self.size_hint = (None, None)
        self.size = (dp(800), dp(600))  # 固定大小
        self.background_color = (0.5, 0.7, 1, 1)  # 淺藍色背景

    def _create_content(self):
        """創建彈出窗口內容"""
        content = BoxLayout(orientation="vertical", spacing=dp(20))
        content.add_widget(self._create_title())   # 添加標題
        content.add_widget(self._create_grid())    # 添加五十音格子
        self.content = content

    def _create_title(self):
        """創建標題"""
        title_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=None,
            height=dp(50)
        )
        
        title = Label(
            text="五十音",
            font_name="ChineseFont",
            font_size=dp(36),
            color=(1, 1, 1, 1),     # 純白色文字
            size_hint=(None, None),
            size=(dp(200), dp(50))
        )
        
        title_layout.add_widget(title)
        return title_layout

    def _create_grid(self):
        """創建五十音格子容器"""
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        
        grid_container = BoxLayout(
            orientation="vertical",
            padding=(dp(20), dp(10), dp(40), dp(20)),  # 左上右下內邊距
            size_hint=(None, None),
            size=(dp(720), dp(480))                    # 固定大小
        )
        
        self.grid = FiftySoundsGrid()
        grid_container.add_widget(self.grid)
        
        anchor_layout.add_widget(grid_container)
        return anchor_layout

    def _cleanup(self, instance):
        """
        清理音頻資源：當彈窗關閉時自動停止播放
        Args:
            instance: 彈窗實例
        """
        if hasattr(self, 'grid') and self.grid:
            self.grid.sound_manager._reset_audio_state()
