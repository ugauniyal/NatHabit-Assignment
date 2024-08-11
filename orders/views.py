from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Order, OrderItem
from books.models import Book
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        books_data = request.data.get('books', [])
        
        total_amount = 0
        order = Order.objects.create(user=user, total_amount=0)
        
        for book_data in books_data:
            book = Book.objects.get(id=book_data['id'])
            quantity = book_data['quantity']
            
            if book.stock < quantity:
                order.delete()
                return Response({"error": f"Not enough stock for book {book.title}"}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(order=order, book=book, quantity=quantity)
            book.stock -= quantity
            book.save()
            
            total_amount += book.price * quantity
        
        # Apply discount for first-time users
        if not Order.objects.filter(user=user).exists():
            discount_type = settings.FIRST_ORDER_DISCOUNT_TYPE
            discount_value = settings.FIRST_ORDER_DISCOUNT_VALUE
            
            if discount_type == 'FLAT':
                total_amount = max(0, total_amount - discount_value)
            elif discount_type == 'PERCENTAGE':
                total_amount *= (1 - discount_value / 100)
        
        order.total_amount = total_amount
        order.save()

        print(f"Discount Type: {settings.FIRST_ORDER_DISCOUNT_TYPE}")
        print(f"Discount Value: {settings.FIRST_ORDER_DISCOUNT_VALUE}")
        
        return Response({"order_id": order.id, "total_amount": total_amount}, status=status.HTTP_201_CREATED)
