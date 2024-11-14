# MongoDB 驗證規則
WORDS_VALIDATOR = {
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

# 新增 tests 集合的驗證規則
TESTS_VALIDATOR = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["japanese", "rank"],
            "properties": {
                "japanese": {
                    "bsonType": "string",
                    "pattern": "^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+$",
                    "description": "必須是日文（平假名、片假名或漢字）"
                },
                "rank": {
                    "bsonType": "string",
                    "enum": ["N1", "N2", "N3", "N4", "N5", "basic"],
                    "description": "必須是 N1 到 N5 或 basic"
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
