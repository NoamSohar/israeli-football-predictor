import pandas as pd

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

    def get_home_form(self, team_id: int, match_date):
        previous_matches = self.matches[
            (self.matches["date"] < match_date)
            &
            (self.matches["home_team_id"] == team_id)
            ]

        if len(previous_matches) < self.last_games:
            return None

        previous_matches = previous_matches.tail(self.last_games)

        points = 0

        for _, match in previous_matches.iterrows():
            if match["home_goals"] > match["away_goals"]:
                points += 3

            elif match["home_goals"] == match["away_goals"]:
                points += 1

        return points / self.last_games

    def get_away_form(self, team_id: int, match_date):
        previous_matches = self.matches[
            (self.matches["date"] < match_date)
            &
            (self.matches["away_team_id"] == team_id)
            ]

        if len(previous_matches) < self.last_games:
            return None

        previous_matches = previous_matches.tail(self.last_games)

        points = 0

        for _, match in previous_matches.iterrows():
            if match["away_goals"] > match["home_goals"]:
                points += 3

            elif match["away_goals"] == match["home_goals"]:
                points += 1

        return points / self.last_games

    def add_features(self) -> pd.DataFrame:
        df = self.matches.copy()

        home_forms = []
        away_forms = []

        home_home_forms = []
        away_away_forms = []

        for _, match in df.iterrows():
            home_team_id = match["home_team_id"]
            away_team_id = match["away_team_id"]
            match_date = match["date"]

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
                self.get_home_form(
                    home_team_id,
                    match_date
                )
            )

            away_away_forms.append(
                self.get_away_form(
                    away_team_id,
                    match_date
                )
            )

        df[f"home_form_{self.last_games}"] = home_forms
        df[f"away_form_{self.last_games}"] = away_forms

        df[f"home_home_form_{self.last_games}"] = home_home_forms
        df[f"away_away_form_{self.last_games}"] = away_away_forms

        return df