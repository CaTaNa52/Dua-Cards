# 1000 Duas – Arafah Flashcard App

A fully offline flashcard app containing 1,000 duas for Arafah and everyday supplication.  
Single HTML file — no internet, no installation, no accounts required.

---

## How to Use on Your Phone

### Step 1 — Transfer the file
Send `index.html` to your phone via **WhatsApp** or **Telegram** as a file attachment.

### Step 2 — Open the file
Download the file on your phone, then open it in **Chrome** or any browser.

> **Note:** If the file opens in a quick viewer or preview app instead of a browser,  
> tap **Share** and choose **Open with Chrome** (or your preferred browser).

---

## Features

- **1,000 duas** — English and Arabic, organised into 40 sections
- **Flashcard navigation** — Previous / Next / Random
- **Swipe gestures** — swipe left for next, swipe right for previous
- **Search** — search by English text, Arabic text, or section name
- **Section filter** — browse duas by topic
- **Favorites** — save duas with ♡, filter to favorites only
- **My Duas** — add and store your own personal duas offline
- **Font size control** — A− and A+ buttons adjust dua text size
- **Dark mode** — follows your phone's theme, or toggle manually
- **Progress saved** — reopening the file resumes where you left off
- **Fully offline** — all data is embedded in the file, no internet needed

---

## Files

| File | Description |
|------|-------------|
| `index.html` | The app — this is the only file you need |
| `build_standalone_flashcards.py` | Build script to regenerate the HTML from source data |

---

## Rebuilding the HTML (optional)

If you want to regenerate the file from the source JSON data:

## Special thanks to below repot which has done 80% of the work 
https://github.com/faisaltheparttimecoder/1000-duas-for-arafah

```bash
python build_standalone_flashcards.py
```

Requires Python 3 and the `duas_repo/data/` folder one level up.
