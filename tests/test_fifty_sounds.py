import pytest
from unittest.mock import Mock, patch
from kivy.uix.button import Button

from ..src.ui.fifty_sounds_main import FiftySoundsGrid

# 測試數據常量
COLORS = {
    "INITIAL": [0.5, 0.7, 1, 1],     # 按鈕初始顏色（淺藍色）
    "PLAYING": [1, 0.5, 0.5, 1],     # 播放時的顏色（粉紅色）
    "SONG_INITIAL": [1, 0.7, 0.7, 1] # 歌曲按鈕初始顏色（淺粉色）
}

# 五十音表：(平假名, 羅馬音)的元組列表
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
    """創建模擬音頻對象：用於測試音頻播放功能"""
    mock_audio = Mock()
    mock_audio.length = 1.0          # 音頻長度（秒）
    mock_audio.play = Mock()         # 播放方法
    mock_audio.stop = Mock()         # 停止方法
    return mock_audio

def create_test_button(japanese, romaji, color=COLORS["INITIAL"]):
    """
    創建測試用按鈕
    Args:
        japanese: 日文字符
        romaji: 羅馬音
        color: 按鈕顏色
    """
    return Button(
        text=f"[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]",
        markup=True,
        background_color=color
    )

@pytest.fixture
def fifty_sounds_grid():
    """提供 FiftySoundsGrid 實例：模擬音頻加載"""
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
            assert mock_audio.play.called                           # 確認音頻被播放
            assert fifty_sounds_grid.current_button == button       # 確認當前按鈕
            assert button.background_color == COLORS["PLAYING"]     # 確認按鈕顏色變化
            
            # 重置狀態
            fifty_sounds_grid._reset_audio_state()
            mock_audio.play.reset_mock()
            
            # 驗證重置後的狀態
            assert button.background_color == COLORS["INITIAL"]     # 確認按鈕恢復原色
            assert fifty_sounds_grid.current_audio is None          # 確認音頻被清除
            assert fifty_sounds_grid.current_button is None         # 確認按鈕被清除

def test_play_fifty_sound_with_invalid_audio(fifty_sounds_grid):
    """測試播放音效文件不存在的情況"""
    test_button = create_test_button("あ", "a")
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=None):
        fifty_sounds_grid.play_sound(test_button)
        
        # 驗證錯誤處理
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
        mock_load.return_value.play.assert_called_once()           # 確認歌曲被播放
        assert song_button.background_color == COLORS["PLAYING"]    # 確認按鈕顏色變化

def test_auto_stop_sound(fifty_sounds_grid):
    """測試音效自動停止功能"""
    test_button = create_test_button("あ", "a")
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=create_mock_audio()):
        fifty_sounds_grid.play_sound(test_button)
        fifty_sounds_grid._reset_audio_state()
        
        # 驗證所有狀態都被正確重置
        assert fifty_sounds_grid.current_audio is None
        assert fifty_sounds_grid.current_button is None
        assert fifty_sounds_grid.audio_event is None
        assert test_button.background_color == COLORS["INITIAL"]

def test_play_multiple_sounds(fifty_sounds_grid):
    """測試連續播放不同音效：確保前一個音效被停止"""
    button1 = create_test_button("あ", "a")
    button2 = create_test_button("い", "i")
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=create_mock_audio()):
        # 播放第一個音效
        fifty_sounds_grid.play_sound(button1)
        fifty_sounds_grid.current_button = button1
        
        # 播放第二個音效
        fifty_sounds_grid.play_sound(button2)
        fifty_sounds_grid.current_audio.stop.assert_called()       # 確認前一個音效被停止
        assert fifty_sounds_grid.current_button == button2         # 確認切換到新按鈕