"""App entry point."""
from flask_app import create_app
from flask_bootstrap import Bootstrap

app = create_app()
bootstrap = Bootstrap(app)

if __name__ == "__main__":
    app.run(port=33507, debug = True)