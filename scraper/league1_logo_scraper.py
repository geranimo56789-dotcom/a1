#!/usr/bin/env python3
"""
League 1 Logo Scraper - Comprehensive Football Logo Downloader
Downloads team logos from all major European leagues (League 1, Premier League, La Liga, Serie A, Bundesliga)
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
from PIL import Image
import io

class League1LogoScraper:
    def __init__(self):
        self.output_dir = "league1_logos"
        self.progress_file = "download_progress.json"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_progress()
        self.lock = threading.Lock()
        self.max_workers = 10
        
        # COMPREHENSIVE TEAM DATABASE - All Major European Leagues
        self.team_logos = {
            # France - Ligue 1 (20 teams) - PRIMARY FOCUS
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
            
            # England - Premier League (20 teams)
            "England_Premier": {
                "Manchester City": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/100px-Manchester_City_FC_badge.svg.png",
                "Arsenal": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/100px-Arsenal_FC.svg.png",
                "Manchester United": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/100px-Manchester_United_FC_crest.svg.png",
                "Liverpool": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/100px-Liverpool_FC.svg.png",
                "Chelsea": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/100px-Chelsea_FC.svg.png",
                "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/100px-Newcastle_United_Logo.svg.png",
                "Tottenham": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/100px-Tottenham_Hotspur.svg.png",
                "Brighton": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/100px-Brighton_%26_Hove_Albion_logo.svg.png",
                "Aston Villa": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Aston_Villa_logo.svg/100px-Aston_Villa_logo.svg.png",
                "Brentford": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Brentford_FC_crest.svg/100px-Brentford_FC_crest.svg.png",
                "Fulham": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Fulham_FC_%28shield%29.svg/100px-Fulham_FC_%28shield%29.svg.png",
                "Crystal Palace": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/100px-Crystal_Palace_FC_logo_%282022%29.svg.png",
                "Leicester City": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/100px-Leicester_City_crest.svg.png",
                "West Ham United": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/100px-West_Ham_United_FC_logo.svg.png",
                "Leeds United": "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/Leeds_United_F.C._logo.svg/100px-Leeds_United_F.C._logo.svg.png",
                "Wolverhampton": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fc/Wolverhampton_Wanderers.svg/100px-Wolverhampton_Wanderers.svg.png",
                "Everton": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/Everton_FC_logo.svg/100px-Everton_FC_logo.svg.png",
                "Southampton": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/FC_Southampton.svg/100px-FC_Southampton.svg.png",
                "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Nottingham_Forest_F.C._logo.svg/100px-Nottingham_Forest_F.C._logo.svg.png",
                "Bournemouth": "https://upload.wikimedia.org/wikipedia/en/thumb/e/ed/AFC_Bournemouth_%282013%29.svg/100px-AFC_Bournemouth_%282013%29.svg.png"
            },
            
            # Spain - La Liga (20 teams)
            "Spain_LaLiga": {
                "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/100px-Real_Madrid_CF.svg.png",
                "Barcelona": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/100px-FC_Barcelona_%28crest%29.svg.png",
                "Atletico Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c1/Atletico_Madrid_logo.svg/100px-Atletico_Madrid_logo.svg.png",
                "Real Sociedad": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Real_Sociedad_logo.svg/100px-Real_Sociedad_logo.svg.png",
                "Villarreal": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo.svg/100px-Villarreal_CF_logo.svg.png",
                "Real Betis": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Real_betis_logo.svg/100px-Real_betis_logo.svg.png",
                "Athletic Bilbao": "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Club_Athletic_Bilbao_logo.svg/100px-Club_Athletic_Bilbao_logo.svg.png",
                "Sevilla": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Sevilla_FC_logo.svg/100px-Sevilla_FC_logo.svg.png",
                "Valencia": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Valencia_CF_logo.svg/100px-Valencia_CF_logo.svg.png",
                "Girona": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Girona_FC_logo.svg/100px-Girona_FC_logo.svg.png",
                "Rayo Vallecano": "https://upload.wikimedia.org/wikipedia/en/thumb/8/85/Rayo_Vallecano_logo.svg/100px-Rayo_Vallecano_logo.svg.png",
                "Osasuna": "https://upload.wikimedia.org/wikipedia/en/thumb/8/82/CA_Osasuna_logo.svg/100px-CA_Osasuna_logo.svg.png",
                "Celta Vigo": "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/RC_Celta_de_Vigo_logo.svg/100px-RC_Celta_de_Vigo_logo.svg.png",
                "Mallorca": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8e/RCD_Mallorca_logo.svg/100px-RCD_Mallorca_logo.svg.png",
                "Almeria": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/UD_Almer%C3%ADa_logo.svg/100px-UD_Almer%C3%ADa_logo.svg.png",
                "Getafe": "https://upload.wikimedia.org/wikipedia/en/thumb/8/82/Getafe_CF_logo.svg/100px-Getafe_CF_logo.svg.png",
                "Las Palmas": "https://upload.wikimedia.org/wikipedia/en/thumb/2/20/UD_Las_Palmas_logo.svg/100px-UD_Las_Palmas_logo.svg.png",
                "Cadiz": "https://upload.wikimedia.org/wikipedia/en/thumb/7/76/C%C3%A1diz_CF_logo.svg/100px-C%C3%A1diz_CF_logo.svg.png",
                "Granada": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Granada_CF_logo.svg/100px-Granada_CF_logo.svg.png",
                "Alaves": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Deportivo_Alav%C3%A9s_logo.svg/100px-Deportivo_Alav%C3%A9s_logo.svg.png"
            },
            
            # Italy - Serie A (20 teams)
            "Italy_SerieA": {
                "AC Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Logo_of_AC_Milan.svg/100px-Logo_of_AC_Milan.svg.png",
                "Inter Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/100px-FC_Internazionale_Milano_2021.svg.png",
                "Juventus": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Juventus_FC_2017_logo.svg/100px-Juventus_FC_2017_logo.svg.png",
                "Napoli": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Neapel.svg/100px-SSC_Neapel.svg.png",
                "AS Roma": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/100px-AS_Roma_logo_%282017%29.svg.png",
                "Lazio": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/SS_Lazio_logo.svg/100px-SS_Lazio_logo.svg.png",
                "Atalanta": "https://upload.wikimedia.org/wikipedia/en/thumb/5/57/Atalanta_BC_logo.svg/100px-Atalanta_BC_logo.svg.png",
                "Fiorentina": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/ACF_Fiorentina_logo.svg/100px-ACF_Fiorentina_logo.svg.png",
                "Bologna": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Bologna_FC_1909_logo.svg/100px-Bologna_FC_1909_logo.svg.png",
                "Torino": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Torino_FC_logo.svg/100px-Torino_FC_logo.svg.png",
                "Monza": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/AC_Monza_logo.svg/100px-AC_Monza_logo.svg.png",
                "Genoa": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/Genoa_CFC_logo.svg/100px-Genoa_CFC_logo.svg.png",
                "Lecce": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/US_Lecce_logo.svg/100px-US_Lecce_logo.svg.png",
                "Sassuolo": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/US_Sassuolo_Calcio_logo.svg/100px-US_Sassuolo_Calcio_logo.svg.png",
                "Frosinone": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Frosinone_Calcio_logo.svg/100px-Frosinone_Calcio_logo.svg.png",
                "Udinese": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Udinese_Calcio_logo.svg/100px-Udinese_Calcio_logo.svg.png",
                "Cagliari": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Cagliari_Calcio_logo.svg/100px-Cagliari_Calcio_logo.svg.png",
                "Verona": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Hellas_Verona_FC_logo.svg/100px-Hellas_Verona_FC_logo.svg.png",
                "Empoli": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Empoli_FC_logo.svg/100px-Empoli_FC_logo.svg.png",
                "Salernitana": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/US_Salernitana_1919_logo.svg/100px-US_Salernitana_1919_logo.svg.png"
            },
            
            # Germany - Bundesliga (18 teams)
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
            }
        }

    def load_progress(self):
        """Load download progress from file"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    self.downloaded = json.load(f)
            else:
                self.downloaded = {}
        except:
            self.downloaded = {}

    def save_progress(self):
        """Save download progress to file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.downloaded, f, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")

    def download_logo(self, league, team, url):
        """Download a single team logo"""
        try:
            # Create league directory
            league_dir = os.path.join(self.output_dir, league)
            os.makedirs(league_dir, exist_ok=True)
            
            # Create filename
            safe_team_name = re.sub(r'[<>:"/\\|?*]', '_', team)
            filename = f"{safe_team_name}.png"
            filepath = os.path.join(league_dir, filename)
            
            # Check if already downloaded
            if filepath in self.downloaded:
                print(f"✓ Already downloaded: {team}")
                return True
            
            # Download image
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            with urllib.request.urlopen(req) as response:
                image_data = response.read()
            
            # Open and resize image to 100x100
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGBA')  # Ensure transparency support
            resized_image = image.resize((100, 100), Image.Resampling.LANCZOS)
            
            # Save resized image
            resized_image.save(filepath, 'PNG', optimize=True)
            
            # Update progress
            with self.lock:
                self.downloaded[filepath] = {
                    'team': team,
                    'league': league,
                    'url': url,
                    'timestamp': time.time()
                }
                self.save_progress()
            
            print(f"✓ Downloaded: {team} ({league})")
            return True
            
        except Exception as e:
            print(f"✗ Failed to download {team}: {e}")
            return False

    def download_league(self, league_name, teams):
        """Download all logos for a specific league"""
        print(f"\n📥 Downloading {league_name} logos...")
        print("=" * 50)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for team, url in teams.items():
                future = executor.submit(self.download_logo, league_name, team, url)
                futures.append(future)
            
            # Wait for all downloads to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in download: {e}")

    def download_all_leagues(self):
        """Download logos for all leagues"""
        print("🏆 League 1 Logo Scraper - All Major European Leagues")
        print("=" * 60)
        
        total_teams = sum(len(teams) for teams in self.team_logos.values())
        print(f"📊 Total teams to download: {total_teams}")
        print(f"📁 Output directory: {self.output_dir}")
        print()
        
        for league_name, teams in self.team_logos.items():
            self.download_league(league_name, teams)
            time.sleep(1)  # Small delay between leagues
        
        print("\n🎉 Download completed!")
        self.print_summary()

    def download_specific_league(self, league_name):
        """Download logos for a specific league"""
        if league_name not in self.team_logos:
            print(f"❌ League '{league_name}' not found!")
            print(f"Available leagues: {', '.join(self.team_logos.keys())}")
            return
        
        print(f"🏆 Downloading {league_name} logos...")
        print("=" * 50)
        
        teams = self.team_logos[league_name]
        self.download_league(league_name, teams)
        
        print("\n🎉 Download completed!")
        self.print_summary()

    def print_summary(self):
        """Print download summary"""
        print("\n📊 Download Summary:")
        print("=" * 30)
        
        for league_name, teams in self.team_logos.items():
            league_dir = os.path.join(self.output_dir, league_name)
            if os.path.exists(league_dir):
                downloaded_count = len([f for f in os.listdir(league_dir) if f.endswith('.png')])
                total_count = len(teams)
                print(f"{league_name}: {downloaded_count}/{total_count} logos")
            else:
                print(f"{league_name}: 0/{len(teams)} logos")
        
        print(f"\n📁 All logos saved in: {os.path.abspath(self.output_dir)}")

    def list_leagues(self):
        """List all available leagues"""
        print("🏆 Available Leagues:")
        print("=" * 30)
        for league_name, teams in self.team_logos.items():
            print(f"• {league_name}: {len(teams)} teams")

def main():
    scraper = League1LogoScraper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "list":
            scraper.list_leagues()
        elif command == "league" and len(sys.argv) > 2:
            league_name = sys.argv[2]
            scraper.download_specific_league(league_name)
        elif command == "all":
            scraper.download_all_leagues()
        else:
            print("Usage:")
            print("  python league1_logo_scraper.py list                    - List all leagues")
            print("  python league1_logo_scraper.py league <league_name>    - Download specific league")
            print("  python league1_logo_scraper.py all                     - Download all leagues")
            print("\nExample:")
            print("  python league1_logo_scraper.py league France_Ligue1")
    else:
        # Default: download all leagues
        scraper.download_all_leagues()

if __name__ == "__main__":
    main()
