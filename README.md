# 2026-06-07 小侯脫單訓練營私有連結網站

本專案由 `system/skills/transcribe`、`system/skills/transcript-site-builder` 與 `.agent/workflows/transcript_site_publish.md` 的穩定流程產出。

## 資訊架構

- `index.html`：私有連結入口
- `events/2026-06-07-dating-camp/`：重點整理頁
- `transcripts/2026-06-07-dating-camp/`：完整逐字稿頁
- `content/transcript.json`：網站資料來源

## 搜尋收錄策略

頁面已加入 `<meta name="robots" content="noindex,nofollow,noarchive">`，根目錄也有 `robots.txt` 設定 `Disallow: /`。部署後可用直接網址瀏覽，但不主動給搜尋引擎收錄。

## 來源

- `/Users/dan/Downloads/2026-06-07_脫單訓練營_1.wav`
- `/Users/dan/Downloads/2026-06-07_脫單訓練營2.wav`

第二段已更新為真正音檔並重新轉錄。
