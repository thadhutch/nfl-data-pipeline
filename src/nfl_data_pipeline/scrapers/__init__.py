"""NFL data scrapers for PFF and Pro Football Reference."""

from nfl_data_pipeline.scrapers.pff import scrape_pff_data
from nfl_data_pipeline.scrapers.pfr_urls import collect_boxscore_urls
from nfl_data_pipeline.scrapers.pfr import scrape_all_game_info
