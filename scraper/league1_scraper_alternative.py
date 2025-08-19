#!/usr/bin/env python3
"""
League 1 Logo Scraper - Alternative Sources Version
Downloads team logos from reliable alternative sources (not Wikipedia)
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

class League1LogoScraperAlternative:
    def __init__(self):
        self.output_dir = "league1_logos"
        self.progress_file = "download_progress.json"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_progress()
        self.lock = threading.Lock()
        self.max_workers = 10
        
        # ALTERNATIVE SOURCES - No Wikipedia dependencies
        self.team_logos = {
            # France - Ligue 1 (20 teams) - PRIMARY FOCUS
            "France_Ligue1": {
                "Paris Saint-Germain": "https://www.psg.fr/static/img/logo-psg.png",
                "Lens": "https://www.rclens.fr/sites/default/files/logo-rc-lens.png",
                "Marseille": "https://www.om.fr/sites/default/files/logo-om.png",
                "Rennes": "https://www.staderennais.com/sites/default/files/logo-rennes.png",
                "Monaco": "https://www.asmonaco.com/sites/default/files/logo-monaco.png",
                "Lille": "https://www.losc.fr/sites/default/files/logo-lille.png",
                "Lyon": "https://www.ol.fr/sites/default/files/logo-lyon.png",
                "Nice": "https://www.ogcnice.com/sites/default/files/logo-nice.png",
                "Reims": "https://www.stade-de-reims.com/sites/default/files/logo-reims.png",
                "Montpellier": "https://www.mhscfoot.com/sites/default/files/logo-montpellier.png",
                "Strasbourg": "https://www.rcstrasbourgalsace.fr/sites/default/files/logo-strasbourg.png",
                "Nantes": "https://www.fcnantes.com/sites/default/files/logo-nantes.png",
                "Clermont": "https://www.clermontfoot.com/sites/default/files/logo-clermont.png",
                "Lorient": "https://www.fclorient.bzh/sites/default/files/logo-lorient.png",
                "Brest": "https://www.sb29.bzh/sites/default/files/logo-brest.png",
                "Toulouse": "https://www.toulousefc.com/sites/default/files/logo-toulouse.png",
                "Auxerre": "https://www.aja.fr/sites/default/files/logo-auxerre.png",
                "Ajaccio": "https://www.ac-ajaccio.corsica/sites/default/files/logo-ajaccio.png",
                "Troyes": "https://www.estac.fr/sites/default/files/logo-troyes.png",
                "Angers": "https://www.angers-sco.fr/sites/default/files/logo-angers.png"
            },
            
            # England - Premier League (20 teams) - Alternative sources
            "England_Premier": {
                "Manchester City": "https://www.mancity.com/assets/images/logo.png",
                "Arsenal": "https://www.arsenal.com/sites/default/files/logo-arsenal.png",
                "Manchester United": "https://www.manutd.com/sites/default/files/logo-man-utd.png",
                "Liverpool": "https://www.liverpoolfc.com/sites/default/files/logo-liverpool.png",
                "Chelsea": "https://www.chelseafc.com/sites/default/files/logo-chelsea.png",
                "Newcastle United": "https://www.nufc.co.uk/sites/default/files/logo-newcastle.png",
                "Tottenham": "https://www.tottenhamhotspur.com/sites/default/files/logo-tottenham.png",
                "Brighton": "https://www.brightonandhovealbion.com/sites/default/files/logo-brighton.png",
                "Aston Villa": "https://www.avfc.co.uk/sites/default/files/logo-aston-villa.png",
                "Brentford": "https://www.brentfordfc.com/sites/default/files/logo-brentford.png",
                "Fulham": "https://www.fulhamfc.com/sites/default/files/logo-fulham.png",
                "Crystal Palace": "https://www.cpfc.co.uk/sites/default/files/logo-crystal-palace.png",
                "Leicester City": "https://www.lcfc.com/sites/default/files/logo-leicester.png",
                "West Ham United": "https://www.whufc.com/sites/default/files/logo-west-ham.png",
                "Leeds United": "https://www.leedsunited.com/sites/default/files/logo-leeds.png",
                "Wolverhampton": "https://www.wolves.co.uk/sites/default/files/logo-wolves.png",
                "Everton": "https://www.evertonfc.com/sites/default/files/logo-everton.png",
                "Southampton": "https://www.southamptonfc.com/sites/default/files/logo-southampton.png",
                "Nottingham Forest": "https://www.nottinghamforest.co.uk/sites/default/files/logo-forest.png",
                "Bournemouth": "https://www.afcb.co.uk/sites/default/files/logo-bournemouth.png"
            },
            
            # Spain - La Liga (20 teams) - Alternative sources
            "Spain_LaLiga": {
                "Real Madrid": "https://www.realmadrid.com/sites/default/files/logo-real-madrid.png",
                "Barcelona": "https://www.fcbarcelona.com/sites/default/files/logo-barcelona.png",
                "Atletico Madrid": "https://www.atleticomadrid.com/sites/default/files/logo-atletico.png",
                "Real Sociedad": "https://www.realsociedad.eus/sites/default/files/logo-real-sociedad.png",
                "Villarreal": "https://www.villarrealcf.es/sites/default/files/logo-villarreal.png",
                "Real Betis": "https://www.realbetisbalompie.es/sites/default/files/logo-betis.png",
                "Athletic Bilbao": "https://www.athletic-club.eus/sites/default/files/logo-athletic.png",
                "Sevilla": "https://www.sevillafc.es/sites/default/files/logo-sevilla.png",
                "Valencia": "https://www.valenciacf.com/sites/default/files/logo-valencia.png",
                "Girona": "https://www.gironafc.cat/sites/default/files/logo-girona.png",
                "Rayo Vallecano": "https://www.rayovallecano.es/sites/default/files/logo-rayo.png",
                "Osasuna": "https://www.osasuna.es/sites/default/files/logo-osasuna.png",
                "Celta Vigo": "https://www.celtavigo.net/sites/default/files/logo-celta.png",
                "Mallorca": "https://www.rcdmallorca.es/sites/default/files/logo-mallorca.png",
                "Almeria": "https://www.udalmeriasad.com/sites/default/files/logo-almeria.png",
                "Getafe": "https://www.getafecf.com/sites/default/files/logo-getafe.png",
                "Las Palmas": "https://www.udlaspalmas.es/sites/default/files/logo-las-palmas.png",
                "Cadiz": "https://www.cadizcf.com/sites/default/files/logo-cadiz.png",
                "Granada": "https://www.granadacf.es/sites/default/files/logo-granada.png",
                "Alaves": "https://www.deportivoalaves.com/sites/default/files/logo-alaves.png"
            },
            
            # Italy - Serie A (20 teams) - Alternative sources
            "Italy_SerieA": {
                "AC Milan": "https://www.acmilan.com/sites/default/files/logo-milan.png",
                "Inter Milan": "https://www.inter.it/sites/default/files/logo-inter.png",
                "Juventus": "https://www.juventus.com/sites/default/files/logo-juventus.png",
                "Napoli": "https://www.sscnapoli.it/sites/default/files/logo-napoli.png",
                "AS Roma": "https://www.asroma.com/sites/default/files/logo-roma.png",
                "Lazio": "https://www.sslazio.it/sites/default/files/logo-lazio.png",
                "Atalanta": "https://www.atalanta.it/sites/default/files/logo-atalanta.png",
                "Fiorentina": "https://www.acffiorentina.com/sites/default/files/logo-fiorentina.png",
                "Bologna": "https://www.bolognafc.it/sites/default/files/logo-bologna.png",
                "Torino": "https://www.torinofc.it/sites/default/files/logo-torino.png",
                "Monza": "https://www.acmonza.com/sites/default/files/logo-monza.png",
                "Genoa": "https://www.genoacfc.it/sites/default/files/logo-genoa.png",
                "Lecce": "https://www.uslecce.it/sites/default/files/logo-lecce.png",
                "Sassuolo": "https://www.sassuolocalcio.it/sites/default/files/logo-sassuolo.png",
                "Frosinone": "https://www.frosinonecalcio.com/sites/default/files/logo-frosinone.png",
                "Udinese": "https://www.udinese.it/sites/default/files/logo-udinese.png",
                "Cagliari": "https://www.cagliaricalcio.com/sites/default/files/logo-cagliari.png",
                "Verona": "https://www.hellasverona.it/sites/default/files/logo-verona.png",
                "Empoli": "https://www.empolifc.com/sites/default/files/logo-empoli.png",
                "Salernitana": "https://www.ussalernitana1919.it/sites/default/files/logo-salernitana.png"
            },
            
            # Germany - Bundesliga (18 teams) - Alternative sources
            "Germany_Bundesliga": {
                "FC Bayern Munich": "https://fcbayern.com/sites/default/files/logo-bayern.png",
                "Borussia Dortmund": "https://www.bvb.de/sites/default/files/logo-dortmund.png",
                "RB Leipzig": "https://www.rbleipzig.com/sites/default/files/logo-leipzig.png",
                "Union Berlin": "https://www.fc-union-berlin.de/sites/default/files/logo-union.png",
                "Bayer Leverkusen": "https://www.bayer04.de/sites/default/files/logo-leverkusen.png",
                "Eintracht Frankfurt": "https://www.eintracht.de/sites/default/files/logo-frankfurt.png",
                "VfL Wolfsburg": "https://www.vfl-wolfsburg.de/sites/default/files/logo-wolfsburg.png",
                "SC Freiburg": "https://www.scfreiburg.com/sites/default/files/logo-freiburg.png",
                "Borussia Monchengladbach": "https://www.borussia.de/sites/default/files/logo-gladbach.png",
                "Werder Bremen": "https://www.werder.de/sites/default/files/logo-bremen.png",
                "Mainz 05": "https://www.mainz05.de/sites/default/files/logo-mainz.png",
                "FC Koln": "https://www.fc-koeln.de/sites/default/files/logo-koeln.png",
                "TSG Hoffenheim": "https://www.achtzehn99.de/sites/default/files/logo-hoffenheim.png",
                "VfL Bochum": "https://www.vfl-bochum.de/sites/default/files/logo-bochum.png",
                "FC Augsburg": "https://www.fcaugsburg.de/sites/default/files/logo-augsburg.png",
                "VfB Stuttgart": "https://www.vfb.de/sites/default/files/logo-stuttgart.png",
                "Hertha BSC": "https://www.herthabsc.de/sites/default/files/logo-hertha.png",
                "Schalke 04": "https://www.schalke04.de/sites/default/files/logo-schalke.png"
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
        print("🏆 League 1 Logo Scraper - Alternative Sources")
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
    scraper = League1LogoScraperAlternative()
    
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
            print("  python league1_scraper_alternative.py list                    - List all leagues")
            print("  python league1_scraper_alternative.py league <league_name>    - Download specific league")
            print("  python league1_scraper_alternative.py all                     - Download all leagues")
            print("\nExample:")
            print("  python league1_scraper_alternative.py league France_Ligue1")
    else:
        # Default: download all leagues
        scraper.download_all_leagues()

if __name__ == "__main__":
    main()
