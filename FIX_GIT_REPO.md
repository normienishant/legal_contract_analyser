# 🔧 Fix Git Repository Structure

## ❌ Problem Found!

**Files full path ke saath push ho rahe hain:**
- `OneDrive/Desktop/ai doc anal/...`

**Iska matlab:** Git repository root `OneDrive` ya `Desktop` folder me hai, `ai doc anal` me nahi!

---

## ✅ Solution: Fix Repository Structure

### Option 1: Move .git to Project Folder (Recommended)

```powershell
# 1. Find where .git folder is
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"
git rev-parse --show-toplevel

# 2. If .git is in parent folder, move it:
# (First, backup current repo)
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"
git clone https://github.com/normienishant/legal_contract_analyser.git temp_repo
cd temp_repo
# Copy .git folder to ai doc anal
Copy-Item -Path ".git" -Destination "..\ai doc anal\" -Recurse -Force
cd ..
Remove-Item -Path "temp_repo" -Recurse -Force

# 3. Fix paths
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"
git add .
git commit -m "Fix repository structure"
git push
```

### Option 2: Fresh Start (Easier)

```powershell
# 1. Remove old .git (if in wrong place)
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"
# Check if .git exists here
if (Test-Path ".git") {
    Write-Host "Git repo is here - good!"
} else {
    Write-Host "Need to initialize here"
}

# 2. Initialize fresh repo in project folder
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"
git init
git add .
git commit -m "Initial commit - Contract Analyzer"

# 3. Connect to GitHub (replace old remote)
git remote remove origin
git remote add origin https://github.com/normienishant/legal_contract_analyser.git

# 4. Force push (careful!)
git push -u origin master --force
```

---

## 🔍 Check Current Structure

```powershell
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal"
git rev-parse --show-toplevel
```

**Expected:** `C:\Users\nisha\OneDrive\Desktop\ai doc anal`  
**If different:** Problem hai!

---

## ⚠️ Important

Agar `--force` push karte ho:
- GitHub pe existing files overwrite ho jayenge
- But structure sahi ho jayega

**Pehle check karo kahan .git folder hai!**

