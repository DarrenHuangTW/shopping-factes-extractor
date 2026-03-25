#!/usr/bin/env python3
"""
Test script for the Shopping Facets Extractor
Tests the core functionality without requiring a real API key.
Integration tests require SERPAPI_KEY in .env file.
"""

import os
from dotenv import load_dotenv
from search_utils import validate_keywords, extract_refine_filters

load_dotenv()

def test_keyword_validation():
    """Test keyword validation functionality"""
    print("🧪 Testing keyword validation...")
    
    # Test valid keywords
    valid_input = "running shoes\nwinter jackets\nlow heels"
    keywords, errors = validate_keywords(valid_input, max_keywords=30)
    assert len(keywords) == 3
    assert len(errors) == 0
    print("✅ Valid keywords test passed")
    
    # Test too many keywords
    too_many = "\n".join([f"keyword{i}" for i in range(35)])
    keywords, errors = validate_keywords(too_many, max_keywords=30)
    assert len(errors) > 0
    assert "Too many keywords" in errors[0]
    print("✅ Too many keywords test passed")
    
    # Test empty input
    keywords, errors = validate_keywords("", max_keywords=30)
    assert len(errors) > 0
    assert "at least one keyword" in errors[0]
    print("✅ Empty input test passed")
    
    # Test with empty lines
    mixed_input = "valid keyword\n\n\nanother keyword\n"
    keywords, errors = validate_keywords(mixed_input, max_keywords=30)
    assert len(keywords) == 2
    assert keywords == ["valid keyword", "another keyword"]
    print("✅ Mixed input with empty lines test passed")

def test_refine_filters_extraction():
    """Test refine filters extraction with mock google_shopping API data"""
    print("\n🧪 Testing refine filters extraction...")

    # Mock SerpAPI google_shopping response
    mock_results = {
        "filters": [
            {
                "type": "Department",
                "input_type": "checkbox",
                "options": [
                    {"text": "Women's"},
                    {"text": "Men's"}
                ]
            },
            {
                "type": "Color",
                "input_type": "checkbox",
                "options": [
                    {"text": "Black"},
                    {"text": "White"},
                    {"text": "Red"}
                ]
            },
            {
                "type": "Carousel Filters",
                "options": [
                    {"text": "On sale"},
                    {"text": "New"}
                ]
            }
        ]
    }

    extracted = extract_refine_filters(mock_results, "test shoes")

    # Should extract 5 filters total (2 departments + 3 colors), Carousel Filters excluded
    assert len(extracted) == 5, f"Expected 5, got {len(extracted)}"

    # Check structure: (keyword, type, title)
    assert extracted[0] == ("test shoes", "Department", "Women's")
    assert extracted[1] == ("test shoes", "Department", "Men's")
    assert extracted[2] == ("test shoes", "Color", "Black")
    assert extracted[3] == ("test shoes", "Color", "White")
    assert extracted[4] == ("test shoes", "Color", "Red")

    print("✅ Refine filters extraction test passed")

    # Verify carousel filters are excluded
    types_extracted = [row[1] for row in extracted]
    assert "Carousel Filters" not in types_extracted
    print("✅ Carousel Filters exclusion test passed")

    # Test with no filters key present
    empty_results = {"shopping_results": []}
    extracted_empty = extract_refine_filters(empty_results, "no filters")
    assert len(extracted_empty) == 0
    print("✅ No filters test passed")

def test_csv_structure():
    """Test CSV output structure"""
    print("\n🧪 Testing CSV structure...")
    
    # Sample data
    test_data = [
        ("running shoes", "Brand", "Nike"),
        ("running shoes", "Color", "Black"),
        ("winter jacket", "Size", "Large"),
    ]
    
    # Test data structure
    for item in test_data:
        assert len(item) == 3  # keyword, type, title
        assert isinstance(item[0], str)  # keyword
        assert isinstance(item[1], str)  # type
        assert isinstance(item[2], str)  # title
    
    print("✅ CSV structure test passed")

def test_batch_processing_signature():
    """Test that the batch processing function has the correct signature"""
    print("\n🧪 Testing batch processing function signature...")
    
    from search_utils import process_keywords_batch
    import inspect
    
    # Get function signature
    sig = inspect.signature(process_keywords_batch)
    
    # Check that it has the expected parameters
    expected_params = ['keywords', 'api_key', 'gl', 'hl', 'progress_callback']
    actual_params = list(sig.parameters.keys())
    
    for param in expected_params:
        assert param in actual_params, f"Missing parameter: {param}"
    
    print("✅ Batch processing function signature test passed")

def test_integration_live_api():
    """Integration test: hit real SerpAPI with engine=google_shopping and check filters are returned"""
    print("\n🧪 Testing live API (google_shopping)...")

    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("⚠️  Skipping integration test: SERPAPI_KEY not set in .env")
        return

    from search_utils import perform_search

    results = perform_search("Office Chair", api_key, gl="us", hl="en")
    assert results is not None, "API returned None"
    assert "filters" in results, f"'filters' key missing from response. Keys found: {list(results.keys())}"

    filters = results["filters"]
    assert len(filters) > 0, "filters list is empty"

    # Verify left-panel filters exist (non-carousel)
    left_panel = [f for f in filters if f.get("type") != "Carousel Filters"]
    assert len(left_panel) > 0, "No left-panel filters found"

    # Spot-check structure — type is optional in some filter groups
    first = left_panel[0]
    assert "options" in first
    assert len(first["options"]) > 0
    assert "text" in first["options"][0]

    print(f"✅ Live API test passed — {len(left_panel)} left-panel filter groups found")
    print(f"   Filter types: {[f.get('type', '(no type)') for f in left_panel]}")


def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Shopping Facets Extractor Tests\n")

    try:
        test_keyword_validation()
        test_refine_filters_extraction()
        test_csv_structure()
        test_batch_processing_signature()
        test_integration_live_api()

        print("\n🎉 All tests passed! The application core functionality is working correctly.")
        print("\n📋 Next steps:")
        print("1. Get your SerpAPI key from https://serpapi.com/")
        print("2. Run: uv run streamlit run streamlit_app.py")
        print("3. Open http://localhost:8501 in your browser")
        print("4. Enter your API key and test with real keywords")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)