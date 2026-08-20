import pandas as pd
from src import utils

class FormCalculator:
    def __init__(self, matches: pd.DataFrame, last_games: int = 5):
        self.matches = matches
        self.last_games = last_games

    def get_team_form(self, team_id: int, match_date):
        previous_matches = self.matches[
            (self.matches["date"] < match_date)
            &
            (
                (self.matches["home_team_id"] == team_id)
                |
                (self.matches["away_team_id"] == team_id)
            )
        ]

        if len(previous_matches) < self.last_games:
            return None

        previous_matches = previous_matches.tail(self.last_games)

        points = 0
        home_points = 0
        for _, match in previous_matches.iterrows():
            is_home = match["home_team_id"] == team_id

            if match["home_goals"] == match["away_goals"]:
                points += 1

            elif is_home and match["home_goals"] > match["away_goals"]:
                points += 3

            elif not is_home and match["away_goals"] > match["home_goals"]:
                points += 3

        return points / self.last_games

    def get_location_specific_form(self, team_id: int, match_date, location: str):
        if location not in ("home", "away"):
            raise ValueError("location must be 'home' or 'away'")

        previous_matches = self.matches[
            (self.matches["date"] < match_date)
            &
            (self.matches[f"{location}_team_id"] == team_id)
            ]

        if len(previous_matches) < self.last_games:
            return None

        previous_matches = previous_matches.tail(self.last_games)

        points = 0

        counter_location = "home" if location == "away" else "away"
        for _, match in previous_matches.iterrows():
            if match[f"{location}_goals"] > match[f"{counter_location}_goals"]:
                points += 3

            elif match[f"{location}_goals"] == match[f"{counter_location}_goals"]:
                points += 1

        return points / self.last_games

    def get_seasonal_ppg(self, team_id: int, match_date: pd.Timestamp):
        previous_matches = self.matches[
            (self.matches["date"] < match_date)
            &
            (self.matches["date"] >= utils.get_start_of_season(match_date, self.matches))
            &
            (
                (self.matches["home_team_id"] == team_id)
                |
                (self.matches["away_team_id"] == team_id)
            )
        ]

        if previous_matches.empty:
            return None

        points = 0
        for _, match in previous_matches.iterrows():
            is_home = match["home_team_id"] == team_id

            if match["home_goals"] == match["away_goals"]:
                points += 1

            elif is_home and match["home_goals"] > match["away_goals"]:
                points += 3

            elif not is_home and match["away_goals"] > match["home_goals"]:
                points += 3

        return round((points / len(previous_matches)), 2)

    def add_features(self) -> pd.DataFrame:
        df = self.matches.copy()

        home_forms = []
        away_forms = []

        home_home_forms = []
        away_away_forms = []

        season_form_home = []
        season_form_away = []

        for _, match in df.iterrows():
            home_team_id = match["home_team_id"]
            away_team_id = match["away_team_id"]
            match_date = match["date"]

            season_form_home.append(
                self.get_seasonal_ppg(
                    home_team_id,
                    match_date
                )
            )

            season_form_away.append(
                self.get_seasonal_ppg(
                    away_team_id,
                    match_date
                )
            )

            home_forms.append(
                self.get_team_form(
                    home_team_id,
                    match_date
                )
            )

            away_forms.append(
                self.get_team_form(
                    away_team_id,
                    match_date
                )
            )

            home_home_forms.append(
                self.get_location_specific_form(
                    home_team_id,
                    match_date,
                    "home"
                )
            )

            away_away_forms.append(
                self.get_location_specific_form(
                    away_team_id,
                    match_date,
                    "away"
                )
            )

        df[f"home_form_{self.last_games}"] = home_forms
        df[f"away_form_{self.last_games}"] = away_forms

        df[f"home_home_form_{self.last_games}"] = home_home_forms
        df[f"away_away_form_{self.last_games}"] = away_away_forms

        df["home_season_form"] = season_form_home
        df["away_season_form"] = season_form_away

        return df