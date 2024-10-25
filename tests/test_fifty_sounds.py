import pytest
from kivy.base import EventLoop
from kivy.core.window import Window
from functions.fifty_sounds import FiftySoundsGrid
from unittest.mock import MagicMock, patch


@pytest.fixture(scope="module", autouse=True)
def setup_kivy():
    """Initialize Kivy environment before running tests"""
    EventLoop.ensure_window()


@pytest.fixture(scope="function")
def fifty_sounds_grid():
    """Creates a fresh FiftySoundsGrid instance for each test"""
    return FiftySoundsGrid()


@pytest.mark.ui
def test_grid_initialization(fifty_sounds_grid):
    """Test FiftySoundsGrid initialization state

    Verifies:
    - Correct number of sounds loaded
    - Initial audio state is None
    - Initial button state is None
    """
    assert len(fifty_sounds_grid.sounds) == 46
    assert fifty_sounds_grid.current_audio is None
    assert fifty_sounds_grid.current_button is None


@pytest.mark.ui
@patch("kivy.core.audio.SoundLoader.load")
def test_play_sound(mock_sound_loader, fifty_sounds_grid):
    """Test sound playing functionality

    Verifies:
    - Sound loading with correct file path
    - Audio playback
    - Current audio and button state updates
    """
    mock_audio = MagicMock()
    mock_audio.length = 1.0
    mock_sound_loader.return_value = mock_audio

    mock_button = MagicMock()
    mock_button.text = "[size=30]あ[/size]\n[size=24]a[/size]"

    fifty_sounds_grid.play_sound(mock_button)

    mock_sound_loader.assert_called_once_with("sounds/あ.mp3")
    mock_audio.play.assert_called_once()
    assert fifty_sounds_grid.current_audio == mock_audio
    assert fifty_sounds_grid.current_button == mock_button


@pytest.mark.ui
def test_reset_audio_state(fifty_sounds_grid):
    """Test audio state reset functionality

    Verifies:
    - Audio playback stops
    - Current audio and button states are cleared
    """
    mock_audio = MagicMock()
    mock_button = MagicMock()
    fifty_sounds_grid.current_audio = mock_audio
    fifty_sounds_grid.current_button = mock_button

    fifty_sounds_grid._reset_audio_state()

    mock_audio.stop.assert_called_once()
    assert fifty_sounds_grid.current_audio is None
    assert fifty_sounds_grid.current_button is None


@pytest.mark.ui
def test_reset_button_color(fifty_sounds_grid):
    """Test button color reset functionality

    Verifies:
    - Regular buttons get correct background color
    - Song buttons get correct background color
    """
    mock_button = MagicMock()
    mock_button.text = "一般按鈕"
    fifty_sounds_grid._reset_button_color(mock_button)
    assert mock_button.background_color == (0.5, 0.7, 1, 1)

    song_button = MagicMock()
    song_button.text = "一首歌記住五十音"
    fifty_sounds_grid._reset_button_color(song_button)
    assert song_button.background_color == (1, 0.7, 0.7, 1)
