"""Simple acceptance test: POST a single query to the running API and print the response."""

import json
import sys

import requests

API_URL = "http://127.0.0.1:8000/query"


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else API_URL
    question = "Who has the highest total deposit?"

    print(f"Sending query to {url}")
    print(f"Question: {question}\n")

    resp = requests.post(url, json={"query": question}, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    print("=" * 50)
    print("Answer:")
    print(data.get("answer", "(no answer)"))
    print()
    print("Generated SQL:")
    print(data.get("generated_sql", "(none)"))
    print()
    print("Query Result:")
    print(json.dumps(data.get("query_result"), indent=2, ensure_ascii=False))

    if data.get("error"):
        print(f"\nError: {data['error']}")


if __name__ == "__main__":
    main()
