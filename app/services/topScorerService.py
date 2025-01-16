from app.models.top_scorer import TopScorer
from app.models.league import League
from app.models.season import Season
from app.config import db

def get_top_scorers(league_name, season):
    season_start_year = season.split('-')[0]

    league = db.session.query(League).filter_by(league_name=league_name).first()
    season = db.session.query(Season).filter_by(league_id=league.league_id, start_year=season_start_year).first()

    if not league or not season:
        return {'error': 'League or season not found'}

    top_scorers = db.session.query(TopScorer).filter_by(season_id=season.season_id).order_by(TopScorer.goals.desc()).all()
    top_scorers_data = []

    for top_scorer in top_scorers:
        top_scorers_data.append({
            "player_name": top_scorer.player_name,
            "team_name": top_scorer.Team.team_name,
            "goals": top_scorer.goals,
            "assists": top_scorer.assists
        })

    top_scorers_data.sort(key=lambda x: (x['goals'], x['assists']), reverse=True)

    for index, player in enumerate(top_scorers_data, start=1):
        player['position'] = index

    return top_scorers_data

def get_top_scorers_canadian(league_name, season):
    season_start_year = season.split('-')[0]

    league = db.session.query(League).filter_by(league_name=league_name).first()
    season = db.session.query(Season).filter_by(league_id=league.league_id, start_year=season_start_year).first()

    if not league or not season:
        return {'error': 'League or season not found'}

    top_scorers = db.session.query(TopScorer).filter_by(season_id=season.season_id).order_by(TopScorer.goals.desc()).all()
    top_scorers_data = []

    for top_scorer in top_scorers:
        top_scorers_data.append({
            "player_name": top_scorer.player_name,
            "team_name": top_scorer.Team.team_name,
            "goals": top_scorer.goals,
            "assists": top_scorer.assists,
            "points": top_scorer.goals + top_scorer.assists
        })

    top_scorers_data.sort(key=lambda x: (x['points'], x['goals']), reverse=True)

    for index, player in enumerate(top_scorers_data, start=1):
        player['position'] = index

    return top_scorers_data