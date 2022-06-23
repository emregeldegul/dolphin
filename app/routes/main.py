from flask import Blueprint, render_template, redirect, url_for
from flask import current_user

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@main.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("collection.collection_index"))
    
    return render_template("views/main/index.html", title="Home")


@main.route("/about")
def about():
    return render_template("views/main/about.html", title="About")


@main.route("/public_collections")
def public_collections():
    return render_template("views/main/public_collections.html", title="Public Collections")
