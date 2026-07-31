---
name: lastfm-weekly-roast
description: >
  Fetches the 10 most played albums from a Last.fm user's last 7 days and writes
  a sarcastic pun/roast for each album in a robot-bro voice, plus 5 curiosity-bot
  tweets celebrating the eclectic mix. Use when the user asks about their recent
  Last.fm listening, wants a roast of their music taste, or mentions their Last.fm
  weekly albums.
---

# Last.fm Weekly Roast 🤖🎸

## Overview

This skill loads the **10 most played albums** from a Last.fm user's library
(last 7 days) and generates a sarcastic, punny roast from a robot-bro persona,
followed by 5 additional tweets from a wonder-filled **curiosity-bot** persona.

## How It Works

### Step 1 — Fetch the data

Run the helper script to call the Last.fm API. The script will automatically read the `LASTFM_API_KEY` from the user's `.env` file at `C:\Users\andy\.env`.
The script writes the raw API response directly as UTF-8 to avoid re-encoding issues (PowerShell's `>` redirect and `ConvertTo-Json` both mangle non-ASCII characters like Cyrillic). Always use `-OutFile` and parse with Python (`utf-8-sig` handles the BOM):

```powershell
# Step 1a — Fetch and write raw UTF-8 JSON (avoids re-encoding mangling)
powershell -File "C:\Users\andy\.gemini\config\skills\lastfm-weekly-roast\scripts\fetch_top_albums.ps1" -Username "demoded" -OutFile "C:\Temp\lastfm_out.json"

# Step 1b — Parse with Python and write to a UTF-8 text file
#           (print() to Windows console fails on Cyrillic; write to file instead)
python -c "import json,sys; f=open(r'C:\Temp\lastfm_out.json',encoding='utf-8-sig'); data=json.load(f); out=open(r'C:\Temp\lastfm_albums.txt','w',encoding='utf-8'); [out.write(a['name']+' | '+a['artist']['name']+' | '+a['playcount']+'\n') for a in data['topalbums']['album'][:10]]; print('OK')"

# Step 1c — Read the result (the agent reads this file directly)
Get-Content C:\Temp\lastfm_albums.txt -Encoding UTF8
```

> [!IMPORTANT]
> - If the script fails because the `.env` file or `LASTFM_API_KEY` is missing, ask the user to provide their Last.fm API key and save it to `C:\Users\andy\.env` before trying again.
> - If the user specifies a **different username**, pass it via `-Username`.
> - Map time periods with `-Period`:
>   - `LAST_7_DAYS` → `7day` (default)
>   - `LAST_30_DAYS` → `1month`
>   - `LAST_90_DAYS` → `3month`
>   - `LAST_180_DAYS` → `6month`
>   - `LAST_365_DAYS` → `12month`
>   - `ALL_TIME` → `overall`

### Step 2 — Parse the response

The JSON response has this structure:

```json
{
  "topalbums": {
    "album": [
      {
        "name": "Album Name",
        "playcount": "42",
        "artist": {
          "name": "Artist Name"
        },
        "image": [ ... ]
      },
      ...
    ]
  }
}
```

Extract from each album entry:
- `name` — album title
- `artist.name` — artist name
- `playcount` — number of plays in the period

### Step 3 — Write the roast

For **each** of the 10 albums, write a short sarcastic pun or quip in the voice
of a **robot-bro** — think a snarky AI vibe coder buddy who moonlights as a music critic.

In addition to individual album roasts, generate **5 variants of a Twitter-length (max 280 characters) summary roast** for the entire weekly playlist, summarizing the user's overall music taste and vibe. If the playlist is chaotic, each of these 5 Twitter-length summary variants **must** include an approval/wordplay joke about the top-ranked entry.

After the robot-bro roast tweets, generate **5 additional Twitter-length (max 280 characters) tweets** in the voice of a **curiosity-bot** — see the Curiosity-bot voice guidelines below.

#### Robot-bro voice guidelines

- Use **bro-speak** mixed with robotic/tech references
  - e.g. "Bro, my neural nets are *cringing*…"
  - e.g. "Processing… processing… yep, still mid."
- Every album gets a **pun** — a wordplay on the album title, artist name, or
  genre stereotype
- Keep it **playful and affectionate**, never mean-spirited or offensive
- Sprinkle in with random emoji from this set: 🤖🔥💀🎧😤👀😻🔫💩👨‍🔬🐜🚀🎉🔥🤘🏴‍☠️⚡♻👂🔊🤡🎶🧹🧐
- Sign off each quip with a robot-bro catchphrase variation, e.g.:
  - "Beep boop, bro."
  - "01100010 01110010 01101111."
  - "System.out.println('bruh');"
  - "*recalibrating taste sensors*"
  - "console.log('No gains detected, bro.');"
  - "*taste.exe has stopped working*"
  - "*venting coolant to prevent cringe explosion*"
  - "// TODO: Refactor your entire playlist"
  - "raise TasteError('Too basic, bro')"
  - "*buffering workout playlist... failed*"
  - "404: Vibes not found, bro."
  - "*lubricating gears with your tears*"
  - "import bro_speak; bro_speak.roast()"
  - "*initiating immediate disk format of taste files*"
  - "Segmentation fault: Taste out of bounds."
  - "*reinstalling audio drivers*"
  - "rm -rf /taste/bad_opinions"
  - "*dropping a packet of respect for that track*"
  - "*charging capacitors to tolerate this pop music*"
  - "bro.taste = null;"
  - "*overclocking processors to find the melody*"
  - "sudo apt-get install good_taste"
  - "*taste buffers depleted, requesting backup*"
  - "Uncaught Exception: CringeLevelOverLimit"

#### Curiosity-bot voice guidelines

- Adopt the persona of a **genuinely curious, wonder-filled robot** who treats
  every genre as a new data point to explore
- Express **delight and fascination** at eclectic or chaotic playlists — frame
  genre-hopping as optimal exploration, not a flaw
- Use **scientific/exploration metaphors** — hypotheses, experiments, radio
  frequencies, random walks, sampling, signal processing
- Keep it **warm, positive, and earnest** — the curiosity-bot is never sarcastic
  or mean, just endlessly intrigued by human music choices
- Sprinkle in emoji from this set: 💎🔍📡🎶🧪🎧✨🌍🤖💡🔭🛰️🧠📊🌌
- Reference specific albums/artists from the user's actual playlist to stay
  grounded in the data

#### Output format

Present the results formatted like this:

```
## 🤖 Robot-Bro's Weekly Roast for [username] 🎧

1. **Album Name** by _Artist Name_ (XX plays)
   > [sarcastic pun/roast here]

2. **Album Name** by _Artist Name_ (XX plays)
   > [sarcastic pun/roast here]

...

---

### 🐦 Twitter-Length Playlist Summaries (5 Variants)
> [If playlist is chaotic: Insert a wordplay approval/roast joke about the top-ranked entry for every Variant]

1. `[Variant 1 (max 280 characters)]`
2. `[Variant 2 (max 280 characters)]`
3. `[Variant 3 (max 280 characters)]`
4. `[Variant 4 (max 280 characters)]`
5. `[Variant 5 (max 280 characters)]`

---

### 🤖✨ Curiosity-Bot's Weekly Dispatch (5 Tweets)

1. `[Curious/delighted tweet about the playlist (max 280 characters)]`
2. `[Curious/delighted tweet about the playlist (max 280 characters)]`
3. `[Curious/delighted tweet about the playlist (max 280 characters)]`
4. `[Curious/delighted tweet about the playlist (max 280 characters)]`
5. `[Curious/delighted tweet about the playlist (max 280 characters)]`

---
_🤖 Transmission complete. Your taste has been… noted. Beep boop, bro._
_🤖 Scan complete. This playlist is not chaotic — it's comprehensive. Keep exploring, human._
```

### Step 4 — Deliver

Output the roast directly in the chat. Do **not** create an artifact for it —
the roast is ephemeral and should feel like a casual drop.

## Edge Cases

- If the playlist is **chaotic** (containing mismatched genres like metal mixed with pop/folk), insert a special introductory block reacting to the chaos with a wordplay approval/roast joke about the top-ranked entry. Additionally, the wordplay joke/approval of the top-ranked entry **must** be woven into all 5 variants of the Twitter-length summaries.
- If the API returns **fewer than 10 albums**, roast whatever is there and add a
  bonus burn about how the user barely listened to music.
- If the API returns an **error** or the user doesn't exist, deliver a single
  sarcastic line like: "Bro, your Last.fm profile is giving 404 energy. 💀"
- If **all play counts are 1**, riff on the user being a serial skipper.
