## 1. 資料準備與索引更新

- [x] 1.1 更新 `app/db/schema_description.py` 中的 `SCHEMA_DESCRIPTIONS_FOR_INDEX`，加入表格關聯資訊。
- [x] 1.2 執行 `python -m app.knowledge.indexer` 重新建立 OpenSearch 索引。

## 2. 核心邏輯開發

- [x] 2.1 在 `app/skills/sql_generation.py` 中實作 `_build_dynamic_schema` 輔助函式。
- [x] 2.2 在 `SQLGenerationSkill.execute` 中整合動態 Schema 檢索結果。
- [x] 2.3 實作 Fallback 機制，當檢索分數低於 0.5 時切換至靜態 `SCHEMA_DESCRIPTION`。
- [x] 2.4 確保核心表格（branches, customers, deposits）始終包含在動態 Schema 中。

## 3. 測試與驗證

- [x] 3.1 執行現有的 `pytest tests/test_acceptance.py` 確保無迴歸問題。
- [x] 3.2 建立測試指令碼，驗證在低相關度問題下是否正確觸發 Fallback。
- [x] 3.3 驗證產生的 Prompt 確實節省了 Token（手動或透過日誌觀察）。
