#!/usr/bin/env python3
"""
Test script to verify that the SQL query parser correctly replaces SELECT clauses with SELECT *.
"""

from src.realtor_buddy.langchain_agent.sql_agent import SQLQueryParser

def test_select_star_replacement():
    """Test the SQL query parser's ability to replace SELECT clauses with SELECT *."""
    parser = SQLQueryParser()
    
    test_cases = [
        {
            "input": "SELECT id, title, price FROM agency_properties WHERE lokacija LIKE '%Zagreb%' LIMIT 20",
            "expected": "SELECT * FROM agency_properties WHERE lokacija LIKE '%Zagreb%' LIMIT 20",
            "description": "Basic SELECT with specific columns"
        },
        {
            "input": "SELECT id, title, price, lokacija, broj_soba, povrsina FROM agency_properties WHERE price < 200000 ORDER BY price ASC LIMIT 20",
            "expected": "SELECT * FROM agency_properties WHERE price < 200000 ORDER BY price ASC LIMIT 20",
            "description": "SELECT with multiple columns and ORDER BY"
        },
        {
            "input": "```sql\nSELECT id, title FROM agency_properties\n```",
            "expected": "SELECT * FROM agency_properties",
            "description": "SQL in markdown code block"
        },
        {
            "input": "```\nSELECT id, title FROM agency_properties\n```",
            "expected": "SELECT * FROM agency_properties",
            "description": "SQL in generic code block"
        },
        {
            "input": "SELECT * FROM agency_properties WHERE price > 100000",
            "expected": "SELECT * FROM agency_properties WHERE price > 100000",
            "description": "Already has SELECT * (should remain unchanged)"
        },
        {
            "input": "SELECT id, price FROM agency_properties WHERE lokacija LIKE '%Rijeka%'\nSQLResult: | id | price |\n| --- | --- |",
            "expected": "SELECT * FROM agency_properties WHERE lokacija LIKE '%Rijeka%'",
            "description": "SQL with SQLResult formatting should be cleaned"
        }
    ]
    
    print("Testing SQL Query Parser - SELECT * Replacement...")
    print("=" * 60)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Input:    {test_case['input']!r}")
        
        result = parser.parse(test_case['input'])
        print(f"Output:   {result!r}")
        print(f"Expected: {test_case['expected']!r}")
        
        if result == test_case['expected']:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    success = test_select_star_replacement()
    import sys
    sys.exit(0 if success else 1)