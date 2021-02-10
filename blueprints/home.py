import flask

__all__ = ["home_blueprint"]

home_blueprint = flask.Blueprint("Home", "home")


@home_blueprint.route("/home")
def home():
    return flask.render_template("basic/page.html",
                                 page_name="Home",
                                 body_page="home/home.html",
                                 person_1_picture="/static/img/Andrea.svg",
                                 person_1_name="Andrea Velasquez",
                                 person_1_description="",
                                 person_2_picture="/static/img/Christian.jfif",
                                 person_2_name="Christian Monsalve",
                                 person_2_description="",
                                 person_3_picture="/static/img/Antonio.png",
                                 person_3_name="Antonio Donis",
                                 person_3_description="My name is Antonio, I am student at UPB Bucaramanga and you can find more creations like this one in my <a href=\"https://github.com/shoriwe\" style=\"text-decoration:none\">Github</a>"
                                 )
