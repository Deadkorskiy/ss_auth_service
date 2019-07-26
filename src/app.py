from settings import settings
from bootstrap import app


application = app   # alias for gunicorn


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
