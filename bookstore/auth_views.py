# bookstore/auth_views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, get_user_model
from authors.models import Author
from customers.models import Customer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        user_type = request.data.get('user_type')  # 'author' or 'customer'

        if not all([username, password, email, user_type]):
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        if user_type == 'author':
            Author.objects.create(user=user)
        elif user_type == 'customer':
            Customer.objects.create(user=user)
        else:
            user.delete()
            return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_type': user_type}, status=status.HTTP_201_CREATED)

class AuthorLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'author'):
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_type': 'author'})
        else:
            return Response({'error': 'Invalid credentials or not an author'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'customer'):
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_type': 'customer'})
        else:
            return Response({'error': 'Invalid credentials or not a customer'}, status=status.HTTP_401_UNAUTHORIZED)