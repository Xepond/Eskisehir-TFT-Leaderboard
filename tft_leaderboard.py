import requests
import os
import json

# Yapılandırma
API_KEY = os.getenv("RIOT_API_KEY")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
REGION = "europe" # Account-v1 için
PLATFORM = "tr1"  # TFT-v1 için

# Rankları sayısal değere çevirme tablosu (Matematiksel kıyas için)
TIER_VALUE = {
    "IRON": 0, "BRONZE": 400, "SILVER": 800, "GOLD": 1200,
    "PLATINUM": 1600, "EMERALD": 2000, "DIAMOND": 2400,
    "MASTER": 2800, "GRANDMASTER": 2800, "CHALLENGER": 2800
}
RANK_VALUE = {"IV": 0, "III": 100, "II": 200, "I": 300}

def get_summoner_ids(name, tag):
    # Riot ID -> PUUID (Account-v1)
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={API_KEY}"
    res = requests.get(url).json()
    puuid = res.get('puuid')
    
    # PUUID -> Summoner ID (TFT-v1)
    url_id = f"https://{PLATFORM}.api.riotgames.com/tft/summoner/v1/by-puuid/{puuid}?api_key={API_KEY}"
    res_id = requests.get(url_id).json()
    return res_id.get('id'), puuid

def get_tft_data(summoner_id):
    url = f"https://{PLATFORM}.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}?api_key={API_KEY}"
    res = requests.get(url).json()
    if not res: return None
    
    stats = res[0] # TFT verisi listenin ilk elemanıdır
    total_lp = TIER_VALUE.get(stats['tier'], 0) + RANK_VALUE.get(stats['rank'], 0) + stats['leaguePoints']
    
    return {
        "tier": stats['tier'],
        "rank": stats['rank'],
        "lp": stats['leaguePoints'],
        "total_lp": total_lp
    }

def main():
    with open('players.json', 'r') as f:
        players = json.load(f)
    
    leaderboard = []
    
    for p in players:
        try:
            s_id, _ = get_summoner_ids(p['name'], p['tag'])
            data = get_tft_data(s_id)
            if data:
                leaderboard.append({
                    "name": f"{p['name']}#{p['tag']}",
                    "rank_str": f"{data['tier']} {data['rank']} ({data['lp']} LP)",
                    "total_lp": data['total_lp']
                })
        except Exception as e:
            print(f"{p['name']} verisi alınamadı: {e}")

    # Sıralama: En yüksek toplam LP'den en düşüğe
    leaderboard.sort(key=lambda x: x['total_lp'], reverse=True)

    # Discord Mesajı Hazırlama
    fields = []
    for i, player in enumerate(leaderboard, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        fields.append({
            "name": f"{medal} {i}. {player['name']}",
            "value": f"Current Rank: **{player['rank_str']}**",
            "inline": False
        })

    payload = {
        "embeds": [{
            "title": "🏆 OGÜ Kampüsü - TFT Haftalık Liderlik Tablosu",
            "color": 15844367,
            "fields": fields,
            "footer": {"text": "Riot Kampüs Elçiliği Otomasyonu"}
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    main()