from flask import Blueprint, render_template

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@main.route("/index")
def index():
    return render_template("views/main/index.html", title="Home")


@main.route("/about")
def about():
    return render_template("views/main/about.html", title="About")
