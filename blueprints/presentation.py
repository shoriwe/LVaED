import flask

__all__ = ["presentation_blueprint"]

presentation_blueprint = flask.Blueprint("Presentation", "presentation")


@presentation_blueprint.route("/presentation")
def presentation():
    return flask.render_template("basic/page.html",
                                 page_name="Presentation",
                                 body_page="presentation/navigation.html"
                                 )


@presentation_blueprint.route("/presentation/<datatype>")
def present_datatype(datatype: str):
    if datatype == "list":
        return flask.render_template("basic/page.html",
                                     page_name="List",
                                     body_page="article.html",
                                     content=flask.current_app.config["articles"].list())
    return flask.redirect("/home")
