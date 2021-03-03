import io

import flask

__all__ = ["example_blueprint"]

example_blueprint = flask.Blueprint("Example", "Example")


@example_blueprint.route("/examples")
def examples():
    return flask.render_template("basic/page.html",
                                 page_name="Examples",
                                 body_page="examples/navigation.html",
                                 )


@example_blueprint.route("/examples/download/<library>")
def download(library: str):
    if library == "c":
        return flask.send_file(io.BytesIO(flask.current_app.config["libraries"].c()), attachment_filename="c.zip")
    elif library == "java":
        return flask.send_file(io.BytesIO(flask.current_app.config["libraries"].java()),
                               attachment_filename="java.zip")
    elif library == "python":
        return flask.send_file(io.BytesIO(flask.current_app.config["libraries"].python()),
                               attachment_filename="python.zip")
    elif library == "all":
        return flask.send_file(io.BytesIO(flask.current_app.config["libraries"].all()),
                               attachment_filename="all.zip")
    else:
        return flask.redirect("/home")
