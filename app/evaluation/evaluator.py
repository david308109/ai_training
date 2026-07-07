"""
SQL comparison logic for evaluation: structural (AST-SM), result-set (EX), and exact match (EM).
SQL 評估邏輯：包含結構匹配 (AST-SM)、執行結果比對 (EX) 與精確比對 (EM)。
"""

import logging
import sqlglot
from sqlglot.optimizer import optimize

from app.db.database import execute_query

logger = logging.getLogger(__name__)


def normalize_sql(sql: str) -> str:
    """
    Normalize SQL using sqlglot for logical consistency.
    使用 sqlglot 進行 SQL 標準化，確保邏輯一致性。
    """
    try:
        # Transpile to a standard dialect (sqlite) and minified format
        # 轉譯為標準方言 (sqlite) 並進行壓縮，統一語法與格式
        return sqlglot.transpile(sql, read=None, write="sqlite", identify=True)[
            0
        ].lower()
    except Exception:
        # Fallback to simple normalization if parsing fails
        # 如果解析失敗，退回到基礎字串標準化（去多餘空格、轉小寫）
        return " ".join(sql.lower().split()).rstrip(";")


def structural_match(generated: str, expected: str) -> bool:
    """
    Check if two SQL statements are logically equivalent using AST optimization.
    使用 AST 優化檢查兩個 SQL 語句在邏輯上是否等價。

    This version ignores parameter names (e.g., :start vs :p1) by anonymizing them.
    此版本會在比對前將參數名稱匿名化（例如將 :start 與 :p1 視為相同），並能捕捉到等效邏輯。
    """
    try:
        # Step 1: Parse with sqlite dialect to generate AST
        # 步驟 1: 使用 sqlite 方言解析 SQL 語句生成 AST
        gen_ast = sqlglot.parse_one(generated, read="sqlite")
        exp_ast = sqlglot.parse_one(expected, read="sqlite")

        # Step 2: Anonymize parameters (:name -> :p) to ignore naming differences
        # 步驟 2: 參數匿名化 (:name -> :p)，確保比對時忽略參數命名慣例的差異
        def anonymize(node):
            if isinstance(node, (sqlglot.exp.Parameter, sqlglot.exp.Placeholder)):
                return sqlglot.exp.Parameter(
                    this=sqlglot.exp.Identifier(this="p", quoted=False)
                )
            return node

        gen_ast = gen_ast.transform(anonymize)
        exp_ast = exp_ast.transform(anonymize)

        # Step 3: Optimize ASTs (flattens expressions, reorders joins, normalizes logic)
        # 步驟 3: 優化 AST（展開表達式、重新排列 JOIN 順序並標準化邏輯）
        gen_optimized = optimize(gen_ast)
        exp_optimized = optimize(exp_ast)

        return gen_optimized == exp_optimized
    except Exception:
        # Fallback to string normalization comparison if parsing/optimization fails
        # 如果解析或優化失敗，退回到標準化字串比對
        return normalize_sql(generated) == normalize_sql(expected)


def result_match(generated_sql: str, expected_sql: str) -> bool:
    """
    Execute both queries and compare result sets (order-independent).
    執行兩個查詢並比對結果集（不考慮順序）。

    Returns True if both queries produce the same set of rows.
    如果兩個查詢產生相同的行集合，則返回 True。
    """
    gen_result = execute_query(generated_sql)
    exp_result = execute_query(expected_sql)

    # If either errored, they don't match
    # 如果其中一個執行出錯，則視為不匹配
    if "error" in gen_result or "error" in exp_result:
        return False

    gen_rows = gen_result.get("rows", [])
    exp_rows = exp_result.get("rows", [])

    # Compare as sets of tuples (order-independent)
    # 將每一行轉換為 tuple 並以集合 (set) 進行比對，忽略順序
    try:
        gen_set = {tuple(str(v) for v in row) for row in gen_rows}
        exp_set = {tuple(str(v) for v in row) for row in exp_rows}
        return gen_set == exp_set
    except Exception:
        return False


def exact_match(generated: str, expected: str) -> bool:
    """
    Very strict string match after basic normalization (lowercase, strip).
    極其嚴格的字串比對，僅進行基礎標準化（轉小寫、去多餘空格）。
    """

    def basic_norm(s: str) -> str:
        return " ".join(s.lower().split()).rstrip(";")

    return basic_norm(generated) == basic_norm(expected)


def evaluate_single(generated_sql: str, expected_sql: str) -> dict:
    """
    Evaluate a single generated SQL against the expected ground truth.
    針對單一生成的 SQL 與標準答案進行評估。

    Returns a dict with EX, AST-SM, EM, and normalized SQL strings.
    傳回值包含 EX、AST-SM、EM 以及標準化後的 SQL 字串。
    """
    r_match = result_match(generated_sql, expected_sql)  # 執行準確度
    s_match = structural_match(generated_sql, expected_sql)  # 結構準確度
    e_match = exact_match(generated_sql, expected_sql)  # 精確匹配度

    return {
        "EX": r_match,
        "AST-SM": s_match,
        "EM": e_match,
        "generated_normalized": normalize_sql(generated_sql),
        "expected_normalized": normalize_sql(expected_sql),
    }


if __name__ == "__main__":
    # Example usage
    gen_sql = "SELECT * FROM document d WHERE d.last_updated BETWEEN :start AND :end ORDER BY d.last_updated DESC LIMIT :n"
    exp_sql = "SELECT * FROM document d WHERE d.last_updated >= :p1 AND d.last_updated <= :p2 ORDER BY d.last_updated DESC LIMIT :p3"
    result = structural_match(gen_sql, exp_sql)
    print(result)
