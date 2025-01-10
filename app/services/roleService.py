from app.models.role import Role
from app.config import db

def get_role(id):
    return Role.query.get(id)

def get_role_by_name(name):
    return Role.query.filter_by(name=name).first()

def init_roles():
    roles = ['admin', 'user']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()