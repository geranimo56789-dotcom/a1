# 🏆 League 1 Logo Scraper

A comprehensive Python tool to download team logos from all major European football leagues, with a focus on **France Ligue 1**.

## 📋 Features

- **98+ Team Logos** from 5 major European leagues
- **Automatic Image Resizing** to 100x100 pixels
- **Multi-threaded Downloads** for fast performance
- **Progress Tracking** with resume capability
- **Organized Output** by league/country
- **High-Quality Sources** from Wikipedia/Wikimedia Commons

## 🏅 Supported Leagues

| League | Country | Teams |
|--------|---------|-------|
| **France_Ligue1** | 🇫🇷 France | 20 teams |
| **England_Premier** | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 England | 20 teams |
| **Spain_LaLiga** | 🇪🇸 Spain | 20 teams |
| **Italy_SerieA** | 🇮🇹 Italy | 20 teams |
| **Germany_Bundesliga** | 🇩🇪 Germany | 18 teams |

## 🚀 Quick Start

### Method 1: Using the Batch File (Recommended)
```bash
# Download all leagues
run_scraper.bat

# List available leagues
run_scraper.bat list

# Download specific league (e.g., France Ligue 1)
run_scraper.bat league France_Ligue1
```

### Method 2: Direct Python Command
```bash
# Download all leagues
.\python.bat league1_logo_scraper.py

# List available leagues
.\python.bat league1_logo_scraper.py list

# Download specific league
.\python.bat league1_logo_scraper.py league France_Ligue1

# Download all leagues explicitly
.\python.bat league1_logo_scraper.py all
```

## 📁 Output Structure

```
league1_logos/
├── France_Ligue1/
│   ├── Paris_Saint-Germain.png
│   ├── Lens.png
│   ├── Marseille.png
│   └── ...
├── England_Premier/
│   ├── Manchester_City.png
│   ├── Arsenal.png
│   └── ...
├── Spain_LaLiga/
├── Italy_SerieA/
└── Germany_Bundesliga/
```

## 🎯 France Ligue 1 Teams

The scraper includes all 20 current Ligue 1 teams:

1. **Paris Saint-Germain** - PSG
2. **Lens** - RC Lens
3. **Marseille** - Olympique de Marseille
4. **Rennes** - Stade Rennais FC
5. **Monaco** - AS Monaco FC
6. **Lille** - LOSC Lille
7. **Lyon** - Olympique Lyonnais
8. **Nice** - OGC Nice
9. **Reims** - Stade de Reims
10. **Montpellier** - Montpellier HSC
11. **Strasbourg** - RC Strasbourg Alsace
12. **Nantes** - FC Nantes
13. **Clermont** - Clermont Foot 63
14. **Lorient** - FC Lorient
15. **Brest** - Stade Brestois 29
16. **Toulouse** - Toulouse FC
17. **Auxerre** - AJ Auxerre
18. **Ajaccio** - AC Ajaccio
19. **Troyes** - ES Troyes AC
20. **Angers** - Angers SCO

## ⚙️ Requirements

- Python 3.7+
- Required packages (automatically installed):
  - `requests` - HTTP requests
  - `Pillow` - Image processing

## 🔧 Installation

1. **Python Setup**: The script uses `python.bat` to run Python in Cursor AI
2. **Dependencies**: Run once to install required packages:
   ```bash
   .\python.bat -m pip install requests pillow
   ```

## 📊 Progress Tracking

The scraper automatically tracks download progress in `download_progress.json`:
- Resumes interrupted downloads
- Skips already downloaded logos
- Maintains download history

## 🎨 Image Quality

- **Source**: High-quality SVG logos from Wikipedia/Wikimedia Commons
- **Output**: 100x100 pixel PNG files with transparency support
- **Optimization**: Compressed for web use while maintaining quality

## 🚨 Troubleshooting

### Common Issues:

1. **Python not found**: Use `.\python.bat` instead of `python`
2. **Missing packages**: Run `.\python.bat -m pip install requests pillow`
3. **Download errors**: Check internet connection and try again
4. **Permission errors**: Ensure write access to the output directory

### Error Messages:
- `✗ Failed to download [team]: [error]` - Network or file access issue
- `✓ Already downloaded: [team]` - Logo already exists, skipping

## 📈 Performance

- **Multi-threaded**: Downloads 10 logos simultaneously
- **Resume capability**: Continues from where it left off
- **Progress tracking**: Shows real-time download status
- **Memory efficient**: Processes images in chunks

## 🔄 Updates

The scraper can be easily updated with new teams or leagues by modifying the `team_logos` dictionary in the script.

## 📝 License

This tool is for educational and personal use. Please respect the original sources of the logos and their respective copyright holders.

## 🤝 Contributing

Feel free to:
- Add more leagues or teams
- Improve error handling
- Enhance the user interface
- Report bugs or issues

---

**Enjoy downloading your favorite team logos! ⚽🏆**
