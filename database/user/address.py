from mongoengine import EmbeddedDocument, StringField


# source: https://gist.github.com/pingwping/92219a8a1e9d44e1dd8a
class Address(EmbeddedDocument):
    address = StringField()
    city = StringField(max_length=120)
