from mongoengine import Document
from mongoengine.fields import ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author, dbref=True)
    quote = StringField()

    def __repr__(self):
        return self.quote
