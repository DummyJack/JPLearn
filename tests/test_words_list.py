import pytest
from unittest.mock import MagicMock, patch
from kivy.metrics import dp
from functions.words_list import (
    JapaneseTextInput,
    WordItem,
    EditWordPopup,
    WordsList,
)

@pytest.fixture(scope="module")
def mock_mongodb():
    """提供模擬的 MongoDB 連接"""
    with patch("functions.words_list.MongoClient", autospec=True) as mock_client:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        
        # 設置 mock 鏈
        mock_client.return_value = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        
        # 注入模擬對象
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
    """提供 JapaneseTextInput 測試實例"""
    return JapaneseTextInput()

@pytest.fixture
def word_item():
    """提供帶有模擬回調的 WordItem 測試實例"""
    return WordItem(
        word="テスト",
        explanation="測試",
        delete_callback=MagicMock(),
        edit_callback=MagicMock(),
        word_id="test_id"
    )

@pytest.fixture
def edit_popup():
    """提供帶有模擬回調的 EditWordPopup 測試實例"""
    return EditWordPopup(
        japanese="テスト",
        explanation="測試",
        edit_callback=MagicMock(),
        word_id="test_id"
    )

class TestJapaneseInput:
    """測試日文輸入功能"""
    
    def test_hiragana_input(self, japanese_input):
        """測試平假名輸入"""
        japanese_input.text = ""
        japanese_input.insert_text("あいうえお")
        assert japanese_input.text == "あいうえお"
    
    def test_katakana_input(self, japanese_input):
        """測試片假名輸入"""
        japanese_input.text = ""
        japanese_input.insert_text("カタカナ")
        assert japanese_input.text == "カタカナ"
    
    def test_kanji_input(self, japanese_input):
        """測試漢字輸入"""
        japanese_input.text = ""
        japanese_input.insert_text("漢字")
        assert japanese_input.text == "漢字"
    
    def test_mixed_input_filtering(self, japanese_input):
        """測試混合輸入過濾"""
        japanese_input.text = ""
        japanese_input.insert_text("あabc漢字123カナ")
        assert japanese_input.text == "あ漢字カナ"
    
    def test_non_japanese_filtering(self, japanese_input):
        """測試非日文字符過濾"""
        japanese_input.text = ""
        japanese_input.insert_text("abc123")
        assert japanese_input.text == ""

class TestWordItem:
    """測試單字項目功能"""
    
    def test_word_update(self, word_item):
        """測試更新單字"""
        word_item.update_word("新テスト", "新測試")
        assert word_item.word == "新テスト"
        assert word_item.explanation == "新測試"
    
    def test_word_deletion(self, word_item):
        """測試刪除單字"""
        word_item.delete_word(None)
        word_item.delete_callback.assert_called_once_with(word_item)

class TestEditPopup:
    """測試編輯彈窗功能"""
    
    def test_initialization(self, edit_popup):
        """測試初始狀態"""
        assert edit_popup.japanese_input.text == "テスト"
        assert edit_popup.explanation_input.text == "測試"
        assert edit_popup.error_label.text == ""
    
    @pytest.mark.parametrize("char,expected", [
        ("あ", True),
        ("ア", True),
        ("漢", True),
        ("a", False),
        ("1", False),
        ("@", False)
    ])
    def test_japanese_char_validation(self, edit_popup, char, expected):
        """測試日文字符驗證"""
        assert edit_popup.is_japanese_char(char) == expected
    
    def test_empty_input_validation(self, edit_popup):
        """測試空輸入驗證"""
        edit_popup.japanese_input.text = ""
        edit_popup.edit_word(None)
        assert edit_popup.error_label.text == "必須輸入單字"
    
    def test_invalid_input_validation(self, edit_popup):
        """測試無效輸入驗證"""
        edit_popup.japanese_input.text = "abc123"
        edit_popup.edit_word(None)
        assert edit_popup.error_label.text == "請只輸入日文字符"

class TestWordsList:
    """測試單字列表功能"""
    
    def test_search_functionality(self, mock_mongodb):
        """測試搜索功能"""
        mock_find = MagicMock()
        mock_find.sort.return_value = mock_find
        mock_find.skip.return_value = mock_find
        mock_find.limit.return_value = [
            {"_id": "1", "japanese": "テスト1", "explanation": "測試1"},
            {"_id": "2", "japanese": "テスト2", "explanation": "測試2"}
        ]
        
        mock_mongodb.find.return_value = mock_find
        mock_mongodb.count_documents.return_value = 2
        
        words_list = WordsList()
        words_list.search_words("テスト")
        
        assert words_list.search_mode is True
        mock_mongodb.find.assert_called_with(
            {"japanese": {"$regex": "テスト", "$options": "i"}}
        )
