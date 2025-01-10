
from app.config import db

class MatchRating(db.Model):
    __tablename__ = 'match_rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.match_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    __table_args__ = (db.UniqueConstraint('user_id', 'match_id', name='unique_user_match_rating'),)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    match = db.relationship('Match', backref=db.backref('ratings', lazy=True))

    def __repr__(self):
        return f"<MatchRating User: {self.user.username}, Match: {self.match.match_id}, Rating: {self.rating}>"
    
    def to_json(self):
        return {
            "user": self.user.firstName + " " + self.user.lastName,
            "match_id": self.match_id,
            "rating": self.rating,
            "created_at": self.created_at
        }
