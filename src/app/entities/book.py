from db.entity import BaseEntity
from utils.settings import lazy_settings


class Book(BaseEntity):
    _fields = [lazy_settings.PRIMARY_KEY_LOOKUP, "title", "author", "year", "status"]

    def __str__(self):
        return \
            "ID: {id}\n" \
            "Title: {title}\n" \
            "Author: {author}\n" \
            "Year: {year}\n" \
            "Status: {status}\n".format(
                id=self.id,
                title=self.title,
                author=self.author,
                year=self.year,
                status=self.status
            )