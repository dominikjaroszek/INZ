from flask_sqlalchemy import SQLAlchemy
from app.config import db

class League(db.Model):
    __tablename__ = 'league'
    league_id= db.Column(db.Integer, primary_key=True)  
    name_league = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"<League {self.name}>"   
    
