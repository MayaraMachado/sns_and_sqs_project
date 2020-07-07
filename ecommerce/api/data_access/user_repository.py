from api.data_access.repository_base import RepositoryBase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction

class UserRepository(RepositoryBase):
    def __init__(self):
        super().__init__(User)

    def create(self, user_data):
        with transaction.atomic():
            user_data['password'] = make_password(user_data.pop('password'))
            user = self.model.objects.create(**user_data)
        
        return user