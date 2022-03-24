# Dolphin
Dolphin is a snippet organizer for developers.


## Development Setup
```bash
~$ git clone https://github.com/emregeldegul/dolphin.git && cd dolphin
~$ python3 -m virtualenv venv && source venv/bin/activate
~$ pip install -r requirements.txt
~$ flask db upgrade
~$ flask run
```

## Add Yourself Routes
You can add a file in `app/routes` folder and create yourself blueprint app.

Example for order blueprint:

`app/routes/order.py`

```python
from flask import Blueprint, render_template

order = Blueprint('order', __name__, url_prefix='/order')


@order.route('/')
def index():
    return render_template('views/order/index.html', title='Order')
```

## Base Model
You can use inside `app/models/abstract.py` in `BaseModel` as the base model.

`app/models/order.py`

```python
from app.models.abstract import BaseModel


class Order(BaseModel):
    number = db.Column(db.String(50), nullable=False, unique=True)
    ...

    def __repr__(self):
        return "Order({})".format(self.number)
```

It will automatically create the creation and update columns for you and add the save method.
