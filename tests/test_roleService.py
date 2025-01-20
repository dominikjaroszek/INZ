from app.services.roleService import *

def test_get_role_by_name(setup_database_user):
    role = get_role_by_name("admin")
    assert role.name == "admin"

def test_get_role(setup_database_user):
    role = get_role(1)
    assert role.name == "admin"