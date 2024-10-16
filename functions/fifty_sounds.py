# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from components.custom_widgets import TitleBar
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout


class FiftySoundsGrid(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(5)
        self.padding = dp(5)

        # 定義五十音及其羅馬字對應
        sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn"
        self.sounds = sounds.split("|")
        self.button_size = dp(70)
        self.spacing = dp(5)

        self.current_audio = None
        self.current_button = None
        self.audio_event = None

        self.update_layout()

    def update_layout(self, *args):
        self.clear_widgets()

        # 固定每行9個按鈕
        buttons_per_row = 9

        for i in range(
            0, len(self.sounds) - 1, buttons_per_row
        ):  # 減1是為了排除最後的 "ん"
            row = BoxLayout(
                orientation="horizontal",
                spacing=self.spacing,
                size_hint_y=None,
                height=self.button_size,
            )
            for j in range(buttons_per_row):
                if i + j < len(self.sounds) - 1:  # 減1是為了排除最後的 "ん"
                    sound = self.sounds[i + j]
                    japanese, romaji = sound[0], sound[1:]
                    btn = Button(
                        text=f"[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]",
                        markup=True,
                        font_name="ChineseFont",
                        background_color=(0.5, 0.7, 1, 1),
                        size_hint=(None, None),
                        size=(self.button_size, self.button_size),
                        halign="center",
                        valign="middle",
                        text_size=(self.button_size, self.button_size),
                    )
                    btn.bind(on_press=self.play_sound)
                    row.add_widget(btn)
            self.add_widget(row)

        # 添加最後一行（包含 "ん" 和 "一首歌記住五十音" 按鈕）
        last_row = BoxLayout(
            orientation="horizontal",
            spacing=self.spacing,
            size_hint_y=None,
            height=self.button_size,
        )

        # 添加 "ん" 按鈕
        n_sound = self.sounds[-1]
        n_japanese, n_romaji = n_sound[0], n_sound[1:]
        n_btn = Button(
            text=f"[size=30]{n_japanese}[/size]\n[size=24]{n_romaji}[/size]",
            markup=True,
            font_name="ChineseFont",
            background_color=(0.5, 0.7, 1, 1),
            size_hint=(None, None),
            size=(self.button_size, self.button_size),
            halign="center",
            valign="middle",
            text_size=(self.button_size, self.button_size),
        )
        n_btn.bind(on_press=self.play_sound)
        last_row.add_widget(n_btn)

        # 添加間隔
        spacer = BoxLayout(
            size_hint_x=None, width=self.button_size * 5 + self.spacing * 4
        )
        last_row.add_widget(spacer)

        # 添加 "一首歌記住五十音" 按鈕
        song_btn = Button(
            text="一首歌記住五十音",
            font_name="ChineseFont",
            background_color=(1, 0.7, 0.7, 1),
            size_hint=(None, None),
            size=(self.button_size * 3, self.button_size),
            halign="center",
            valign="middle",
        )
        song_btn.bind(on_press=self.play_song)
        last_row.add_widget(song_btn)

        self.add_widget(last_row)

    def play_sound(self, instance):
        # 播放單個音節的聲音
        sound = instance.text.split()[0].strip("[size=30][/")  # 獲取日文字符
        sound_file = f"sounds/{sound}.mp3"
        self._play_audio(instance, sound_file, sound)

    def play_song(self, instance):
        # 播放五十音歌曲
        song_file = "sounds/fifty_sounds_song.mp3"
        self._play_audio(instance, song_file, "五十音歌曲")

    def _play_audio(self, instance, audio_file, audio_name):
        if self.current_audio:
            self.current_audio.stop()
            if self.audio_event:
                self.audio_event.cancel()  # 取消之前的事件
            if self.current_button == instance:
                # 如果按下的是前正在播放的按鈕，則停止播放並重置狀態
                self._reset_audio_state()
                print(f"停止播放音頻: {audio_name}")
                return

        # 播放新的音頻
        audio = SoundLoader.load(audio_file)
        if audio:
            audio.play()
            self.current_audio = audio
            self.current_button = instance
            instance.background_color = (1, 0.5, 0.5, 1)  # 改變按鈕顏色以表示正在播放
            print(f"播放音頻: {audio_name}")

            # 設置音頻結束後的回調
            self.audio_event = Clock.schedule_once(self._on_audio_finish, audio.length)
        else:
            print(f"未找到音頻文件: {audio_file}")

        # 重置其他按鈕的顏色
        self._reset_other_buttons(instance)

    def _on_audio_finish(self, dt):
        # 音頻播放結束後的回調函數
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


class FiftySoundsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (None, None)
        self.size = (dp(800), dp(600))

        content = BoxLayout(orientation="vertical", spacing=dp(20))

        title_bar = TitleBar("五十音", self.dismiss)
        content.add_widget(title_bar)

        # 創建一個 AnchorLayout 來包裹 FiftySoundsGrid
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")

        # 創建一個 BoxLayout 來包裹 FiftySoundsGrid，並添加 padding
        grid_container = BoxLayout(
            orientation="vertical", padding=(dp(20), dp(20), dp(20), dp(20))
        )

        self.grid = FiftySoundsGrid()
        grid_container.add_widget(self.grid)

        # 將 grid_container 添加到 AnchorLayout 中
        anchor_layout.add_widget(grid_container)

        # 將 AnchorLayout 添加到主要內容中
        content.add_widget(anchor_layout)

        self.content = content


# FiftySoundsGrid 類保持不變
