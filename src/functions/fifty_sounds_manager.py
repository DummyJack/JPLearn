# -*- coding: utf-8 -*-

from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from components.buttons import SoundButton, SongButton

class FiftySoundsManager:
    """五十音聲音管理器"""
    def __init__(self):
        self.current_audio = None
        self.current_button = None
        self.audio_event = None

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
                # print(f"停止播放音頻: {audio_name}")
                return

        audio = SoundLoader.load(audio_file)
        if audio:
            audio.play()
            self.current_audio = audio
            self.current_button = instance
            instance.background_color = (1, 0.5, 0.5, 1) # 粉紅色 - 播放時的按鈕顏色
            # print(f"播放音頻: {audio_name}")
            self.audio_event = Clock.schedule_once(self._on_audio_finish, audio.length)
        else:
            # print(f"未找到音頻文件: {audio_file}")
            pass

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
        if isinstance(button, SongButton):
            button.background_color = (1, 0.7, 0.7, 1) # 淺粉紅色 - 歌曲按鈕的默認顏色
        else:
            button.background_color = (0.5, 0.7, 1, 1) # 淺藍色 - 一般按鈕的默認顏色

    def _reset_other_buttons(self, current_instance):
        for child in current_instance.parent.parent.children:
            for btn in child.children:
                if (isinstance(btn, SoundButton) or isinstance(btn, SongButton)) and btn != current_instance:
                    self._reset_button_color(btn)
