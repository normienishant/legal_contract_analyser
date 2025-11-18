# 🔧 RENDER START COMMAND FIX

## ❌ Current Error
```
ModuleNotFoundError: No module named 'app.models'
```

## ✅ Solution

### Step 1: Update Start Command in Render

1. Go to **Render Dashboard** → Your Backend Service
2. Click **"Settings"** tab
3. Scroll to **"Start Command"**
4. **Replace** the current command with:

```
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Click **"Save Changes"**

### Step 2: Manual Redeploy

1. Go to **"Manual Deploy"** tab
2. Click **"Deploy latest commit"**
3. Wait for deployment

---

## Why This Works

- `python -m uvicorn` ensures Python path is set correctly
- It runs uvicorn as a module, which handles imports better
- This is the same command used in local development

---

## Alternative (If Still Doesn't Work)

If the above doesn't work, try this start command:

```
cd /opt/render/project/src/backend && PYTHONPATH=/opt/render/project/src/backend:$PYTHONPATH python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## ✅ All Fixes Applied

1. ✅ Added missing `__init__.py` files
2. ✅ Fixed `app/models/__init__.py` to avoid circular imports
3. ✅ Updated `.gitignore` to not ignore `app/models`
4. ✅ Updated start command to use `python -m uvicorn`

---

**Ab Render me start command update karo aur redeploy karo!**

