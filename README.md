# 2026-06-07 小侯脫單訓練營私有連結網站

本專案由 `system/skills/transcribe`、`system/skills/transcript-site-builder` 與 `.agent/workflows/transcript_site_publish.md` 的穩定流程產出。

## 資訊架構

- `index.html`：私有連結入口
- `events/2026-06-07-dating-camp/`：重點整理頁
- `transcripts/2026-06-07-dating-camp/`：完整逐字稿頁
- `content/transcript.json`：網站資料來源

## 發言人版本

本版逐字稿頁使用文字脈絡做保守發言人推定，並把同一推定發言人的連續片段合併成較長段落，以減少 Whisper 原始小片段造成的閱讀碎裂。這不是聲紋 diarization；若要更精準版本，可在有 HF token 與 pyannote 模型授權後重跑 `scripts/transcribe_with_speakers.sh`。

## 搜尋收錄策略

頁面已加入 `<meta name="robots" content="noindex,nofollow,noarchive">`，根目錄也有 `robots.txt` 設定 `Disallow: /`。部署後可用直接網址瀏覽，但不主動給搜尋引擎收錄。

## 來源

- `/Users/dan/Downloads/2026-06-07_脫單訓練營_1.wav`
- `/Users/dan/Downloads/2026-06-07_脫單訓練營2.wav`

第二段已更新為真正音檔並重新轉錄。
