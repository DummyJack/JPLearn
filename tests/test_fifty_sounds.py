import pytest
from unittest.mock import Mock, patch
from kivy.uix.button import Button
from functions.fifty_sounds import FiftySoundsGrid, FiftySoundsPopup

@pytest.fixture
def fifty_sounds_grid():
    """提供 FiftySoundsGrid 實例"""
    with patch('kivy.core.audio.SoundLoader.load') as mock_load:
        grid = FiftySoundsGrid()
        mock_audio = Mock()
        mock_audio.length = 1.0
        mock_audio.play = Mock()
        mock_audio.stop = Mock()
        mock_load.return_value = mock_audio
        yield grid

def test_play_all_fifty_sounds(fifty_sounds_grid):
    """測試播放所有五十音字詞的功能"""
    # 定義顏色常量
    INITIAL_COLOR = [0.5, 0.7, 1, 1]     # 初始顏色
    PLAYING_COLOR = [1, 0.5, 0.5, 1]     # 播放時的顏色
    
    # 定義測試用的五十音字詞列表
    fifty_sounds = [
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
    
    # 創建模擬音頻
    mock_audio = Mock()
    mock_audio.length = 1.0
    mock_audio.play = Mock()
    mock_audio.stop = Mock()
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=mock_audio):
        # 測試每個五十音字詞
        for japanese, romaji in fifty_sounds:
            # 創建按鈕
            button = Button(
                text=f"[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]",
                markup=True,
                background_color=INITIAL_COLOR
            )
            
            # 播放音效
            fifty_sounds_grid.play_sound(button)
            
            # 驗證
            assert mock_audio.play.called
            assert fifty_sounds_grid.current_button == button
            assert button.background_color == PLAYING_COLOR  # 使用正確的播放時顏色
            
            # 重置音效狀態
            fifty_sounds_grid._reset_audio_state()
            mock_audio.play.reset_mock()
            
            # 驗證重置後的狀態
            assert button.background_color == INITIAL_COLOR  # 使用正確的初始顏色
            assert fifty_sounds_grid.current_audio is None
            assert fifty_sounds_grid.current_button is None

def test_play_fifty_sound_with_invalid_audio(fifty_sounds_grid):
    """測試播放音效文件不存在的情況"""
    test_button = Button(
        text="[size=30]あ[/size]\n[size=24]a[/size]",
        markup=True,
        background_color=[0.5, 0.7, 1, 1]
    )
    
    # 模擬音頻載入失敗
    with patch('kivy.core.audio.SoundLoader.load', return_value=None):
        fifty_sounds_grid.play_sound(test_button)
        
        # 驗證狀態
        assert fifty_sounds_grid.current_audio is None
        assert fifty_sounds_grid.current_button is None
        assert test_button.background_color == [0.5, 0.7, 1, 1]



def test_play_fifty_sounds_song(fifty_sounds_grid):
    """測試播放五十音歌曲的功能"""
    # 初始顏色
    INITIAL_COLOR = [1, 0.7, 0.7, 1]
    # 播放時的顏色
    PLAYING_COLOR = [1, 0.5, 0.5, 1]  # 修改為實際使用的顏色值
    
    song_button = Button(
        text="一首歌記住五十音",
        background_color=INITIAL_COLOR
    )
    
    # 播放前先模擬音頻載入
    mock_audio = Mock()
    mock_audio.length = 1.0
    mock_audio.play = Mock()
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=mock_audio):
        fifty_sounds_grid.play_sound(song_button)
        mock_audio.play.assert_called_once()
        assert song_button.background_color == PLAYING_COLOR  # 使用正確的播放時顏色值


def test_auto_stop_sound(fifty_sounds_grid):
    """測試音效自動停止功能"""
    test_button = Button(
        text="[size=30]あ[/size]\n[size=24]a[/size]",
        markup=True,
        background_color=[0.5, 0.7, 1, 1]
    )
    
    mock_audio = Mock()
    mock_audio.length = 1.0
    mock_audio.play = Mock()
    mock_audio.stop = Mock()
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=mock_audio):
        fifty_sounds_grid.play_sound(test_button)
        fifty_sounds_grid._reset_audio_state()
        
        assert fifty_sounds_grid.current_audio is None
        assert fifty_sounds_grid.current_button is None
        assert fifty_sounds_grid.audio_event is None
        assert test_button.background_color == [0.5, 0.7, 1, 1]


def test_play_multiple_sounds(fifty_sounds_grid):
    """測試連續播放不同音效"""
    button1 = Button(
        text="[size=30]あ[/size]\n[size=24]a[/size]",
        markup=True,
        background_color=[0.5, 0.7, 1, 1]
    )
    button2 = Button(
        text="[size=30]い[/size]\n[size=24]i[/size]",
        markup=True,
        background_color=[0.5, 0.7, 1, 1]
    )
    
    mock_audio = Mock()
    mock_audio.length = 1.0
    mock_audio.play = Mock()
    mock_audio.stop = Mock()
    
    with patch('kivy.core.audio.SoundLoader.load', return_value=mock_audio):
        fifty_sounds_grid.play_sound(button1)
        fifty_sounds_grid.current_button = button1
        
        fifty_sounds_grid.play_sound(button2)
        mock_audio.stop.assert_called()
        assert fifty_sounds_grid.current_button == button2