#!/usr/bin/env python3
import os
import sys
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
import re
import json
from urllib.parse import urljoin

class FootballLogoScraper:
    def __init__(self, output_dir="football_logos", logo_size=(100, 100)):
        self.output_dir = output_dir
        self.logo_size = logo_size
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Progress tracking
        self.progress_file = "download_progress.json"
        self.load_progress()
        
        # Define leagues and their teams
        self.leagues = {
            'Germany_Bundesliga': [
                'FC Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Union Berlin',
                'SC Freiburg', 'Bayer Leverkusen', 'Eintracht Frankfurt', 'VfL Wolfsburg',
                'Borussia Mönchengladbach', 'FC Augsburg', 'VfB Stuttgart', 'Werder Bremen',
                'TSG Hoffenheim', 'VfL Bochum', 'FC Köln', 'Hertha BSC', 'Mainz 05', 'Schalke 04'
            ],
            'France_Ligue1': [
                'Paris Saint-Germain', 'Lens', 'Marseille', 'Rennes', 'Monaco',
                'Lille', 'Lyon', 'Nice', 'Clermont', 'Lorient', 'Reims', 'Montpellier',
                'Strasbourg', 'Brest', 'Nantes', 'Toulouse', 'Auxerre', 'Ajaccio',
                'Troyes', 'Angers'
            ],
            'Spain_LaLiga': [
                'Real Madrid', 'Barcelona', 'Atlético Madrid', 'Real Sociedad',
                'Villarreal', 'Real Betis', 'Osasuna', 'Athletic Bilbao', 'Mallorca',
                'Girona', 'Celta Vigo', 'Cádiz', 'Sevilla', 'Rayo Vallecano',
                'Valencia', 'Almería', 'Real Valladolid', 'Getafe', 'Espanyol', 'Elche'
            ],
            'Portugal_PrimeiraLiga': [
                'FC Porto', 'Benfica', 'Sporting CP', 'Braga', 'Vitória Guimarães',
                'Gil Vicente', 'Casa Pia', 'Boavista', 'Arouca', 'Estoril',
                'Famalicão', 'Rio Ave', 'Portimonense', 'Marítimo', 'Vizela',
                'Santa Clara', 'Chaves', 'Paços de Ferreira'
            ],
            'Brazil_SerieA': [
                'Flamengo', 'Palmeiras', 'Internacional', 'Fluminense', 'Atlético Mineiro',
                'São Paulo', 'Corinthians', 'Athletico Paranaense', 'Grêmio', 'Botafogo',
                'Santos', 'Fortaleza', 'Bragantino', 'Ceará', 'Atlético Goianiense',
                'Cuiabá', 'América Mineiro', 'Avaí', 'Juventude', 'Goiás'
            ],
            'Scotland_Premiership': [
                'Celtic', 'Rangers', 'Hearts', 'Aberdeen', 'Hibernian', 'Dundee United',
                'Motherwell', 'Ross County', 'St. Johnstone', 'Livingston',
                'St. Mirren', 'Kilmarnock'
            ],
            'Saudi_ProLeague': [
                'Al Hilal', 'Al Nassr', 'Al Ittihad', 'Al Ahli', 'Al Shabab',
                'Al Fateh', 'Al Tai', 'Al Raed', 'Al Ettifaq', 'Al Batin',
                'Al Fayha', 'Al Hazem', 'Damac', 'Abha', 'Al Wehda', 'Al Riyadh'
            ],
            'Turkey_SuperLig': [
                'Galatasaray', 'Fenerbahçe', 'Beşiktaş', 'Başakşehir', 'Trabzonspor',
                'Adana Demirspor', 'Konyaspor', 'Sivasspor', 'Alanyaspor', 'Kasımpaşa',
                'Gaziantep FK', 'Antalyaspor', 'Fatih Karagümrük', 'Kayserispor',
                'Hatayspor', 'Giresunspor', 'İstanbulspor', 'Ümraniyespor'
            ],
            'Italy_SerieA': [
                'Napoli', 'AC Milan', 'Inter Milan', 'Juventus', 'Lazio', 'AS Roma',
                'Atalanta', 'Fiorentina', 'Torino', 'Udinese', 'Sassuolo', 'Bologna',
                'Empoli', 'Monza', 'Lecce', 'Hellas Verona', 'Spezia', 'Salernitana',
                'Sampdoria', 'Cremonese'
            ],
            'England_PremierLeague': [
                'Manchester City', 'Arsenal', 'Manchester United', 'Newcastle United',
                'Liverpool', 'Brighton', 'Aston Villa', 'Tottenham', 'Brentford',
                'Fulham', 'Crystal Palace', 'Chelsea', 'Wolves', 'West Ham',
                'Leeds United', 'Everton', 'Nottingham Forest', 'Leicester City',
                'Bournemouth', 'Southampton'
            ],
            'Switzerland_SuperLeague': [
                'Young Boys', 'FC Zürich', 'Basel', 'Servette', 'St. Gallen',
                'Lugano', 'Luzern', 'Grasshoppers', 'Sion', 'Winterthur'
            ],
            'Greece_SuperLeague': [
                'Olympiacos', 'PAOK', 'AEK Athens', 'Panathinaikos', 'Aris',
                'Volos', 'Atromitos', 'OFI Crete', 'Ionikos', 'Lamia',
                'Levadiakos', 'PAS Giannina', 'Apollon Smyrnis', 'Asteras Tripolis'
            ],
            'USA_MLS': [
                'LAFC', 'Philadelphia Union', 'LA Galaxy', 'Austin FC', 'FC Cincinnati',
                'New York Red Bulls', 'New York City FC', 'Nashville SC', 'Orlando City',
                'Atlanta United', 'CF Montréal', 'Columbus Crew', 'Inter Miami',
                'Toronto FC', 'Chicago Fire', 'New England Revolution', 'FC Dallas',
                'Houston Dynamo', 'Minnesota United', 'Portland Timbers', 'Seattle Sounders',
                'Real Salt Lake', 'Colorado Rapids', 'Sporting Kansas City', 'Vancouver Whitecaps',
                'San Jose Earthquakes'
            ]
        }
    
    def load_progress(self):
        """Load download progress from file"""
        try:
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        except:
            self.progress = {}
    
    def save_progress(self):
        """Save download progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f)
    
    def clean_filename(self, filename):
        """Clean filename to be filesystem-safe"""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove multiple spaces and replace with single underscore
        filename = re.sub(r'\s+', '_', filename)
        return filename.strip('_')
    
    def download_image(self, url, save_path):
        """Download and resize image"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Open image
            image = Image.open(BytesIO(response.content))
            
            # Convert to RGBA if it's not already
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Resize image
            image = image.resize(self.logo_size, Image.Resampling.LANCZOS)
            
            # Save as PNG to preserve transparency
            image.save(save_path, 'PNG')
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
    
    def search_wikipedia_logo(self, team_name, country=None):
        """Search for team logo on Wikipedia"""
        try:
            # Try different search variations
            search_terms = [
                team_name,
                f"{team_name} FC",
                f"{team_name} football club",
                f"{team_name} soccer"
            ]
            
            for search_term in search_terms:
                # Wikipedia search URL
                search_url = f"https://en.wikipedia.org/w/api.php"
                params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': search_term,
                    'srlimit': 3
                }
                
                response = self.session.get(search_url, params=params, timeout=10)
                data = response.json()
                
                if 'query' in data and 'search' in data['query']:
                    for result in data['query']['search']:
                        page_title = result['title']
                        logo_url = self.get_wikipedia_page_logo(page_title)
                        if logo_url:
                            return logo_url
            
            return None
        except Exception as e:
            print(f"Error searching Wikipedia for {team_name}: {e}")
            return None
    
    def get_wikipedia_page_logo(self, page_title):
        """Get logo from Wikipedia page"""
        try:
            # Get page content
            api_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': page_title,
                'prop': 'pageimages',
                'pithumbsize': 300
            }
            
            response = self.session.get(api_url, params=params, timeout=10)
            data = response.json()
            
            if 'query' in data and 'pages' in data['query']:
                for page_id, page_info in data['query']['pages'].items():
                    if 'thumbnail' in page_info:
                        return page_info['thumbnail']['source']
            
            # Alternative: parse page content for infobox image
            page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
            response = self.session.get(page_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for infobox image
            infobox = soup.find('table', {'class': ['infobox', 'vcard']})
            if infobox:
                img = infobox.find('img')
                if img and img.get('src'):
                    img_url = img['src']
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    return img_url
            
            return None
        except Exception as e:
            print(f"Error getting logo from Wikipedia page {page_title}: {e}")
            return None
    
    def search_transfermarkt_logo(self, team_name):
        """Search for team logo on Transfermarkt"""
        try:
            # Search on Transfermarkt
            search_url = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche"
            params = {'query': team_name}
            
            response = self.session.get(search_url, params=params, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for team results
            results = soup.find_all('td', {'class': 'hauptlink'})
            for result in results:
                link = result.find('a')
                if link and '/verein/' in link.get('href', ''):
                    team_url = 'https://www.transfermarkt.com' + link['href']
                    logo_url = self.get_transfermarkt_team_logo(team_url)
                    if logo_url:
                        return logo_url
            
            return None
        except Exception as e:
            print(f"Error searching Transfermarkt for {team_name}: {e}")
            return None
    
    def get_transfermarkt_team_logo(self, team_url):
        """Get logo from Transfermarkt team page"""
        try:
            response = self.session.get(team_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for team logo
            logo_img = soup.find('img', {'class': ['dataBild', 'vereinslogo']})
            if logo_img and logo_img.get('src'):
                logo_url = logo_img['src']
                if logo_url.startswith('//'):
                    logo_url = 'https:' + logo_url
                elif logo_url.startswith('/'):
                    logo_url = 'https://www.transfermarkt.com' + logo_url
                return logo_url
            
            return None
        except Exception as e:
            print(f"Error getting logo from Transfermarkt page {team_url}: {e}")
            return None
    
    def download_team_logo(self, team_name, league):
        """Download logo for a specific team"""
        team_key = f"{league}_{team_name}"
        
        # Check if already downloaded successfully
        if team_key in self.progress and self.progress[team_key]:
            print(f"✓ {team_name} already downloaded")
            return True
        
        print(f"Downloading {team_name}...")
        
        # Create league directory
        league_dir = os.path.join(self.output_dir, league)
        os.makedirs(league_dir, exist_ok=True)
        
        # Clean team name for filename
        clean_name = self.clean_filename(team_name)
        save_path = os.path.join(league_dir, f"{clean_name}.png")
        
        # Try multiple sources
        logo_url = self.search_wikipedia_logo(team_name)
        if not logo_url:
            logo_url = self.search_transfermarkt_logo(team_name)
        
        if logo_url:
            success = self.download_image(logo_url, save_path)
            self.progress[team_key] = success
            self.save_progress()
            
            if success:
                print(f"✓ {team_name}")
                return True
            else:
                print(f"✗ Failed {team_name}")
                return False
        else:
            print(f"✗ No logo {team_name}")
            self.progress[team_key] = False
            self.save_progress()
            return False
    
    def download_all_logos(self):
        """Download logos for all teams"""
        total_teams = sum(len(teams) for teams in self.leagues.values())
        successful_downloads = 0
        current_team = 0
        
        print(f"🏈 Downloading {total_teams} team logos to {self.output_dir}")
        print(f"Size: {self.logo_size[0]}x{self.logo_size[1]} pixels")
        
        for league, teams in self.leagues.items():
            print(f"\n📁 {league} ({len(teams)} teams)")
            
            for team in teams:
                current_team += 1
                print(f"[{current_team}/{total_teams}] ", end="")
                
                success = self.download_team_logo(team, league)
                if success:
                    successful_downloads += 1
                
                time.sleep(0.3)  # Rate limiting
        
        # Summary
        success_rate = (successful_downloads/total_teams)*100
        print(f"\n📊 Results: {successful_downloads}/{total_teams} ({success_rate:.1f}%)")
        
        # Count actual files
        total_files = 0
        for league in self.leagues.keys():
            league_dir = os.path.join(self.output_dir, league)
            if os.path.exists(league_dir):
                files = [f for f in os.listdir(league_dir) if f.endswith('.png')]
                total_files += len(files)
                print(f"  {league}: {len(files)} files")
        
        return successful_downloads, total_teams

def main():
    """Main function - runs automatically without user input"""
    scraper = FootballLogoScraper()
    
    # Show team count
    total_teams = sum(len(teams) for teams in scraper.leagues.values())
    print(f"📋 {total_teams} teams from 13 countries")
    
    # Run downloads
    max_retries = 3
    for attempt in range(max_retries):
        print(f"\n🔄 Attempt {attempt + 1}/{max_retries}")
        successful, total = scraper.download_all_logos()
        
        if successful == total:
            print("✅ All logos downloaded successfully!")
            break
        elif attempt < max_retries - 1:
            failed = total - successful
            print(f"🔄 Retrying {failed} failed downloads...")
            time.sleep(2)
        else:
            print(f"⚠️ Completed with {successful}/{total} downloads")

if __name__ == "__main__":
    main()
