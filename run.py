from app.config import db
from app import create_app
from app.services.roleService import init_roles
from app.services.apiService import check_update
import threading
import time
import os
baza =os.getenv("DATABASE_URI")

app = create_app(baza)

def run_periodically(interval, func, *args, **kwargs):
    def wrapper():
        while True:
            with app.app_context():
                func(*args, **kwargs)
            time.sleep(interval)
    
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()

# run_periodically(60, check_update, 39)
# run_periodically(60, check_update, 140)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        init_roles()
    app.run(debug=True)