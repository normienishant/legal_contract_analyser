-- Supabase Storage Policy for article-thumbnails bucket
-- Run this in Supabase SQL Editor to make bucket objects publicly accessible

-- Step 1: Create policy to allow public SELECT (read) access to all objects in article-thumbnails bucket
CREATE POLICY "Public Access for article-thumbnails"
ON storage.objects
FOR SELECT
USING (bucket_id = 'article-thumbnails');

-- Step 2: Create policy to allow authenticated users to INSERT (upload) objects
CREATE POLICY "Authenticated users can upload to article-thumbnails"
ON storage.objects
FOR INSERT
WITH CHECK (
  bucket_id = 'article-thumbnails' 
  AND auth.role() = 'authenticated'
);

-- Step 3: Create policy to allow authenticated users to UPDATE objects
CREATE POLICY "Authenticated users can update article-thumbnails"
ON storage.objects
FOR UPDATE
USING (
  bucket_id = 'article-thumbnails' 
  AND auth.role() = 'authenticated'
);

-- Step 4: Create policy to allow authenticated users to DELETE objects
CREATE POLICY "Authenticated users can delete article-thumbnails"
ON storage.objects
FOR DELETE
USING (
  bucket_id = 'article-thumbnails' 
  AND auth.role() = 'authenticated'
);

-- Alternative: If you want to allow anonymous uploads (for backend service)
-- Uncomment the following policy instead of Step 2:
/*
CREATE POLICY "Anonymous upload to article-thumbnails"
ON storage.objects
FOR INSERT
WITH CHECK (bucket_id = 'article-thumbnails');
*/

