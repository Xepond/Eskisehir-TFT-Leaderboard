# 🏆 TFT Campus Automation

> **Automated Discord community management for TFT players at Eskişehir Osmangazi University — powered by Riot Games API & GitHub Actions.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Riot Games API](https://img.shields.io/badge/Riot%20Games%20API-TFT--v1%20%7C%20Account--v1-D32936?style=for-the-badge&logo=riotgames&logoColor=white)](https://developer.riotgames.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Serverless%20Cron-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📖 Overview

This project is a fully serverless automation suite for managing a **Teamfight Tactics (TFT) Discord community** at Eskişehir Osmangazi University (OGÜ). Built by a Riot Games Campus Ambassador, it removes manual overhead from community management by automatically delivering weekly ranked leaderboards directly into Discord channels.

The entire infrastructure runs on **GitHub Actions cron jobs**, meaning zero server costs and zero maintenance overhead.

---

## ✨ Features

### 🏅 Weekly Ranked Leaderboard

- Fetches live ranked data for all registered campus players via the **Riot Games TFT API**.
- Resolves Riot IDs (`Name#TAG`) to PUUIDs using `Account-v1`, then to Summoner IDs using `TFT-v1`.
- Constructs a **sorted leaderboard** from Gold to Challenger and posts it as a rich **Discord Embed** with medal decorations (🥇🥈🥉).

### 🧮 Rank-to-Integer Progression Algorithm

- Implements a custom **tier + division + LP mapping** to produce a single comparable integer per player:

  ```
  Total LP = TIER_VALUE[tier] + RANK_VALUE[division] + leaguePoints
  ```

  Example: `Gold II (75 LP)` → `1200 + 200 + 75 = 1475`
- Enables **cross-tier comparisons** (e.g., Gold II vs. Platinum IV) and net LP gain/loss calculation week-over-week.

### 📦 Persistent Player Registry

- Player roster is stored in a lightweight **`players.json`** file — no database required.
- Easily extensible; add a new player by appending a `{ "name": "...", "tag": "..." }` entry.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11+ |
| **API Client** | `requests` |
| **HTML Parsing** | `BeautifulSoup4` |
| **Data Persistence** | JSON (flat-file) |
| **Riot APIs** | `Account-v1`, `TFT-v1` (League) |
| **Notifications** | Discord Webhooks (Embeds) |
| **Infrastructure** | GitHub Actions (Cron Jobs) |

---

## 🚀 Setup & Installation

### 1. Fork & Clone the Repository

```bash
git clone https://github.com/<your-username>/Eskisehir-TFT-Leaderboard.git
cd Eskisehir-TFT-Leaderboard
```

### 2. Install Dependencies

```bash
pip install requests beautifulsoup4
```

### 3. Configure Secrets (GitHub Actions)

This project reads credentials from environment variables, which should be stored as **GitHub Repository Secrets** — never hardcoded.

Navigate to your repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

| Secret Name | Description |
|---|---|
| `RIOT_API_KEY` | Your Riot Games Developer API Key from [developer.riotgames.com](https://developer.riotgames.com/) |
| `DISCORD_WEBHOOK` | Your Discord channel Webhook URL |

### 4. Register Players

Edit `players.json` to add your community members:

```json
[
  { "name": "PlayerOne", "tag": "TR1" },
  { "name": "PlayerTwo", "tag": "EUW" }
]
```

### 5. Configure the Cron Schedule

The GitHub Actions workflow (`.github/workflows/*.yml`) uses a cron expression to trigger jobs automatically. Edit the schedule to your preference:

```yaml
on:
  schedule:
    - cron: '0 18 * * 1'  # Every Monday at 18:00 UTC
```

---

## ⚙️ How It Works

```
GitHub Actions (Cron Trigger)
         │
         ▼
  tft_leaderboard.py
         │
         ├─► Read players.json
         │
         ├─► [For each player]
         │       ├─ Account-v1: Riot ID → PUUID
         │       ├─ TFT-v1 Summoner: PUUID → Summoner ID
         │       └─ TFT-v1 League: Summoner ID → Rank Data
         │
         ├─► Apply Rank-to-Integer algorithm → Sort leaderboard
         │
         └─► POST Discord Webhook → Rich Embed in channel
```

---

## 📁 Project Structure

```
Eskisehir-TFT-Leaderboard/
├── .github/
│   └── workflows/
│       └── leaderboard.yml      # GitHub Actions cron job definition
├── tft_leaderboard.py           # Core automation script
├── players.json                 # Registered player roster
└── README.md
```

---

## 👤 Author

**Kadir** — 3rd Year Computer Engineering Student & Riot Games Campus Ambassador  
📍 Eskişehir Osmangazi University

> Building community tools at the intersection of software engineering and gaming culture.

---

## ⚖️ Legal Jibber Jabber

*TFT Campus Automation isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.*

This project is developed in accordance with [Riot Games' Third-Party Development Policies](https://developer.riotgames.com/policies/general).
