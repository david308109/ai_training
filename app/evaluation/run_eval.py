"""CLI script to run batch evaluation against the running API."""

import json
import logging
import sys

import httpx

from app.evaluation.evaluator import evaluate_single
from app.evaluation.test_dataset import TEST_CASES

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

API_URL = "http://127.0.0.1:8000/query"


def run_evaluation(api_url: str = API_URL) -> dict:
    """Run all test cases and return summary metrics."""
    total = len(TEST_CASES)
    ex_ok = 0
    ast_sm_ok = 0
    em_ok = 0
    errors = 0
    details = []

    logger.info("=" * 60)
    logger.info("Running evaluation: %d test cases", total)
    logger.info("=" * 60)

    with httpx.Client(timeout=60.0) as client:
        for i, tc in enumerate(TEST_CASES, 1):
            question = tc["question"]
            expected_sql = tc["expected_sql"]

            logger.info("\n[%d/%d] %s", i, total, question)

            try:
                resp = client.post(api_url, json={"query": question})
                resp.raise_for_status()
                data = resp.json()
                generated_sql = data.get("generated_sql", "")

                if not generated_sql:
                    logger.warning("  ✗ No SQL generated")
                    errors += 1
                    details.append(
                        {
                            "question": question,
                            "status": "no_sql",
                            "generated_sql": "",
                            "expected_sql": expected_sql,
                        }
                    )
                    continue

                eval_result = evaluate_single(generated_sql, expected_sql)

                ex = "✓" if eval_result["EX"] else "✗"
                ast = "✓" if eval_result["AST-SM"] else "✗"
                em = "✓" if eval_result["EM"] else "✗"
                logger.info("  EX: %s | AST-SM: %s | EM: %s", ex, ast, em)
                logger.info("  Generated:  %s", generated_sql[:120])
                logger.info("  Expected:   %s", expected_sql[:120])

                if eval_result["EX"]:
                    ex_ok += 1
                if eval_result["AST-SM"]:
                    ast_sm_ok += 1
                if eval_result["EM"]:
                    em_ok += 1

                details.append(
                    {
                        "question": question,
                        "status": "ok",
                        "generated_sql": generated_sql,
                        "expected_sql": expected_sql,
                        **eval_result,
                    }
                )

            except Exception as exc:
                logger.error("  ✗ Error: %s", exc)
                errors += 1
                details.append(
                    {
                        "question": question,
                        "status": "error",
                        "error": str(exc),
                    }
                )

    summary = {
        "total": total,
        "EX": ex_ok,
        "AST-SM": ast_sm_ok,
        "EM": em_ok,
        "errors": errors,
        "EX_accuracy": f"{(ex_ok / total if total else 0) * 100:.1f}%",
        "AST_SM_accuracy": f"{(ast_sm_ok / total if total else 0) * 100:.1f}%",
        "EM_accuracy": f"{(em_ok / total if total else 0) * 100:.1f}%",
    }

    logger.info("\n%s", "=" * 60)
    logger.info("EVALUATION RESULTS")
    logger.info("=" * 60)
    logger.info("Total test cases:     %d", total)
    logger.info("EX (Execution):       %d (%s)", ex_ok, summary["EX_accuracy"])
    logger.info("AST-SM (Structural):  %d (%s)", ast_sm_ok, summary["AST_SM_accuracy"])
    logger.info("EM (Exact Match):     %d (%s)", em_ok, summary["EM_accuracy"])
    logger.info("Errors:               %d", errors)

    return {"summary": summary, "details": details}


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else API_URL
    results = run_evaluation(url)
    # Save detailed results
    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info("\nDetailed results saved to evaluation_results.json")
