from datetime import datetime, timedelta
import pytest
from app.models.user import User
from app import create_app
from app.config import db
from app.services.tokenService  import generate_access_token
from app.models.role import Role
from app.models.team import Team
from app.models.season import Season
from app.models.match import Match
from app.models.league import League

@pytest.fixture()
def app():
    flask_app = create_app("sqlite://")

    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture(scope='function')
def setup_database_user(app):
    with app.app_context():
        # Tworzenie ról
        role_admin = Role(name="admin")
        role_user = Role(name="user")
        db.session.add(role_admin)
        db.session.add(role_user)
        db.session.commit()

        # Tworzenie użytkowników
        user1 = User(
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            password="Password1!",
            role_id=role_user.role_id  # Przypisanie roli jeden-do-jednego
        )
        user2 = User(
            firstName="John2",
            lastName="Doe2",
            email="john.doe2@example.com",
            password="Password2!",
            role_id=role_user.role_id  # Przypisanie tej samej roli
        )

        db.session.add_all([user1, user2])
        db.session.commit()

@pytest.fixture(scope='function')
def setup_database_match(app):
    with app.app_context():
        # Przykładowe ligi
        league1 = League(league_id=1, league_name="Premier League", logo="premier_league_logo.png", country="England")
        league2 = League(league_id=2, league_name="La Liga", logo="la_liga_logo.png", country="Spain")
        
        db.session.add_all([league1, league2])
        db.session.commit()

        # Przykładowe sezony
        season1 = Season(
            season_id=1,
            league_id=1,
            start_year=2024,
            end_year=2025,
            is_current=True
        )
        season2 = Season(
            season_id=2,
            league_id=2,
            start_year=2024,
            end_year=2025,
            is_current=True
        )

        db.session.add_all([season1, season2])
        db.session.commit()

        # Przykładowe drużyny
        team1 = Team(
            team_id=1,
            team_name="Team A",
            league_id=1,
            logo="team_a_logo.png",
            venue_name="Stadium A",
            city="City A",
            capacity=40000,
            founded=1901
        )
        team2 = Team(
            team_id=2,
            team_name="Team B",
            league_id=1,
            logo="team_b_logo.png",
            venue_name="Stadium B",
            city="City B",
            capacity=50000,
            founded=1923
        )
        team3 = Team(
            team_id=3,
            team_name="Team C",
            league_id=1,
            logo="team_c_logo.png",
            venue_name="Stadium C",
            city="City C",
            capacity=45000,
            founded=1910
        )
        team4 = Team(
            team_id=4,
            team_name="Team D",
            league_id=1,
            logo="team_d_logo.png",
            venue_name="Stadium D",
            city="City D",
            capacity=55000,
            founded=1930
        )
        team5 = Team(
            team_id=5,
            team_name="Team E",
            league_id=2,
            logo="team_e_logo.png",
            venue_name="Stadium E",
            city="City E",
            capacity=35000,
            founded=1899
        )
        team6 = Team(
            team_id=6,
            team_name="Team F",
            league_id=2,
            logo="team_f_logo.png",
            venue_name="Stadium F",
            city="City F",
            capacity=60000,
            founded=1945
        )
            
        db.session.add_all([team1, team2, team3, team4, team5, team6])
        db.session.commit()


        base_date = datetime(2024, 7, 1, 15, 0, 0)
        # Przykładowe mecze z pełnymi statystykami
        matches = []

        for i in range(5):  # 6 meczów dla Team A jako gospodarza
            match_date = base_date + timedelta(days=i)  # Zmiana daty o 1 dzień za każdym razem
            match = Match(
                match_id=i+1,
                season_id=1,
                home_team_id=1,
                away_team_id=2,
                home_score=2,
                away_score=1,
                referee="Referee A",
                match_date=match_date,
                venue_name="Stadium A",
                round=f"Round {i+1}",
                status_short="FT",
                status_long="Finished",
                type="Finished",
                home_team_shots_on_goal=10,
                home_team_shots_off_goal=5,
                home_team_total_shots=15,
                home_team_blocked_shots=2,
                home_team_shots_insidebox=8,
                home_team_shots_outsidebox=7,
                home_team_fouls=10,
                home_team_corner_kicks=6,
                home_team_offsides=2,
                home_team_ball_possession=55.5,
                home_team_yellow_cards=1,
                home_team_red_cards=0,
                home_team_goalkeeper_saves=4,
                home_team_total_passes=500,
                home_team_passes_accuracy=85.0,
                home_team_passes_percent=85,
                away_team_shots_on_goal=7,
                away_team_shots_off_goal=3,
                away_team_total_shots=10,
                away_team_blocked_shots=3,
                away_team_shots_insidebox=5,
                away_team_shots_outsidebox=5,
                away_team_fouls=12,
                away_team_corner_kicks=4,
                away_team_offsides=1,
                away_team_ball_possession=44.5,
                away_team_yellow_cards=2,
                away_team_red_cards=0,
                away_team_goalkeeper_saves=6,
                away_team_total_passes=400,
                away_team_passes_accuracy=80.0,
                away_team_passes_percent=80,
   
            )
            matches.append(match)


        for i in range(6, 10):  # 6 meczów dla Team A jako gospodarza
            match_date = base_date + timedelta(days=i)  # Zmiana daty o 1 dzień za każdym razem
            match = Match(
                match_id=i+1,
                season_id=1,
                home_team_id=2,
                away_team_id=3,
                home_score=2,
                away_score=1,
                referee="Referee A",
                match_date=match_date,
                venue_name="Stadium A",
                round=f"Round {i+1}",
                status_short="FT",
                status_long="Finished",
                type="Finished",
                home_team_shots_on_goal=10,
                home_team_shots_off_goal=5,
                home_team_total_shots=15,
                home_team_blocked_shots=2,
                home_team_shots_insidebox=8,
                home_team_shots_outsidebox=7,
                home_team_fouls=10,
                home_team_corner_kicks=6,
                home_team_offsides=2,
                home_team_ball_possession=55.5,
                home_team_yellow_cards=1,
                home_team_red_cards=0,
                home_team_goalkeeper_saves=4,
                home_team_total_passes=500,
                home_team_passes_accuracy=85.0,
                home_team_passes_percent=85,
                away_team_shots_on_goal=7,
                away_team_shots_off_goal=3,
                away_team_total_shots=10,
                away_team_blocked_shots=3,
                away_team_shots_insidebox=5,
                away_team_shots_outsidebox=5,
                away_team_fouls=12,
                away_team_corner_kicks=4,
                away_team_offsides=1,
                away_team_ball_possession=44.5,
                away_team_yellow_cards=2,
                away_team_red_cards=0,
                away_team_goalkeeper_saves=6,
                away_team_total_passes=400,
                away_team_passes_accuracy=80.0,
                away_team_passes_percent=80,

            )
            matches.append(match)

        for i in range(11, 15):   # 6 meczów dla Team A jako gospodarza
            match_date = base_date + timedelta(days=i)  # Zmiana daty o 1 dzień za każdym razem
            match = Match(
                match_id=i+1,
                season_id=1,
                home_team_id=1,
                away_team_id=4,
                home_score=2,
                away_score=1,
                referee="Referee A",
                match_date=match_date,
                venue_name="Stadium A",
                round=f"Round {i+1}",
                status_short="FT",
                status_long="Finished",
                type="Finished",
                home_team_shots_on_goal=10,
                home_team_shots_off_goal=5,
                home_team_total_shots=15,
                home_team_blocked_shots=2,
                home_team_shots_insidebox=8,
                home_team_shots_outsidebox=7,
                home_team_fouls=10,
                home_team_corner_kicks=6,
                home_team_offsides=2,
                home_team_ball_possession=55.5,
                home_team_yellow_cards=1,
                home_team_red_cards=0,
                home_team_goalkeeper_saves=4,
                home_team_total_passes=500,
                home_team_passes_accuracy=85.0,
                home_team_passes_percent=85,
                away_team_shots_on_goal=7,
                away_team_shots_off_goal=3,
                away_team_total_shots=10,
                away_team_blocked_shots=3,
                away_team_shots_insidebox=5,
                away_team_shots_outsidebox=5,
                away_team_fouls=12,
                away_team_corner_kicks=4,
                away_team_offsides=1,
                away_team_ball_possession=44.5,
                away_team_yellow_cards=2,
                away_team_red_cards=0,
                away_team_goalkeeper_saves=6,
                away_team_total_passes=400,
                away_team_passes_accuracy=80.0,
                away_team_passes_percent=80,

            )
            matches.append(match)

        
        match_date = datetime(2025, 7, 1, 15, 0, 0) # Zmiana daty o 1 dzień za każdym razem
        match = Match(
            match_id=16,
            season_id=1,
            home_team_id=1,
            away_team_id=2,
            referee="Referee A",
            match_date=match_date,
            venue_name="Stadium A",
            round="Round 20",
            status_short="NS",
            status_long="Scheduled",
            type="Scheduled",
            home_team_shots_on_goal=10,
            home_team_shots_off_goal=5,
            home_team_total_shots=15,
            home_team_blocked_shots=2,
            home_team_shots_insidebox=8,
            home_team_shots_outsidebox=7,
            home_team_fouls=10,
            home_team_corner_kicks=6,
            home_team_offsides=2,
            home_team_ball_possession=55.5,
            home_team_yellow_cards=1,
            home_team_red_cards=0,
            home_team_goalkeeper_saves=4,
            home_team_total_passes=500,
            home_team_passes_accuracy=85.0,
            home_team_passes_percent=85,
            away_team_shots_on_goal=7,
            away_team_shots_off_goal=3,
            away_team_total_shots=10,
            away_team_blocked_shots=3,
            away_team_shots_insidebox=5,
            away_team_shots_outsidebox=5,
            away_team_fouls=12,
            away_team_corner_kicks=4,
            away_team_offsides=1,
            away_team_ball_possession=44.5,
            away_team_yellow_cards=2,
            away_team_red_cards=0,
            away_team_goalkeeper_saves=6,
            away_team_total_passes=400,
            away_team_passes_accuracy=80.0,
            away_team_passes_percent=80,
        )
        matches.append(match)
        match_date = base_date + timedelta(days=21)
        match = Match(
            match_id=17,
            season_id=2,
            home_team_id=5,
            away_team_id=6,
            referee="Referee A",
            match_date=match_date,
            venue_name="Stadium A",
            round="Round 20",
            status_short="NS",
            status_long="Scheduled",
            type="Scheduled",
            home_team_shots_on_goal=10,
            home_team_shots_off_goal=5,
            home_team_total_shots=15,
            home_team_blocked_shots=2,
            home_team_shots_insidebox=8,
            home_team_shots_outsidebox=7,
            home_team_fouls=10,
            home_team_corner_kicks=6,
            home_team_offsides=2,
            home_team_ball_possession=55.5,
            home_team_yellow_cards=1,
            home_team_red_cards=0,
            home_team_goalkeeper_saves=4,
            home_team_total_passes=500,
            home_team_passes_accuracy=85.0,
            home_team_passes_percent=85,
            away_team_shots_on_goal=7,
            away_team_shots_off_goal=3,
            away_team_total_shots=10,
            away_team_blocked_shots=3,
            away_team_shots_insidebox=5,
            away_team_shots_outsidebox=5,
            away_team_fouls=12,
            away_team_corner_kicks=4,
            away_team_offsides=1,
            away_team_ball_possession=44.5,
            away_team_yellow_cards=2,
            away_team_red_cards=0,
            away_team_goalkeeper_saves=6,
            away_team_total_passes=400,
            away_team_passes_accuracy=80.0,
            away_team_passes_percent=80,
        )
        matches.append(match)

        # Dodanie meczów do bazy danych
        db.session.add_all(matches)
        db.session.commit()


@pytest.fixture(scope='function')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def get_token(app_context):
    return generate_access_token("1", "user", "John", "Doe")

@pytest.fixture(scope='function')
def app_context(app):
    with app.app_context():
        yield