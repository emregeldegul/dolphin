from app import create_app
from app import db
from app.models.user import User
from app.models.collection import Collection, Snippet, Tag, tags

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

user = User()
user.first_name = "Yunus Emre"
user.last_name = "Geldegül"
user.username = "hazel"
user.email = "yunusemregeldegul@gmail.com"
user.generate_password_hash("123456")
user.save()

tag_one = Tag()
tag_one.user = user
tag_one.name = "MyBB"
tag_one.save()

tag_two = Tag()
tag_two.user = user
tag_two.name = "Flask"
tag_two.save()

tag_three = Tag()
tag_three.user = user
tag_three.name = "Linux"
tag_three.save()

tag_four = Tag()
tag_four.user = user
tag_four.name = "Django"
tag_four.save()

collection_one = Collection()
collection_one.user = user
collection_one.title = "My First Collection"
collection_one.description = "pembe bir mezarlık gördüm rüyamda"
collection_one.tags.append(tag_one)
collection_one.save()

snippet_one = Snippet()
snippet_one.collection = collection_one
snippet_one.name = "hazel.py"
snippet_one.language = "python"
snippet_one.content = "print('hello everybody')"
snippet_one.save()

snippet_two = Snippet()
snippet_two.collection = collection_one
snippet_two.name = "hazel.php"
snippet_two.language = "php"
snippet_two.content = "<?php echo 'hi'; ?>"
snippet_two.save()


collection_two = Collection()
collection_two.user = user
collection_two.title = "My Second Collection"
collection_two.description = "kalbi atan ölü bedenlerdi hepsi"
collection_two.tags.append(tag_one)
collection_two.tags.append(tag_four)
collection_two.save()


snippet_three = Snippet()
snippet_three.collection = collection_two
snippet_three.name = "setup.md"
snippet_three.language = "markdown"
snippet_three.content = "# setup sonra next next next"
snippet_three.save()
