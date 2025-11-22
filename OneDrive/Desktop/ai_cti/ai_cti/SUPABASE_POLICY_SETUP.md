# Supabase Storage Policy Setup for Thumbnails

## Problem
Bucket is marked "Public" but objects return 400 errors because **no policies are created**.

## Solution: Create Storage Policies

### Method 1: Using Supabase Dashboard (Easiest)

1. **Go to Storage → Files → Policies tab** (you're already there!)

2. **Click "New policy" button** next to "ARTICLE-THUMBNAILS" bucket

3. **Create a SELECT policy for public access:**
   - Policy name: `Public Access for article-thumbnails`
   - Allowed operation: `SELECT`
   - Target roles: `public` (or `anon`)
   - USING expression: `bucket_id = 'article-thumbnails'`
   - Click "Review" then "Save policy"

4. **Create an INSERT policy for authenticated uploads:**
   - Click "New policy" again
   - Policy name: `Authenticated upload to article-thumbnails`
   - Allowed operation: `INSERT`
   - Target roles: `authenticated`
   - WITH CHECK expression: `bucket_id = 'article-thumbnails'`
   - Click "Review" then "Save policy"

### Method 2: Using SQL Editor (Faster)

1. **Go to SQL Editor** in Supabase dashboard

2. **Run this SQL:**
   ```sql
   -- Allow public read access
   CREATE POLICY "Public Access for article-thumbnails"
   ON storage.objects
   FOR SELECT
   USING (bucket_id = 'article-thumbnails');
   
   -- Allow authenticated uploads
   CREATE POLICY "Authenticated upload to article-thumbnails"
   ON storage.objects
   FOR INSERT
   WITH CHECK (
     bucket_id = 'article-thumbnails' 
     AND auth.role() = 'authenticated'
   );
   ```

3. **Click "Run"**

### Method 3: Using Service Role (For Backend)

If your backend uses service role key (not authenticated user), use this instead:

```sql
-- Allow service role to upload (no auth check)
CREATE POLICY "Service role upload to article-thumbnails"
ON storage.objects
FOR INSERT
WITH CHECK (bucket_id = 'article-thumbnails');

-- Allow public read
CREATE POLICY "Public Access for article-thumbnails"
ON storage.objects
FOR SELECT
USING (bucket_id = 'article-thumbnails');
```

## Verify

After creating policies:

1. **Check Policies tab** - should show policies under "ARTICLE-THUMBNAILS"
2. **Test a URL** - try accessing:
   ```
   https://krhvbebqvefdcdlyuqvz.supabase.co/storage/v1/object/public/article-thumbnails/67c880cacfd4a218.jpg
   ```
   Should return 200, not 400

3. **Run backend again** - thumbnails should upload and be accessible!

## Troubleshooting

- **Still getting 400?** Check bucket name is exactly `article-thumbnails` (lowercase)
- **403 Forbidden?** Policy might not be active, check it's enabled
- **Upload fails?** Make sure INSERT policy allows your auth method (authenticated/service role)

