from random import choices
from string import ascii_lowercase, digits


def generate_uuid(model=None, k=32):
    uuid = "".join(choices(ascii_lowercase + digits, k=k))

    if not model:
        return uuid

    the_check = model.query.filter_by(uuid=uuid).first()

    if the_check:
        generate_uuid(model)

    return uuid
