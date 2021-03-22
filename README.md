# LVaED

![](https://github.com/shoriwe/LVaED/raw/main/static/img/logo_transparent_background.png)

## Powered by

<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/> <img alt="C" src="https://img.shields.io/badge/c%20-%2300599C.svg?&style=for-the-badge&logo=c&logoColor=white"/> <img alt="Java" src="https://img.shields.io/badge/java-%23ED8B00.svg?&style=for-the-badge&logo=java&logoColor=white"/> <img alt="HTML5" src="https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/> <img alt="Markdown" src="https://img.shields.io/badge/markdown-%23000000.svg?&style=for-the-badge&logo=markdown&logoColor=white"/> <img alt="Flask" src="https://img.shields.io/badge/flask%20-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/>

## Description

LVaED is blog like web application that let people understand the concept and implementation of common DataTypes like `Lists`, `Stacks`, `Queues`, etc.

## Important

The DataTypes that you will find here are only for education purpose, never use them in production software, since it is possible that they will break.

## Preview

A preview of the website

### Homepage

<table><tr><td>
    <img src="https://github.com/shoriwe/LVaED/raw/main/resources/HomePage.png" />
</td></tr></table>

### Presentation

<table><tr><td>
    <img src="https://github.com/shoriwe/LVaED/raw/main/resources/Presentation.png"/>
</td></tr></table>

#### Article

<table><tr><td>
    <img src="https://github.com/shoriwe/LVaED/raw/main/resources/Article.png"/>
</td></tr></table>

### Examples

<table><tr><td>
    <img src="https://github.com/shoriwe/LVaED/raw/main/resources/Examples.png"/>
</td></tr></table>

#### Code Preview

<table><tr><td>
    <img src="https://github.com/shoriwe/LVaED/raw/main/resources/CodePreview.png"/>
</td></tr></table>

### Transformation

<table>
    <tr>
        <td>
            <img src="https://github.com/shoriwe/LVaED/raw/main/resources/Transformations.png"/>
        </td>
    </tr>
</table>

#### Source Code to Network Graph

<table>
    <tr>
        <td>
            <img src="https://github.com/shoriwe/LVaED/raw/main/resources/Transformations-Graph.png"/>
        </td>
    </tr>
</table>

#### AST-like representation and Source code View

<table>
    <tr>
        <td>
            <img src="https://github.com/shoriwe/LVaED/raw/main/resources/Transformations-Results-SourceCode.png"/>
        </td>
    </tr>
</table>

## Installation

1. Clone the repository

```shell script
git clone https://github.com/shoriwe/LVaED.git
```

2. Go the the cloned directory

```shell script
cd LVaED
```

3. (OPTIONAL) Create a Virtual Python environment

```shell script
python -m venv venv
```

And activate it

```shell script
source venv/scripts/activate
```

4. Install the dependencies

```shell script
pip install -r requirements.txt
```

5. Start the web server (If you run it as a script, it will run by default in `127.0.0.1:5000`)

```shell script
python main.py
```

## Image resources

Almost all the image resources where taken from [Wikipedia.org](https://es.wikipedia.org/) and [GeekForGeeks](https://www.geeksforgeeks.org/), so special thanks to this online reference platforms and the image authors for providing them.

By clicking on the images of this website you should be redirected to the page where they were found, with the proper reference in `Wikipedia` or the respective article in `GeekForGeeks`.

## Production

You should be able to create a production ready setup with [gunicorn](https://gunicorn.org/)
