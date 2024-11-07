# -*- coding: utf-8 -*-

from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from components.buttons import SoundButton, SongButton

class FiftySoundsManager:
    """五十音聲音管理器：負責管理和播放五十音的音頻"""
    def __init__(self):
        # 初始化音頻相關狀態
        self.current_audio = None     # 當前播放的音頻
        self.current_button = None    # 當前播放音頻的按鈕
        self.audio_event = None       # 音頻播放完成的計時器事件

    def play_sound(self, instance):
        """播放五十音單音：從按鈕文本中提取音節並播放對應音頻"""
        # 從按鈕文本中提取音節（去除標籤）
        sound = instance.text.split()[0].strip("[size=30][/")
        sound_file = f"resources/sounds/{sound}.mp3"
        self._play_audio(instance, sound_file, sound)

    def play_song(self, instance):
        """播放五十音之歌"""
        song_file = "resources/sounds/fifty_sounds_song.mp3"
        self._play_audio(instance, song_file, "五十音歌曲")

    def _play_audio(self, instance, audio_file, audio_name):
        """
        播放音頻的核心邏輯
        Args:
            instance: 觸發播放的按鈕實例
            audio_file: 音頻文件路徑
            audio_name: 音頻名稱（用於調試）
        """
        # 如果有音頻正在播放，先停止它
        if self.current_audio:
            self.current_audio.stop()
            if self.audio_event:
                self.audio_event.cancel()
            # 如果點擊的是當前正在播放的按鈕，則停止播放
            if self.current_button == instance:
                self._reset_audio_state()
                # print(f"停止播放音頻: {audio_name}")
                return

        # 加載並播放新的音頻
        audio = SoundLoader.load(audio_file)
        if audio:
            audio.play()
            self.current_audio = audio
            self.current_button = instance
            instance.background_color = (1, 0.5, 0.5, 1) # 粉紅色 - 播放時的按鈕顏色
            # print(f"播放音頻: {audio_name}")
            
            # 設置音頻播放完成的回調
            self.audio_event = Clock.schedule_once(self._on_audio_finish, audio.length)
        else:
            # print(f"未找到音頻文件: {audio_file}")
            pass

        # 重置其他按鈕的狀態
        self._reset_other_buttons(instance)

    def _on_audio_finish(self, dt):
        """音頻播放完成的回調：重置所有狀態"""
        self._reset_audio_state()

    def _reset_audio_state(self):
        """重置所有音頻相關的狀態"""
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
        """重置按鈕顏色到默認狀態"""
        if isinstance(button, SongButton):
            button.background_color = (1, 0.7, 0.7, 1)  # 淺粉紅色 - 歌曲按鈕的默認顏色
        else:
            button.background_color = (0.5, 0.7, 1, 1)  # 淺藍色 - 一般按鈕的默認顏色

    def _reset_other_buttons(self, current_instance):
        """重置除當前按鈕外的所有按鈕顏色"""
        # 遍歷所有按鈕並重置顏色
        for child in current_instance.parent.parent.children:
            for btn in child.children:
                if (isinstance(btn, SoundButton) or isinstance(btn, SongButton)) and btn != current_instance:
                    self._reset_button_color(btn)
