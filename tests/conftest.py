import pytest
import os
import logging
import contextlib
from coverage import Coverage
from pymongo import MongoClient
from kivy.base import EventLoop
from kivy.core.text import LabelBase

# 配置常量
MONGODB_CONFIG = {
    "URL": "mongodb://localhost:27017/",
    "TIMEOUT": 5000,
    "TEST_DB": "test_japanese_db",
    "COLLECTION": "words"
}

COVERAGE_CONFIG = {
    "FILE": ".coverage",
    "SOURCE": ["functions"],
    "PERMISSIONS": 0o666
}

FONT_CONFIG = {
    "NAME": "ChineseFont",
    "PATH": os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'resources',
        'fonts', 
        'NotoSansTC-VariableFont_wght.ttf'
    )
}

# MongoDB 驗證規則
MONGODB_VALIDATOR = {
    "collMod": MONGODB_CONFIG["COLLECTION"],
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["japanese"],
            "properties": {
                "japanese": {
                    "bsonType": "string",
                    "pattern": "^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+$",
                    "description": "必須是日文（平假名、片假名或漢字）"
                },
                "explanation": {
                    "bsonType": "string",
                }
            }
        }
    },
    "validationLevel": "strict",
    "validationAction": "error"
}

# 禁用 MongoDB 日誌
logging.getLogger('pymongo').setLevel(logging.ERROR)

@pytest.fixture(scope="session")
def mongo_client():
    """提供 MongoDB 客戶端連接"""
    client = MongoClient(
        MONGODB_CONFIG["URL"],
        serverSelectionTimeoutMS=MONGODB_CONFIG["TIMEOUT"]
    )
    yield client
    client.close()

@pytest.fixture(scope="function")
def test_db(mongo_client):
    """創建測試用臨時資料庫"""
    # 清理現有數據庫
    with contextlib.suppress(Exception):
        mongo_client.drop_database(MONGODB_CONFIG["TEST_DB"])
    
    test_db = mongo_client[MONGODB_CONFIG["TEST_DB"]]
    
    try:
        # 創建集合
        test_db.create_collection(MONGODB_CONFIG["COLLECTION"])
        test_collection = test_db[MONGODB_CONFIG["COLLECTION"]]
        
        # 設置驗證規則
        test_db.command(MONGODB_VALIDATOR)
        
        yield test_collection
        
    finally:
        # 清理測試數據庫
        with contextlib.suppress(Exception):
            mongo_client.drop_database(MONGODB_CONFIG["TEST_DB"])

@pytest.fixture(autouse=True)
def coverage_cleanup():
    """確保每次測試運行前都有乾淨的 coverage 數據"""
    def cleanup_coverage_file():
        """清理舊的覆蓋率文件"""
        if os.path.exists(COVERAGE_CONFIG["FILE"]):
            try:
                os.chmod(COVERAGE_CONFIG["FILE"], COVERAGE_CONFIG["PERMISSIONS"])
                os.remove(COVERAGE_CONFIG["FILE"])
            except Exception as e:
                print(f"清理 coverage 文件時出錯: {e}")
    
    # 清理並初始化 Coverage 對象
    cleanup_coverage_file()
    
    # 創建並配置 Coverage 對象
    cov = Coverage(
        source=COVERAGE_CONFIG["SOURCE"],  # 指定要收集覆蓋率的源代碼目錄
        branch=True,  # 啟用分支覆蓋率
        data_file=COVERAGE_CONFIG["FILE"]  # 指定覆蓋率數據文件路徑
    )
    
    # 啟動覆蓋率收集
    cov.start()
    
    yield
    
    # 停止覆蓋率收集並保存
    try:
        cov.stop()
        cov.save()
    except Exception as e:
        print(f"保存 coverage 數據時出錯: {e}")

@pytest.fixture(autouse=True)
def kivy_config():
    """配置 Kivy 環境"""
    # 設置字體
    LabelBase.register(
        name=FONT_CONFIG["NAME"],
        fn_regular=FONT_CONFIG["PATH"]
    )
    
    # 初始化 Kivy 窗口
    EventLoop.ensure_window()
    
    yield