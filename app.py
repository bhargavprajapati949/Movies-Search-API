from main import app

from database.database import db

from user import routes
from movie import routes


if __name__ == '__main__':
    app.run()