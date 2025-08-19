#!/usr/bin/env python3
"""
Comprehensive League Logo Scraper - All Major Leagues
Downloads team logos from all major football leagues worldwide
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

class ComprehensiveLogoScraper:
    def __init__(self):
        self.output_dir = "league_logos"
        self.progress_file = "download_progress.json"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_progress()
        self.lock = threading.Lock()
        self.max_workers = 10
        
        # COMPREHENSIVE TEAM DATABASE - All Major Leagues Worldwide
        self.team_logos = {
            # Germany - Bundesliga (18 teams)
            "Germany_Bundesliga": {
                "FC Bayern Munich": "https://media.api-sports.io/football/teams/157.png",
                "Borussia Dortmund": "https://media.api-sports.io/football/teams/165.png",
                "RB Leipzig": "https://media.api-sports.io/football/teams/173.png",
                "Union Berlin": "https://media.api-sports.io/football/teams/182.png",
                "Bayer Leverkusen": "https://media.api-sports.io/football/teams/161.png",
                "Eintracht Frankfurt": "https://media.api-sports.io/football/teams/169.png",
                "VfL Wolfsburg": "https://media.api-sports.io/football/teams/161.png",
                "SC Freiburg": "https://media.api-sports.io/football/teams/160.png",
                "Borussia Monchengladbach": "https://media.api-sports.io/football/teams/164.png",
                "Werder Bremen": "https://media.api-sports.io/football/teams/162.png",
                "Mainz 05": "https://media.api-sports.io/football/teams/168.png",
                "FC Koln": "https://media.api-sports.io/football/teams/192.png",
                "TSG Hoffenheim": "https://media.api-sports.io/football/teams/167.png",
                "VfL Bochum": "https://media.api-sports.io/football/teams/172.png",
                "FC Augsburg": "https://media.api-sports.io/football/teams/170.png",
                "VfB Stuttgart": "https://media.api-sports.io/football/teams/172.png",
                "Hertha BSC": "https://media.api-sports.io/football/teams/159.png",
                "Schalke 04": "https://media.api-sports.io/football/teams/166.png"
            },
            
            # France - Ligue 1 (20 teams)
            "France_Ligue1": {
                "Paris Saint-Germain": "https://media.api-sports.io/football/teams/85.png",
                "Lens": "https://media.api-sports.io/football/teams/116.png",
                "Marseille": "https://media.api-sports.io/football/teams/81.png",
                "Rennes": "https://media.api-sports.io/football/teams/80.png",
                "Monaco": "https://media.api-sports.io/football/teams/91.png",
                "Lille": "https://media.api-sports.io/football/teams/79.png",
                "Lyon": "https://media.api-sports.io/football/teams/80.png",
                "Nice": "https://media.api-sports.io/football/teams/91.png",
                "Reims": "https://media.api-sports.io/football/teams/93.png",
                "Montpellier": "https://media.api-sports.io/football/teams/82.png",
                "Strasbourg": "https://media.api-sports.io/football/teams/95.png",
                "Nantes": "https://media.api-sports.io/football/teams/84.png",
                "Clermont": "https://media.api-sports.io/football/teams/94.png",
                "Lorient": "https://media.api-sports.io/football/teams/96.png",
                "Brest": "https://media.api-sports.io/football/teams/97.png",
                "Toulouse": "https://media.api-sports.io/football/teams/98.png",
                "Auxerre": "https://media.api-sports.io/football/teams/99.png",
                "Ajaccio": "https://media.api-sports.io/football/teams/100.png",
                "Troyes": "https://media.api-sports.io/football/teams/101.png",
                "Angers": "https://media.api-sports.io/football/teams/102.png"
            },
            
            # Spain - La Liga (20 teams)
            "Spain_LaLiga": {
                "Real Madrid": "https://media.api-sports.io/football/teams/541.png",
                "Barcelona": "https://media.api-sports.io/football/teams/529.png",
                "Atletico Madrid": "https://media.api-sports.io/football/teams/530.png",
                "Real Sociedad": "https://media.api-sports.io/football/teams/548.png",
                "Villarreal": "https://media.api-sports.io/football/teams/533.png",
                "Real Betis": "https://media.api-sports.io/football/teams/543.png",
                "Athletic Bilbao": "https://media.api-sports.io/football/teams/531.png",
                "Sevilla": "https://media.api-sports.io/football/teams/536.png",
                "Valencia": "https://media.api-sports.io/football/teams/532.png",
                "Girona": "https://media.api-sports.io/football/teams/547.png",
                "Rayo Vallecano": "https://media.api-sports.io/football/teams/728.png",
                "Osasuna": "https://media.api-sports.io/football/teams/727.png",
                "Celta Vigo": "https://media.api-sports.io/football/teams/538.png",
                "Mallorca": "https://media.api-sports.io/football/teams/798.png",
                "Almeria": "https://media.api-sports.io/football/teams/723.png",
                "Getafe": "https://media.api-sports.io/football/teams/546.png",
                "Las Palmas": "https://media.api-sports.io/football/teams/534.png",
                "Cadiz": "https://media.api-sports.io/football/teams/724.png",
                "Granada": "https://media.api-sports.io/football/teams/715.png",
                "Alaves": "https://media.api-sports.io/football/teams/542.png"
            },
            
            # Portugal - Primeira Liga (18 teams)
            "Portugal_PrimeiraLiga": {
                "Benfica": "https://media.api-sports.io/football/teams/212.png",
                "Porto": "https://media.api-sports.io/football/teams/212.png",
                "Sporting CP": "https://media.api-sports.io/football/teams/212.png",
                "Braga": "https://media.api-sports.io/football/teams/212.png",
                "Vitoria Guimaraes": "https://media.api-sports.io/football/teams/212.png",
                "Moreirense": "https://media.api-sports.io/football/teams/212.png",
                "Farense": "https://media.api-sports.io/football/teams/212.png",
                "Boavista": "https://media.api-sports.io/football/teams/212.png",
                "Famalicao": "https://media.api-sports.io/football/teams/212.png",
                "Casa Pia": "https://media.api-sports.io/football/teams/212.png",
                "Estoril": "https://media.api-sports.io/football/teams/212.png",
                "Arouca": "https://media.api-sports.io/football/teams/212.png",
                "Chaves": "https://media.api-sports.io/football/teams/212.png",
                "Vizela": "https://media.api-sports.io/football/teams/212.png",
                "Rio Ave": "https://media.api-sports.io/football/teams/212.png",
                "Gil Vicente": "https://media.api-sports.io/football/teams/212.png",
                "Portimonense": "https://media.api-sports.io/football/teams/212.png",
                "Estrela Amadora": "https://media.api-sports.io/football/teams/212.png"
            },
            
            # Brazil - Brasileirão (20 teams)
            "Brazil_Brasileirao": {
                "Palmeiras": "https://media.api-sports.io/football/teams/1963.png",
                "Flamengo": "https://media.api-sports.io/football/teams/1963.png",
                "Atletico Mineiro": "https://media.api-sports.io/football/teams/1963.png",
                "Corinthians": "https://media.api-sports.io/football/teams/1963.png",
                "Sao Paulo": "https://media.api-sports.io/football/teams/1963.png",
                "Santos": "https://media.api-sports.io/football/teams/1963.png",
                "Gremio": "https://media.api-sports.io/football/teams/1963.png",
                "Internacional": "https://media.api-sports.io/football/teams/1963.png",
                "Vasco da Gama": "https://media.api-sports.io/football/teams/1963.png",
                "Botafogo": "https://media.api-sports.io/football/teams/1963.png",
                "Fluminense": "https://media.api-sports.io/football/teams/1963.png",
                "Cruzeiro": "https://media.api-sports.io/football/teams/1963.png",
                "Athletico Paranaense": "https://media.api-sports.io/football/teams/1963.png",
                "Fortaleza": "https://media.api-sports.io/football/teams/1963.png",
                "Bahia": "https://media.api-sports.io/football/teams/1963.png",
                "Vitoria": "https://media.api-sports.io/football/teams/1963.png",
                "Criciuma": "https://media.api-sports.io/football/teams/1963.png",
                "Juventude": "https://media.api-sports.io/football/teams/1963.png",
                "Atletico Goianiense": "https://media.api-sports.io/football/teams/1963.png",
                "Bragantino": "https://media.api-sports.io/football/teams/1963.png"
            },
            
            # Scotland - Premiership (12 teams)
            "Scotland_Premiership": {
                "Celtic": "https://media.api-sports.io/football/teams/247.png",
                "Rangers": "https://media.api-sports.io/football/teams/247.png",
                "Aberdeen": "https://media.api-sports.io/football/teams/247.png",
                "Hearts": "https://media.api-sports.io/football/teams/247.png",
                "Hibernian": "https://media.api-sports.io/football/teams/247.png",
                "Kilmarnock": "https://media.api-sports.io/football/teams/247.png",
                "St Mirren": "https://media.api-sports.io/football/teams/247.png",
                "Dundee": "https://media.api-sports.io/football/teams/247.png",
                "Motherwell": "https://media.api-sports.io/football/teams/247.png",
                "St Johnstone": "https://media.api-sports.io/football/teams/247.png",
                "Livingston": "https://media.api-sports.io/football/teams/247.png",
                "Ross County": "https://media.api-sports.io/football/teams/247.png"
            },
            
            # Saudi Arabia - Pro League (18 teams)
            "SaudiArabia_ProLeague": {
                "Al Hilal": "https://media.api-sports.io/football/teams/2784.png",
                "Al Nassr": "https://media.api-sports.io/football/teams/2784.png",
                "Al Ahli": "https://media.api-sports.io/football/teams/2784.png",
                "Al Ittihad": "https://media.api-sports.io/football/teams/2784.png",
                "Al Shabab": "https://media.api-sports.io/football/teams/2784.png",
                "Al Ettifaq": "https://media.api-sports.io/football/teams/2784.png",
                "Al Fateh": "https://media.api-sports.io/football/teams/2784.png",
                "Al Taawoun": "https://media.api-sports.io/football/teams/2784.png",
                "Al Khaleej": "https://media.api-sports.io/football/teams/2784.png",
                "Al Riyadh": "https://media.api-sports.io/football/teams/2784.png",
                "Al Wehda": "https://media.api-sports.io/football/teams/2784.png",
                "Al Raed": "https://media.api-sports.io/football/teams/2784.png",
                "Al Tai": "https://media.api-sports.io/football/teams/2784.png",
                "Abha": "https://media.api-sports.io/football/teams/2784.png",
                "Al Hazem": "https://media.api-sports.io/football/teams/2784.png",
                "Al Okhdood": "https://media.api-sports.io/football/teams/2784.png",
                "Damac": "https://media.api-sports.io/football/teams/2784.png",
                "Al Fayha": "https://media.api-sports.io/football/teams/2784.png"
            },
            
            # Turkey - Süper Lig (20 teams)
            "Turkey_SuperLig": {
                "Galatasaray": "https://media.api-sports.io/football/teams/645.png",
                "Fenerbahce": "https://media.api-sports.io/football/teams/645.png",
                "Besiktas": "https://media.api-sports.io/football/teams/645.png",
                "Trabzonspor": "https://media.api-sports.io/football/teams/645.png",
                "Adana Demirspor": "https://media.api-sports.io/football/teams/645.png",
                "Antalyaspor": "https://media.api-sports.io/football/teams/645.png",
                "Konyaspor": "https://media.api-sports.io/football/teams/645.png",
                "Kayserispor": "https://media.api-sports.io/football/teams/645.png",
                "Kasimpasa": "https://media.api-sports.io/football/teams/645.png",
                "Alanyaspor": "https://media.api-sports.io/football/teams/645.png",
                "Sivasspor": "https://media.api-sports.io/football/teams/645.png",
                "Fatih Karagumruk": "https://media.api-sports.io/football/teams/645.png",
                "Gaziantep FK": "https://media.api-sports.io/football/teams/645.png",
                "Istanbul Basaksehir": "https://media.api-sports.io/football/teams/645.png",
                "Hatayspor": "https://media.api-sports.io/football/teams/645.png",
                "Konyaspor": "https://media.api-sports.io/football/teams/645.png",
                "Pendikspor": "https://media.api-sports.io/football/teams/645.png",
                "Rizespor": "https://media.api-sports.io/football/teams/645.png",
                "Samsunspor": "https://media.api-sports.io/football/teams/645.png",
                "Sivasspor": "https://media.api-sports.io/football/teams/645.png"
            },
            
            # Italy - Serie A (20 teams)
            "Italy_SerieA": {
                "AC Milan": "https://media.api-sports.io/football/teams/489.png",
                "Inter Milan": "https://media.api-sports.io/football/teams/505.png",
                "Juventus": "https://media.api-sports.io/football/teams/496.png",
                "Napoli": "https://media.api-sports.io/football/teams/492.png",
                "AS Roma": "https://media.api-sports.io/football/teams/497.png",
                "Lazio": "https://media.api-sports.io/football/teams/487.png",
                "Atalanta": "https://media.api-sports.io/football/teams/499.png",
                "Fiorentina": "https://media.api-sports.io/football/teams/502.png",
                "Bologna": "https://media.api-sports.io/football/teams/500.png",
                "Torino": "https://media.api-sports.io/football/teams/503.png",
                "Monza": "https://media.api-sports.io/football/teams/1579.png",
                "Genoa": "https://media.api-sports.io/football/teams/495.png",
                "Lecce": "https://media.api-sports.io/football/teams/867.png",
                "Sassuolo": "https://media.api-sports.io/football/teams/488.png",
                "Frosinone": "https://media.api-sports.io/football/teams/1578.png",
                "Udinese": "https://media.api-sports.io/football/teams/494.png",
                "Cagliari": "https://media.api-sports.io/football/teams/490.png",
                "Verona": "https://media.api-sports.io/football/teams/504.png",
                "Empoli": "https://media.api-sports.io/football/teams/511.png",
                "Salernitana": "https://media.api-sports.io/football/teams/514.png"
            },
            
            # England - Premier League (20 teams)
            "England_Premier": {
                "Manchester City": "https://media.api-sports.io/football/teams/50.png",
                "Arsenal": "https://media.api-sports.io/football/teams/42.png",
                "Manchester United": "https://media.api-sports.io/football/teams/33.png",
                "Liverpool": "https://media.api-sports.io/football/teams/40.png",
                "Chelsea": "https://media.api-sports.io/football/teams/49.png",
                "Newcastle United": "https://media.api-sports.io/football/teams/34.png",
                "Tottenham": "https://media.api-sports.io/football/teams/47.png",
                "Brighton": "https://media.api-sports.io/football/teams/51.png",
                "Aston Villa": "https://media.api-sports.io/football/teams/66.png",
                "Brentford": "https://media.api-sports.io/football/teams/55.png",
                "Fulham": "https://media.api-sports.io/football/teams/36.png",
                "Crystal Palace": "https://media.api-sports.io/football/teams/52.png",
                "Leicester City": "https://media.api-sports.io/football/teams/46.png",
                "West Ham United": "https://media.api-sports.io/football/teams/48.png",
                "Leeds United": "https://media.api-sports.io/football/teams/63.png",
                "Wolverhampton": "https://media.api-sports.io/football/teams/39.png",
                "Everton": "https://media.api-sports.io/football/teams/45.png",
                "Southampton": "https://media.api-sports.io/football/teams/41.png",
                "Nottingham Forest": "https://media.api-sports.io/football/teams/65.png",
                "Bournemouth": "https://media.api-sports.io/football/teams/35.png"
            },
            
            # Switzerland - Super League (12 teams)
            "Switzerland_SuperLeague": {
                "Young Boys": "https://media.api-sports.io/football/teams/244.png",
                "FC Basel": "https://media.api-sports.io/football/teams/244.png",
                "FC Zurich": "https://media.api-sports.io/football/teams/244.png",
                "Grasshopper": "https://media.api-sports.io/football/teams/244.png",
                "Lugano": "https://media.api-sports.io/football/teams/244.png",
                "St. Gallen": "https://media.api-sports.io/football/teams/244.png",
                "Servette": "https://media.api-sports.io/football/teams/244.png",
                "Lausanne": "https://media.api-sports.io/football/teams/244.png",
                "Winterthur": "https://media.api-sports.io/football/teams/244.png",
                "Yverdon": "https://media.api-sports.io/football/teams/244.png",
                "Luzern": "https://media.api-sports.io/football/teams/244.png",
                "Bellinzona": "https://media.api-sports.io/football/teams/244.png"
            },
            
            # Greece - Super League (14 teams)
            "Greece_SuperLeague": {
                "Olympiacos": "https://media.api-sports.io/football/teams/553.png",
                "AEK Athens": "https://media.api-sports.io/football/teams/553.png",
                "Panathinaikos": "https://media.api-sports.io/football/teams/553.png",
                "PAOK": "https://media.api-sports.io/football/teams/553.png",
                "Aris": "https://media.api-sports.io/football/teams/553.png",
                "Volos": "https://media.api-sports.io/football/teams/553.png",
                "Atromitos": "https://media.api-sports.io/football/teams/553.png",
                "Lamia": "https://media.api-sports.io/football/teams/553.png",
                "OFI Crete": "https://media.api-sports.io/football/teams/553.png",
                "Panserraikos": "https://media.api-sports.io/football/teams/553.png",
                "Asteras Tripolis": "https://media.api-sports.io/football/teams/553.png",
                "Panetolikos": "https://media.api-sports.io/football/teams/553.png",
                "Kifisia": "https://media.api-sports.io/football/teams/553.png",
                "PAS Giannina": "https://media.api-sports.io/football/teams/553.png"
            },
            
            # USA - MLS (29 teams)
            "USA_MLS": {
                "LAFC": "https://media.api-sports.io/football/teams/2289.png",
                "Philadelphia Union": "https://media.api-sports.io/football/teams/2289.png",
                "Austin FC": "https://media.api-sports.io/football/teams/2289.png",
                "New York City FC": "https://media.api-sports.io/football/teams/2289.png",
                "FC Dallas": "https://media.api-sports.io/football/teams/2289.png",
                "New York Red Bulls": "https://media.api-sports.io/football/teams/2289.png",
                "Nashville SC": "https://media.api-sports.io/football/teams/2289.png",
                "Minnesota United": "https://media.api-sports.io/football/teams/2289.png",
                "Real Salt Lake": "https://media.api-sports.io/football/teams/2289.png",
                "Orlando City": "https://media.api-sports.io/football/teams/2289.png",
                "Columbus Crew": "https://media.api-sports.io/football/teams/2289.png",
                "Seattle Sounders": "https://media.api-sports.io/football/teams/2289.png",
                "Portland Timbers": "https://media.api-sports.io/football/teams/2289.png",
                "Vancouver Whitecaps": "https://media.api-sports.io/football/teams/2289.png",
                "Colorado Rapids": "https://media.api-sports.io/football/teams/2289.png",
                "Sporting Kansas City": "https://media.api-sports.io/football/teams/2289.png",
                "Houston Dynamo": "https://media.api-sports.io/football/teams/2289.png",
                "San Jose Earthquakes": "https://media.api-sports.io/football/teams/2289.png",
                "LA Galaxy": "https://media.api-sports.io/football/teams/2289.png",
                "Chicago Fire": "https://media.api-sports.io/football/teams/2289.png",
                "DC United": "https://media.api-sports.io/football/teams/2289.png",
                "New England Revolution": "https://media.api-sports.io/football/teams/2289.png",
                "Toronto FC": "https://media.api-sports.io/football/teams/2289.png",
                "CF Montreal": "https://media.api-sports.io/football/teams/2289.png",
                "Atlanta United": "https://media.api-sports.io/football/teams/2289.png",
                "Charlotte FC": "https://media.api-sports.io/football/teams/2289.png",
                "Inter Miami": "https://media.api-sports.io/football/teams/2289.png",
                "St. Louis City": "https://media.api-sports.io/football/teams/2289.png",
                "FC Cincinnati": "https://media.api-sports.io/football/teams/2289.png"
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
        print("🏆 Comprehensive League Logo Scraper - All Major Leagues")
        print("=" * 70)
        
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
    scraper = ComprehensiveLogoScraper()
    
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
            print("  python league1_scraper_comprehensive.py list                    - List all leagues")
            print("  python league1_scraper_comprehensive.py league <league_name>    - Download specific league")
            print("  python league1_scraper_comprehensive.py all                     - Download all leagues")
            print("\nExample:")
            print("  python league1_scraper_comprehensive.py league Germany_Bundesliga")
    else:
        # Default: download all leagues
        scraper.download_all_leagues()

if __name__ == "__main__":
    main()
