# NTNUx Backend

本資料夾負責爬取 NTNU 課程網資料，透過 Selenium 觸發操作，並搭配 mitmproxy 擷取後端 API 回應。

## 📁 檔案與資料夾說明

### main.py

主流程控制器。執行此檔將同時：

1. 啟動 mitmproxy 攔截器（使用 `hook/save.py` 腳本）
2. 啟動瀏覽器並模擬操作以觸發課程 API 請求（使用 `crawl/browser.py`）

### crawl/browser.py

使用 Selenium 控制 Chrome 瀏覽器，模擬使用者操作以發送課程查詢請求。

### hook/save.py

mitmproxy 腳本，攔截課程 API 的 JSON 回應，並將其追加寫入 `data/courses.json`。

### tool/proxy.py

封裝 `mitmdump` 的啟動流程，作為子程序啟動 `hook/save.py`。

### data/courses.json

儲存由 mitmproxy 擷取到的課程資料，為 JSON 陣列結構。

### requirements.txt

列出執行本專案所需的 Python 套件（如 selenium、mitmproxy）。

## 🚀 使用方式

```bash
cd backend
python main.py
```

## 📦 套件安裝

```bash
pip install -r requirements.txt
```