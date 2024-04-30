from flask_wtf import FlaskForm
from wtforms import (
    Form, StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    SelectMultipleField,
    FieldList,
    FormField,
)
from wtforms.validators import DataRequired, Optional, Length
from wtforms.widgets import ListWidget, CheckboxInput


from app.models.enums import PrivacyType, LangType


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SnippetForm(Form):
    file_name = StringField(
        "Snippet Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Snippet Name"}
    )
    file_lang = SelectField(
        "Snippet Lang",  # or ext.
        validators=[DataRequired()],
        choices=[
            (LangType.text.name, LangType.text.value),
            (LangType.markdown.name, LangType.markdown.value),
            (LangType.html.name, LangType.html.value),
            (LangType.python.name, LangType.python.value),
            (LangType.php.name, LangType.php.value),
            (LangType.sql.name, LangType.sql.value),
            (LangType.javascript.name, LangType.javascript.value),
            (LangType.go.name, LangType.go.value),
        ],
        render_kw={"placeholder": "Snippet Lang"},
    )
    content = TextAreaField(
        "Snippet Content",
        validators=[DataRequired()],
        render_kw={"placeholder": "Snippet Content"}
    )


class CreateCollectionForm(FlaskForm):
    title = StringField(
        "Collection Title",
        validators=[DataRequired(), Length(min=3, max=255)]
    )
    description = TextAreaField("Description")
    privacy = SelectField(
        "Privacy",
        validators=[DataRequired()],
        choices=[
            (PrivacyType.private.name, PrivacyType.private.value),
            (PrivacyType.public.name, PrivacyType.public.value),
        ]
    )
    tags = MultiCheckboxField(
        "Tags",
        validators=[Optional()],
        coerce=int,
    )
    snippets = FieldList(FormField(SnippetForm), min_entries=1, max_entries=20)

    submit = SubmitField("Save")


class UpdateCollectionForm(FlaskForm):
    title = StringField(
        "Collection Title",
        validators=[DataRequired(), Length(min=3, max=255)]
    )
    description = TextAreaField("Description")
    privacy = SelectField(
        "Privacy",
        validators=[DataRequired()],
        choices=[
            (PrivacyType.public.name, PrivacyType.public.value),
            (PrivacyType.private.name, PrivacyType.private.value)
        ]
    )
    tags = MultiCheckboxField(
        "Tags",
        validators=[Optional()],
        coerce=int,
    )

    submit = SubmitField("Save")


class CreateSnippetForm(FlaskForm):
    name = StringField(
        "Snippet Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Snippet Name"}
    )
    language = SelectField(
        "Snippet  Language",
        validators=[DataRequired()],
        choices=[
            (LangType.text.name, LangType.text.value),
            (LangType.markdown.name, LangType.markdown.value),
            (LangType.html.name, LangType.html.value),
            (LangType.python.name, LangType.python.value),
            (LangType.php.name, LangType.php.value),
            (LangType.sql.name, LangType.sql.value),
            (LangType.javascript.name, LangType.javascript.value),
            (LangType.go.name, LangType.go.value),
        ],
    )
    privacy = SelectField(
        "Snippet  Privacy",
        validators=[DataRequired()],
        choices=[
            (PrivacyType.private.name, PrivacyType.private.value),
            (PrivacyType.public.name, PrivacyType.public.value),
        ],
    )
    content = TextAreaField(
        "Snippet Content",
        validators=[DataRequired()],
        render_kw={"placeholder": "Snippet Content"}
    )
    submit = SubmitField("Save")


class CreateTagForm(FlaskForm):
    name = StringField(
        "Tag Name",
        validators=[DataRequired(), Length(min=1, max=50)],

    )
    color = SelectField(
        "Tag Color",
        validators=[Optional()],
        choices=[
            ("red", "Red"),
            ("blue", "Blue"),
            ("green", "Green"),
            ("purple", "Purple"),
        ]
    )
    privacy = SelectField(
        "Privacy",
        validators=[DataRequired()],
        choices=[
            (PrivacyType.private.name, PrivacyType.private.value),
            (PrivacyType.public.name, PrivacyType.public.value),
        ]
    )
    submit = SubmitField("Save")
