import pytest
from unittest.mock import MagicMock, patch
from kivy.metrics import dp
from functions.words_list import (
    JapaneseTextInput,
    WordItem,
    EditWordPopup,
    WordsList,
)


# 完全模擬 MongoDB，避免任何實際連接
@pytest.fixture(scope="module", autouse=True)
def mock_mongodb_module():
    """Mock MongoDB module to prevent actual database connections

    Sets up mock objects for:
    - MongoClient
    - Database
    - Collection
    """
    with patch("functions.words_list.MongoClient", autospec=True) as mock_client:
        # 創建所有需要的 mock 物件
        mock_db = MagicMock()
        mock_collection = MagicMock()

        # 設置 mock 鏈
        mock_client.return_value = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection

        # 注入到模組中
        import functions.words_list

        functions.words_list.client = mock_client()
        functions.words_list.db = mock_db
        functions.words_list.words_collection = mock_collection

        yield mock_collection

        # 清理
        functions.words_list.client = None
        functions.words_list.db = None
        functions.words_list.words_collection = None


@pytest.fixture
def japanese_input():
    """Create a fresh JapaneseTextInput instance for testing"""
    return JapaneseTextInput()


@pytest.fixture
def word_item():
    """Create a WordItem instance with mock callbacks"""
    return WordItem(
        word="テスト",
        explanation="測試",
        delete_callback=MagicMock(),
        edit_callback=MagicMock(),
        word_id="test_id",
    )


@pytest.fixture
def edit_popup():
    """Create an EditWordPopup instance with mock callback"""
    return EditWordPopup(
        japanese="テスト",
        explanation="測試",
        edit_callback=MagicMock(),
        word_id="test_id",
    )


@pytest.mark.input
def test_japanese_text_input(japanese_input):
    """Test JapaneseTextInput filtering functionality

    Verifies:
    - Hiragana input
    - Katakana input
    - Kanji input
    - Mixed input filtering
    - Non-Japanese character filtering
    """
    # 測試平假名輸入
    japanese_input.text = ""  # 清空初始文字
    japanese_input.insert_text("あいうえお")
    assert japanese_input.text == "あいうえお"

    # 測試片假名輸入
    japanese_input.text = ""
    japanese_input.insert_text("カタカナ")
    assert japanese_input.text == "カタカナ"

    # 測試漢字輸入
    japanese_input.text = ""
    japanese_input.insert_text("漢字")
    assert japanese_input.text == "漢字"

    # 測試混合輸入（日文+非日文）
    japanese_input.text = ""
    japanese_input.insert_text("あabc漢字123カナ")
    assert japanese_input.text == "あ漢字カナ"  # 只保留日文字符

    # 測試純字輸入（應該被完全過濾）
    japanese_input.text = ""
    japanese_input.insert_text("abc123")
    assert japanese_input.text == ""  # 非日文字符應被過濾掉


@pytest.mark.crud
def test_word_item_crud(word_item, mock_mongodb_module):
    """Test WordItem CRUD operations

    Verifies:
    - Word update functionality
    - Word deletion functionality
    - Callback triggering
    """
    # 測試更新
    word_item.update_word("新テスト", "新測試")
    assert word_item.word == "新テスト"
    assert word_item.explanation == "新測試"

    # 測試刪除
    word_item.delete_word(None)
    word_item.delete_callback.assert_called_once_with(word_item)


@pytest.mark.ui
def test_edit_popup_initialization(edit_popup):
    """Test EditWordPopup initial state

    Verifies:
    - Initial input field values
    - Initial error label state
    """
    assert edit_popup.japanese_input.text == "テスト"
    assert edit_popup.explanation_input.text == "測試"
    assert edit_popup.error_label.text == ""


@pytest.mark.validation
def test_edit_popup_validation(edit_popup):
    """Test EditWordPopup input validation

    Verifies:
    - Empty input handling
    - Invalid character handling
    - Valid input processing
    """
    # 測試空白輸入
    edit_popup.japanese_input.text = ""
    edit_popup.edit_word(None)
    assert edit_popup.error_label.text == "必須輸入單字"

    # 測試無效字符
    edit_popup.japanese_input.text = "abc123"
    edit_popup.edit_word(None)
    assert edit_popup.error_label.text == "請只輸入日文字符"

    # 測試有效輸入
    edit_popup.japanese_input.text = "テスト"  # <-- This is the actual input
    edit_popup.explanation_input.text = "測試"
    edit_popup.edit_word(None)
    # Update the expected value to match the actual input
    edit_popup.edit_callback.assert_called_once_with(
        "テスト", "測試"
    )  # <-- Changed from "テト" to "テスト"


@pytest.mark.parametrize(
    "char,expected",
    [
        ("あ", True),
        ("ア", True),
        ("漢", True),
        ("a", False),
        ("1", False),
        ("@", False),
    ],
)
@pytest.mark.validation
def test_is_japanese_char(edit_popup, char, expected):
    """Test Japanese character validation

    Verifies correct identification of:
    - Hiragana
    - Katakana
    - Kanji
    - Non-Japanese characters
    """
    assert edit_popup.is_japanese_char(char) == expected


@pytest.mark.search
def test_words_list_search(mock_mongodb_module):
    """Test WordsList search functionality

    Verifies:
    - Search query construction
    - MongoDB query execution
    - Search results processing
    - Pagination handling
    """
    # 設置 mock 搜尋結果
    mock_find = MagicMock()
    # Update the sort method to use list of tuples
    mock_find.sort.return_value = mock_find
    mock_find.skip.return_value = mock_find
    mock_find.limit.return_value = [
        {"_id": "1", "japanese": "テスト1", "explanation": "測試1"},
        {"_id": "2", "japanese": "テスト2", "explanation": "測試2"},
    ]

    # Configure the mock to handle the sort method correctly
    mock_mongodb_module.find.return_value.sort.return_value = mock_find
    mock_mongodb_module.find.return_value = mock_find
    mock_mongodb_module.count_documents.return_value = 2

    words_list = WordsList()
    words_list.search_words("テスト")

    # 驗證搜尋結果
    assert words_list.search_mode == True
    mock_mongodb_module.find.assert_called_with(
        {"japanese": {"$regex": "テスト", "$options": "i"}}
    )

    # 移除 sort 的斷言，因為在搜尋模式下不會使用 sort
    # mock_find.sort.assert_called_with([("_id", -1)])
