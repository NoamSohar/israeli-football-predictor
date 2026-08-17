import pandas as pd

class GoalCalculator:
    def __init__(self, matches: pd.DataFrame, last_games: int=5):
        self.matches = matches
        self.last_games = last_games

    def get_team_goals(self, team_id: int, match_date: pd.Timestamp):
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

        goals_scored = 0
        goals_scored_against_team = 0

        for _, match in previous_matches.iterrows():
            is_home = match["home_team_id"] == team_id

            if is_home:
                goals_scored += match["home_goals"]
                goals_scored_against_team += match["away_goals"]
            else:
                goals_scored += match["away_goals"]
                goals_scored_against_team += match["home_goals"]

        return  goals_scored / self.last_games, goals_scored_against_team / self.last_games

    def add_features(self) -> pd.DataFrame:
        df = self.matches.copy()

        home_goals_scored = []
        home_goals_scored_against = []
        away_goals_scored = []
        away_goals_scored_against = []

        for _, match in df.iterrows():
            home_goals = self.get_team_goals(
                match["home_team_id"],
                match["date"]
            )

            away_goals = self.get_team_goals(
                match["away_team_id"],
                match["date"]
            )

            if home_goals is None:
                home_goals_scored.append(None)
                home_goals_scored_against.append(None)
            else:
                home_goals_scored.append(home_goals[0])
                home_goals_scored_against.append(home_goals[1])

            if away_goals is None:
                away_goals_scored.append(None)
                away_goals_scored_against.append(None)
            else:
                away_goals_scored.append(away_goals[0])
                away_goals_scored_against.append(away_goals[1])

        df[f"home_goals_scored_{self.last_games}"] = home_goals_scored
        df[f"home_goals_against_{self.last_games}"] = home_goals_scored_against

        df[f"away_goals_scored_{self.last_games}"] = away_goals_scored
        df[f"away_goals_against_{self.last_games}"] = away_goals_scored_against

        return df