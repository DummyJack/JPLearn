import pytest
from unittest.mock import Mock, patch
from functions.words_list import WordsList, WordItem
@pytest.fixture
def words_list(test_db):
    """提供 WordsList 實例和測試數據庫集合"""
    with patch('functions.words_list.words_collection', test_db):
        words_list = WordsList()
        yield words_list

def test_add_word(words_list, test_db):
    """測試新增單字功能"""
    # 新增單字（確保使用有效的日文字符）
    japanese = "てすと"  # 使用平假名
    explanation = "測試"
    
    # 先插入到數據庫
    word_id = test_db.insert_one({
        "japanese": japanese,
        "explanation": explanation
    }).inserted_id
    
    words_list.add_word(japanese, explanation, word_id)
    
    # 驗證界面更新
    assert len(words_list.layout.children) == 1
    word_item = words_list.layout.children[0]
    assert isinstance(word_item, WordItem)
    assert word_item.word == japanese
    assert word_item.explanation == explanation
    assert word_item.word_id == word_id

def test_delete_word(words_list, test_db):
    """測試刪除單字功能"""
    # 先新增一個單字（使用有效的日文字符）
    word_id = test_db.insert_one({
        "japanese": "ひらがな",  # 使用平假名
        "explanation": "平假名"
    }).inserted_id
    
    words_list.load_words_from_db()
    assert len(words_list.layout.children) == 1
    
    # 刪除單字
    word_item = words_list.layout.children[0]
    with patch('kivy.uix.popup.Popup.open'):
        words_list.show_delete_confirmation(word_item)
        words_list.delete_word(word_item, Mock())
    
    # 驗證刪除結果
    assert len(words_list.layout.children) == 0
    assert test_db.count_documents({}) == 0

def test_edit_word(words_list, test_db):
    """測試編輯單字功能"""
    # 先新增一個單字（使用有效的日文字符）
    word_id = test_db.insert_one({
        "japanese": "かんじ",  # 使用平假名
        "explanation": "漢字"
    }).inserted_id
    
    words_list.load_words_from_db()
    word_item = words_list.layout.children[0]
    
    # 編輯單字（確保新的日文也是有效的）
    new_japanese = "ひらがな"  # 使用平假名
    new_explanation = "平假名"
    
    # 模擬編輯操作
    with patch.object(word_item, 'word', new_japanese):  # 模擬更新 word 屬性
        with patch.object(word_item, 'explanation', new_explanation):  # 模擬更新 explanation 屬性
            words_list.edit_word(word_item, new_japanese, new_explanation)
            
            # 驗證數據庫更新
            updated_word = test_db.find_one({"_id": word_id})
            assert updated_word["japanese"] == new_japanese
            assert updated_word["explanation"] == new_explanation

def test_search_words(words_list, test_db):
    """測試搜索單字功能"""
    # 插入測試數據（使用有效的日文字符）
    test_db.insert_many([
        {"japanese": "あいうえお", "explanation": "五十音圖第一行"},
        {"japanese": "かきくけこ", "explanation": "五十音圖第二行"},
        {"japanese": "さしすせそ", "explanation": "五十音圖第三行"}
    ])
    
    # 執行搜索
    words_list.search_words("あ")
    
    # 驗證搜索結果
    assert words_list.search_mode == True
    assert len(words_list.search_results) == 1
    assert len(words_list.layout.children) == 1
    assert words_list.layout.children[0].word == "あいうえお"

def test_pagination(words_list, test_db):
    """測試分頁功能"""
    # 插入超過一頁的數據（使用有效的日文字符）
    test_data = [
        {
            "japanese": f"ひらがな",  # 不要加數字，保持純日文
            "explanation": f"平假名{i}"
        }
        for i in range(7)  # 插入7個項目
    ]
    
    # 逐個插入以避免批量插入的驗證問題
    for data in test_data:
        test_db.insert_one(data)
    
    words_list.load_words_from_db()
    
    # 驗證第一頁
    assert len(words_list.layout.children) == 5
    assert words_list.current_page == 1
    assert words_list.total_pages == 2
    
    # 測試翻頁
    words_list.current_page = 2
    words_list.load_words_from_db()
    assert len(words_list.layout.children) == 2  # 第二頁應該有2個項目
