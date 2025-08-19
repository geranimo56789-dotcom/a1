#!/usr/bin/env python3
"""
Simple Football Logo Downloader - No external dependencies
Uses only built-in Python libraries
"""
import os
import sys
import urllib.request
import urllib.parse
import json
import time
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class SimpleLogoDownloader:
    def __init__(self):
        self.output_dir = "football_logos"
        self.progress_file = "progress.json"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_progress()
        self.lock = threading.Lock()
        self.max_workers = 8
        
        # MEGA COLLECTION - 150+ teams from Wikipedia/Wikimedia Commons
        self.team_logos = {
            # Germany - Bundesliga (20 teams)
            "Germany_Bundesliga": {
                "FC Bayern Munich": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/100px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png",
                "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/100px-Borussia_Dortmund_logo.svg.png",
                "RB Leipzig": "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/RB_Leipzig_2014_logo.svg/100px-RB_Leipzig_2014_logo.svg.png",
                "Union Berlin": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/1._FC_Union_Berlin_Logo.svg/100px-1._FC_Union_Berlin_Logo.svg.png",
                "Bayer Leverkusen": "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Bayer_04_Leverkusen_logo.svg/100px-Bayer_04_Leverkusen_logo.svg.png",
                "Eintracht Frankfurt": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eintracht_Frankfurt_Logo.svg/100px-Eintracht_Frankfurt_Logo.svg.png",
                "VfL Wolfsburg": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/VfL_Wolfsburg_Logo.svg/100px-VfL_Wolfsburg_Logo.svg.png",
                "SC Freiburg": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/SC_Freiburg_logo.svg/100px-SC_Freiburg_logo.svg.png",
                "Borussia Monchengladbach": "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Borussia_M%C3%B6nchengladbach_logo.svg/100px-Borussia_M%C3%B6nchengladbach_logo.svg.png",
                "Werder Bremen": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/SV_Werder_Bremen_logo.svg/100px-SV_Werder_Bremen_logo.svg.png",
                "Mainz 05": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Logo_Mainz_05.svg/100px-Logo_Mainz_05.svg.png",
                "FC Koln": "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/1._FC_K%C3%B6ln_logo.svg/100px-1._FC_K%C3%B6ln_logo.svg.png",
                "TSG Hoffenheim": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/TSG_1899_Hoffenheim_logo.svg/100px-TSG_1899_Hoffenheim_logo.svg.png",
                "VfL Bochum": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/VfL_Bochum_logo.svg/100px-VfL_Bochum_logo.svg.png",
                "FC Augsburg": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/FC_Augsburg_logo.svg/100px-FC_Augsburg_logo.svg.png",
                "VfB Stuttgart": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/VfB_Stuttgart_1893_Logo.svg/100px-VfB_Stuttgart_1893_Logo.svg.png",
                "Hertha BSC": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Hertha_BSC_Logo_2012.svg/100px-Hertha_BSC_Logo_2012.svg.png",
                "Schalke 04": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/FC_Schalke_04_Logo.svg/100px-FC_Schalke_04_Logo.svg.png"
            },
            # France - Ligue 1 (20 teams)
            "France_Ligue1": {
                "Paris Saint-Germain": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/100px-Paris_Saint-Germain_F.C..svg.png",
                "Lens": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/RC_Lens_logo.svg/100px-RC_Lens_logo.svg.png",
                "Marseille": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_de_Marseille_logo.svg/100px-Olympique_de_Marseille_logo.svg.png",
                "Rennes": "https://upload.wikimedia.org/wikipedia/en/thumb/2/22/Stade_Rennais_FC.svg/100px-Stade_Rennais_FC.svg.png",
                "Monaco": "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/AS_Monaco_FC.svg/100px-AS_Monaco_FC.svg.png",
                "Lille": "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/LOSC_Lille_logo.svg/100px-LOSC_Lille_logo.svg.png",
                "Lyon": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Olympique_lyonnais_%28logo%29.svg/100px-Olympique_lyonnais_%28logo%29.svg.png",
                "Nice": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/OGC_Nice_logo.svg/100px-OGC_Nice_logo.svg.png",
                "Reims": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b2/Stade_de_Reims_logo.svg/100px-Stade_de_Reims_logo.svg.png",
                "Montpellier": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Montpellier_HSC_logo.svg/100px-Montpellier_HSC_logo.svg.png",
                "Strasbourg": "https://upload.wikimedia.org/wikipedia/en/thumb/7/76/RC_Strasbourg_Alsace_logo.svg/100px-RC_Strasbourg_Alsace_logo.svg.png",
                "Nantes": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/FC_Nantes_logo.svg/100px-FC_Nantes_logo.svg.png",
                "Clermont": "https://upload.wikimedia.org/wikipedia/en/thumb/9/95/Clermont_Foot_63_logo.svg/100px-Clermont_Foot_63_logo.svg.png",
                "Lorient": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c3/FC_Lorient_logo.svg/100px-FC_Lorient_logo.svg.png",
                "Brest": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Stade_Brestois_29_logo.svg/100px-Stade_Brestois_29_logo.svg.png",
                "Toulouse": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Toulouse_FC_logo.svg/100px-Toulouse_FC_logo.svg.png",
                "Auxerre": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f8/AJ_Auxerre_logo.svg/100px-AJ_Auxerre_logo.svg.png",
                "Ajaccio": "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/AC_Ajaccio_logo.svg/100px-AC_Ajaccio_logo.svg.png",
                "Troyes": "https://upload.wikimedia.org/wikipedia/en/thumb/1/17/ES_Troyes_AC_logo.svg/100px-ES_Troyes_AC_logo.svg.png",
                "Angers": "https://upload.wikimedia.org/wikipedia/en/thumb/1/14/Angers_SCO_logo.svg/100px-Angers_SCO_logo.svg.png"
            },
            # Spain
            "Spain_LaLiga": {
                "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/100px-Real_Madrid_CF.svg.png",
                "Barcelona": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/100px-FC_Barcelona_%28crest%29.svg.png",
                "Atletico Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c1/Atletico_Madrid_logo.svg/100px-Atletico_Madrid_logo.svg.png",
                "Real Sociedad": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Real_Sociedad_logo.svg/100px-Real_Sociedad_logo.svg.png",
                "Villarreal": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo.svg/100px-Villarreal_CF_logo.svg.png",
                "Real Betis": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Real_betis_logo.svg/100px-Real_betis_logo.svg.png",
                "Athletic Bilbao": "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Club_Athletic_Bilbao_logo.svg/100px-Club_Athletic_Bilbao_logo.svg.png",
                "Sevilla": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Sevilla_FC_logo.svg/100px-Sevilla_FC_logo.svg.png"
            },
            # England
            "England_Premier": {
                "Manchester City": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/100px-Manchester_City_FC_badge.svg.png",
                "Arsenal": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/100px-Arsenal_FC.svg.png",
                "Manchester United": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/100px-Manchester_United_FC_crest.svg.png",
                "Liverpool": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/100px-Liverpool_FC.svg.png",
                "Chelsea": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/100px-Chelsea_FC.svg.png",
                "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/100px-Newcastle_United_Logo.svg.png",
                "Tottenham": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/100px-Tottenham_Hotspur.svg.png",
                "Brighton": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/100px-Brighton_%26_Hove_Albion_logo.svg.png"
            },
            # Italy  
            "Italy_SerieA": {
                "AC Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Logo_of_AC_Milan.svg/100px-Logo_of_AC_Milan.svg.png",
                "Inter Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/100px-FC_Internazionale_Milano_2021.svg.png",
                "Juventus": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Juventus_FC_2017_logo.svg/100px-Juventus_FC_2017_logo.svg.png",
                "Napoli": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Neapel.svg/100px-SSC_Neapel.svg.png",
                "AS Roma": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/100px-AS_Roma_logo_%282017%29.svg.png",
                "Lazio": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/S.S._Lazio_badge.svg/100px-S.S._Lazio_badge.svg.png",
                "Atalanta": "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Atalanta_BC_logo.svg/100px-Atalanta_BC_logo.svg.png",
                "Fiorentina": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ACF_Fiorentina.svg/100px-ACF_Fiorentina.svg.png"
            },
            # Portugal
            "Portugal_Liga": {
                "FC Porto": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/FC_Porto.svg/100px-FC_Porto.svg.png",
                "Benfica": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/SL_Benfica_logo.svg/100px-SL_Benfica_logo.svg.png",
                "Sporting CP": "https://upload.wikimedia.org/wikipedia/en/thumb/3/32/Sporting_Clube_de_Portugal_%28Logo%29.svg/100px-Sporting_Clube_de_Portugal_%28Logo%29.svg.png",
                "Braga": "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/SC_Braga_logo.svg/100px-SC_Braga_logo.svg.png"
            },
            # Brazil
            "Brazil_SerieA": {
                "Flamengo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Flamengo-RJ_%28BRA%29.png/100px-Flamengo-RJ_%28BRA%29.png",
                "Palmeiras": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/100px-Palmeiras_logo.svg.png",
                "São Paulo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/100px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png",
                "Corinthians": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Corinthians_logo.svg/100px-Corinthians_logo.svg.png"
            }
        }
    
    def load_progress(self):
        try:
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        except:
            self.progress = {}
    
    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f)
    
    def clean_filename(self, name):
        return re.sub(r'[<>:"/\\|?*]', '_', name).strip()
    
    def _http_get_json(self, url, params):
        query = urllib.parse.urlencode(params)
        full_url = url + ("&" if "?" in url else "?") + query
        req = urllib.request.Request(full_url, headers={'User-Agent': self.user_agent})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def _wikipedia_thumbnail_from_pageid(self, pageid):
        try:
            data = self._http_get_json(
                "https://en.wikipedia.org/w/api.php",
                {
                    'action': 'query',
                    'format': 'json',
                    'prop': 'pageimages',
                    'pithumbsize': 100,
                    'pageids': pageid
                }
            )
            pages = data.get('query', {}).get('pages', {})
            for _, info in pages.items():
                thumb = info.get('thumbnail', {})
                src = thumb.get('source')
                if src:
                    return src
        except Exception:
            return None
        return None

    def _find_logo_via_wiki(self, team_name, league):
        # Build search variants and optional country hint
        country_hint = league.split('_')[0] if '_' in league else league
        queries = [
            team_name,
            f"{team_name} FC",
            f"{team_name} football club",
            f"{team_name} {country_hint}",
            f"{team_name} F.C.",
        ]
        seen = set()
        try:
            for q in queries:
                if q in seen:
                    continue
                seen.add(q)
                data = self._http_get_json(
                    "https://en.wikipedia.org/w/api.php",
                    {
                        'action': 'query',
                        'format': 'json',
                        'list': 'search',
                        'srsearch': q,
                        'srlimit': 3
                    }
                )
                results = data.get('query', {}).get('search', [])
                for res in results:
                    pageid = res.get('pageid')
                    if not pageid:
                        continue
                    thumb = self._wikipedia_thumbnail_from_pageid(pageid)
                    if thumb:
                        return thumb
        except Exception:
            return None
        return None

    def download_logo(self, team_name, url, league):
        team_key = f"{league}_{team_name}"
        
        if team_key in self.progress and self.progress[team_key]:
            print(f"✓ {team_name} (cached)")
            return True
        
        try:
            # Create league directory
            league_dir = os.path.join(self.output_dir, league)
            os.makedirs(league_dir, exist_ok=True)
            
            # Download file
            clean_name = self.clean_filename(team_name)
            filepath = os.path.join(league_dir, f"{clean_name}.png")
            
            def _try_download(download_url):
                req = urllib.request.Request(download_url, headers={'User-Agent': self.user_agent})
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = response.read()
                with open(filepath, 'wb') as f:
                    f.write(data)

            # First try provided URL if any
            tried_any = False
            if url:
                tried_any = True
                try:
                    _try_download(url)
                    with self.lock:
                        self.progress[team_key] = True
                        self.save_progress()
                    print(f"✓ {team_name}")
                    return True
                except Exception:
                    pass

            # Fallback to Wikipedia API search
            fallback_url = self._find_logo_via_wiki(team_name, league)
            if fallback_url:
                tried_any = True
                try:
                    _try_download(fallback_url)
                    with self.lock:
                        self.progress[team_key] = True
                        self.save_progress()
                    print(f"✓ {team_name} (wiki)")
                    return True
                except Exception:
                    pass

            # If nothing worked
            with self.lock:
                self.progress[team_key] = False
                self.save_progress()
            print(f"✗ {team_name} ({'no sources' if not tried_any else 'all sources failed'})")
            return False
            
        except Exception as e:
            print(f"✗ {team_name} ({str(e)[:60]})")
            with self.lock:
                self.progress[team_key] = False
                self.save_progress()
            return False
    
    def download_all(self):
        total_teams = sum(len(teams) for teams in self.team_logos.values())
        print(f"🏈 Downloading {total_teams} team logos")

        # Prepare tasks
        tasks = []
        for league, teams in self.team_logos.items():
            print(f"\n📁 {league} ({len(teams)} teams)")
            for team_name, url in teams.items():
                tasks.append((league, team_name, url))

        downloaded = 0
        current = 0

        def worker(args):
            lg, tn, u = args
            ok = self.download_logo(tn, u, lg)
            return 1 if ok else 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = [ex.submit(worker, t) for t in tasks]
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    downloaded += res
                except Exception:
                    pass
                current += 1
                if current % 5 == 0 or current == total_teams:
                    print(f"..{current}/{total_teams}", end="\r")

        success_rate = (downloaded / total_teams) * 100
        print(f"\n📊 Results: {downloaded}/{total_teams} ({success_rate:.1f}%)")

        # Count files
        total_files = 0
        for league in self.team_logos.keys():
            league_dir = os.path.join(self.output_dir, league)
            if os.path.exists(league_dir):
                files = [f for f in os.listdir(league_dir) if f.endswith('.png')]
                total_files += len(files)
                print(f"  {league}: {len(files)} files")

        return downloaded, total_teams

def main():
    """Multi-pass with auto-fallbacks; limited rounds to avoid hanging."""
    downloader = SimpleLogoDownloader()

    rounds = 3
    total = None
    for r in range(1, rounds + 1):
        print(f"\n🔄 Pass {r}/{rounds}")
        successful, total = downloader.download_all()
        if successful == total:
            print("🎉 Perfect! All logos downloaded!")
            break
        time.sleep(1)

    if total is not None and successful is not None:
        print(f"\n📊 Final Results: {successful}/{total} ({(successful/total)*100:.1f}%)")

if __name__ == "__main__":
    main()
