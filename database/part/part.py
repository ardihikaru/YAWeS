from mongoengine import Document, StringField, DateTimeField, ListField, IntField
import datetime


class PartModel(Document):
    meta = {'collection': 'Parts'}
    name = StringField(required=True)
    manufacturer = StringField(required=True)
    catalog_number = IntField(unique=True, required=True)
    parts = ListField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def update(self, **kwargs):
        kwargs["updated_at"] = datetime.datetime.now()
        return super(PartModel, self).update(**kwargs)
