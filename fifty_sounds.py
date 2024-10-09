# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from custom_widgets import TitleBar
from kivy.core.window import Window
from kivy.metrics import dp

class FiftySoundsGrid(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(5)
        self.padding = dp(5)

        sounds = "あa|いi|うu|えe|おo|かka|きki|くku|けke|こko|さsa|しshi|すsu|せse|そso|たta|ちchi|つtsu|てte|とto|なna|にni|ぬnu|ねne|のno|はha|ひhi|ふfu|へhe|ほho|まma|みmi|むmu|めme|もmo|やya|ゆyu|よyo|らra|りri|るru|れre|ろro|わwa|をo|んn"
        self.sounds = sounds.split("|")
        self.button_size = dp(70)
        self.spacing = dp(5)

        self.current_audio = None
        self.current_button = None

        self.update_layout()

    def update_layout(self, *args):
        self.clear_widgets()
        width = self.width if self.width else Window.width
        max_buttons_per_row = max(1, int((width - self.spacing) / (self.button_size + self.spacing)))
        
        current_row = None
        for i, sound in enumerate(self.sounds):
            if i % max_buttons_per_row == 0:
                current_row = BoxLayout(orientation='horizontal', spacing=self.spacing, size_hint_y=None, height=self.button_size)
                self.add_widget(current_row)

            japanese, romaji = sound[0], sound[1:]
            btn = Button(
                text=f'[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]',
                markup=True,
                font_name='ChineseFont',
                background_color=(0.5, 0.7, 1, 1),
                size_hint=(None, None),
                size=(self.button_size, self.button_size),
                halign='center',
                valign='middle',
                text_size=(self.button_size, self.button_size)
            )
            btn.bind(on_press=self.play_sound)
            current_row.add_widget(btn)

        # 添加間隔
        spacer = BoxLayout(size_hint_x=None, width=dp(10))
        current_row.add_widget(spacer)

        # 添加"一首歌記住五十音"按鈕
        song_btn = Button(
            text='一首歌記住五十音',
            font_name='ChineseFont',
            background_color=(1, 0.7, 0.7, 1),
            size_hint=(None, None),
            size=(self.button_size * 2.5, self.button_size),  # 增加寬度以容納文字
            halign='center',
            valign='middle',
        )
        song_btn.bind(on_press=self.play_song)
        current_row.add_widget(song_btn)

    def play_sound(self, instance):
        sound = instance.text.split()[0].strip("[size=30][/")  # 獲取日文字符
        sound_file = f"sounds/{sound}.mp3"
        self._play_audio(instance, sound_file, sound)

    def play_song(self, instance):
        song_file = "sounds/fifty_sounds_song.mp3"  # 假設歌曲文件名為 fifty_sounds_song.mp3
        self._play_audio(instance, song_file, "五十音歌曲")

    def _play_audio(self, instance, audio_file, audio_name):
        if self.current_audio:
            self.current_audio.stop()
            if self.current_button == instance:
                # 如果按下的是當前正在播放的按鈕，則停止播放並重置狀態
                self.current_audio = None
                self.current_button = None
                instance.background_color = (0.5, 0.7, 1, 1) if audio_name != "五十音歌曲" else (1, 0.7, 0.7, 1)
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
        else:
            print(f"未找到音頻文件: {audio_file}")

        # 重置其他按鈕的顏色
        for child in self.children:
            for btn in child.children:
                if isinstance(btn, Button) and btn != instance:
                    if btn.text == '一首歌\n記住\n五十音':
                        btn.background_color = (1, 0.7, 0.7, 1)
                    else:
                        btn.background_color = (0.5, 0.7, 1, 1)

    def on_size(self, *args):
        self.update_layout()

class FiftySoundsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        
        content = BoxLayout(orientation='vertical', spacing=dp(20))  # 增加間距

        title_bar = TitleBar("五十音", self.dismiss)
        content.add_widget(title_bar)

        self.grid = FiftySoundsGrid()
        content.add_widget(self.grid)
        
        self.content = content

    def on_size(self, *args):
        # 當彈出窗口大小改變時，調整網格的列數和寬度
        if hasattr(self, 'grid'):
            self.grid.update_layout()