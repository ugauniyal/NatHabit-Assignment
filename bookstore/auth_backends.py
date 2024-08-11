# bookstore/auth_backends.py

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from authors.models import Author
from customers.models import Customer

User = get_user_model()

class AuthorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                try:
                    author = Author.objects.get(user=user)
                    return user
                except Author.DoesNotExist:
                    return None
        except User.DoesNotExist:
            return None

class CustomerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                try:
                    customer = Customer.objects.get(user=user)
                    return user
                except Customer.DoesNotExist:
                    return None
        except User.DoesNotExist:
            return None