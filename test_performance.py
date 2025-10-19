#!/usr/bin/env python3
"""
Performance testing script for the coachfinder application.
Tests performance with and without database indexes.
"""

import time
import statistics
import requests

def test_performance(base_url="http://localhost:5000", pages=5):
    """Test performance of the application"""
    print(f"Testing performance for {pages} pages...")

    times = []

    for page in range(1, pages + 1):
        url = f"{base_url}/{page}" if page > 1 else base_url
        print(f"Testing page {page}...")

        start_time = time.time()
        try:
            response = requests.get(url, timeout=30)
            end_time = time.time()

            elapsed = end_time - start_time
            times.append(elapsed)

            print(f"  Page {page}: {elapsed:.2f}s (Status: {response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"  Page {page}: Error - {e}")
            times.append(float('inf'))

    if times and all(t != float('inf') for t in times):
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)

        print("\nPerformance Summary:")
        print(f"  Average time: {avg_time:.2f}s")
        print(f"  Min time: {min_time:.2f}s")
        print(f"  Max time: {max_time:.2f}s")
        print(f"  All times: {[f'{t:.2f}s' for t in times]}")
    else:
        print("Performance test failed - could not connect to server")

    return times

if __name__ == "__main__":
    test_performance()
