import io
import os
import re
import zipfile

import flask
import markdown

import blueprints.example
import blueprints.home
import blueprints.presentation
import blueprints.transformations


class Zipper(object):
	def __init__(self):
		self._content = None
		self._content_handler = io.BytesIO()

	def append(self, filename: str, content: bytes):
		zip_file = zipfile.ZipFile(self._content_handler, "a", zipfile.ZIP_DEFLATED, False)
		zip_file.writestr(filename, content)
		for file in zip_file.filelist:
			file.create_system = 0
		zip_file.close()
		self._content_handler.seek(0)
		self._content = self._content_handler.read()

	def append_directory(self, path: str):
		for directory_path, directories, files in os.walk(path):
			for file in files:
				file_path = os.path.join(directory_path, file)
				with open(file_path, "rb") as file_object:
					self.append(file_path, file_object.read())
		self._content_handler.seek(0)
		self._content = self._content_handler.read()

	def content(self) -> bytes:
		return self._content


def pygmentize(raw_markdown: str) -> str:
	languages = re.findall(re.compile("(?<=^```)\\w+$", re.M), raw_markdown)
	last_index = 0
	for language in languages:
		list_markdown = raw_markdown.split("\n")

		code_block_start_index = list_markdown.index(f"```{language}", last_index)
		code_block_end_index = list_markdown.index("```", code_block_start_index)
		for index in range(code_block_start_index + 1, code_block_end_index):
			list_markdown[index] = f"\t{list_markdown[index]}"
		list_markdown[code_block_start_index] = "\t" + list_markdown[code_block_start_index].replace("```", ":::")
		list_markdown[code_block_end_index] = "\n"
		raw_markdown = "\n".join(list_markdown)
		last_index = code_block_end_index
	return raw_markdown


def render_article(article_path: str) -> str:
	with open(article_path) as file:
		content = file.read()
	html = markdown.markdown(pygmentize(content), extensions=["codehilite", "extra"])
	return html


def zip_library(library_directory: str) -> Zipper:
	z = Zipper()
	z.append_directory(library_directory)
	return z


def load_articles(app: flask.Flask):
	app.config["articles"] = {
		"list": render_article("markdown/articles/list.md"),
		"stack": render_article("markdown/articles/stack.md"),
		"queue": render_article("markdown/articles/queue.md"),
		"binary_tree": render_article("markdown/articles/binary_tree.md"),
		"avl_tree": render_article("markdown/articles/avl_tree.md"),
		"b_tree": render_article("markdown/articles/b_tree.md")
	}


def load_libraries(app: flask.Flask):
	app.config["libraries"] = {
		"all": zip_library("DataTypes").content(),
		"c": zip_library("DataTypes/C").content(),
		"java": zip_library("DataTypes/Java").content(),
		"python": zip_library("DataTypes/Python").content()
	}


def load_examples(app: flask.Flask):
	app.config["examples"] = {}
	app.config["examples"]["c"] = {
		"simple_list": render_article("markdown/examples/c/simple_list.md"),
		"double_list": render_article("markdown/examples/c/double_list.md"),
		"circular_simple_list": render_article("markdown/examples/c/circular_simple_list.md"),
		"circular_double_list": render_article("markdown/examples/c/circular_double_list.md"),
		"array_stack": render_article("markdown/examples/c/array_stack.md"),
		"list_stack": render_article("markdown/examples/c/list_stack.md"),
		"array_queue": render_article("markdown/examples/c/array_queue.md"),
		"list_queue": render_article("markdown/examples/c/list_queue.md"),
		"priority_queue": render_article("markdown/examples/c/priority_queue.md"),
		"binary_tree": render_article("markdown/examples/c/binary_tree.md"),
		"avl_tree": render_article("markdown/examples/c/avl_tree.md"),
		"b_tree": render_article("markdown/examples/c/b_tree.md")
	}
	app.config["examples"]["java"] = {
		"simple_list": render_article("markdown/examples/java/simple_list.md"),
		"double_list": render_article("markdown/examples/java/double_list.md"),
		"circular_simple_list": render_article("markdown/examples/java/circular_simple_list.md"),
		"circular_double_list": render_article("markdown/examples/java/circular_double_list.md"),
		"array_stack": render_article("markdown/examples/java/array_stack.md"),
		"list_stack": render_article("markdown/examples/java/list_stack.md"),
		"array_queue": render_article("markdown/examples/java/array_queue.md"),
		"list_queue": render_article("markdown/examples/java/list_queue.md"),
		"priority_queue": render_article("markdown/examples/java/priority_queue.md"),
		"binary_tree": render_article("markdown/examples/java/binary_tree.md"),
		"avl_tree": render_article("markdown/examples/java/avl_tree.md"),
		"b_tree": render_article("markdown/examples/java/b_tree.md")
	}
	app.config["examples"]["python"] = {
		"simple_list": render_article("markdown/examples/python/simple_list.md"),
		"double_list": render_article("markdown/examples/python/double_list.md"),
		"circular_simple_list": render_article("markdown/examples/python/circular_simple_list.md"),
		"circular_double_list": render_article("markdown/examples/python/circular_double_list.md"),
		"array_stack": render_article("markdown/examples/python/array_stack.md"),
		"list_stack": render_article("markdown/examples/python/list_stack.md"),
		"array_queue": render_article("markdown/examples/python/array_queue.md"),
		"list_queue": render_article("markdown/examples/python/list_queue.md"),
		"priority_queue": render_article("markdown/examples/python/priority_queue.md"),
		"binary_tree": render_article("markdown/examples/python/binary_tree.md"),
		"avl_tree": render_article("markdown/examples/python/avl_tree.md"),
		"b_tree": render_article("markdown/examples/python/b_tree.md")
	}


def setup() -> flask.Flask:
	app = flask.Flask(__name__, template_folder="templates")
	app.register_blueprint(blueprints.home.home_blueprint)
	app.register_blueprint(blueprints.presentation.presentation_blueprint)
	app.register_blueprint(blueprints.example.example_blueprint)
	app.register_blueprint(blueprints.transformations.transformations_blueprint)
	load_articles(app)
	load_libraries(app)
	load_examples(app)
	return app


app = setup()


def main():
	app.run("127.0.0.1", 5000, debug=False)


if __name__ == '__main__':
	main()
