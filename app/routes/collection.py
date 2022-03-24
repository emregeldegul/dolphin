from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from app.models.enums import Status, PrivacyType
from app.models.collection import Collection, Snippet, Tag
from app.forms.collection import (
    CreateSnippetForm,
    CreateTagForm,
    CreateCollectionForm,
    SnippetForm,
    UpdateCollectionForm,
)
from app.helpers.string_helper import generate_uuid

collection = Blueprint("collection", __name__, url_prefix="/collection")


@collection.route("/")
@collection.route("/index")
@login_required
def collection_index():
    filter_array = []

    if request.args.get("tag", None):
        filter_array.append(
            Collection.tags.any(Tag.name == request.args.get("tag"))
        )

    if request.args.get("type", None):
        filter_array.append(~Collection.tags.any())

    the_collections = (
        Collection.query
        .filter_by(user=current_user)
        .filter_by(status=Status.active)
        .filter(*filter_array)
        .order_by(Collection.updated_at.desc())
        .all()
    )

    return render_template(
        "views/collection/collection_index.html",
        title="My Collections",
        the_collections=the_collections,
    )


@collection.route("/create", methods=["GET", "POST"])
@login_required
def collection_create():
    form = CreateCollectionForm()
    sub_form = SnippetForm(prefix="snippets-_-")
    the_tags = Tag.query.filter_by(user=current_user).all()
    form.tags.choices = [(i.id, i.name) for i in the_tags]

    if form.validate_on_submit():
        new_collection = Collection()
        new_collection.user = current_user
        new_collection.title = form.title.data
        new_collection.description = form.description.data
        new_collection.privacy = form.privacy.data
        new_collection.uuid = generate_uuid(Collection)

        db.session.add(new_collection)
        db.session.flush()

        for _snippet in form.snippets.data:
            new_snippet = Snippet()
            new_snippet.collection = new_collection
            new_snippet.name = _snippet["file_name"]
            new_snippet.language = _snippet["file_lang"]
            new_snippet.content = _snippet["content"]
            new_snippet.uuid = generate_uuid(Snippet)

            db.session.add(new_snippet)

        for _tag in form.tags.data:
            tag_check = Tag.query.filter_by(id=_tag).filter_by(user=current_user).first()

            if tag_check:
                new_collection.tags.append(tag_check)
                db.session.flush()

        db.session.commit()

        return redirect(url_for("collection.collection_detail", uuid=new_collection.uuid))

    form.tags.choices = [(i.id, i.name) for i in the_tags]

    return render_template(
        "views/collection/collection_create.html",
        title="Collection Create",
        form=form,
        sub_form=sub_form,
    )


@collection.route("/detail/<string:uuid>")
@login_required
def collection_detail(uuid):
    the_collection = (
        Collection.query
        .filter_by(user=current_user)
        .filter_by(status=Status.active)
        .filter_by(uuid=uuid)
        .first_or_404()
    )

    the_snippets = (
        Snippet.query
        .filter_by(collection=the_collection)
        .filter_by(status=Status.active)
        .all()
    )

    return render_template(
        "views/collection/collection_detail.html",
        title="Collection: {}".format(the_collection.title),
        the_collection=the_collection,
        the_snippets=the_snippets,
    )


@collection.route("/detail/<string:uuid>/edit", methods=["GET", "POST"])
@login_required
def collection_update(uuid):
    the_collection = (
        Collection.query
        .filter_by(uuid=uuid)
        .filter_by(user=current_user)
        .filter_by(status=Status.active)
        .first_or_404()
    )

    form = UpdateCollectionForm()
    the_tags = Tag.query.filter_by(user=current_user).all()
    form.tags.choices = [(i.id, i.name) for i in the_tags]

    if form.validate_on_submit():
        the_collection.title = form.title.data
        the_collection.description = form.description.data
        the_collection.privacy = form.privacy.data
        the_collection.tags = []

        for _tag in form.tags.data:
            tag_check = Tag.query.filter_by(id=_tag).filter_by(user=current_user).first()

            if tag_check:
                the_collection.tags.append(tag_check)
                db.session.flush()

        the_collection.save()

        flash("Collection Successfully Updated", "success")

    form.title.data = the_collection.title
    form.description.data = the_collection.description
    form.privacy.data = the_collection.privacy.name
    form.tags.data = [i.id for i in the_collection.tags]

    return render_template(
        "views/collection/collection_update.html",
        title="Collection Edit: {}".format(the_collection.title),
        form=form,
        the_collection=the_collection,
    )


@collection.route("/detail/<string:uuid>/delete", methods=["DELETE"])
@login_required
def collection_delete(uuid):
    the_collection = (
        Collection.query
        .filter_by(user=current_user)
        .filter_by(status=Status.active)
        .filter_by(uuid=uuid)
        .first_or_404()
    )

    the_collection.status = Status.deleted
    the_collection.save()

    return {"message": "Collection Successfully Deleted"}


@collection.route("/detail/<string:uuid>/snippet_create", methods=["GET", "POST"])
@login_required
def snippet_create(uuid):
    the_collection = (
        Collection.query
        .filter_by(user=current_user)
        .filter_by(status=Status.active)
        .filter_by(uuid=uuid)
        .first_or_404()
    )

    form = CreateSnippetForm()

    if form.validate_on_submit():
        the_snippet = Snippet()
        the_snippet.collection = the_collection
        the_snippet.name = form.name.data
        the_snippet.language = form.language.data
        the_snippet.content = form.content.data
        the_snippet.privacy = form.privacy.data
        the_snippet.uuid = generate_uuid(Snippet)
        the_snippet.save()

        flash("Snippet Successfully Updated", "success")

        return redirect(url_for("collection.snippet_detail", uuid=the_snippet.uuid))

    return render_template(
        "views/collection/snippet_create.html",
        title="Create Snippet: {}".format(the_collection.title),
        form=form,
        the_collection=the_collection,
    )


@collection.route("/snippet/detail/<string:uuid>", methods=["GET", "POST"])
@login_required
def snippet_detail(uuid):
    the_snippet = (
        Snippet.query
        .filter_by(uuid=uuid)
        .filter_by(status=Status.active)
        .filter(Snippet.collection.has(user=current_user))
        .first_or_404()
    )

    form = CreateSnippetForm()

    if form.validate_on_submit():
        the_snippet.name = form.name.data
        the_snippet.language = form.language.data
        the_snippet.privacy = form.privacy.data
        the_snippet.content = form.content.data
        the_snippet.save()

        flash("Snippet Successfully Updated", "success")

    form.name.data = the_snippet.name
    form.language.data = the_snippet.language
    form.privacy.data = the_snippet.privacy.name
    form.content.data = the_snippet.content

    return render_template(
        "views/collection/snippet_detail.html",
        title="Snippet: {}".format(the_snippet.name),
        the_snippet=the_snippet,
        form=form,
    )


@collection.route("/snippet/detail/<string:uuid>/public")
def snippet_detail_public(uuid):
    the_snippet = (
        Snippet.query
        .filter_by(uuid=uuid)
        .filter_by(status=Status.active)
        .filter_by(privacy=PrivacyType.public)
        .first_or_404()
    )

    return render_template(
        "views/collection/snippet_detail_public.html",
        title="Snippet: {}".format(the_snippet.name),
        the_snippet=the_snippet,
    )


@collection.route("/snippet/detail/<string:uuid>/public/raw")
def snippet_detail_raw(uuid):
    the_snippet = (
        Snippet.query
        .filter_by(uuid=uuid)
        .filter_by(status=Status.active)
        .filter_by(privacy=PrivacyType.public)
        .first_or_404()
    )

    return render_template(
        "views/collection/snippet_detail_raw.html",
        title="Snippet: {}".format(the_snippet.name),
        the_snippet=the_snippet,
    )

@collection.route("/snippet/detail/<string:uuid>/delete", methods=["DELETE"])
@login_required
def snippet_delete(uuid):
    the_snippet = (
        Snippet.query
        .filter_by(uuid=uuid)
        .filter_by(status=Status.active)
        .filter(Snippet.collection.has(user=current_user))
        .first_or_404()
    )

    the_snippet.status = Status.deleted
    the_snippet.save()

    return {"message": "Snippet Successfully Deleted"}


@collection.route("/tag/", methods=["GET", "POST"])
@collection.route("/tag/index", methods=["GET", "POST"])
@login_required
def tag_index():
    form = CreateTagForm()

    if form.validate_on_submit():
        tag_check = (
            Tag.query
            .filter(func.lower(Tag.name) == func.lower(form.name.data.strip()))
            .filter_by(user=current_user)
            .first()
        )

        if tag_check:
            flash("This Tag Already Exists", "danger")
        else:
            the_tag = Tag()
            the_tag.user = current_user
            the_tag.name = form.name.data.strip()
            the_tag.color = form.color.data
            the_tag.privacy = form.privacy.data
            the_tag.uuid = generate_uuid(Tag)
            the_tag.save()

            flash("Tag Created Successfully", "success")

    the_tags = Tag.query.filter_by(user=current_user).all()

    return render_template(
        "views/collection/tag_index.html",
        title="Tag Management",
        the_tags=the_tags,
        form=form,
    )


@collection.route("/tag/detail/<string:uuid>", methods=["GET", "POST"])
@login_required
def tag_detail(uuid):
    the_tag = Tag.query.filter_by(user=current_user).filter_by(uuid=uuid).first_or_404()
    form = CreateTagForm()

    if form.validate_on_submit():
        tag_check = (
            Tag.query.filter(
                func.lower(Tag.name) == func.lower(form.name.data.strip())
            ).filter_by(
                user=current_user
            ).first()
        )

        if tag_check and tag_check != the_tag:
            flash("This Tag Already Exists", "danger")
        else:
            the_tag.name = form.name.data
            the_tag.color = form.color.data
            the_tag.privacy = form.privacy.data
            the_tag.save()

            flash("Tag Updated Successfully", "success")

    form.name.data = the_tag.name
    form.color.data = the_tag.color
    form.privacy.data = the_tag.privacy.name

    tags = Tag.query.filter_by(user=current_user).all()
    return render_template(
        "views/collection/tag_detail.html",
        title="Edit Tag: {}".format(the_tag.name),
        form=form,
        tags=tags,
        the_tag=the_tag,
    )


@collection.route("/tag/detail/<string:uuid>/delete", methods=["DELETE"])
@login_required
def tag_delete(uuid):
    the_tag = (
        Tag.query
        .filter_by(uuid=uuid)
        .filter_by(user=current_user)
        .first_or_404()
    )

    the_tag.delete()

    return {"message": "Snippet Successfully Deleted"}
