# 🔧 FFmpeg Installation Fix

## The Lock File Error

You're seeing: `Unable to obtain lock file access` because Chocolatey needs administrator permissions.

---

## ✅ Solution: Run as Administrator

### Step 1: Close Current Terminal

Close your current PowerShell window.

### Step 2: Open PowerShell as Admin

1. Press `Windows Key`
2. Type: `PowerShell`
3. **Right-click** on "Windows PowerShell"
4. Select: **"Run as administrator"**
5. Click "Yes" if prompted by UAC

### Step 3: Install FFmpeg

In the admin PowerShell window, run:

```powershell
choco install ffmpeg -y
```

**Expected output:**
```
Chocolatey v2.x.x
Installing the following packages:
ffmpeg
...
The install of ffmpeg was successful.
```

### Step 4: Verify Installation

```powershell
ffmpeg -version
```

**Should show:**
```
ffmpeg version 8.1.1
...
configuration: --enable-gpl --enable-version3
```

### Step 5: Continue Video Generator Setup

Now go back to your regular terminal:

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
```

---

## 🔄 Alternative: Manual Installation (If Chocolatey Still Fails)

If Chocolatey continues to have issues:

### Download FFmpeg Manually:

1. **Download:** https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. **Extract** to: `C:\ffmpeg`
3. **Add to PATH:**
   - Press `Windows Key` → Search "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables" button
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\ffmpeg\bin`
   - Click OK on all windows

4. **Restart terminal** and verify:
   ```bash
   ffmpeg -version
   ```

---

## 🆘 Still Having Issues?

### Check if FFmpeg is already installed:

```powershell
ffmpeg -version
```

If you see version info, **FFmpeg is already installed!** You can skip this step and continue with:

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
```

### Remove Chocolatey lock manually:

If Chocolatey is stuck:

```powershell
# As Administrator
Remove-Item "C:\ProgramData\chocolatey\lib\c00565a56f0e64a50f2ea5badcb97694d43e0755" -Recurse -Force
choco install ffmpeg -y
```

---

## ✅ Once FFmpeg is Installed

Continue with video generator setup:

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
```

This will install all remaining dependencies (Node.js packages, Playwright, Python packages).

---

## 💡 Quick Summary

**Problem:** Chocolatey lock file error  
**Cause:** Missing admin permissions  
**Solution:** Run PowerShell as Administrator

**Commands:**
```powershell
# In Admin PowerShell:
choco install ffmpeg -y
ffmpeg -version

# Then in regular terminal:
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
```

That's it! 🚀
