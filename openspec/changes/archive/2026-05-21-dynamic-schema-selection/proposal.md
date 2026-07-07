## Why

當前系統將完整的資料庫 Schema（包含所有資料表、欄位描述及業務規則）硬編碼在 Prompt 中。隨著資料庫規模擴大，這將導致：
1. **Token 消耗過高**：每次請求都要帶上完整的 Schema 資訊。
2. **干擾 AI 判斷**：過多不相關的表格描述可能干擾 LLM 生成 SQL 的準確性。

透過動態 Schema 選取，我們能根據使用者問題僅提取最相關的資訊，並在檢索失敗時提供可靠的備援。

## What Changes

- **動態檢索實作**：擴展 `SQLGenerationSkill`，使其能利用 `retriever` 從 OpenSearch 中獲取相關的資料表描述。
- **Fallback 機制實作**：
    - 若檢索結果信心度不足，自動回退至原有的靜態 Schema。
    - 定義「核心表格」（如 `customers`），無論檢索結果如何皆會包含在 Prompt 中。
- **Schema 索引優化**：在 OpenSearch 索引中加入表格間的關聯關係（Join Paths），確保檢索出的片段足以構成完整的 SQL。
- **Prompt 結構調整**：將 SQL 生成的 Prompt 改為動態建構，根據檢索結果填入 Schema 區塊。

## Capabilities

### New Capabilities
- `dynamic-schema-retrieval`: 實作從向量資料庫中檢索相關資料表元資料的能力，並根據相關度進行排序與選取。

### Modified Capabilities
- `sql-generation`: 修改 SQL 生成邏輯，從接受硬編碼 Schema 改為接受動態生成的 Schema 字串，並包含 Fallback 邏輯。
- `vector-knowledge-base`: 更新資料庫索引邏輯，確保表格描述包含足夠的關聯上下文。

## Impact

- `app/db/schema_description.py`: 重新組織靜態 Schema 資訊，以便進行局部選取與備援。
- `app/skills/sql_generation.py`: 主要修改邏輯所在地，需整合檢索結果。
- `app/retrieval/retriever.py`: 可能需要優化對 `schema_descriptions` 索引的查詢參數。
- `app/knowledge/indexer.py`: 需要重新運行索引以包含加強後的 Schema 描述。
