import re

import flask
import markdown

import blueprints.home
import blueprints.presentation


class Articles(object):
    def __init__(self, list_article_html: str):
        self.__list = list_article_html

    def list(self):
        return self.__list


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


def load_articles(app: flask.Flask):
    app.config["articles"] = Articles(
        render_article("articles/markdown/list.md", "articles/html/list.html")
    )


def setup() -> flask.Flask:
    app = flask.Flask(__name__, template_folder="templates")
    app.register_blueprint(blueprints.home.home_blueprint)
    app.register_blueprint(blueprints.presentation.presentation_blueprint)
    load_articles(app)
    return app


def main():
    app = setup()
    app.run("127.0.0.1", 5000, debug=False)


if __name__ == '__main__':
    main()
