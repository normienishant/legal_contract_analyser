#!/usr/bin/env python3
"""
Quick test script to check if image extraction is working
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from data_ingest.live_ingest_supabase import _extract_image_url, _get_screenshot_url, _upload_image_to_supabase

# Test URLs from recent articles
test_urls = [
    "https://www.bleepingcomputer.com/news/security/us-sanctions-russian-bulletproof-hosting-provider-media-land-over-ransomware-ties/",
    "https://thehackernews.com/2025/11/hackers-actively-exploiting-7-zip.html",
    "https://www.darkreading.com/cyber-risk/cloudflare-blames-outage-internal-error",
]

print("=" * 60)
print("Testing Image Extraction")
print("=" * 60)

for url in test_urls:
    print(f"\n[TEST] Testing: {url[:60]}...")
    
    # Test OG image extraction
    print("[TEST] 1. Extracting OG image...")
    og_image = _extract_image_url(url)
    if og_image:
        print(f"[TEST]   ✓ Found OG image: {og_image[:80]}")
        
        # Test upload
        print("[TEST] 2. Uploading to Supabase...")
        uploaded_url = _upload_image_to_supabase(og_image)
        if uploaded_url:
            print(f"[TEST]   ✓ Uploaded: {uploaded_url[:80]}")
        else:
            print(f"[TEST]   ✗ Upload failed")
            # Try screenshot as fallback
            print("[TEST] 3. Trying screenshot service...")
            screenshot_url = _get_screenshot_url(url)
            if screenshot_url:
                print(f"[TEST]   ✓ Got screenshot: {screenshot_url[:80]}")
                uploaded_url = _upload_image_to_supabase(screenshot_url)
                if uploaded_url:
                    print(f"[TEST]   ✓ Uploaded screenshot: {uploaded_url[:80]}")
                else:
                    print(f"[TEST]   ✗ Screenshot upload failed")
            else:
                print(f"[TEST]   ✗ Screenshot service failed")
    else:
        print(f"[TEST]   ✗ No OG image found")
        # Try screenshot
        print("[TEST] 2. Trying screenshot service...")
        screenshot_url = _get_screenshot_url(url)
        if screenshot_url:
            print(f"[TEST]   ✓ Got screenshot: {screenshot_url[:80]}")
            uploaded_url = _upload_image_to_supabase(screenshot_url)
            if uploaded_url:
                print(f"[TEST]   ✓ Uploaded screenshot: {uploaded_url[:80]}")
            else:
                print(f"[TEST]   ✗ Screenshot upload failed")
        else:
            print(f"[TEST]   ✗ Screenshot service failed")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)

