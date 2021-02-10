import flask

import blueprints.home


def setup() -> flask.Flask:
    app = flask.Flask(__name__, template_folder="templates")
    app.register_blueprint(blueprints.home.home_blueprint)
    return app


def main():
    app = setup()
    app.run("127.0.0.1", 5000, debug=False)


if __name__ == '__main__':
    main()
