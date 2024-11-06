# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.clock import Clock

# 常量定義
COLORS = {
    "INITIAL": (0.5, 0.7, 1, 1),
    "PLAYING": (1, 0.5, 0.5, 1),
    "SONG_INITIAL": (1, 0.7, 0.7, 1)
}

BUTTON_CONFIG = {
    "SIZE": dp(70),
    "SPACING": dp(5),
    "BUTTONS_PER_ROW": 9
}

class FiftySoundsGrid(BoxLayout):
    """五十音格子視圖"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_layout()
        self._init_state()
        self._create_sound_buttons()

    def _init_layout(self):
        """初始化佈局設置"""
        self.orientation = "vertical"
        self.spacing = BUTTON_CONFIG["SPACING"]
        self.padding = BUTTON_CONFIG["SPACING"]
        
        # 定義五十音數據
        self.sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn".split("|")

    def _init_state(self):
        """初始化狀態變量"""
        self.current_audio = None
        self.current_button = None
        self.audio_event = None

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
        btn = Button(
            text=f"[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]",
            markup=True,
            font_name="ChineseFont",
            background_color=COLORS["INITIAL"],
            size_hint=(None, None),
            size=(BUTTON_CONFIG["SIZE"], BUTTON_CONFIG["SIZE"]),
            halign="center",
            valign="middle",
            text_size=(BUTTON_CONFIG["SIZE"], BUTTON_CONFIG["SIZE"])
        )
        btn.bind(on_press=self.play_sound)
        return btn

    def _create_song_button(self):
        """創建歌曲按鈕"""
        btn = Button(
            text="一首歌記住五十音",
            font_name="ChineseFont",
            background_color=COLORS["SONG_INITIAL"],
            size_hint=(None, None),
            size=(BUTTON_CONFIG["SIZE"] * 3, BUTTON_CONFIG["SIZE"]),
            halign="center",
            valign="middle"
        )
        btn.bind(on_press=self.play_song)
        return btn

    def play_sound(self, instance):
        sound = instance.text.split()[0].strip("[size=30][/")
        sound_file = f"resources/sounds/{sound}.mp3"
        self._play_audio(instance, sound_file, sound)

    def play_song(self, instance):
        song_file = "resources/sounds/fifty_sounds_song.mp3"
        self._play_audio(instance, song_file, "五十音歌曲")

    def _play_audio(self, instance, audio_file, audio_name):
        if self.current_audio:
            self.current_audio.stop()
            if self.audio_event:
                self.audio_event.cancel()
            if self.current_button == instance:
                self._reset_audio_state()
                print(f"停止播放音頻: {audio_name}")
                return

        audio = SoundLoader.load(audio_file)
        if audio:
            audio.play()
            self.current_audio = audio
            self.current_button = instance
            instance.background_color = [1, 0.5, 0.5, 1]
            print(f"播放音頻: {audio_name}")
            self.audio_event = Clock.schedule_once(self._on_audio_finish, audio.length)
        else:
            print(f"未找到音頻文件: {audio_file}")

        self._reset_other_buttons(instance)

    def _on_audio_finish(self, dt):
        self._reset_audio_state()

    def _reset_audio_state(self):
        if self.current_audio:
            self.current_audio.stop()
        self.current_audio = None
        if self.current_button:
            self._reset_button_color(self.current_button)
        self.current_button = None
        if self.audio_event:
            self.audio_event.cancel()
        self.audio_event = None

    def _reset_button_color(self, button):
        if button.text == "一首歌記住五十音":
            button.background_color = (1, 0.7, 0.7, 1)
        else:
            button.background_color = (0.5, 0.7, 1, 1)

    def _reset_other_buttons(self, current_instance):
        for child in self.children:
            for btn in child.children:
                if isinstance(btn, Button) and btn != current_instance:
                    self._reset_button_color(btn)
