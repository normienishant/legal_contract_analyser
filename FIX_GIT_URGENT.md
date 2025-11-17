# ⚠️ URGENT: Git Repository Fix Required!

## ❌ MAJOR PROBLEM FOUND!

**Git repository root:** `C:/Users/nisha`  
**This means:** Entire user folder is being tracked! ❌

**Files push ho rahe hain with path:** `OneDrive/Desktop/ai doc anal/...`

---

## ✅ SOLUTION: Fresh Repository in Project Folder

### Step 1: Remove Old Git (if exists in wrong place)

```powershell
# DON'T delete .git from Users/nisha yet!
# First, let's create proper repo in project folder
```

### Step 2: Create Fresh Repo in Project Folder

```powershell
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"

# Remove old remote connection (if any)
git remote remove origin 2>$null

# Initialize fresh git repo HERE
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Contract Analyzer with user isolation"

# Connect to GitHub
git remote add origin https://github.com/normienishant/legal_contract_analyser.git

# Force push (this will overwrite GitHub repo with correct structure)
git push -u origin master --force
```

---

## ⚠️ WARNING

`--force` push se:
- GitHub pe existing files overwrite ho jayenge
- But structure sahi ho jayega
- Sirf project files push hongi (not entire user folder)

---

## ✅ After Fix

GitHub pe sirf ye dikhega:
```
contract-analyzer/
├── backend/
├── frontend/
├── ml_data/
└── ...
```

**NOT:**
```
OneDrive/
└── Desktop/
    └── ai doc anal/
        └── ...
```

---

**Ye fix karo immediately!** 🚨

