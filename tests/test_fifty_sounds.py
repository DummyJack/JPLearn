import pytest
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.uix.button import Button
from functions.fifty_sounds import FiftySoundsGrid, FiftySoundsPopup
from kivy.clock import Clock
from kivy.metrics import dp


# 初始化 Kivy 環境
def setup_module():
    EventLoop.ensure_window()
    Window.size = (800, 600)


@pytest.fixture(scope="module", autouse=True)
def setup_kivy():
    """Initialize Kivy environment before running tests"""
    EventLoop.ensure_window()


@pytest.fixture(scope="function")
def fifty_sounds_grid():
    """Creates a fresh FiftySoundsGrid instance for each test"""
    return FiftySoundsGrid()


@pytest.fixture(scope="function")
def fifty_sounds_popup():
    """Creates a fresh FiftySoundsPopup instance for each test"""
    return FiftySoundsPopup()


@pytest.mark.ui
def test_grid_initialization(fifty_sounds_grid):
    """Test FiftySoundsGrid initialization state

    Verifies:
    - Correct orientation
    - Correct spacing
    - Correct padding
    - Initial audio state is None
    - Initial button state is None
    """
    assert fifty_sounds_grid.orientation == "vertical"
    assert fifty_sounds_grid.spacing == dp(5)
    # padding 是一個列表，需要分別比較每個值
    padding = fifty_sounds_grid.padding
    expected_padding = dp(5)
    assert all(
        p == expected_padding for p in padding
    ), f"Expected all padding values to be {expected_padding}, but got {padding}"
    assert fifty_sounds_grid.current_audio is None
    assert fifty_sounds_grid.current_button is None
    assert fifty_sounds_grid.audio_event is None


@pytest.mark.ui
def test_grid_layout(fifty_sounds_grid):
    """Test FiftySoundsGrid layout

    Verifies:
    - Correct number of buttons
    """
    # 檢查按鈕數量
    total_buttons = 0
    for child in fifty_sounds_grid.children:
        total_buttons += len(
            [widget for widget in child.children if isinstance(widget, Button)]
        )
    assert total_buttons == 47  # 五十音圖的按鈕數量 + 歌曲按鈕


@pytest.mark.ui
def test_play_sound(fifty_sounds_grid):
    """Test sound playing functionality

    Verifies:
    - Sound loading with correct file path
    - Audio playback
    - Current audio and button state updates
    """
    # 模擬按鈕點擊
    first_row = fifty_sounds_grid.children[-1]  # 最後一個 child 是第一行
    first_button = [b for b in first_row.children if isinstance(b, Button)][-1]

    # 測試播放音頻
    fifty_sounds_grid.play_sound(first_button)
    assert fifty_sounds_grid.current_button == first_button

    # 測試停止音頻
    fifty_sounds_grid.play_sound(first_button)  # 再次點擊同一個按鈕
    assert fifty_sounds_grid.current_button is None


@pytest.mark.ui
def test_play_song(fifty_sounds_grid):
    """Test song playing functionality

    Verifies:
    - Song button is found
    - Song playback
    - Current audio and button state updates
    """
    # 找到歌曲按鈕
    last_row = fifty_sounds_grid.children[0]
    song_button = next(
        (
            child
            for child in last_row.children
            if isinstance(child, Button) and child.text == "一首歌記住五十音"
        ),
        None,
    )

    assert song_button is not None
    fifty_sounds_grid.play_song(song_button)
    assert fifty_sounds_grid.current_button == song_button


@pytest.mark.ui
def test_popup_initialization(fifty_sounds_popup):
    """Test FiftySoundsPopup initialization state

    Verifies:
    - Correct title
    - Correct separator height
    - Correct size
    - Correct background color
    """
    assert fifty_sounds_popup.title == ""
    assert fifty_sounds_popup.separator_height == 0
    # 比較 size 列表中的值而不是元組
    size = fifty_sounds_popup.size
    expected_size = [dp(800), dp(600)]
    assert (
        size[0] == expected_size[0] and size[1] == expected_size[1]
    ), f"Expected size {expected_size}, but got {size}"
    assert tuple(fifty_sounds_popup.background_color) == (0.5, 0.7, 1, 1)


@pytest.mark.ui
def test_reset_audio_state(fifty_sounds_grid):
    """Test audio state reset functionality

    Verifies:
    - Audio playback stops
    - Current audio and button states are cleared
    """
    fifty_sounds_grid._reset_audio_state()
    assert fifty_sounds_grid.current_audio is None
    assert fifty_sounds_grid.current_button is None
    assert fifty_sounds_grid.audio_event is None


@pytest.mark.ui
def test_reset_button_color(fifty_sounds_grid):
    """Test button color reset functionality

    Verifies:
    - Regular buttons get correct background color
    - Song buttons get correct background color
    """
    # 測試普通按鈕
    first_row = fifty_sounds_grid.children[-1]
    normal_button = [b for b in first_row.children if isinstance(b, Button)][-1]
    fifty_sounds_grid._reset_button_color(normal_button)
    assert list(normal_button.background_color) == [0.5, 0.7, 1, 1]

    # 測試歌曲按鈕
    last_row = fifty_sounds_grid.children[0]
    song_button = next(
        (
            child
            for child in last_row.children
            if isinstance(child, Button) and child.text == "一首歌記住五十音"
        ),
        None,
    )
    assert song_button is not None
    fifty_sounds_grid._reset_button_color(song_button)
    assert list(song_button.background_color) == [1, 0.7, 0.7, 1]
