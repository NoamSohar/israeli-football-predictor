REQUIRED_COLUMNS = {
    "fixture_id",
    "date",
    "round",
    "home_team_id",
    "home_team",
    "away_team_id",
    "away_team",
    "home_goals",
    "away_goals",
    "status"
}


def validate_columns(df):
    missing = []

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing.append(column)

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def validate_fixture_ids(df):
    if df["fixture_id"].duplicated().any():
        raise ValueError("Duplicate fixture IDs found")


def validate_teams(df):
    if (df["home_team_id"] == df["away_team_id"]).any():
        raise ValueError("Home team and away team cannot be the same")


def validate_finished_scores(df):
    finished = df[df["status"] == "FT"]

    if finished[["home_goals", "away_goals"]].isna().any().any():
        raise ValueError("Finished matches contain missing scores")