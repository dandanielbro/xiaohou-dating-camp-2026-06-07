#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PART1_JSON = REPO / "output/transcribe/2026-06-07-dating-camp/2026-06-07_脫單訓練營_1.json"
PART2_JSON = REPO / "output/transcribe/2026-06-07-dating-camp/2026-06-07_脫單訓練營2.json"
CONTENT = ROOT / "content"
EVENT_SLUG = "2026-06-07-dating-camp"
EVENT_DIR = ROOT / "events" / EVENT_SLUG
TRANSCRIPT_DIR = ROOT / "transcripts" / EVENT_SLUG


PART1_SECTIONS = [
    {
        "id": "section-01",
        "start": 0,
        "end": 190,
        "kicker": "Interaction Design",
        "title": "讓聊天與不聊天的互動都變好玩",
        "tag": "聊天與共謀",
        "summary": "開場先回到約會互動的底層：不要把討論變成嚴肅解題，聊天的目的常常是創造一起做事、一起發想的感覺。小侯把「討論、打鬧、一起運動、一起體驗」都放進同一個框架：讓互動有共同感。",
        "highlights": [
            "聊天不是每次都要討論出結論，而是要讓兩個人有共同參與感。",
            "不聊天時也可以透過打鬧、運動、共同活動創造互動張力。",
            "下一步要準備能分享、能邀請對方一起做的體驗。"
        ],
    },
    {
        "id": "section-02",
        "start": 190,
        "end": 290,
        "kicker": "Experience Library",
        "title": "把能創造體驗的點子先列出來",
        "tag": "約會素材庫",
        "summary": "這段在盤點可以帶給對方的體驗，例如做菜、調酒、滑板、遊戲、共同挑戰。重點不是每個點子都要很厲害，而是要開始建立自己的約會素材庫，讓互動不只剩下聊天。",
        "highlights": [
            "體驗可以是一起學、一起玩、一起挑戰，也可以是生活中的小技能。",
            "遊戲、共謀、挑戰可以疊在一起，讓互動更有層次。",
            "團隊可以一起丟 idea，幫每個人補足可執行的體驗選項。"
        ],
    },
    {
        "id": "section-03",
        "start": 290,
        "end": 530,
        "kicker": "Healthy Pipeline",
        "title": "不要只押一個人，脫單要有健康選項池",
        "tag": "生活圈與選項",
        "summary": "小侯提醒，若目前只有一個有興趣的人，而且對方還沒有明確好感訊號，投入感很容易失衡。比較健康的節奏是讓生活圈裡有三到五個可能對象，不是濫聊，而是讓成功機率與心理狀態都更穩。",
        "highlights": [
            "只有一個選項時，成功率與心理穩定度都會偏低。",
            "沒有興趣的人不必花太多聊天成本，除非真的很閒或有明確目的。",
            "把有興趣的人用團體活動拉進生活圈，比一開始就一對一重壓更穩。"
        ],
    },
    {
        "id": "section-04",
        "start": 530,
        "end": 670,
        "kicker": "Activity Flywheel",
        "title": "用活動擴生活圈，讓團隊一起產生機會",
        "tag": "辦活動",
        "summary": "這段把策略落到行動：與其繼續依賴交友軟體，不如反覆辦活動，讓不同人的專長與生活圈互相帶動。小侯也把它設成團隊代辦，要求每個人和擅長辦活動的人共創一個活動。",
        "highlights": [
            "如果交友軟體長期沒有遇到喜歡的人，就該評估主戰場是否放錯。",
            "活動可以從五六人的小聚開始，不一定一開始就要三十人規模。",
            "每個人都能用自己的技能或專長包成活動，讓生活圈重新流動。"
        ],
    },
    {
        "id": "section-05",
        "start": 670,
        "end": 770,
        "kicker": "Coaching Format",
        "title": "QPNT：把問題、過去行動與下一步寫清楚",
        "tag": "紀錄框架",
        "summary": "小侯現場臨時命名 QPNT，用來要求學員把狀態寫清楚：現在的問題、挑戰或目標是什麼；過去為了這件事做過什麼；接下來需要小侯與團隊怎麼幫。這是讓 coaching 能夠累積，而不是每次重講一次背景。",
        "highlights": [
            "先寫現在的問題、挑戰或目標，不要只講零散事件。",
            "再補上前面經歷與已做過的行動，讓討論有上下文。",
            "最後整理下一步與團隊可以協助的地方。"
        ],
    },
    {
        "id": "section-06",
        "start": 770,
        "end": 920,
        "kicker": "Boundary Talk",
        "title": "異性單獨出去，不只是在解情境題",
        "tag": "界線溝通",
        "summary": "學員提出伴侶在意自己和異性單獨出去的問題。小侯先打斷就事論事的處理法，提醒這種議題如果只解單一情境，很容易一直卡住；要上升到價值觀與需求層面，先問清楚自己為什麼需要這些社交或互動。",
        "highlights": [
            "不要只問某個女生、某次聯絡該怎麼辦，否則會一直解個案。",
            "先釐清自己需要的是社交、娛樂、任務完成，還是基本需求。",
            "價值觀談清楚後，後面的情境規則才有依據。"
        ],
    },
    {
        "id": "section-07",
        "start": 920,
        "end": 1200,
        "kicker": "Need Clarification",
        "title": "把社交需求拆成娛樂、基本需求與任務完成",
        "tag": "需求分類",
        "summary": "小侯進一步拆解：如果異性社交只是娛樂，伴侶可能會覺得交往後還去找別人娛樂很難接受；如果是基本需求，例如外向者需要社交能量，就要討論怎麼被滿足；如果只是某個組織或工作任務，那就不是社交問題，而是任務完成問題。",
        "highlights": [
            "娛樂、基本需求、任務完成，會導出完全不同的溝通方式。",
            "把需求說清楚後，才不是單方面接受限制，而是讓對方一起面對問題。",
            "任務型互動可以回到「要完成什麼、還有哪些替代做法」。"
        ],
    },
    {
        "id": "section-08",
        "start": 1200,
        "end": 1396,
        "kicker": "Relationship Needs",
        "title": "列出關係裡最重視的三個需求",
        "tag": "親密關係練習",
        "summary": "小侯示範可以和伴侶聊：什麼事情會讓你覺得被愛、有安全感，什麼事情會讓你覺得不被愛或受傷。最後他給出作業：每個人寫下三個在關係中重視的需求，並定義怎樣算有、怎樣算沒有。",
        "highlights": [
            "需求不要只停在抽象詞，要寫出怎樣算有、怎樣算沒有。",
            "安全感、陪伴、親密互動都可以被具體化成可討論行為。",
            "把需求丟出來不是要求對方照單全收，而是開啟共同解法。"
        ],
    },
    {
        "id": "section-09",
        "start": 1396,
        "end": 1475,
        "kicker": "Privacy Wrap",
        "title": "現場收尾：資料拍照、紙本處理與隱私提醒",
        "tag": "現場收尾",
        "summary": "尾聲開始處理現場紙本與資料保密。小侯提到把紙拍下來後收回或銷毀，也提醒不要把內容傳出去。這段和主題內容關聯較低，但對訓練營資料管理很重要。",
        "highlights": [
            "現場紙本有個人狀態與關係內容，不能隨意外傳。",
            "拍照留存後集中回收，比讓紙本流出去更安全。",
            "這也提醒網站版本不應公開原始音檔或敏感個資。"
        ],
    },
]


PART2_SECTIONS = [
    {
        "id": "section-10",
        "part": "part2",
        "partLabel": "第二段",
        "start": 0,
        "end": 280,
        "kicker": "Signal Design",
        "title": "用貼文和限動自然釋放感情話題訊號",
        "tag": "話題入口",
        "summary": "第二段從如何讓別人自然來聊感情開始。小侯提醒，不一定要一開口就推課或講大道理，而是可以透過 IG、貼文、限動或日常對話，把「我在關心感情議題」這件事放到台面上，讓朋友有機會順著話題問進來。",
        "highlights": [
            "感情話題可以從限動、貼文或共同脈絡切入，不需要一開始就很用力。",
            "先用朋友式聊天建立安全感，再讓對方知道你正在學習或參與感情相關內容。",
            "角色可以透明，但語氣要像分享近況，而不是突然推銷。"
        ],
    },
    {
        "id": "section-11",
        "part": "part2",
        "partLabel": "第二段",
        "start": 280,
        "end": 585,
        "kicker": "Invitation Path",
        "title": "邀請不是硬推任務，而是從關心與分享延伸",
        "tag": "邀請方法",
        "summary": "小侯把邀請拆成兩條路：一條是關心原本的朋友，一條是認識新朋友後了解對方的感情狀況。兩者的共同點都是先關心、先分享，再判斷對方是否真的有需求，而不是把邀請做成硬性的業務話術。",
        "highlights": [
            "可以從原本朋友開始，多關心、多分享，再看對方是否接得住。",
            "也可以認識新朋友，但重點仍是了解對方的感情狀態與需求。",
            "有效邀請的前提不是技巧，而是對方感覺你真的在意他。"
        ],
    },
    {
        "id": "section-12",
        "part": "part2",
        "partLabel": "第二段",
        "start": 585,
        "end": 920,
        "kicker": "Share The Change",
        "title": "不要替別人預測立場，用自己的改變讓人想聽",
        "tag": "分享感受",
        "summary": "這段處理邀請時常見的卡點：還沒開口就先幫對方預測立場。小侯提醒，真正有力量的不是說服對方，而是分享自己來這裡後的感受與改變；對方聽到真實收穫，才更容易判斷這是不是他的好康。",
        "highlights": [
            "不要幫人家預測立場，先讓對方有機會表達。",
            "用自己當下最深的感受和改變去分享，而不是背一段標準說詞。",
            "好康分享門檻低，但仍要在對方有需求時才推薦。"
        ],
    },
    {
        "id": "section-13",
        "part": "part2",
        "partLabel": "第二段",
        "start": 920,
        "end": 1210,
        "kicker": "Story Craft",
        "title": "社交表不是流水帳，要寫成能分享的故事",
        "tag": "社交表",
        "summary": "小侯檢查社交表時提醒，記錄不能只停在負面事件或流水帳。要補上自己學到什麼、玩到什麼、感受是什麼，才會變成可以自然分享的故事，也才能看見自己其實正在變好。",
        "highlights": [
            "社交表可以先記錄細節，但最後要整理成故事。",
            "故事的關鍵是加入感受、收穫與改變，而不是只記下發生了什麼。",
            "把負面紀錄轉成學習與體驗，才會成為下一次分享的素材。"
        ],
    },
    {
        "id": "section-14",
        "part": "part2",
        "partLabel": "第二段",
        "start": 1210,
        "end": 1485,
        "kicker": "Need Discovery",
        "title": "不要卡在找超痛的人，先把對方感情狀態聊深",
        "tag": "需求辨識",
        "summary": "學員容易以為要找到非常痛、非常想改變的人才算有效。小侯把順序拉回來：先聊深，最後通常會得到兩種答案，對方需要或不需要。若有需要再推薦，若沒有需要，也就知道自己暫時幫不上忙。",
        "highlights": [
            "不用一開始就找超痛的人，先讓對話真的聊到對方的感情狀態。",
            "如果聊得夠深，通常會分成需要或不需要兩種結果。",
            "付費上課是最後一步，前面是關心、幫助，以及帶對方一起玩。"
        ],
    },
    {
        "id": "section-15",
        "part": "part2",
        "partLabel": "第二段",
        "start": 1485,
        "end": 1735,
        "kicker": "Follow-up System",
        "title": "名單要有下一步與時間，不要刪掉重寫",
        "tag": "名單追蹤",
        "summary": "小侯把行動落到名單管理：接下來這些人都要有新的進展，而且每個人都要寫下一步和時間。若遇到心累、沒希望、覺得一個人很好的人，不要只停在表面答案，要繼續問到底是沒有需求，還是覺得沒有希望。",
        "highlights": [
            "名單不是寫完就放著，每個人都要有下一步與追蹤時間。",
            "不要把原本訊息刪掉重寫，而是一直往下累積脈絡。",
            "心累可能是不想要，也可能是覺得沒希望，兩者要分清楚。"
        ],
    },
    {
        "id": "section-16",
        "part": "part2",
        "partLabel": "第二段",
        "start": 1735,
        "end": 1820,
        "kicker": "Warm Strategy",
        "title": "不同熟度用不同邀請方式，用自己的故事降低距離",
        "tag": "熟度分流",
        "summary": "不同關係熟度適合不同邀請方式。熟人可以更直接地關心，對自己有恩的人可以從互相幫忙切入；如果對方說一個人很好，也要分辨是真的很好，還是只是懶、累、覺得沒希望。自己的行動故事，會比抽象建議更有說服力。",
        "highlights": [
            "熟人、恩人、新朋友的切入方式不同，但核心仍是關心。",
            "「一個人很好」需要被拆開：是真的好，還是只是沒看到希望。",
            "分享自己的約會、練習和改變，比直接給建議更自然。"
        ],
    },
    {
        "id": "section-17",
        "part": "part2",
        "partLabel": "第二段",
        "start": 1820,
        "end": 2066,
        "kicker": "Group Vision",
        "title": "把業務感轉成愛：關心身邊的人，看到他改變",
        "tag": "群組願景",
        "summary": "尾段把這件事拉回群組願景。小侯說，對他來說這可能是業務，但對學員來說希望是愛；目標不是把大家變成業務，而是練出一套能關心朋友、看見朋友改變的模型。最後作業是列出想關心的人，用成長版的自己重新看過去的人。",
        "highlights": [
            "這不是要把群組變成一堆業務，而是幫真正的朋友一把。",
            "即使對某個人的觀感不同，也要練習一視同仁地關心。",
            "負面情緒也會透露自己的訊息，作業是列出想關心的名字並重新看待他們。"
        ],
    },
]


SECTIONS = PART1_SECTIONS + PART2_SECTIONS


SAFE_REPLACEMENTS = {
    "脫胆": "脫單",
    "內號": "內耗",
    "性能感": "性冷感",
    "陪同吧": "陪伴吧",
    "陪同": "陪伴",
    "一握為舉例": "以我為舉例",
}


def seconds(ms: int) -> float:
    return ms / 1000


def fmt_time(value: float) -> str:
    total = int(value)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    for old, new in SAFE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def paragraphize(turns: list[dict], max_chars: int = 180) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    size = 0
    for turn in turns:
        text = turn["text"]
        if not text:
            continue
        current.append(text)
        size += len(text)
        if size >= max_chars or text.endswith(("。", "？", "！", "嗎", "OK", "好")):
            paragraphs.append(" ".join(current))
            current = []
            size = 0
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


QUESTION_CUES = (
    "嗎", "是不是", "對不對", "可不可以", "可以嗎", "有沒有", "要不要", "怎麼辦",
    "怎麼樣", "為什麼", "什麼意思", "你覺得", "那如果", "如果說",
)

COACH_CUES = (
    "我問你", "我跟你講", "我覺得", "我希望", "我會", "我先", "我來", "我看一下",
    "你要", "你可以", "你們要", "你們可以", "你就", "所以", "好", "OK", "這個是",
    "重點是", "接下來", "我們", "大家", "作業", "我相信",
)

STUDENT_CUES = (
    "我想問", "我可以", "那我", "可是我", "但是我", "我的問題", "我現在",
    "她是我", "他是我", "我覺得我", "我不知道", "我想說",
)

BACKCHANNELS = {
    "嗯", "對", "好", "OK", "可以", "是", "不是", "沒有", "有", "喔", "啊", "對啊",
    "好啊", "沒錯", "真的", "可以啊",
}


def is_question_like(text: str) -> bool:
    return "?" in text or "？" in text or any(cue in text for cue in QUESTION_CUES)


def has_recent_question(turns: list[dict], idx: int) -> bool:
    for prev in turns[max(0, idx - 3):idx]:
        if is_question_like(prev["text"]):
            return True
    return False


def infer_speaker(turns: list[dict], idx: int, previous: str | None) -> str:
    text = turns[idx]["text"]
    compact = text.replace(" ", "")

    if compact in BACKCHANNELS:
        if has_recent_question(turns, idx):
            return "現場回應（推定）"
        return previous or "小侯（推定）"

    if any(cue in compact for cue in STUDENT_CUES) and not any(cue in compact for cue in COACH_CUES):
        return "學員（推定）"

    if (
        is_question_like(compact)
        and len(compact) <= 42
        and "我問你" not in compact
        and not compact.startswith(("你", "你們"))
        and any(cue in compact for cue in ("我想", "那我", "可是", "但是", "如果我", "可以問"))
    ):
        return "學員提問（推定）"

    if len(compact) <= 10 and previous and previous != "小侯（推定）":
        return previous

    return "小侯（推定）"


def speaker_class(speaker: str) -> str:
    if speaker.startswith("小侯"):
        return "speaker-coach"
    if speaker.startswith("學員"):
        return "speaker-student"
    return "speaker-room"


def merge_speaker_turns(turns: list[dict], max_chars: int = 900, merge_gap: float = 2.5) -> list[dict]:
    inferred: list[dict] = []
    previous: str | None = None
    for idx, turn in enumerate(turns):
        speaker = infer_speaker(turns, idx, previous)
        previous = speaker
        inferred.append({**turn, "speaker": speaker, "speakerClass": speaker_class(speaker)})

    merged: list[dict] = []
    for turn in inferred:
        if not merged:
            merged.append({**turn, "segmentCount": 1})
            continue

        last = merged[-1]
        gap = float(turn["start"]) - float(last["end"])
        combined_text = f"{last['text']} {turn['text']}".strip()
        if (
            turn["speaker"] == last["speaker"]
            and gap <= merge_gap
            and len(combined_text) <= max_chars
        ):
            last["end"] = turn["end"]
            last["endTime"] = turn["endTime"]
            last["text"] = combined_text
            last["segmentCount"] = int(last["segmentCount"]) + 1
        else:
            merged.append({**turn, "segmentCount": 1})

    return merged


def load_turns(source_path: Path, part_key: str, part_label: str) -> list[dict]:
    raw = json.loads(source_path.read_text(encoding="utf-8"))
    turns = []
    for item in raw["transcription"]:
        start = seconds(item["offsets"]["from"])
        end = seconds(item["offsets"]["to"])
        text = clean_text(item["text"])
        if not text:
            continue
        turns.append(
            {
                "part": part_key,
                "partLabel": part_label,
                "start": start,
                "end": end,
                "time": f"{part_label} {fmt_time(start)}",
                "partTime": fmt_time(start),
                "endTime": fmt_time(end),
                "text": text,
            }
        )
    return turns


def build_data() -> dict:
    turn_pools = {
        "part1": load_turns(PART1_JSON, "part1", "第一段"),
        "part2": load_turns(PART2_JSON, "part2", "第二段"),
    }
    section_data = []
    for idx, section in enumerate(SECTIONS, start=1):
        part_key = section.get("part", "part1")
        part_label = section.get("partLabel", "第一段")
        matched = [turn for turn in turn_pools[part_key] if section["start"] <= turn["start"] < section["end"]]
        speaker_turns = merge_speaker_turns(matched)
        section_data.append(
            {
                "id": section["id"],
                "index": f"{idx:02d}",
                "part": part_key,
                "partLabel": part_label,
                "kicker": section["kicker"],
                "title": section["title"],
                "tag": section["tag"],
                "timeRange": f"{part_label} {fmt_time(section['start'])} - {fmt_time(section['end'])}",
                "summary": section["summary"],
                "highlights": section["highlights"],
                "paragraphs": paragraphize(matched),
                "turns": matched,
                "speakerTurns": speaker_turns,
            }
        )

    return {
        "title": "2026-06-07 小侯脫單訓練營逐字稿網站",
        "subtitle": "從約會互動、生活圈擴張，到關係需求、邀請關心與名單追蹤的現場 coaching 整理。",
        "contentNote": "本頁依本機 Whisper large-v3-turbo 轉錄結果整理。正文保留原始順序與口語感，刪除大量重複、雜訊與明顯辨識錯詞；逐字稿頁新增保守發言人推定與連續段落合併，未做模型級聲紋 diarization。",
        "meta": {
            "primarySpeaker": "小侯",
            "recordedAt": "2026-06-07",
            "duration": "第一段 24:30；第二段 35:24",
            "scope": "local-only",
            "status": "兩段皆已本機轉錄；逐字稿頁已加推定發言人與連續段落合併",
        },
        "speakers": [
            {
                "id": "coach",
                "name": "小侯（推定）",
                "note": "依內容脈絡推定為主要教練發言，非聲紋 diarization。",
            },
            {
                "id": "student",
                "name": "學員 / 學員提問（推定）",
                "note": "依提問、第一人稱分享與回應脈絡推定。",
            },
            {
                "id": "room",
                "name": "現場回應（推定）",
                "note": "依短促回覆與前後問答脈絡推定。",
            },
        ],
        "sourceQuality": [
            "第一段：成功產出 TXT/SRT/JSON，已納入正文與完整時間軸。",
            "第二段：真正音檔長度為 35:24，已重新轉錄並納入正文；先前 03:18 錯檔輸出已被覆蓋。",
            "講者：本版以文字脈絡做保守發言人推定，並合併同一推定發言人的連續片段；尚未跑 Hugging Face / pyannote 聲紋 diarization。",
        ],
        "summaryHighlights": [
            "互動的目的不是把每次聊天變成解題，而是創造一起討論、一起玩、一起做事的共同感。",
            "脫單要健康，不能只押一個曖昧對象；生活圈裡最好持續有三到五個可能選項。",
            "活動是擴生活圈的主戰場：用自己的專長和團隊共創活動，比硬滑交友軟體更符合這場訓練的方向。",
            "QPNT 是這場 coaching 的紀錄框架：問題/挑戰/目標、過去做了什麼、下一步怎麼做、團隊怎麼幫。",
            "伴侶界線議題不能只解單一情境，要拉到價值觀與需求：那是娛樂、基本需求，還是任務完成？",
            "關係需求要具體化：寫下三個重視的需求，分別定義怎樣算有、怎樣算沒有，才能真的拿來溝通。",
            "第二段把焦點從自己脫單延伸到如何關心身邊的人，發現對方有需求時再自然邀請。",
            "社交表不只是紀錄，要補上感受、收穫與改變，才會變成能分享的故事素材。",
            "名單追蹤要有下一步與時間，不要刪掉重寫；一直往下累積，才能看見關係進展。",
            "這套練習的願景不是把大家變成業務，而是用更成熟的自己幫真正的朋友一把。",
        ],
        "sections": section_data,
    }


def e(value: object) -> str:
    return escape(str(value), quote=True)


def nav_links(data: dict, target_prefix: str) -> str:
    links = []
    for section in data["sections"]:
        links.append(
            f'<a class="toc-link" href="{target_prefix}#{e(section["id"])}">'
            f'<strong>{e(section["index"])} {e(section["title"])}</strong>'
            f'<span>{e(section["timeRange"])}</span></a>'
        )
    return "\n".join(links)


def section_switch(section: dict, target: str, label: str) -> str:
    return f'<a class="button" href="{target}#{e(section["id"])}">{e(label)}</a>'


def render_home(data: dict) -> str:
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>{e(data["title"])}</title>
  <meta name="description" content="小侯脫單訓練營整理版與完整逐字稿入口。">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main class="shell landing">
    <p class="eyebrow">Private link archive · noindex</p>
    <h1>{e(data["title"])}</h1>
    <p class="lead">{e(data["subtitle"])}</p>
    <div class="landing-actions">
      <a class="button primary" href="events/{EVENT_SLUG}/">重點整理</a>
      <a class="button" href="transcripts/{EVENT_SLUG}/">完整逐字稿</a>
    </div>
    <p class="privacy-note">這個站可以用直接網址瀏覽，但頁面已加入 noindex 與 robots 設定，避免被搜尋引擎主動收錄。</p>
  </main>
</body>
</html>
"""


def render_summary(data: dict) -> str:
    overview = "\n".join(f"<li>{e(item)}</li>" for item in data["summaryHighlights"])
    quality = "\n".join(f"<li>{e(item)}</li>" for item in data["sourceQuality"])
    chapters = []
    for section in data["sections"]:
        highlights = "\n".join(f"<li>{e(item)}</li>" for item in section["highlights"])
        paragraphs = "\n".join(f"<p>{e(text)}</p>" for text in section["paragraphs"][:3])
        chapters.append(
            f"""<article class="chapter" id="{e(section["id"])}">
  <header class="chapter-head">
    <div class="chapter-index">{e(section["index"])}</div>
    <div>
      <p class="eyebrow">{e(section["kicker"])}</p>
      <h2>{e(section["title"])}</h2>
      <div class="chapter-meta">
        <span class="badge">{e(section["timeRange"])}</span>
        <span class="badge">{e(section["tag"])}</span>
      </div>
    </div>
  </header>
  <div class="chapter-body">
    <p class="chapter-summary">{e(section["summary"])}</p>
    <ul class="highlight-list">{highlights}</ul>
    <div class="paragraphs">{paragraphs}</div>
    <div class="chapter-actions">
      {section_switch(section, "../../transcripts/" + EVENT_SLUG + "/", "看本章逐字稿")}
    </div>
  </div>
</article>"""
        )

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>小侯脫單訓練營重點整理</title>
  <meta name="description" content="2026-06-07 小侯脫單訓練營重點整理。">
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <a class="home-button" href="../../">回入口</a>
  <header class="hero">
    <div class="shell hero-inner">
      <p class="eyebrow">2026-06-07 · 小侯脫單訓練營</p>
      <h1>小侯脫單訓練營重點整理</h1>
      <p class="lead">{e(data["subtitle"])}</p>
      <div class="meta-grid">
        <span class="meta-chip">主講：{e(data["meta"]["primarySpeaker"])}</span>
        <span class="meta-chip">長度：{e(data["meta"]["duration"])}</span>
        <span class="meta-chip">狀態：{e(data["meta"]["status"])}</span>
      </div>
      <div class="hero-actions">
        <a class="button primary" href="../../transcripts/{EVENT_SLUG}/">查看完整逐字稿</a>
      </div>
    </div>
  </header>
  <nav class="toc-wrap" aria-label="章節導讀">
    <div class="shell">
      <p class="toc-title">章節導讀 · 點選後會到逐字稿同章節</p>
      <div class="toc-list">{nav_links(data, "../../transcripts/" + EVENT_SLUG + "/")}</div>
    </div>
  </nav>
  <main class="shell page-grid">
    <aside class="side-note">
      <h2>整理策略</h2>
      <p>{e(data["contentNote"])}</p>
    </aside>
    <section class="content-flow">
      <section class="panel">
        <p class="eyebrow">Overview</p>
        <h2>這場訓練營在講什麼</h2>
        <ul class="summary-list">{overview}</ul>
      </section>
      {"".join(chapters)}
      <section class="panel" id="source-quality">
        <p class="eyebrow">Source Quality</p>
        <h2>來源狀態</h2>
        <ul class="summary-list">{quality}</ul>
      </section>
    </section>
  </main>
  <footer class="footer">Direct-link archive · noindex</footer>
</body>
</html>
"""


def render_transcript(data: dict) -> str:
    chapters = []
    for section in data["sections"]:
        rows = []
        for turn_idx, turn in enumerate(section["speakerTurns"], start=1):
            turn_id = f't-{turn["part"]}-{int(turn["start"]):04d}-{turn_idx:03d}'
            rows.append(
                f'<section class="transcript-row {e(turn["speakerClass"])}" id="{e(turn_id)}">'
                f'<time>{e(turn["time"])}</time>'
                f'<strong class="speaker-label">{e(turn["speaker"])}</strong>'
                f'<p>{e(turn["text"])}</p></section>'
            )
        chapters.append(
            f"""<article class="transcript-chapter" id="{e(section["id"])}">
  <header class="transcript-chapter-head">
    <div>
      <p class="eyebrow">{e(section["timeRange"])}</p>
      <h2>{e(section["index"])} {e(section["title"])}</h2>
    </div>
    {section_switch(section, "../../events/" + EVENT_SLUG + "/", "回本章整理")}
  </header>
  <div class="transcript-list">{"".join(rows)}</div>
</article>"""
        )

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>小侯脫單訓練營完整逐字稿</title>
  <meta name="description" content="2026-06-07 小侯脫單訓練營完整逐字稿。">
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <a class="home-button" href="../../">回入口</a>
  <main class="shell transcript-page" id="top">
    <p class="eyebrow">Raw Timeline · 兩段錄音合併索引</p>
    <h1>小侯脫單訓練營完整逐字稿</h1>
    <p class="lead">完整逐字稿依章節分段，並加入推定發言人與連續段落合併。每個章節右上角都可以切回同一章的重點整理。</p>
    <div class="hero-actions">
      <a class="button primary" href="../../events/{EVENT_SLUG}/">查看重點整理</a>
    </div>
    <nav class="transcript-toc" aria-label="逐字稿目錄">
      <h2>逐字稿目錄 · 點選後會到逐字稿章節</h2>
      <div class="toc-list compact">{nav_links(data, "")}</div>
    </nav>
    {"".join(chapters)}
  </main>
  <footer class="footer">Direct-link archive · noindex</footer>
</body>
</html>
"""


def write_site(data: dict) -> None:
    CONTENT.mkdir(parents=True, exist_ok=True)
    EVENT_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    (CONTENT / "transcript.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (CONTENT / "transcript.inline.js").write_text(
        "window.__TRANSCRIPT_DATA__ = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    (ROOT / "index.html").write_text(render_home(data), encoding="utf-8")
    (EVENT_DIR / "index.html").write_text(render_summary(data), encoding="utf-8")
    (TRANSCRIPT_DIR / "index.html").write_text(render_transcript(data), encoding="utf-8")
    (ROOT / "styles.css").write_text(SPLIT_STYLES_CSS, encoding="utf-8")
    (ROOT / "app.js").write_text("// Static split-site archive. Content is generated by scripts/build_site.py.\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    (ROOT / "README.md").write_text(SPLIT_README_MD, encoding="utf-8")


SPLIT_STYLES_CSS = """:root {
  --bg: #f5f2ec;
  --paper: #fffdfa;
  --paper-2: #f8f3ea;
  --ink: #25221e;
  --muted: #6b655c;
  --line: #d9cdbd;
  --accent: #256c5a;
  --accent-2: #ad4f34;
  --gold: #c18a2c;
  --shadow: 0 18px 48px rgba(39, 32, 23, .11);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: linear-gradient(180deg, #fbf8f1 0%, var(--bg) 46%, #eee8dc 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", sans-serif;
  line-height: 1.75;
}

a { color: inherit; }
.shell { width: min(1120px, calc(100vw - 32px)); margin: 0 auto; }

.landing {
  min-height: 100vh;
  display: grid;
  align-content: center;
  gap: 18px;
  padding: 64px 0;
}

.hero {
  padding: 76px 0 52px;
  border-bottom: 1px solid var(--line);
  background:
    linear-gradient(120deg, rgba(255,253,250,.98), rgba(255,248,236,.88)),
    radial-gradient(circle at 14% 18%, rgba(37,108,90,.14), transparent 30%),
    radial-gradient(circle at 88% 8%, rgba(173,79,52,.12), transparent 26%);
}

.hero-inner { display: grid; gap: 16px; }
.eyebrow {
  margin: 0;
  color: var(--accent);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .08em;
  text-transform: uppercase;
}

h1, h2, h3 { margin: 0; line-height: 1.16; letter-spacing: 0; }
h1 {
  max-width: 900px;
  font-family: Georgia, "Times New Roman", "Noto Serif TC", serif;
  font-size: clamp(42px, 7vw, 82px);
}
h2 {
  font-family: Georgia, "Times New Roman", "Noto Serif TC", serif;
  font-size: clamp(28px, 4vw, 46px);
}

.lead {
  max-width: 72ch;
  margin: 0;
  color: var(--muted);
  font-size: 18px;
}

.home-button {
  position: fixed;
  top: 14px;
  left: 14px;
  z-index: 10;
  display: inline-flex;
  align-items: center;
  min-height: 38px;
  padding: 8px 12px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: rgba(255,253,250,.94);
  color: var(--ink);
  font-weight: 900;
  text-decoration: none;
  box-shadow: 0 8px 22px rgba(0,0,0,.08);
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 9px 14px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
  color: var(--ink);
  font-weight: 900;
  text-decoration: none;
}
.button.primary { border-color: var(--accent); background: var(--accent); color: #fffdfa; }
.button:hover { border-color: var(--accent-2); color: var(--accent-2); }
.button.primary:hover { border-color: var(--accent-2); background: var(--accent-2); color: #fffdfa; }

.landing-actions, .hero-actions, .chapter-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.privacy-note { max-width: 68ch; margin: 0; color: var(--muted); }

.meta-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.meta-chip, .badge {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: 5px 10px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--paper);
  color: var(--muted);
  font-size: 14px;
}

.toc-wrap {
  position: sticky;
  top: 0;
  z-index: 5;
  padding: 16px 0;
  border-bottom: 1px solid var(--line);
  background: rgba(255,253,250,.94);
  backdrop-filter: blur(10px);
}
.toc-title { margin: 0 0 10px; color: var(--muted); font-weight: 900; }
.toc-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}
.toc-list.compact { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.toc-link {
  display: grid;
  gap: 3px;
  min-height: 64px;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  border-radius: 6px;
  background: var(--paper);
  text-decoration: none;
}
.toc-link span { color: var(--muted); font-size: 13px; }
.toc-link:hover { border-color: var(--accent-2); border-left-color: var(--accent-2); }

.page-grid {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 24px;
  padding: 28px 0 72px;
}
.side-note {
  position: sticky;
  top: 126px;
  align-self: start;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
}
.side-note h2 { font-size: 24px; }
.side-note p { margin-bottom: 0; color: var(--muted); }
.content-flow { display: grid; gap: 18px; }

.panel, .chapter, .transcript-chapter {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  box-shadow: var(--shadow);
}
.panel { padding: clamp(22px, 4vw, 34px); }
.summary-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
}
.summary-list li {
  padding: 14px;
  border-top: 3px solid var(--accent);
  background: var(--paper-2);
}

.chapter { overflow: hidden; scroll-margin-top: 112px; }
.chapter:target, .transcript-chapter:target {
  outline: 3px solid rgba(173,79,52,.24);
  outline-offset: 4px;
}
.chapter-head {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr);
  gap: 18px;
  padding: 22px;
  border-bottom: 1px solid var(--line);
  background: var(--paper-2);
}
.chapter-index {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: var(--ink);
  color: #fffdfa;
  font-weight: 900;
}
.chapter-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.chapter-body { padding: 22px; }
.chapter-summary { margin-top: 0; font-size: 18px; }
.highlight-list {
  display: grid;
  gap: 8px;
  margin: 18px 0;
  padding-left: 20px;
}
.paragraphs {
  display: grid;
  gap: 10px;
  margin: 18px 0 0;
  padding-top: 16px;
  border-top: 1px solid var(--line);
  color: var(--muted);
}
.paragraphs p { margin: 0; }

.transcript-page { padding: 64px 0 76px; }
.transcript-page .lead { margin-top: 14px; }
.transcript-toc {
  margin: 28px 0;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper-2);
}
.transcript-toc h2 { margin-bottom: 14px; font-size: 28px; }
.transcript-chapter {
  margin-top: 18px;
  overflow: hidden;
  scroll-margin-top: 24px;
}
.transcript-chapter-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: start;
  padding: 20px;
  border-bottom: 1px solid var(--line);
  background: var(--paper-2);
}
.transcript-chapter-head h2 { font-size: clamp(24px, 3vw, 36px); }
.transcript-list { padding: 0 20px 10px; }
.transcript-row {
  display: grid;
  grid-template-columns: 128px 124px minmax(0, 1fr);
  gap: 14px;
  padding: 12px 0;
  border-top: 1px solid var(--line);
}
.transcript-row:first-child { border-top: 0; }
.transcript-row time {
  color: var(--accent);
  font-weight: 900;
  font-variant-numeric: tabular-nums;
}
.speaker-label {
  color: var(--muted);
  font-weight: 900;
}
.speaker-coach .speaker-label { color: var(--accent); }
.speaker-student .speaker-label { color: var(--accent-2); }
.speaker-room .speaker-label { color: var(--gold); }
.transcript-row p { margin: 0; }

.footer {
  padding: 26px 16px;
  color: var(--muted);
  text-align: center;
}

@media (max-width: 900px) {
  .toc-list, .toc-list.compact, .summary-list, .page-grid { grid-template-columns: 1fr; }
  .toc-wrap { position: static; }
  .side-note { position: static; }
}

@media (max-width: 640px) {
  .home-button { position: sticky; top: 8px; margin: 8px 0 0 12px; }
  .hero { padding-top: 44px; }
  .chapter-head, .transcript-chapter-head, .transcript-row { grid-template-columns: 1fr; }
  .transcript-chapter-head { display: grid; }
  .transcript-row { gap: 4px; }
}
"""


SPLIT_README_MD = """# 2026-06-07 小侯脫單訓練營私有連結網站

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
"""


INDEX_HTML = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="2026-06-07 小侯脫單訓練營錄音逐字稿與整理版網站。">
  <title>2026-06-07 小侯脫單訓練營逐字稿網站</title>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <header class="topbar">
    <a href="#top" class="brand">Dating Camp Notes</a>
    <nav aria-label="頁面導覽">
      <a href="#overview">總覽</a>
      <a href="#sections">章節</a>
      <a href="#full-transcript">完整時間軸</a>
      <a href="#source-quality">來源狀態</a>
    </nav>
  </header>

  <main id="top">
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Transcript-first coaching archive</p>
        <h1 id="page-title">2026-06-07 小侯脫單訓練營逐字稿網站</h1>
        <p class="hero-lede" id="page-subtitle">從約會互動、生活圈擴張，到關係需求與界線溝通的現場 coaching 整理。</p>
        <div class="meta-grid" id="meta-grid"></div>
      </div>
      <aside class="hero-card" aria-label="整理策略">
        <strong>整理策略</strong>
        <p id="content-note"></p>
      </aside>
    </section>

    <section class="overview" id="overview">
      <div class="section-heading">
        <p class="eyebrow">Overview</p>
        <h2>這場訓練營在講什麼</h2>
      </div>
      <ul class="summary-list" id="summary-list"></ul>
    </section>

    <section class="chapter-layout">
      <aside class="toc-panel">
        <p class="eyebrow">Chapter Map</p>
        <nav id="section-nav" aria-label="章節目錄"></nav>
      </aside>
      <div class="chapters" id="sections"></div>
    </section>

    <section class="full-transcript" id="full-transcript">
      <div class="section-heading">
        <p class="eyebrow">Raw Timeline</p>
        <h2>完整時間軸逐字稿</h2>
      </div>
      <div class="toolbar">
        <label>
          搜尋文字
          <input id="search-input" type="search" placeholder="例如：生活圈、需求、安全感">
        </label>
        <button id="clear-search" type="button">清除</button>
      </div>
      <div class="timeline" id="timeline"></div>
    </section>

    <section class="source-quality" id="source-quality">
      <div class="section-heading">
        <p class="eyebrow">Source Quality</p>
        <h2>來源狀態</h2>
      </div>
      <ul id="source-quality-list"></ul>
    </section>
  </main>

  <script src="./content/transcript.inline.js"></script>
  <script src="./app.js"></script>
</body>
</html>
"""


STYLES_CSS = """:root {
  --bg: #f4f0e8;
  --paper: #fffdfa;
  --paper-2: #fbf6ec;
  --ink: #26231f;
  --muted: #6d665c;
  --line: #d8cab8;
  --accent: #246b5a;
  --accent-2: #a84d32;
  --accent-soft: #e8f1ea;
  --shadow: 0 18px 50px rgba(45, 34, 20, 0.10);
  --radius: 8px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: linear-gradient(180deg, #f9f5ee 0%, var(--bg) 42%, #eee7dc 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", sans-serif;
  line-height: 1.75;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  padding: 14px max(22px, calc((100vw - 1180px) / 2));
  background: rgba(255, 253, 250, 0.92);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(10px);
}

.brand {
  color: var(--ink);
  font-weight: 800;
  text-decoration: none;
}

.topbar nav {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.topbar nav a {
  color: var(--muted);
  text-decoration: none;
  font-size: 0.94rem;
}

main {
  width: min(1180px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 30px 0 64px;
}

.hero {
  min-height: 430px;
  display: grid;
  grid-template-columns: minmax(0, 1.6fr) minmax(280px, 0.74fr);
  gap: 26px;
  align-items: stretch;
  padding: clamp(28px, 6vw, 58px);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background:
    linear-gradient(120deg, rgba(255,253,250,0.95), rgba(255,249,239,0.84)),
    radial-gradient(circle at 12% 20%, rgba(36, 107, 90, .16), transparent 34%),
    radial-gradient(circle at 88% 0%, rgba(168, 77, 50, .12), transparent 28%);
  box-shadow: var(--shadow);
}

.hero-copy {
  align-self: center;
}

.eyebrow {
  margin: 0;
  color: var(--accent);
  font-size: 0.76rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h1, h2, h3 {
  margin: 0;
  line-height: 1.16;
  letter-spacing: 0;
}

h1 {
  max-width: 820px;
  margin-top: 14px;
  font-family: Georgia, "Times New Roman", "Noto Serif TC", serif;
  font-size: clamp(2.35rem, 6vw, 4.9rem);
}

h2 {
  margin-top: 8px;
  font-family: Georgia, "Times New Roman", "Noto Serif TC", serif;
  font-size: clamp(1.75rem, 4vw, 3rem);
}

h3 {
  margin-top: 8px;
  font-size: clamp(1.25rem, 2.5vw, 1.9rem);
}

.hero-lede {
  max-width: 62ch;
  margin: 18px 0 0;
  color: var(--muted);
  font-size: 1.08rem;
}

.hero-card {
  display: grid;
  align-content: end;
  gap: 10px;
  padding: 24px;
  border-left: 3px solid var(--accent);
  background: rgba(255, 253, 250, 0.74);
}

.hero-card p {
  margin: 0;
  color: var(--muted);
}

.meta-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}

.meta-chip,
.badge {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 6px 10px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--paper);
  color: var(--muted);
  font-size: 0.92rem;
}

.overview,
.full-transcript,
.source-quality {
  margin-top: 24px;
  padding: clamp(22px, 4vw, 34px);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
}

.summary-list,
.source-quality ul {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin: 22px 0 0;
  padding: 0;
  list-style: none;
}

.summary-list li,
.source-quality li {
  padding: 16px;
  border-top: 3px solid var(--accent);
  background: var(--paper-2);
}

.chapter-layout {
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr);
  gap: 22px;
  margin-top: 24px;
}

.toc-panel {
  position: sticky;
  top: 68px;
  align-self: start;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
}

#section-nav {
  display: grid;
  gap: 8px;
  margin-top: 14px;
}

.toc-link {
  display: grid;
  gap: 2px;
  padding: 10px 12px;
  border-left: 3px solid transparent;
  color: var(--ink);
  text-decoration: none;
  background: var(--paper-2);
}

.toc-link span {
  color: var(--muted);
  font-size: 0.88rem;
}

.toc-link:hover {
  border-color: var(--accent-2);
}

.chapters {
  display: grid;
  gap: 18px;
}

.chapter {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  overflow: hidden;
}

.chapter-head {
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr);
  gap: 16px;
  padding: 22px;
  background: linear-gradient(90deg, var(--paper-2), var(--paper));
}

.chapter-index {
  color: var(--accent-2);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2rem;
  font-weight: 800;
}

.chapter-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.chapter-body {
  display: grid;
  gap: 18px;
  padding: 22px;
}

.chapter-summary {
  margin: 0;
  color: var(--muted);
}

.highlight-list {
  margin: 0;
  padding-left: 20px;
}

.highlight-list li + li {
  margin-top: 8px;
}

.paragraphs {
  display: grid;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--line);
  background: #fffefb;
}

.paragraphs p {
  margin: 0;
  color: #3f3a33;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: end;
  margin-top: 20px;
}

.toolbar label {
  display: grid;
  gap: 6px;
  color: var(--muted);
  font-size: 0.9rem;
}

input[type="search"] {
  width: min(460px, calc(100vw - 80px));
  min-height: 42px;
  padding: 8px 12px;
  border: 1px solid var(--line);
  border-radius: 6px;
  font: inherit;
}

button {
  min-height: 42px;
  padding: 8px 14px;
  border: 1px solid var(--accent);
  border-radius: 6px;
  background: var(--accent);
  color: white;
  font: inherit;
  cursor: pointer;
}

.timeline {
  display: grid;
  gap: 8px;
  margin-top: 18px;
}

.turn {
  display: grid;
  grid-template-columns: 128px minmax(0, 1fr);
  gap: 14px;
  padding: 10px 0;
  border-top: 1px solid var(--line);
}

.turn time {
  color: var(--accent);
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.turn p {
  margin: 0;
}

mark {
  background: #ffe1a6;
  color: inherit;
}

@media (max-width: 880px) {
  .hero,
  .chapter-layout {
    grid-template-columns: 1fr;
  }

  .toc-panel {
    position: static;
  }

  .summary-list,
  .source-quality ul {
    grid-template-columns: 1fr;
  }

  .topbar {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 620px) {
  main {
    width: min(100vw - 20px, 1180px);
    padding-top: 16px;
  }

  .hero {
    min-height: auto;
    padding: 22px;
  }

  .chapter-head,
  .turn {
    grid-template-columns: 1fr;
  }
}
"""


APP_JS = """const state = { data: null, query: "" };

async function loadData() {
  try {
    const response = await fetch("./content/transcript.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  } catch (error) {
    if (window.__TRANSCRIPT_DATA__) return window.__TRANSCRIPT_DATA__;
    throw error;
  }
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function fill(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value || "";
}

function renderMeta(meta) {
  const map = [
    ["主講", meta.primarySpeaker],
    ["錄製", meta.recordedAt],
    ["長度", meta.duration],
    ["範圍", meta.scope],
    ["狀態", meta.status],
  ];
  const container = document.getElementById("meta-grid");
  container.replaceChildren(...map.map(([label, value]) => el("span", "meta-chip", `${label}：${value}`)));
}

function renderList(id, items) {
  const container = document.getElementById(id);
  container.replaceChildren(...items.map((item) => el("li", "", item)));
}

function renderNav(sections) {
  const nav = document.getElementById("section-nav");
  nav.replaceChildren(...sections.map((section) => {
    const link = el("a", "toc-link");
    link.href = `#${section.id}`;
    link.append(el("strong", "", `${section.index} ${section.title}`), el("span", "", section.timeRange));
    return link;
  }));
}

function renderSections(sections) {
  const container = document.getElementById("sections");
  container.replaceChildren(...sections.map((section) => {
    const article = el("article", "chapter");
    article.id = section.id;

    const head = el("header", "chapter-head");
    head.append(el("div", "chapter-index", section.index));
    const titleWrap = el("div");
    titleWrap.append(el("p", "eyebrow", section.kicker), el("h3", "", section.title));
    const meta = el("div", "chapter-meta");
    meta.append(el("span", "badge", section.timeRange), el("span", "badge", section.tag));
    titleWrap.append(meta);
    head.append(titleWrap);

    const body = el("div", "chapter-body");
    body.append(el("p", "chapter-summary", section.summary));

    const highlights = el("ul", "highlight-list");
    highlights.replaceChildren(...section.highlights.map((item) => el("li", "", item)));
    body.append(highlights);

    const paragraphs = el("div", "paragraphs");
    paragraphs.replaceChildren(...section.paragraphs.map((text) => el("p", "", text)));
    body.append(paragraphs);

    article.append(head, body);
    return article;
  }));
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
}

function highlight(text, query) {
  if (!query) return document.createTextNode(text);
  const fragment = document.createDocumentFragment();
  const parts = text.split(new RegExp(`(${escapeRegExp(query)})`, "gi"));
  for (const part of parts) {
    if (part.toLowerCase() === query.toLowerCase()) {
      fragment.append(el("mark", "", part));
    } else {
      fragment.append(document.createTextNode(part));
    }
  }
  return fragment;
}

function renderTimeline() {
  const container = document.getElementById("timeline");
  const query = state.query.trim();
  const turns = state.data.sections.flatMap((section) => section.turns)
    .filter((turn) => !query || turn.text.toLowerCase().includes(query.toLowerCase()));

  container.replaceChildren(...turns.map((turn) => {
    const row = el("div", "turn");
    row.append(el("time", "", turn.time));
    const p = el("p");
    p.append(highlight(turn.text, query));
    row.append(p);
    return row;
  }));
}

async function init() {
  state.data = await loadData();
  fill("page-title", state.data.title);
  fill("page-subtitle", state.data.subtitle);
  fill("content-note", state.data.contentNote);
  renderMeta(state.data.meta);
  renderList("summary-list", state.data.summaryHighlights);
  renderNav(state.data.sections);
  renderSections(state.data.sections);
  renderTimeline();
  renderList("source-quality-list", state.data.sourceQuality);

  const input = document.getElementById("search-input");
  input.addEventListener("input", (event) => {
    state.query = event.target.value;
    renderTimeline();
  });
  document.getElementById("clear-search").addEventListener("click", () => {
    state.query = "";
    input.value = "";
    renderTimeline();
  });
}

init().catch((error) => {
  document.body.innerHTML = `<main class="source-quality"><h1>載入失敗</h1><p>${error.message}</p></main>`;
});
"""


README_MD = """# 2026-06-07 小侯脫單訓練營逐字稿網站

本專案由 `system/skills/transcribe`、`system/skills/transcript-site-builder` 與 `.agent/workflows/transcript_site_publish.md` 的穩定流程產出。

## 來源

- `/Users/dan/Downloads/2026-06-07_脫單訓練營_1.wav`
- `/Users/dan/Downloads/2026-06-07_脫單訓練營2.wav`

## 輸出

- `content/transcript.json`：網站資料來源
- `content/transcript.inline.js`：Safari / file:// fallback
- `index.html`：靜態頁
- `styles.css` / `app.js`：頁面樣式與互動

## 注意

第二段已更新為真正音檔並重新轉錄。網站採本機 JSON 重建，`content/transcript.inline.js` 保留為靜態檔開啟時的 fallback。
"""


def main() -> None:
    write_site(build_data())


if __name__ == "__main__":
    main()
