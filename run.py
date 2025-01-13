from app.config import db
from app import create_app
from app.services.roleService import init_roles
from app.services.apiService import my_function
import threading
import time
app = create_app()

def run_periodically(interval, func, *args, **kwargs):
    def wrapper():
        while True:
            func(*args, **kwargs)
            time.sleep(interval)
    
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()

# run_periodically(60, my_function)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        init_roles()
    app.run(debug=True)