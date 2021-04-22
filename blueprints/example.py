import io

import flask

__all__ = ["example_blueprint"]

example_blueprint = flask.Blueprint("Example", "example")


@example_blueprint.route("/examples")
def examples():
	return flask.render_template("basic/page.html",
								 page_name="Examples",
								 body_page="examples/navigation.html",
								 )


@example_blueprint.route("/examples/<language>/<datatype>")
def present_datatype(language: str, datatype: str):
	language_examples = flask.current_app.config["examples"].get(language)
	if language_examples is not None:
		datatype_example = language_examples.get(datatype)
		if datatype_example is not None:
			return flask.render_template("basic/page.html",
										 page_name="List",
										 body_page="article.html",
										 content=datatype_example)
	return flask.redirect("/home")


@example_blueprint.route("/examples/download/<library>")
def download(library: str):
	content = flask.current_app.config["libraries"].get(library)
	if content is not None:
		return flask.send_file(io.BytesIO(content), attachment_filename=f"{library}.zip")
	return flask.redirect("/home")
