from mongoengine import Document, StringField, DateTimeField, EmailField, ListField, EmbeddedDocumentField
from .address import Address
import datetime


class UserModel(Document):
    meta = {'collection': 'Users'}
    name = StringField(required=True, unique=False)
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    hobby = ListField(StringField(max_length=30))
    # hobby = ListField(required=True, unique=False)
    password = StringField(required=True, unique=False)
    address = ListField(EmbeddedDocumentField(Address))
    # created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    # def save(self, *args, **kwargs):
    #     if not self.created_at:
    #         self.created_at = datetime.datetime.now()
    #     self.updated_at = datetime.datetime.now()
    #     return super(UserModel, self).save(*args, **kwargs)

    def update(self, **kwargs):
        # if not self.created_at:
        #     self.created_at = datetime.datetime.now()
        # self.updated_at = datetime.datetime.now()
        kwargs["updated_at"] = datetime.datetime.now()
        return super(UserModel, self).update(**kwargs)
