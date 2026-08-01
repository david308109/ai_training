# 專案架構概覽 (Data Agent — Text-to-SQL)

本專案是一個具備 RAG (檢索增強生成) 能力的銀行數據代理，透過 LangChain LCEL 進行流程編排。

## 核心目錄與模組說明

### `app/`
- `main.py`: 應用程式入口，定義 FastAPI API `/query` 端點，並在 `lifespan` 中完成 Skill 註冊與資料庫初始化。
- `config.py`: 全域設定檔，透過 `pydantic-settings` 從環境變數讀取 OpenRouter、OpenSearch 及資料庫參數。

### `app/agent/`
- `orchestrator.py`: 核心流程編排器。使用 **LangChain LCEL** (`|`) 將檢索、SQL 生成、執行與分流邏輯串聯成管線，處理整個查詢生命週期。

### `app/db/`
- `database.py`: SQLite 連線管理與 SQL 執行輔助函式。
- `schema.sql`: 資料庫架構定義與預設資料。
- `schema_description.py`: 定義資料庫 schema 的自然語言描述，並提供 `SCHEMA_DESCRIPTIONS_FOR_INDEX` 供向量檢索。目前支援**動態 Schema 選取**與自動 **Fallback** 機制。

### `app/knowledge/`
- `indexer.py`: 負責將 SQL 範本、Schema 說明與業務背景資料批次索引至 OpenSearch。
- `sql_templates.py` / `business_context.py`: 領域知識庫原始資料。

### `app/retrieval/`
- `embeddings.py`: 將文字轉換為向量的本地處理邏輯。
- `opensearch_client.py`: OpenSearch 客戶端，處理向量索引建立 (`create_knn_index`) 與檢索 (`knn_search`)。
- `retriever.py`: RAG 檢索器，整合三種索引 (`sql_templates`, `schema_descriptions`, `business_context`) 的檢索結果。

### `app/skills/`
- `base.py`: 定義 `Skill` 抽象基類，繼承自 LangChain `Runnable`，確保所有技能均可透過 LCEL 串接。
- `registry.py`: 技能註冊中心。
- `sql_generation.py`: 將自然語言問題轉換為 SQL 的 Skill。內建 **Intent Guard（意圖守衛）**，在同一次 LLM 呼叫中判斷使用者問題是否與資料庫相關——若為閒聊或無關問題，直接回傳 `sql: null` 並短路後續流程，不會產生額外 LLM 呼叫。採用**動態 Schema 選取**（優先從 OpenSearch 檢索相關表，並始終包含核心表），若檢索分數過低則自動 Fallback 到全量 Schema。同時輸出複雜度判斷與回答模板。
- `response_formatter.py`: 智慧分流模組，嘗試以本地 Python 邏輯格式化答案，減少不必要的 LLM 調用。
- `answer_synthesis.py`: AI 合成 Skill，作為複雜問題或本地格式化失敗時的後備機制 (Fallback)。

### `tests/`
- `test_acceptance.py`: 端到端驗收測試，模擬完整查詢流程。
- `test_simple.py`: 測試簡單問題的智慧分流效能與正確性。

---

## 數據流向 (LCEL 管線)
1. **Retrieval**: 取得上下文。
2. **SQL Generation + Intent Guard**: 生成 SQL + 複雜度標籤 + 格式模板。若 LLM 判斷問題與資料庫無關，回傳 `sql: null`，直接進入閒聊回覆分支。
3. **DB Execution**: 執行 SQL 取得資料（閒聊問題跳過此步）。
4. **Smart Branching**:
   - 若為 `CHITCHAT`（Intent Guard 攔截）-> **直接回覆引導訊息** (0 次額外 LLM)。
   - 若為 `simple` 且格式化成功 -> **本地 Python 拼湊答案** (0 次額外 LLM)。
   - 若為 `complex` 或格式化失敗 -> **呼叫 Answer Synthesis** (LLM 合成)。
