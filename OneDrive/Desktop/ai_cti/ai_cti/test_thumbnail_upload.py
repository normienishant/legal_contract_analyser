#!/usr/bin/env python3
"""
Quick test script to verify Supabase storage bucket configuration and thumbnail upload.
Run this to diagnose thumbnail issues.
"""
import os
import sys
import requests
from io import BytesIO

try:
    from supabase import create_client
except ImportError:
    print("ERROR: supabase package not installed. Run: pip install supabase")
    sys.exit(1)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_IMAGE_BUCKET = os.getenv("SUPABASE_IMAGE_BUCKET", "article-thumbnails")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY environment variables must be set")
    sys.exit(1)

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_IMAGE_BUCKET: {SUPABASE_IMAGE_BUCKET}")
print("-" * 60)

# Create client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
image_storage = supabase.storage.from_(SUPABASE_IMAGE_BUCKET)

# Test 1: List buckets
print("\n[TEST 1] Checking available buckets...")
try:
    buckets = supabase.storage.list_buckets()
    print(f"Available buckets: {[b.name for b in buckets]}")
    bucket_names = [b.name for b in buckets]
    if SUPABASE_IMAGE_BUCKET not in bucket_names:
        print(f"⚠️  WARNING: Bucket '{SUPABASE_IMAGE_BUCKET}' not found in available buckets!")
        print(f"   Available buckets: {bucket_names}")
        print(f"   Please create the bucket '{SUPABASE_IMAGE_BUCKET}' in Supabase dashboard")
except Exception as e:
    print(f"ERROR listing buckets: {e}")

# Test 2: Try to upload a test image
print(f"\n[TEST 2] Testing upload to bucket '{SUPABASE_IMAGE_BUCKET}'...")
test_key = "test_thumbnail_123.jpg"
test_image_data = b"fake_image_data_for_testing"

try:
    buffer = BytesIO(test_image_data)
    result = image_storage.upload(test_key, buffer, {"content-type": "image/jpeg"})
    print(f"✓ Upload successful: {result}")
except Exception as e:
    error_str = str(e).lower()
    if "already exists" in error_str or "duplicate" in error_str or "409" in error_str:
        print(f"✓ File already exists (that's okay)")
    else:
        print(f"✗ Upload failed: {e}")
        print(f"   This might mean the bucket doesn't exist or you don't have permissions")

# Test 3: Try to get public URL
print(f"\n[TEST 3] Testing public URL generation...")
try:
    result = image_storage.get_public_url(test_key)
    print(f"get_public_url() returned: {result} (type: {type(result)})")
    if isinstance(result, dict):
        url = result.get("publicUrl") or result.get("publicURL") or result.get("public_url")
        print(f"Extracted URL from dict: {url}")
    elif isinstance(result, str):
        url = result
        print(f"URL (string): {url}")
    else:
        url = None
        print(f"Could not extract URL from result")
except Exception as e:
    print(f"✗ get_public_url() failed: {e}")
    url = None

# Test 4: Manual URL construction
print(f"\n[TEST 4] Testing manual URL construction...")
manual_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_IMAGE_BUCKET}/{test_key}"
print(f"Manual URL: {manual_url}")

# Test 5: Verify URL accessibility
print(f"\n[TEST 5] Testing URL accessibility...")
if url:
    print(f"Testing URL: {url}")
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        print(f"HEAD request status: {resp.status_code}")
        if resp.status_code == 200:
            print("✓✓✓ URL is accessible!")
        elif resp.status_code == 404:
            print("✗✗✗ URL returned 404 - bucket might not be public or file doesn't exist")
            print("   SOLUTION: Go to Supabase Dashboard > Storage > {bucket_name}")
            print("   Make sure 'Public bucket' is checked!")
        else:
            print(f"✗ URL returned {resp.status_code}")
    except Exception as e:
        print(f"✗ Could not access URL: {e}")

print(f"\nTesting manual URL: {manual_url}")
try:
    resp = requests.head(manual_url, timeout=10, allow_redirects=True)
    print(f"HEAD request status: {resp.status_code}")
    if resp.status_code == 200:
        print("✓✓✓ Manual URL is accessible!")
    elif resp.status_code == 404:
        print("✗✗✗ Manual URL returned 404")
    else:
        print(f"✗ Manual URL returned {resp.status_code}")
except Exception as e:
    print(f"✗ Could not access manual URL: {e}")

# Test 6: List files in bucket
print(f"\n[TEST 6] Listing files in bucket...")
try:
    files = image_storage.list()
    print(f"Files in bucket: {len(files) if files else 0}")
    if files:
        print(f"First 5 files: {files[:5]}")
except Exception as e:
    print(f"✗ Could not list files: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
print("\nIf upload failed or URLs return 404:")
print("1. Go to Supabase Dashboard > Storage")
print(f"2. Check if bucket '{SUPABASE_IMAGE_BUCKET}' exists")
print("3. Make sure the bucket is set to 'Public bucket'")
print("4. Check bucket policies allow public read access")

