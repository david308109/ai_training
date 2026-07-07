## ADDED Requirements

### Requirement: 基於相關性的 Schema 檢索
系統必須能從 `schema_descriptions` 索引中檢索與使用者問題最相關的資料表元資料。

#### Scenario: 成功檢索到相關表
- **WHEN** 使用者詢問「哪個分行的存款最多？」
- **THEN** 系統必須檢索出 `branches` 與 `deposits` 表的描述。

### Requirement: 核心表格強行注入
系統必須在任何動態選取的 Schema 中包含定義好的核心表格。

#### Scenario: 包含核心表
- **WHEN** 使用者詢問任何問題
- **THEN** 檢索結果中必須包含 `customers`, `deposits`, `branches` 的描述，無論其檢索分數為何。

### Requirement: 檢索閾值與 Fallback
當檢索結果的最高相關性分數低於預設閾值（0.5）時，系統必須回退至使用全量 Schema。

#### Scenario: 觸發 Fallback
- **WHEN** 使用者輸入無意義或與資料庫無關的問題，導致最高檢索分數為 0.3
- **THEN** 系統生成的 Prompt 必須包含完整的靜態 Schema 描述。
