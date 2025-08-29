import os
import json
import csv
from typing import List, Dict, Any, Optional, Tuple
from serpapi.google_search import GoogleSearch


def perform_search(query: str, api_key: str, gl: str = "us", hl: str = "en") -> Optional[Dict[str, Any]]:
    """
    Perform a Google search using SerpAPI and return the results.
    
    Args:
        query: Search query string
        api_key: SerpAPI key
        gl: Country code (default: "us")
        hl: Language code (default: "en")
    
    Returns:
        Dictionary containing search results or None if failed
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "gl": gl,
        "hl": hl
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Validate if results is valid JSON
        json.dumps(results, indent=2)
        return results
        
    except Exception as e:
        print(f"Error during search for '{query}': {e}")
        return None


def extract_refine_filters(results: Dict[str, Any], query: str) -> List[Tuple[str, str, str]]:
    """
    Extract refine_search_filters data from search results.
    
    Args:
        results: Search results dictionary from SerpAPI
        query: The search query (for reference)
    
    Returns:
        List of tuples containing (keyword, filter_type, title)
    """
    if "refine_search_filters" not in results:
        return []
    
    extracted_data = []
    filters = results["refine_search_filters"]
    
    for filter_group in filters:
        filter_type = filter_group.get("type", "Unknown")
        options = filter_group.get("options", [])
        
        for option in options:
            title = option.get("title", "Unknown")
            extracted_data.append((query, filter_type, title))
    
    return extracted_data


def save_consolidated_csv(all_data: List[Tuple[str, str, str]], filename: str) -> bool:
    """
    Save consolidated refine filters data to CSV file.
    
    Args:
        all_data: List of tuples containing (keyword, filter_type, title)
        filename: Output CSV filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Keyword', 'Type', 'Title'])  # Header
            writer.writerows(all_data)
        return True
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return False


def process_keywords_batch(keywords: List[str], api_key: str, gl: str = "us", hl: str = "en",
                          progress_callback=None) -> Tuple[List[Tuple[str, str, str]], List[str], List[Dict[str, Any]]]:
    """
    Process multiple keywords and extract refine filters from each.
    
    Args:
        keywords: List of search keywords
        api_key: SerpAPI key
        gl: Country code (default: "us")
        hl: Language code (default: "en")
        progress_callback: Optional callback function to report progress
    
    Returns:
        Tuple of (all_extracted_data, failed_keywords, search_metadata_list)
    """
    all_data = []
    failed_keywords = []
    search_metadata_list = []
    
    for i, keyword in enumerate(keywords):
        if progress_callback:
            progress_callback(i, len(keywords), keyword)
        
        # Perform search
        results = perform_search(keyword.strip(), api_key, gl, hl)
        
        if results is None:
            failed_keywords.append(keyword)
            continue
        
        # Extract search metadata
        if "search_metadata" in results:
            metadata = results["search_metadata"].copy()
            metadata["keyword"] = keyword.strip()
            search_metadata_list.append(metadata)
        
        # Extract refine filters
        extracted_data = extract_refine_filters(results, keyword.strip())
        all_data.extend(extracted_data)
    
    return all_data, failed_keywords, search_metadata_list


def validate_keywords(keywords_text: str, max_keywords: int = 30) -> Tuple[List[str], List[str]]:
    """
    Validate and clean keywords input.
    
    Args:
        keywords_text: Raw text input containing keywords
        max_keywords: Maximum number of keywords allowed
    
    Returns:
        Tuple of (valid_keywords, error_messages)
    """
    errors = []
    
    if not keywords_text.strip():
        errors.append("Please enter at least one keyword.")
        return [], errors
    
    # Split by lines and clean
    keywords = [line.strip() for line in keywords_text.strip().split('\n') if line.strip()]
    
    if len(keywords) == 0:
        errors.append("Please enter at least one valid keyword.")
        return [], errors
    
    if len(keywords) > max_keywords:
        errors.append(f"Too many keywords. Maximum allowed: {max_keywords}, provided: {len(keywords)}")
        return [], errors
    
    # Check for empty keywords
    empty_lines = [i+1 for i, keyword in enumerate(keywords) if not keyword]
    if empty_lines:
        errors.append(f"Empty keywords found at lines: {', '.join(map(str, empty_lines))}")
    
    # Remove empty keywords
    valid_keywords = [k for k in keywords if k]
    
    return valid_keywords, errors




