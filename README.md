# Vynnify Aim Tweaks 2.0

A clean Vynnify-branded Windows desktop app for sensitivity calculations, reaction training, profiles, and conservative Windows optimization.

## Build the Windows EXE

### Easiest: GitHub Actions (free)
1. Create a GitHub repository and upload this folder.
2. Push the files, including `.github/workflows/build-windows.yml`.
3. Open **Actions** → **Build Vynnify Aim Tweaks** → **Run workflow**.
4. When it finishes, open the workflow run and download the **Vynnify-Aim-Tweaks-Windows** artifact.

### Local Windows build
1. Install Python 3.12+.
2. Double-click `build_windows.bat`.
3. The EXE will be in `dist`.
4. To make an installer, install Inno Setup and compile `installer.iss`.

The app does not automate aiming, recoil, clicks, game memory, or anti-cheat bypasses.
