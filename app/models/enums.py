from enum import Enum


# General Enums
class Status(Enum):
    active = "Aktif"
    passive = "Pasif"
    deleted = "Silinmiş"


# Collection and Snippet Enums
class PrivacyType(Enum):
    public = "Public"
    private = "Private"


class LangType(Enum):
    text = "Text"
    markdown = "Markdown"
    html = "HTML"
    python = "Python"
    php = "PHP"
    sql = "SQL"
    javascript = "JavaScript"
    go = "GO"
