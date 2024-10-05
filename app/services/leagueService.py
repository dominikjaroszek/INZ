from app.config import API_KEY, BASE_URL,db
import requests
from app.models.league import League

# Lista ID lig oraz sezon od którego zaczynamy
ids = [39, 140]
since = 2023

def get_league_coverage():
    for id_league in ids:
        # Pobieranie dostępnych sezonów od roku 2023
        for season in range(since, 2025):  # Załóżmy, że pobieramy dane do sezonu 2023/24
            url = f'{BASE_URL}/leagues?id={id_league}&season={season}'
            headers = {
                'x-rapidapi-key': API_KEY,
                'x-rapidapi-host': 'v3.football.api-sports.io'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                leagues = data.get('response', [])
                
                # Iteracja po ligach i zapis do bazy danych
                for league_data in leagues:
                    league_info = league_data['league']
                    country_info = league_data['country']

                    # Sprawdzanie, czy liga z danym IdS (ID ligi z API) i sezonem już istnieje w bazie danych
                    existing_league = League.query.filter_by(IdS=league_info['id'], Season=str(season)).first()

                    if not existing_league:
                        # Tworzenie nowej ligi
                        new_league = League(
                            IdS=league_info['id'],  # IdS to ID ligi z API
                            NameLeague=league_info['name'],
                            Country=country_info['name'],
                            Logo=league_info['logo'],
                            Season=str(season)
                        )
                        db.session.add(new_league)

                db.session.commit()
    return None
