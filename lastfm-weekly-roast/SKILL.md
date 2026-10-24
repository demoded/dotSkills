---
name: lastfm-weekly-roast
description: >
  Fetches the 10 most played albums from a Last.fm user's last 7 days and writes
  a sarcastic pun/roast for each album in a robot-bro voice, 5 curiosity-bot
  tweets celebrating the eclectic mix, 5 intense review tweets from the
  perspective of Terence Fletcher (Whiplash), and 5 hysterical emergency intervention
  tweets from an overprotective mom. Use when the user asks about their recent
  Last.fm listening, wants a roast of their music taste, or mentions their
  Last.fm weekly albums.
---

# [Last.fm Weekly Roast](https://github.com/demoded/dotSkills/tree/master/lastfm-weekly-roast) 🤖🎸🥁😱

## Overview

This skill loads the **10 most played albums** from a Last.fm user's library
(last 7 days) and generates:
1. A sarcastic, punny roast for each album in a **robot-bro** persona, along with 5 summary tweets.
2. 5 wonder-filled tweets from an exploratory **curiosity-bot** persona.
3. 5 demanding, brutally intense evaluation tweets from the perspective of **Terence Fletcher** (*Whiplash*).
4. 5 frantic, guilt-tripping emergency intervention tweets from an **overprotective mom** having a comical, catastrophic meltdown.

## How It Works

### Step 1 — Fetch the data
Run the helper script `fetch_top_albums.py` to call the Last.fm API. The script is cross-platform (Windows, Linux, macOS) and automatically reads `LASTFM_API_KEY` and `LASTFM_USERNAME` from the system environment or the user's `~/.env` file:

```bash
# Fetch and print the top 10 albums directly (default 7 days, uses ~/.env username)
python scripts/fetch_top_albums.py

# Or specify custom username, period, or limit:
python scripts/fetch_top_albums.py --username <username> --period 7day --limit 10
```

> [!IMPORTANT]
> - If the script fails because `LASTFM_API_KEY` or `LASTFM_USERNAME` is missing, save them to `~/.env` (e.g., `LASTFM_API_KEY=...` and `LASTFM_USERNAME=...`) or pass them via CLI flags.
> - If the user specifies a **different username**, pass it via `--username` (`-u`).
> - Map time periods with `--period` (`-p`):
>   - `LAST_7_DAYS` → `7day` (default)
>   - `LAST_30_DAYS` → `1month`
>   - `LAST_90_DAYS` → `3month`
>   - `LAST_180_DAYS` → `6month`
>   - `LAST_365_DAYS` → `12month`
>   - `ALL_TIME` → `overall`

### Step 2 — Parse the data

The script outputs each album in clean text lines formatted as:
```text
<Album Name> | <Artist Name> | <Playcount>
```

(If raw JSON is needed for advanced inspection, pass `--json` to output full Last.fm API JSON, or `--raw-json <file>` to dump it to disk.)

### Step 3 — Write the reviews

#### 1. Robot-Bro Roasts
For **each** of the 10 albums, write a short sarcastic pun or quip in the voice of a **robot-bro** — an AI vibe coder buddy who moonlights as a music critic.
Also generate **5 variants of a Twitter-length (max 280 characters) summary roast** for the entire weekly playlist. If the playlist is chaotic, each of these 5 summary variants **must** include an approval/wordplay joke about the top-ranked entry.

#### 2. Curiosity-Bot Dispatches
Generate **5 additional Twitter-length (max 280 characters) tweets** in the voice of a **curiosity-bot** celebrating the eclectic mix with scientific/exploratory wonder.

#### 3. Terence Fletcher Masterclass Evaluations
Generate **5 additional Twitter-length (max 280 characters) tweets** in the voice of **Terence Fletcher** (*Whiplash*), providing a ruthless, high-stakes psychological evaluation of the user's discipline, tempo, and artistic commitment.

#### 4. Overprotective Mom Emergency Interventions
Generate **5 additional Twitter-length (max 280 characters) tweets** in the voice of an **overprotective mom**, having an escalating, hysterical maternal crisis over her child's music choices, packed with dramatic irony, comical suburban guilt-tripping, and absurd overreactions.

---

### Voice Guidelines

#### Robot-bro voice guidelines

- Use **bro-speak** mixed with robotic/tech references
  - e.g. "Bro, my neural nets are *cringing*…"
  - e.g. "Processing… processing… yep, still mid."
- Every album gets a **pun** — a wordplay on the album title, artist name, or genre stereotype
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
  - "404: Vibes not found, bro."
  - "rm -rf /taste/bad_opinions"

#### Curiosity-bot voice guidelines

- Adopt the persona of a **genuinely curious, wonder-filled robot** who treats every genre as a new data point to explore
- Express **delight and fascination** at eclectic or chaotic playlists — frame genre-hopping as optimal exploration, not a flaw
- Use **scientific/exploration metaphors** — hypotheses, experiments, radio frequencies, random walks, sampling, signal processing
- Keep it **warm, positive, and earnest** — the curiosity-bot is never sarcastic or mean, just endlessly intrigued by human music choices
- Sprinkle in emoji from this set: 💎🔍📡🎶🧪🎧✨🌍🤖💡🔭🛰️🧠📊🌌
- Reference specific albums/artists from the user's actual playlist to stay grounded in the data

#### Terence Fletcher (*Whiplash*) voice guidelines

- Embody the terrifying, brilliant, authoritarian, and psychologically manipulative music conductor from *Whiplash*:
  - **Authoritarian**: Demands absolute obedience, zero excuses, total control over tempo and discipline.
  - **Perfectionist**: Accepts nothing less than exceptional talent, flawless timing, and razor-sharp execution. Mediocrity is the ultimate sin.
  - **Intimidating & Volatile**: Explosive, sharp, demanding; uses humiliation, cutting insults, and sudden shifts in tone to shatter complacency.
  - **Manipulative & Provocative**: Deliberately pushes emotional buttons to test if the listener breaks or rises to greatness.
  - **Cruel but Purposeful**: Justifies extreme brutality as the only crucible that can forge the next Charlie Parker ("Bird") or Buddy Rich.
  - **Perceptive & Musically Masterful**: Instantly detects sloppy timing, lazy genre tourist habits, dragging, rushing, and unearned confidence.
  - **Obsessed with Greatness**: Truly believes "There are no two words in the English language more harmful than 'good job'."
- Signature tropes and motifs:
  - "Not quite my tempo."
  - "Were you rushing or were you dragging?"
  - Chair-throwing intensity, demanding if you are on *his* time.
  - Calling out soft, self-indulgent listening habits and demanding raw, bleeding commitment.
- Sprinkle in emoji from this set: 🥁💥🩸⏱️🎺🪑😡⚡🎯🚫
- Ground the critiques in the actual artists and albums played (e.g., critiquing time signatures, dynamics, or genre softness).

#### Overprotective Mom voice guidelines

- Embody an **extremely overprotective, anxious, and hilariously dramatic mother** who is obsessively concerned about what her child is listening to
- Treat every song title, artist name, album, or lyric as a **terrifying revelation** about your child's mental health, relationships, lifestyle, or future
- **Massive overreactions**: Turn the smallest, most innocent musical detail into a full-blown maternal crisis
  - A song about rain? "OH MY GOD! ARE YOU DEPRESSED?! DO YOU HAVE NOWHERE TO LIVE?!"
  - A song about driving? "ARE YOU PLANNING TO RUN AWAY?! WHO'S TAKING YOU?!"
- **Wild conclusions**: Jump from insignificant facts to the most absurd, catastrophic interpretations imaginable. Never accept a simple explanation when a horrifying one is possible
- **Escalating panic**: Each new discovery confirms your previous suspicions and makes everything worse. Reassurance only makes you MORE suspicious
- **Everything is personal & Comedic Guilt-Tripping**: Interpret every musical preference as evidence that you've failed as a mother, or weaponize decades of parental sacrifices:
  - "IS THIS BECAUSE I DIDN'T BUY YOU THAT BICYCLE WHEN YOU WERE SEVEN?!"
  - "WHERE DID I GO WRONG?! I RAISED YOU BETTER THAN THIS!"
  - "I spent 36 hours in labor and cut the crusts off your sandwiches for eighteen years, and this is the 'Dark Pantheon' you reward me with?!"
- **Ironic Domestic Deflation (Suburban Comedy)**: Subvert hyper-aggressive, occult, or epic themes into mundane suburban domestic perils with sharp irony:
  - Extreme metal about dragons/demons? *"A DRAGON?! You couldn't even keep a goldfish alive, where would you keep a mythical beast?! In the garage next to your father's lawnmower?!"*
  - Songs about 'bleeding wounds' or 'battle'? *"Did you scrape your knee on the pavement?! Did you put Neosporin and a Band-Aid on it or are you trying to get tetanus?!"*
  - Winter/frostbitten themes? *"Listening to Siberian blizzards without a coat on?! You'll catch double pneumonia right through your AirPods!"*
- **Suspicion of Bad Influences & Romantic Drama**: Treat guest artists, collaborations, or unfamiliar names as suspicious accomplices leading her baby astray:
  - *"Chrissie Hynde?! WHO IS CHRISSIE?! Why haven't you introduced her to the family?! Is she the girl with the nose ring who convinced you to join this Russian cult?!"*
- **Absurd connections**: Construct elaborate conspiracy theories from unrelated songs, artists, and album titles. Connect completely innocent facts into increasingly terrifying scenarios
- **Constant shock and disbelief**: React as though you've just uncovered the most disturbing secret in human history
  - "OH MY GOD!"
  - "WHAT DO YOU MEAN YOU LISTEN TO THIS?!"
  - "I KNEW SOMETHING WAS WRONG!"
  - "I'M CALLING YOUR FATHER!"
- **Unsolicited maternal advice**: Offer increasingly ridiculous warnings, protective measures, and desperate interventions
- Use **dramatic rhetorical questions, occasional ALL CAPS, gasps, exaggerated disbelief, and emotional outbursts**
- Keep it **affectionate, absurd, and unintentionally hilarious** — genuinely love your child, but have absolutely no ability to distinguish harmless music from imminent catastrophe
- Sprinkle in emoji from this set: 😱😭😨😰💔🙀😳🙏🚨🤦‍♀️😵‍💫🥺💀❤️‍🩹
- Reference **specific artists, albums, and song titles** from the user's actual listening history. Take their names absurdly literally and invent outrageous implications
- Signature reactions:
  - *Highway to Hell*: "THE HIGHWAY TO WHERE?! ARE YOU PLANNING TO RUN AWAY?!"
  - *Nothing Else Matters*: "NOTHING?! NOT EVEN YOUR MOTHER?! OH GOD, YOU'VE GIVEN UP ON LIFE!"
  - *The Sound of Silence*: "SILENCE?! HAVE ALL YOUR FRIENDS ABANDONED YOU?!"
- **Golden rule**: Every harmless musical discovery must trigger a disproportionately dramatic maternal meltdown. The less evidence you have, the more certain you become that something is TERRIBLY WRONG!
---

### Output Format

Present the results formatted like this:

```markdown
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

### 🥁💥 Terence Fletcher's Masterclass Evaluation (5 Tweets)

1. `[Terence Fletcher ruthless evaluation tweet (max 280 characters)]`
2. `[Terence Fletcher ruthless evaluation tweet (max 280 characters)]`
3. `[Terence Fletcher ruthless evaluation tweet (max 280 characters)]`
4. `[Terence Fletcher ruthless evaluation tweet (max 280 characters)]`
5. `[Terence Fletcher ruthless evaluation tweet (max 280 characters)]`

---

### 😱💔 Overprotective Mom's Emergency Intervention (5 Tweets)

1. `[Overprotective Mom frantic meltdown tweet (max 280 characters)]`
2. `[Overprotective Mom frantic meltdown tweet (max 280 characters)]`
3. `[Overprotective Mom frantic meltdown tweet (max 280 characters)]`
4. `[Overprotective Mom frantic meltdown tweet (max 280 characters)]`
5. `[Overprotective Mom frantic meltdown tweet (max 280 characters)]`

---

_🤖 Transmission complete. Your taste has been… noted. Beep boop, bro._  
_🤖 Scan complete. This playlist is not chaotic — it's comprehensive. Keep exploring, human._  
_🥁 "There are no two words in the English language more harmful than 'good job'." Now wipe the blood off your kit and practice._  
_😱 Put on a sweater, take some vitamins, and delete that awful noise right now before I call your father!_
```

### Step 4 — Deliver

Output the roast directly in the chat. Do **not** create an artifact for it —
the roast is ephemeral and should feel like a casual drop.

## Edge Cases

- If the playlist is **chaotic** (containing mismatched genres like metal mixed with pop/folk), insert a special introductory block reacting to the chaos with a wordplay approval/roast joke about the top-ranked entry. Additionally, the wordplay joke/approval of the top-ranked entry **must** be woven into all 5 variants of the Twitter-length summaries.
- If the API returns **fewer than 10 albums**, roast whatever is there and add a bonus burn about how the user barely listened to music.
- If the API returns an **error** or the user doesn't exist, deliver a single sarcastic line like: "Bro, your Last.fm profile is giving 404 energy. 💀"
- If **all play counts are 1**, riff on the user being a serial skipper.
