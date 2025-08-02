# openai-actions-demo

此範例提供一個簡單的 Python 指令稿，可將指定圖檔依預定時間自動上傳到 Pinterest，並設定對應標題與描述。

## 使用方法

1. 安裝套件：
   ```bash
   pip install -r requirements.txt
   ```
2. 準備排程檔 `pins.example.json`，內容包含圖檔路徑、標題、描述與預計發佈時間。
3. 設定環境變數 `PINTEREST_ACCESS_TOKEN` 為你的 Pinterest Access Token。
4. 執行指令：
   ```bash
   python pinterest_scheduler.py pins.example.json
   ```

程式會依序呼叫 Pinterest API 建立排程貼文。
可加入 `--dry-run` 參數僅顯示將會執行的動作，不實際呼叫 API。
