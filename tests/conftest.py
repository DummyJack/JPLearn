import pytest
from coverage import Coverage
from kivy.base import EventLoop
from kivy.core.text import LabelBase
import os
from pymongo import MongoClient
import contextlib
import logging

# 禁用 MongoDB 的日誌記錄
logging.getLogger('pymongo').setLevel(logging.ERROR)

@pytest.fixture(scope="session")
def mongo_client():
    """提供 MongoDB 客戶端連接"""
    client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=1,  # 限制連接池大小
        waitQueueTimeoutMS=5000,
        connect=False  # 延遲連接直到第一次操作
    )
    try:
        # 測試連接
        client.admin.command('ping')
        yield client
    finally:
        with contextlib.suppress(Exception):
            client.close()

@pytest.fixture(scope="function")
def test_db(mongo_client):
    """創建測試用臨時資料庫"""
    db_name = "test_japanese_db"
    
    # 確保開始時數據庫是乾淨的
    with contextlib.suppress(Exception):
        mongo_client.drop_database(db_name)
    
    test_db = mongo_client[db_name]
    
    # 創建集合並設置驗證規則
    try:
        test_db.create_collection("words")
        test_collection = test_db.words
        
        # 設置驗證規則
        test_db.command({
            "collMod": "words",
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
        })
        
        yield test_collection
        
    finally:
        # 清理測試資料庫
        with contextlib.suppress(Exception):
            mongo_client.drop_database(db_name)

@pytest.fixture(autouse=True)
def coverage_cleanup():
    """確保每次測試運行前都有乾淨的 coverage 數據"""
    # 清理舊的覆蓋率數據
    coverage_file = ".coverage"
    if os.path.exists(coverage_file):
        try:
            os.chmod(coverage_file, 0o666)
            os.remove(coverage_file)
        except Exception as e:
            print(f"清理 coverage 文件時出錯: {e}")
    
    # 創建並配置 Coverage 對象
    cov = Coverage(
        source=['functions'],  # 指定要收集覆蓋率的源代碼目錄
        branch=True,  # 啟用分支覆蓋率
        data_file=coverage_file  # 指定覆蓋率數據文件路徑
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
    font_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'resources',
        'fonts', 
        'NotoSansTC-VariableFont_wght.ttf'
    )
    
    LabelBase.register(
        name="ChineseFont",
        fn_regular=font_path
    )
    
    # 初始化 Kivy 窗口
    EventLoop.ensure_window()
    
    yield