from django.db.models import Count, Sum, Avg, F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from reviews.models import Review

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    # Shared analytics - Fetching extra fields for ProductItem.jsx
    liked_reviews = (
        Review.objects.values(
            "food_id", 
            "food__name", 
            "food__price", 
            "food__description",
            "food__images__image" # Gets the image path
        )
        .annotate(
            avg_rating=Avg("rating"), 
            total_reviews=Count("id")
        )
        .order_by("-avg_rating")[:6]
    )

    trending_foods = (
        OrderItem.objects.values(
            "food_id", 
            "food__name", 
            "food__price", 
            "food__description",
            "food__images__image"
        )
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:6]
    )

    # User-specific stats
    user_orders = Order.objects.filter(user=user)
    user_total_orders = user_orders.count()
    total_spent = user_orders.aggregate(total=Sum("total_price"))["total"] or 0

    return Response({
        "total_orders_overall": Order.objects.count(),
        "mostly_liked_foods": list(liked_reviews),
        "trending_foods": list(trending_foods),
        "total_orders": user_total_orders,
        "total_spent": float(total_spent),
    })