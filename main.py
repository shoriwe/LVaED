import os

import flask
import requests

import blueprints.home
import blueprints.presentation


class Articles(object):
    def __init__(self, list_article_html: str):
        self.__list = list_article_html

    def list(self):
        return self.__list


def render_article(article_path: str, output_path: str) -> str:
    if not os.path.exists(output_path):
        article = open(article_path)
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        data = {"text": article.read()}
        article.close()
        response = requests.post(
            "https://api.github.com/markdown",
            json=data,
            headers=headers
        )
        file = open(output_path, "w")
        file.write(response.text)
        file.flush()
        file.close()
    file = open(output_path)
    html = file.read()
    file.close()
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
