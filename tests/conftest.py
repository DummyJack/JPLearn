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
    "URL": "mongodb://localhost:27017/",  # MongoDB 連接地址
    "TIMEOUT": 5000,                      # 連接超時時間（毫秒）
    "TEST_DB": "test_japanese_db",        # 測試數據庫名稱
    "COLLECTION": "words"                 # 集合名稱
}

COVERAGE_CONFIG = {
    "FILE": ".coverage",                  # 覆蓋率報告文件
    "SOURCE": ["functions"],              # 需要統計覆蓋率的源碼目錄
    "PERMISSIONS": 0o666                  # 文件權限設置
}

FONT_CONFIG = {
    "NAME": "ChineseFont",                # 字體名稱
    "PATH": os.path.join(                 # 字體文件路徑
        os.path.dirname(os.path.dirname(__file__)), 
        'resources',
        'fonts', 
        'NotoSansTC-VariableFont_wght.ttf'
    )
}

# MongoDB 驗證規則：確保數據格式正確
MONGODB_VALIDATOR = {
    "collMod": MONGODB_CONFIG["COLLECTION"],
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["japanese"],      # japanese 字段為必填
            "properties": {
                "japanese": {
                    "bsonType": "string",
                    "pattern": "^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+$",  # 限制只能輸入日文字符
                    "description": "必須是日文（平假名、片假名或漢字）"
                },
                "explanation": {
                    "bsonType": "string",
                }
            }
        }
    },
    "validationLevel": "strict",          # 嚴格驗證
    "validationAction": "error"           # 驗證失敗時拋出錯誤
}

# 禁用 MongoDB 日誌，避免測試輸出過多日誌
logging.getLogger('pymongo').setLevel(logging.ERROR)

@pytest.fixture(scope="session")
def mongo_client():
    """提供 MongoDB 客戶端連接：整個測試會話共用一個連接"""
    client = MongoClient(
        MONGODB_CONFIG["URL"],
        serverSelectionTimeoutMS=MONGODB_CONFIG["TIMEOUT"]
    )
    yield client
    client.close()

@pytest.fixture(scope="function")
def test_db(mongo_client):
    """創建測試用臨時資料庫：每個測試函數都使用新的數據庫"""
    # 清理現有數據庫
    with contextlib.suppress(Exception):
        mongo_client.drop_database(MONGODB_CONFIG["TEST_DB"])
    
    test_db = mongo_client[MONGODB_CONFIG["TEST_DB"]]
    
    try:
        # 創建集合並設置驗證規則
        test_db.create_collection(MONGODB_CONFIG["COLLECTION"])
        test_collection = test_db[MONGODB_CONFIG["COLLECTION"]]
        test_db.command(MONGODB_VALIDATOR)
        
        yield test_collection
        
    finally:
        # 測試完成後清理數據庫
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
        branch=True,                       # 啟用分支覆蓋率
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
    """配置 Kivy 環境：設置字體和初始化窗口"""
    # 註冊中文字體
    LabelBase.register(
        name=FONT_CONFIG["NAME"],
        fn_regular=FONT_CONFIG["PATH"]
    )
    
    # 確保 Kivy 窗口已初始化
    EventLoop.ensure_window()
    
    yield