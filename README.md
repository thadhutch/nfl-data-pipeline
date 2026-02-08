# scrape-nfl-data

A data pipeline that scrapes NFL team grades from [PFF](https://www.pff.com/) (Pro Football Focus) and game/betting data from [Pro Football Reference](https://www.pro-football-reference.com/), merges the datasets, and runs postprocessing (rolling averages, rankings) to produce a dataset for over/under analysis.

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management
- Google Chrome + [ChromeDriver](https://chromedriver.chromium.org/)
- A [PFF Premium](https://www.pff.com/) subscription (for PFF scraping)
- Rotating proxies in CSV format (for PFR scraping)

## Setup

```bash
# Install dependencies
poetry install

# Copy and fill in credentials
cp .env.example .env

# Add your proxies
mkdir -p proxies
# Place your proxies.csv in proxies/ (format: address:port:user:password per line)

# Create data directories
make dirs
```

## Configuration

All paths and settings are centralized in `config.py`. Override defaults with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `NFL_SEASONS` | `2024` | Comma-separated list of seasons for PFF scraping |
| `NFL_START_YEAR` | `2024` | Start year for PFR URL scraping |
| `NFL_END_YEAR` | `2024` | End year for PFR URL scraping |
| `NFL_MAX_WEEK` | `18` | Last week to scrape in the final year |
| `PFF_EMAIL` | - | PFF account email |
| `PFF_PASSWORD` | - | PFF account password |

## Pipeline

```
PFF Scrape          PFR Scrape
    |                   |
    v                   v
Extract Dates      Normalize Dates
    |                   |
    v                   v
Normalize Names    Normalize Names
    |                   |
    +-------+   +-------+
            |   |
            v   v
           Merge
             |
             v
        Over/Under
             |
             v
      Rolling Averages
             |
             v
       Games Played
             |
             v
         Rankings
```

## Make Commands

```bash
make all            # Run the full pipeline end-to-end
make pff            # Run only the PFF scraping + processing chain
make pfr            # Run only the PFR scraping + processing chain
make merge          # Merge PFF and PFR data (runs both chains first)
make rankings       # Run full postprocessing through rankings
make clean          # Remove all generated data files
make dirs           # Create data directory structure
```

Individual steps can also be run directly:

```bash
python pro_football_focus/historical/main.py
python pro_football_reference/get_regular_season_urls.py
python pro_football_reference/get_game_data.py
python utils/pff/extract_dates.py
# etc.
```

## Project Structure

```
scrape-nfl-data/
├── config.py                          # Centralized paths and settings
├── Makefile                           # Pipeline orchestration
├── pyproject.toml                     # Dependencies (Poetry)
├── .env.example                       # Credential template
├── pro_football_focus/                # PFF scraping
│   ├── teams.py                       # Team name mappings
│   └── historical/
│       ├── main.py                    # Entry point
│       └── scrape.py                  # Selenium scraper
├── pro_football_reference/            # PFR scraping
│   ├── get_regular_season_urls.py     # Collect boxscore URLs
│   └── get_game_data.py              # Scrape individual games
├── utils/
│   ├── authenticate.py                # PFF login helpers
│   ├── merge_pff_and_pfr.py          # Merge datasets
│   ├── pff/
│   │   ├── extract_dates.py          # Parse dates from game strings
│   │   └── normalize_team_names.py   # Map abbreviations to full names
│   └── pfr/
│       ├── normalize_date.py         # Format PFR dates
│       └── normalize_team_names.py   # Extract team names from titles
├── postprocessing/
│   ├── over_under.py                 # Extract O/U betting columns
│   ├── prep_pff_data.py              # Rolling averages
│   ├── games_played.py               # Cumulative games played
│   └── rank.py                       # Feature rankings
└── data/                             # Generated outputs (gitignored)
    ├── pff/
    ├── pfr/
    └── over-under/
```

## Notes

- **PFF scraping is fragile.** It relies on XPath selectors tied to PFF's DOM structure. If PFF changes their frontend, the selectors in `scrape.py` will need updating.
- **PFR scraping requires proxies.** Pro Football Reference rate-limits aggressively. Without rotating proxies, requests will be blocked.
- **The PFF scraper uses a real browser.** It opens Chrome via Selenium, logs in with your credentials, and navigates page by page. This is slow but necessary since PFF renders data client-side.
- **Data files are not tracked in git.** Run the pipeline to generate them, or bring your own data in the expected format.
