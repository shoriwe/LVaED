import io
import os
import re
import zipfile

import flask
import markdown

import blueprints.example
import blueprints.home
import blueprints.presentation


class Articles(object):
    def __init__(self, list_article_html: str):
        self.__list = list_article_html

    def list(self):
        return self.__list


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


class Libraries(object):
    def __init__(self, all_: bytes, c_library: bytes, java_library: bytes, python_library: bytes):
        self.__all = all_
        self.__c_library = c_library
        self.__java_library = java_library
        self.__python_library = python_library

    def all(self):
        return self.__all

    def c(self):
        return self.__c_library

    def java(self):
        return self.__java_library

    def python(self):
        return self.__python_library


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


def render_article(article_path: str, _: str) -> str:
    with open(article_path) as file:
        content = file.read()
    html = markdown.markdown(pygmentize(content), extensions=["codehilite"])
    return html


def zip_library(library_directory: str) -> Zipper:
    z = Zipper()
    z.append_directory(library_directory)
    return z


def load_articles(app: flask.Flask):
    app.config["articles"] = Articles(
        render_article("markdown/articles/list.md", "articles/html/list.html")
    )


def load_libraries(app: flask.Flask):
    app.config["libraries"] = Libraries(
        zip_library("DataTypes").content(),
        zip_library("DataTypes/C").content(),
        zip_library("DataTypes/Java").content(),
        zip_library("DataTypes/Python").content()
    )


def setup() -> flask.Flask:
    app = flask.Flask(__name__, template_folder="templates")
    app.register_blueprint(blueprints.home.home_blueprint)
    app.register_blueprint(blueprints.presentation.presentation_blueprint)
    app.register_blueprint(blueprints.example.example_blueprint)
    load_articles(app)
    load_libraries(app)
    return app


def main():
    app = setup()
    app.run("127.0.0.1", 5000, debug=False)


if __name__ == '__main__':
    main()
