import pytest
from unittest.mock import Mock, patch
from functions.words_list import WordsList, WordItem

# 測試數據常量
TEST_WORDS = {
    "HIRAGANA": {"japanese": "ひらがな", "explanation": "平假名"},
    "KANJI": {"japanese": "かんじ", "explanation": "漢字"},
    "TEST": {"japanese": "てすと", "explanation": "測試"},
    "GOJUON": [
        {"japanese": "あいうえお", "explanation": "五十音圖第一行"},
        {"japanese": "かきくけこ", "explanation": "五十音圖第二行"},
        {"japanese": "さしすせそ", "explanation": "五十音圖第三行"}
    ]
}

@pytest.fixture
def words_list(test_db):
    """提供 WordsList 實例和測試數據庫集合"""
    with patch('functions.words_list.words_collection', test_db):
        yield WordsList()

def insert_test_word(test_db, word_data):
    """輔助函數：插入測試單字"""
    return test_db.insert_one(word_data).inserted_id

def test_add_word(words_list, test_db):
    """測試新增單字功能"""
    word_data = TEST_WORDS["TEST"]
    word_id = insert_test_word(test_db, word_data)
    
    # 執行新增操作
    words_list.add_word(word_data["japanese"], word_data["explanation"], word_id)
    
    # 驗證界面更新
    assert len(words_list.layout.children) == 1
    word_item = words_list.layout.children[0]
    assert isinstance(word_item, WordItem)
    assert word_item.word == word_data["japanese"]
    assert word_item.explanation == word_data["explanation"]
    assert word_item.word_id == word_id

def test_delete_word(words_list, test_db):
    """測試刪除單字功能"""
    # 準備測試數據
    word_id = insert_test_word(test_db, TEST_WORDS["HIRAGANA"])
    words_list.load_words_from_db()
    
    # 驗證初始狀態
    assert len(words_list.layout.children) == 1
    
    # 執行刪除操作
    word_item = words_list.layout.children[0]
    with patch('kivy.uix.popup.Popup.open'):
        words_list.show_delete_confirmation(word_item)
        words_list.delete_word(word_item, Mock())
    
    # 驗證刪除結果
    assert len(words_list.layout.children) == 0
    assert test_db.count_documents({}) == 0

def test_edit_word(words_list, test_db):
    """測試編輯單字功能"""
    # 準備測試數據
    word_id = insert_test_word(test_db, TEST_WORDS["KANJI"])
    words_list.load_words_from_db()
    word_item = words_list.layout.children[0]
    
    # 準備新數據
    new_word_data = TEST_WORDS["HIRAGANA"]
    
    # 執行編輯操作
    with patch.object(word_item, 'word', new_word_data["japanese"]):
        with patch.object(word_item, 'explanation', new_word_data["explanation"]):
            words_list.edit_word(
                word_item, 
                new_word_data["japanese"], 
                new_word_data["explanation"]
            )
            
            # 驗證數據庫更新
            updated_word = test_db.find_one({"_id": word_id})
            assert updated_word["japanese"] == new_word_data["japanese"]
            assert updated_word["explanation"] == new_word_data["explanation"]

def test_search_words(words_list, test_db):
    """測試搜索單字功能"""
    # 準備測試數據
    test_db.insert_many(TEST_WORDS["GOJUON"])
    
    # 執行搜索
    words_list.search_words("あ")
    
    # 驗證搜索結果
    assert words_list.search_mode is True
    assert len(words_list.search_results) == 1
    assert len(words_list.layout.children) == 1
    assert words_list.layout.children[0].word == "あいうえお"

def test_pagination(words_list, test_db):
    """測試分頁功能"""
    # 準備測試數據
    test_data = [
        {
            "japanese": "ひらがな",
            "explanation": f"平假名{i}"
        }
        for i in range(7)
    ]
    
    # 插入測試數據
    for data in test_data:
        test_db.insert_one(data)
    
    # 測試第一頁
    words_list.load_words_from_db()
    assert len(words_list.layout.children) == 5
    assert words_list.current_page == 1
    assert words_list.total_pages == 2
    
    # 測試第二頁
    words_list.current_page = 2
    words_list.load_words_from_db()
    assert len(words_list.layout.children) == 2
