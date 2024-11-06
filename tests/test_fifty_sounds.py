import pytest
from unittest.mock import Mock, patch
from kivy.uix.button import Button
from ..src.functions.fifty_sounds_manager import FiftySoundsGrid

# 測試數據常量
COLORS = {
    "INITIAL": [0.5, 0.7, 1, 1],
    "PLAYING": [1, 0.5, 0.5, 1],
    "SONG_INITIAL": [1, 0.7, 0.7, 1]
}

FIFTY_SOUNDS = [
    ("あ", "a"), ("い", "i"), ("う", "u"), ("え", "e"), ("お", "o"),
    ("か", "ka"), ("き", "ki"), ("く", "ku"), ("け", "ke"), ("こ", "ko"),
    ("さ", "sa"), ("し", "shi"), ("す", "su"), ("せ", "se"), ("そ", "so"),
    ("た", "ta"), ("ち", "chi"), ("つ", "tsu"), ("て", "te"), ("と", "to"),
    ("な", "na"), ("に", "ni"), ("ぬ", "nu"), ("ね", "ne"), ("の", "no"),
    ("は", "ha"), ("ひ", "hi"), ("ふ", "fu"), ("へ", "he"), ("ほ", "ho"),
    ("ま", "ma"), ("み", "mi"), ("む", "mu"), ("め", "me"), ("も", "mo"),
    ("や", "ya"), ("ゆ", "yu"), ("よ", "yo"),
    ("ら", "ra"), ("り", "ri"), ("る", "ru"), ("れ", "re"), ("ろ", "ro"),
    ("わ", "wa"), ("を", "wo"), ("ん", "n")
]

def create_mock_audio():
    """創建模擬音頻對象"""
    mock_audio = Mock()
    mock_audio.length = 1.0
    mock_audio.play = Mock()
    mock_audio.stop = Mock()
    return mock_audio

def create_test_button(japanese, romaji, color=COLORS["INITIAL"]):
    """創建測試用按鈕"""
    return Button(
        text=f"[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]",
        markup=True,
        background_color=color
    )

@pytest.fixture
def fifty_sounds_grid():
    """提供 FiftySoundsGrid 實例"""
    with patch('kivy.core.audio.SoundLoader.load') as mock_load:
        grid = FiftySoundsGrid()
        mock_load.return_value = create_mock_audio()
        yield grid

def test_play_all_fifty_sounds(fifty_sounds_grid):
    """測試播放所有五十音字詞的功能"""
    mock_audio = create_mock_audio()
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=mock_audio):
        for japanese, romaji in FIFTY_SOUNDS:
            # 創建並測試每個按鈕
            button = create_test_button(japanese, romaji)
            
            # 播放音效
            fifty_sounds_grid.play_sound(button)
            
            # 驗證播放狀態
            assert mock_audio.play.called
            assert fifty_sounds_grid.current_button == button
            assert button.background_color == COLORS["PLAYING"]
            
            # 重置狀態
            fifty_sounds_grid._reset_audio_state()
            mock_audio.play.reset_mock()
            
            # 驗證重置後的狀態
            assert button.background_color == COLORS["INITIAL"]
            assert fifty_sounds_grid.current_audio is None
            assert fifty_sounds_grid.current_button is None

def test_play_fifty_sound_with_invalid_audio(fifty_sounds_grid):
    """測試播放音效文件不存在的情況"""
    test_button = create_test_button("あ", "a")
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=None):
        fifty_sounds_grid.play_sound(test_button)
        
        assert fifty_sounds_grid.current_audio is None
        assert fifty_sounds_grid.current_button is None
        assert test_button.background_color == COLORS["INITIAL"]

def test_play_fifty_sounds_song(fifty_sounds_grid):
    """測試播放五十音歌曲的功能"""
    song_button = Button(
        text="一首歌記住五十音",
        background_color=COLORS["SONG_INITIAL"]
    )
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=create_mock_audio()) as mock_load:
        fifty_sounds_grid.play_sound(song_button)
        mock_load.return_value.play.assert_called_once()
        assert song_button.background_color == COLORS["PLAYING"]

def test_auto_stop_sound(fifty_sounds_grid):
    """測試音效自動停止功能"""
    test_button = create_test_button("あ", "a")
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=create_mock_audio()):
        fifty_sounds_grid.play_sound(test_button)
        fifty_sounds_grid._reset_audio_state()
        
        assert fifty_sounds_grid.current_audio is None
        assert fifty_sounds_grid.current_button is None
        assert fifty_sounds_grid.audio_event is None
        assert test_button.background_color == COLORS["INITIAL"]

def test_play_multiple_sounds(fifty_sounds_grid):
    """測試連續播放不同音效"""
    button1 = create_test_button("あ", "a")
    button2 = create_test_button("い", "i")
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=create_mock_audio()):
        # 播放第一個音效
        fifty_sounds_grid.play_sound(button1)
        fifty_sounds_grid.current_button = button1
        
        # 播放第二個音效
        fifty_sounds_grid.play_sound(button2)
        fifty_sounds_grid.current_audio.stop.assert_called()
        assert fifty_sounds_grid.current_button == button2