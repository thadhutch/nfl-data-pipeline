PYTHON = python

.PHONY: dirs scrape-pff pff-dates pff-names pff scrape-pfr-urls scrape-pfr-games pfr-dates pfr-names pfr merge over-under averages games-played rankings all clean

dirs:
	mkdir -p data/pff data/pfr data/over-under

# --- PFF Pipeline ---

scrape-pff: dirs
	$(PYTHON) pro_football_focus/historical/main.py

pff-dates: scrape-pff
	$(PYTHON) utils/pff/extract_dates.py

pff-names: pff-dates
	$(PYTHON) utils/pff/normalize_team_names.py

pff: pff-names

# --- PFR Pipeline ---

scrape-pfr-urls: dirs
	$(PYTHON) pro_football_reference/get_regular_season_urls.py

scrape-pfr-games: scrape-pfr-urls
	$(PYTHON) pro_football_reference/get_game_data.py

pfr-dates: scrape-pfr-games
	$(PYTHON) utils/pfr/normalize_date.py

pfr-names: pfr-dates
	$(PYTHON) utils/pfr/normalize_team_names.py

pfr: pfr-names

# --- Merge + Postprocessing ---

merge: pff pfr
	$(PYTHON) utils/merge_pff_and_pfr.py

over-under: merge
	$(PYTHON) postprocessing/over_under.py

averages: over-under
	$(PYTHON) postprocessing/prep_pff_data.py

games-played: averages
	$(PYTHON) postprocessing/games_played.py

rankings: games-played
	$(PYTHON) postprocessing/rank.py

all: rankings

clean:
	rm -rf data/pff/* data/pfr/* data/over-under/*
