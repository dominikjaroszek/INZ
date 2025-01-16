from app.models.league import League
from app.models.season import Season
from app.models.team import Team
from app.models.standing import Standing

def get_all_league_names():
    leagues = League.query.all()
    return [{"league_id": league.league_id, "name": league.league_name, "logo": league.logo} for league in leagues]

def get_league(league_name, season):
    season_start_year = season.split("-")[0]
    league = League.query.filter_by(league_name=league_name).first()
    season = Season.query.filter_by(league_id=league.league_id, start_year=season_start_year).first()

    if league and season:
        return {
            "league_id": league.league_id,
            "name": league.league_name,
            "country": league.country,
            "logo": league.logo,
            "season_start_year": season.start_year,
            "season_end_year": season.end_year
        }
    
def get_all_seasons(league_name):
    league = League.query.filter_by(league_name=league_name).first()
    if not league:
        return {'error': 'League not found'}

    seasons = Season.query.filter_by(league_id=league.league_id).all()
    season_data = []

    for season in seasons:
        season_info = {
            "season_id": season.season_id,
            "start_year": season.start_year,
            "end_year": season.end_year
        }
        if not season.is_current:
            winner = Standing.query.filter_by(season_id=season.season_id, position=1).first()
            if winner:
                team = Team.query.get(winner.team_id)
                season_info["winner"] = team.team_name
            else:
                season_info["winner"] = "Unknown"
        else:
            season_info["winner"] = "Season ongoing"

        season_data.append(season_info)

    return season_data