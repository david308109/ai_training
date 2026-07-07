"""Unit test for dynamic schema selection logic."""

import logging
from app.skills.sql_generation import _build_dynamic_schema
from app.db.schema_description import SCHEMA_DESCRIPTION

def test_fallback_on_low_score():
    """Test that it falls back to full schema when max score is < 0.5."""
    retrieved = [
        {"table_name": "branches", "_score": 0.4},
        {"table_name": "customers", "_score": 0.3}
    ]
    result = _build_dynamic_schema(retrieved)
    # Should be the exact static full schema
    assert result == SCHEMA_DESCRIPTION
    print("✓ Fallback on low score passed")

def test_fallback_on_no_results():
    """Test that it falls back to full schema when no results are found."""
    result = _build_dynamic_schema([])
    assert result == SCHEMA_DESCRIPTION
    print("✓ Fallback on no results passed")

def test_dynamic_selection_with_core_tables():
    """Test that it includes core tables + high scoring tables."""
    retrieved = [
        {"table_name": "relationship_managers", "_score": 0.9},
        {"table_name": "branches", "_score": 0.1} # Too low, but it's core!
    ]
    result = _build_dynamic_schema(retrieved)
    
    # Must include core tables
    assert "TABLE: branches" in result
    assert "TABLE: customers" in result
    assert "TABLE: deposits" in result
    # Must include high scoring table
    assert "TABLE: relationship_managers" in result
    
    # Must contain join paths
    assert "=== Common Join Paths ===" in result
    print("✓ Dynamic selection with core tables passed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        test_fallback_on_low_score()
        test_fallback_on_no_results()
        test_dynamic_selection_with_core_tables()
        print("\nAll dynamic schema unit tests PASSED!")
    except AssertionError as e:
        print(f"\nTest FAILED: {e}")
