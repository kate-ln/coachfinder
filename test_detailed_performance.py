#!/usr/bin/env python3
"""
Detailed performance testing script that tests specific database operations.
"""

import requests
import time
import statistics

def test_detailed_performance(base_url="http://localhost:5000"):
    """Test detailed performance of specific operations"""
    print("Testing detailed performance...")
    
    # Test main page performance
    print("\n=== Main Page Performance ===")
    main_page_times = []
    for i in range(5):
        start_time = time.time()
        response = requests.get(base_url, timeout=30)
        end_time = time.time()
        elapsed = end_time - start_time
        main_page_times.append(elapsed)
        print(f"  Request {i+1}: {elapsed:.3f}s")
    
    avg_main = statistics.mean(main_page_times)
    print(f"  Average main page time: {avg_main:.3f}s")
    
    # Test pagination performance
    print("\n=== Pagination Performance ===")
    page_times = []
    for page in range(1, 11):  # Test 10 pages
        start_time = time.time()
        response = requests.get(f"{base_url}/{page}", timeout=30)
        end_time = time.time()
        elapsed = end_time - start_time
        page_times.append(elapsed)
        print(f"  Page {page}: {elapsed:.3f}s")
    
    avg_pages = statistics.mean(page_times)
    print(f"  Average page time: {avg_pages:.3f}s")
    
    # Test search performance
    print("\n=== Search Performance ===")
    search_times = []
    search_terms = ["Tennis", "Helsinki", "Aloittelija", "test", "sport"]
    for term in search_terms:
        start_time = time.time()
        response = requests.get(f"{base_url}/find_announcement?query={term}", timeout=30)
        end_time = time.time()
        elapsed = end_time - start_time
        search_times.append(elapsed)
        print(f"  Search '{term}': {elapsed:.3f}s")
    
    avg_search = statistics.mean(search_times)
    print(f"  Average search time: {avg_search:.3f}s")
    
    # Summary
    print(f"\n=== Performance Summary ===")
    print(f"Main page average: {avg_main:.3f}s")
    print(f"Pagination average: {avg_pages:.3f}s") 
    print(f"Search average: {avg_search:.3f}s")
    print(f"Overall average: {statistics.mean([avg_main, avg_pages, avg_search]):.3f}s")
    
    return {
        'main_page': avg_main,
        'pagination': avg_pages,
        'search': avg_search
    }

if __name__ == "__main__":
    test_detailed_performance()
