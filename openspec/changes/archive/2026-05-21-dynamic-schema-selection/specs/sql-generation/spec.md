## MODIFIED Requirements

### Requirement: 使用 RAG 上下文生成 SQL
系統必須利用檢索到的資料庫 Schema、SQL 範本和業務背景資訊生成 SQLite 相容的 SELECT 查詢。

#### Scenario: 動態 Schema 注入成功
- **WHEN** 系統成功檢索到 `branches` 表且分數達標
- **THEN** 生成的 Prompt 應僅包含檢索到的表格描述加上核心表格，而非全量 Schema。

#### Scenario: 回退至全量 Schema
- **WHEN** 檢索系統回傳空結果或分數過低
- **THEN** 生成的 Prompt 必須包含 `SCHEMA_DESCRIPTION` 中的全量字串。
