import flask

__all__ = ["home_blueprint"]

home_blueprint = flask.Blueprint("Home", "home")


@home_blueprint.route("/home")
def home():
    return flask.render_template("basic/page.html", page_name="Home", body_page="navigation/home.html")
