# 🔍 How to Find Existing PostgreSQL Database on Render

## Method 1: Dashboard me Check

1. **Render Dashboard** me jao: https://dashboard.render.com
2. **Left sidebar** me dekho:
   - "Databases" section me click karo
   - Ya "Services" section me jao
3. **List me dekho:**
   - Agar database hai, woh dikhega
   - Name: `contract-analyzer-db` ya kuch similar

---

## Method 2: Different Name se Create

Agar database nahi mila, **naya name se create karo:**

### Option A: Unique Name
```
contract-analyzer-db-2024
contract-analyzer-db-v2
legal-contract-db
contract-analyzer-prod
```

### Option B: Random Suffix
```
contract-analyzer-db-abc123
contract-analyzer-db-xyz
```

---

## Method 3: Existing Database Use

Agar database mil gaya:

1. **Database service** me jao
2. **"Connect"** button click karo
3. **"Internal Database URL"** copy karo
4. **Backend service** me use karo

---

## Quick Fix: New Name se Create

1. **"New +"** → **"PostgreSQL"**
2. **Name:** `contract-analyzer-db-v2` (ya koi unique name)
3. **Rest same settings**
4. **Create**

---

**Note:** Agar pehle wala database delete ho gaya ho, toh woh nahi milega. Naya create karna hoga.

