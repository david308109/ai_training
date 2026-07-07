## Context

目前 `SQLGenerationSkill` 使用靜態字串 `SCHEMA_DESCRIPTION` 作為資料庫 Schema 的唯一來源。這種做法在表格數量增加時會導致 Prompt 過長。專案已具備 OpenSearch 向量檢索能力（`retriever.py`），且已存在 `schema_descriptions` 索引，為動態選取奠定了基礎。

## Goals / Non-Goals

**Goals:**
- 根據使用者問題動態檢索最相關的資料表。
- 實作 Fallback 機制，確保檢索失敗時仍能生成正確 SQL。
- 核心表格（如 `customers`）始終包含在 Prompt 中。
- 保持現有的 SQL 生成準確性。

**Non-Goals:**
- 實作多輪對話中的上下文記憶。
- 修改資料庫實際的 DDL。
- 處理超過資料庫現有表格量級的大規模分表（當前僅針對中小型 Schema 優化）。

## Decisions

### 1. 動態 Prompt 組裝邏輯
將 `SQLGenerationSkill` 中的 `SCHEMA_DESCRIPTION` 替換為 `_build_dynamic_schema` 函式。
- **原因**：解耦 Prompt 與 Schema 來源，方便注入檢索結果。
- **邏輯**：核心表 (Core) + 檢索表 (Retrieved) + Join 關係 (Join Paths)。

### 2. Fallback 機制與閾值
設定檢索分數閾值與最小表格數量。
- **決策**：若檢索出的最高分數低於 `0.5`（暫定），或檢索結果為空，則直接回退到 `SCHEMA_DESCRIPTION`（全量 Schema）。
- **理由**：與其給 LLM 片段且不相關的資訊導致其混亂，不如給予完整資訊讓其自行過濾。

### 3. Schema 索引增強
更新 `app/db/schema_description.py` 中的 `SCHEMA_DESCRIPTIONS_FOR_INDEX`。
- **決策**：在每個 table 的 `description` 中加入其主要的 Foreign Key 關係描述。
- **理由**：確保當某張表被檢索到時，AI 也能感知到它的關聯表，從而觸發關聯表的連帶檢索或提示 LLM 需要 Join。

### 4. 核心表格 (Core Tables) 定義
定義 `branches`, `customers`, `deposits` 為核心表。
- **理由**：銀行系統 90% 的業務操作都圍繞這三張表展開。始終包含它們能大幅提高基礎查詢的成功率。

## Risks / Trade-offs

- **[Risk] 檢索不到位** ➔ **Mitigation**: 實作 Fallback 至全量 Schema，並始終包含核心表。
- **[Risk] OpenSearch 延遲** ➔ **Mitigation**: Schema 檢索通常極快，且可快取常用問題的檢索結果（暫不實作快取，視性能需求而定）。
- **[Trade-off] 索引同步成本** ➔ 每次修改 DDL 或描述後，需重新執行 `python -m app.knowledge.indexer`。
