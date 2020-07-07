import mongoengine
import datetime


class UserModel(mongoengine.Document):
    meta = {'collection': 'Users'}
    name = mongoengine.StringField(required=True, unique=False)
    username = mongoengine.StringField(required=True, unique=True)
    email = mongoengine.StringField(required=True, unique=True)
    hobby = mongoengine.StringField(required=True, unique=False)
    password = mongoengine.StringField(required=True, unique=False)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(UserModel, self).save(*args, **kwargs)
