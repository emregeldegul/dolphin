from app import db
from app.models.abstract import BaseModel
from app.models.enums import Status, PrivacyType
from app.helpers.string_helper import generate_uuid

tags = db.Table(
    "tags",
    db.Column("tag_id", db.ForeignKey("tag.id"), primary_key=True),
    db.Column("collection_id", db.ForeignKey("collection.id"), primary_key=True)
)


class Collection(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", backref="collections")
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    privacy = db.Column(db.Enum(PrivacyType), nullable=True, default=PrivacyType.private)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.active)
    uuid = db.Column(db.String(32), nullable=False, default=generate_uuid)
    tags = db.relationship("Tag", secondary=tags, lazy="subquery", backref=db.backref("collections", lazy=True))

    def __repr__(self):
        return "Collection({})".format(self.title)


class Snippet(BaseModel):
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=True)
    collection = db.relationship("Collection", backref="snippets")
    name = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(10), nullable=False)  # this field may be enum.
    content = db.Column(db.Text, nullable=True)
    privacy = db.Column(db.Enum(PrivacyType), nullable=True, default=PrivacyType.private)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.active)
    uuid = db.Column(db.String(32), nullable=False, default=generate_uuid)

    def __repr__(self):
        return "Snippet({} -> {})".format(self.collection.title, self.name)


class Tag(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", backref="tags")
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), nullable=True)
    privacy = db.Column(db.Enum(PrivacyType), nullable=True, default=PrivacyType.private)
    uuid = db.Column(db.String(32), nullable=False, default=generate_uuid)

    def active_collection_count(self):
        total_active_collection = (
            Collection.query
            .join(tags)
            .filter((tags.c.collection_id == Collection.id) & (tags.c.tag_id == self.id))
            .filter(Collection.status == Status.active)
            .count()
        )
        return total_active_collection

    def __repr__(self):
        return "Tag({})".format(self.name)


class Comment(BaseModel):
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=False)
    collection = db.relationship("Collection", backref="comments")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User")
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.active)
