import pytest
from kivy.base import EventLoop
from kivy.core.window import Window
from functions.fifty_sounds import FiftySoundsGrid
from unittest.mock import MagicMock, patch


# 初始化 Kivy 環境
def setup_module(module):
    EventLoop.ensure_window()


@pytest.fixture
def fifty_sounds_grid():
    return FiftySoundsGrid()


def test_grid_initialization(fifty_sounds_grid):
    # 測試五十音格子初始化
    assert len(fifty_sounds_grid.sounds) == 46  # 五十音總數
    assert fifty_sounds_grid.current_audio is None
    assert fifty_sounds_grid.current_button is None


@patch("kivy.core.audio.SoundLoader.load")
def test_play_sound(mock_sound_loader, fifty_sounds_grid):
    # 模擬音頻載入
    mock_audio = MagicMock()
    mock_audio.length = 1.0
    mock_sound_loader.return_value = mock_audio

    # 創建模擬按鈕
    mock_button = MagicMock()
    mock_button.text = "[size=30]あ[/size]\n[size=24]a[/size]"

    # 測試播放音頻
    fifty_sounds_grid.play_sound(mock_button)

    # 驗證
    mock_sound_loader.assert_called_once_with("sounds/あ.mp3")
    mock_audio.play.assert_called_once()
    assert fifty_sounds_grid.current_audio == mock_audio
    assert fifty_sounds_grid.current_button == mock_button


def test_reset_audio_state(fifty_sounds_grid):
    # 設置初始狀態
    mock_audio = MagicMock()
    mock_button = MagicMock()
    fifty_sounds_grid.current_audio = mock_audio
    fifty_sounds_grid.current_button = mock_button

    # 測試重置
    fifty_sounds_grid._reset_audio_state()

    # 驗證
    mock_audio.stop.assert_called_once()
    assert fifty_sounds_grid.current_audio is None
    assert fifty_sounds_grid.current_button is None


def test_reset_button_color(fifty_sounds_grid):
    # 測試一般按鈕
    mock_button = MagicMock()
    mock_button.text = "一般按鈕"
    fifty_sounds_grid._reset_button_color(mock_button)
    assert mock_button.background_color == (0.5, 0.7, 1, 1)

    # 測試歌曲按鈕
    song_button = MagicMock()
    song_button.text = "一首歌記住五十音"
    fifty_sounds_grid._reset_button_color(song_button)
    assert song_button.background_color == (1, 0.7, 0.7, 1)
