# 完全離線 Python 桌面監控系統實作計畫（Windows）

## 1) 需求與範圍

### 需求
- 24 小時螢幕畫面監控。
- 即時影像判斷（本地模型或規則）。
- 自動建立 log（至少包含時間與檔名）。
- 可在 Windows 直接運行。
- 不使用任何網路 API（全離線）。

### 非目標（初期）
- 雲端同步、遠端通知、線上訓練。
- 跨平台 UI 最佳化（先以 Windows 為主）。

---

## 2) 推薦技術棧

- UI：`PySide6`
- 螢幕擷取：`mss`
- 影像處理：`opencv-python`
- 本地推論：`onnxruntime`（搭配 ONNX 模型）
- 本地儲存：`sqlite3`（Python 內建）
- 打包：`PyInstaller`

> 全部可離線部署；模型檔（`.onnx`）與字典檔案均放在本機目錄。

---

## 3) 系統架構

```text
UI (PySide6)
  ├─ Monitor Controller
  │   ├─ Capture Worker (mss)
  │   ├─ Inference Worker (OpenCV/ONNX Runtime)
  │   └─ Logger Worker (SQLite + 檔案系統)
  ├─ Health Monitor (CPU/RAM/Queue)
  └─ Config Manager (JSON)
```

### 核心流程
1. Capture Worker 以固定 FPS 擷取螢幕。
2. 將影格放入佇列（Queue）。
3. Inference Worker 做即時判斷。
4. 事件觸發時輸出截圖檔並寫入 SQLite log。
5. UI 持續顯示健康狀態與最近事件。

---

## 4) 專案目錄建議

```text
offline_monitor/
  app/
    main.py
    ui/
      main_window.py
    core/
      capture.py
      inference.py
      logger.py
      retention.py
      health.py
    config/
      default.json
    models/
      detector.onnx
    storage/
      app.db
      captures/
  scripts/
    run_dev.ps1
    build_windows.ps1
  requirements.txt
  README.md
```

---

## 5) Log 與資料規格

### SQLite 表（`events`）
- `id` INTEGER PRIMARY KEY
- `timestamp` TEXT NOT NULL
- `event_type` TEXT NOT NULL
- `confidence` REAL
- `file_name` TEXT NOT NULL
- `screen_id` INTEGER
- `region` TEXT
- `extra_json` TEXT

### 檔名格式
- `cap_YYYYMMDD_HHMMSS_mmm.jpg`

### 文字 log（選配）
- `2026-02-07 14:23:05.421, ALERT_WINDOW, 0.91, cap_20260207_142305_421.jpg`

---

## 6) 24 小時穩定運行設計

- 以固定 FPS（例如 5~15）運行，避免 CPU 爆滿。
- Capture 與 Inference 解耦（Producer/Consumer Queue）。
- Queue 設上限，超過時丟棄最舊影格避免積壓。
- Worker 心跳（每 30~60 秒）寫入健康資訊。
- 例外處理與自動重啟 worker。
- 每日輪替資料夾與容量保護（例如上限 50GB）。
- 開機自啟（Windows 工作排程器或啟動資料夾）。

---

## 7) 開發里程碑

### Milestone A：MVP（1 週）
- UI 啟停
- 螢幕擷取 + 截圖落地
- SQLite log 寫入

**驗收**：連跑 2 小時，無崩潰。

### Milestone B：即時判斷（第 2 週）
- OpenCV 規則型判斷（模板匹配/區域偵測）
- 事件觸發與 confidence 記錄

**驗收**：目標 FPS 穩定、誤報率可接受。

### Milestone C：AI 推論（第 3 週）
- 接 ONNX Runtime + 本地模型
- 可在 UI 調整閾值

**驗收**：推論延遲與準確率達標。

### Milestone D：部署（第 4 週）
- PyInstaller 打包
- 安裝與運維文件

**驗收**：Windows 無 Python 環境可直接執行。

---

## 8) 安全與合規建議

- 明確告知使用者正在監控（UI 狀態與托盤圖示）。
- 依資料治理要求設定保留天數（例如 7/30 天）。
- 敏感畫面可做遮罩（PII 區域）。
- log 與截圖路徑需權限控管。

---

## 9) 風險與對策

- **效能不足**：降低 FPS、改用 ROI、調整模型大小。
- **磁碟爆滿**：啟用容量上限與自動清理。
- **誤報偏高**：增加後處理（連續 N 幀才觸發）。
- **UI 卡頓**：所有重任務放背景執行緒。

---

## 10) 下一步（可直接執行）

1. 先實作 MVP：`capture + sqlite log + ui start/stop`。
2. 加入最小事件判斷（例如模板匹配）。
3. 壓測 24 小時並記錄 CPU/RAM/磁碟變化。
4. 最後接 ONNX 模型並完成 Windows 打包。


---

## 11) Windows 打包落地（已提供腳本）

本專案已提供可直接使用的 PowerShell 腳本：

- `scripts/build_windows.ps1`：建立虛擬環境、安裝依賴、執行 PyInstaller。
- `scripts/run_dev.ps1`：本機開發啟動。

### 一鍵打包

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

### 打包輸出

```text
dist/offline-monitor/offline-monitor.exe
```

### 常見注意事項

- 若 PowerShell 執行策略限制，請使用 `-ExecutionPolicy Bypass`。
- 若缺少 VC++ Runtime，請在目標機安裝 Microsoft Visual C++ Redistributable。
- 首次安裝依賴較慢屬正常。
