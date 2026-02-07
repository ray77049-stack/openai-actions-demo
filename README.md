# openai-actions-demo

## Offline Python Desktop Monitoring Plan

- 規劃文件：`docs/offline-python-desktop-monitoring-plan.md`
- MVP 啟動程式：`app/main.py`
- Windows 開發啟動腳本：`scripts/run_dev.ps1`
- Windows 打包腳本：`scripts/build_windows.ps1`

## 完成 Windows 打包（PyInstaller）

1. 在 Windows PowerShell 進入專案根目錄。
2. 執行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

3. 產物會在：

```text
dist/offline-monitor/offline-monitor.exe
```

> `build_windows.ps1` 會自動建立 `.venv`、安裝 `requirements.txt`，再呼叫 PyInstaller 打包。
