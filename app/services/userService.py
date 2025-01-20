from app.models.user import User
from app.config import db
from app.services.roleService import get_role_by_name


def create_user( firstName, lastName,email, password):
    rola = get_role_by_name('user')
    new_user = User(firstName=firstName, lastName=lastName,  email=email, password=password, role_id=rola.role_id)
    new_user.role = rola
    db.session.add(new_user)
    db.session.commit()
    return new_user

def check_password_controller(user, password):
    return user.check_password(password)

def get_user_by_id(id):
    return User.query.get(id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def change_password(data, user):
    user.set_password(data.newPassword)
    db.session.commit()
    return True
